#!/usr/bin/env python3
"""PyAutoMind prompt-file lifecycle engine.

The Mind runs the prompt file through three states that mirror the task ledger:

    draft/<work-type>/<target>/<name>.md   intaken, not started   (backlog)
    active/<name>.md                        issued, in flight      (active.md)
    complete/<YYYY>/<MM>/<slug>.md          shipped                (the record IS the ledger)

Completion state lives ONLY in the dated records plus the generated
`complete/index.md`. The monolithic `complete.md` ledger was retired on
2026-07-16 (issue #81) — its history is in git, and the one-time split/backfill
tooling (`split-complete`, `migrate`) was deleted with it.

Subcommands
-----------
  move <name> [--date YYYY-MM-DD]
        Advance one file active/<name>.md -> complete/<YYYY>/<MM>/<name>.md.
        Date from --date, else inferred from an existing dated record with the
        same slug. For a shipped task prefer `record`, which writes the rich
        record and folds the prompt in one step.

  record <slug> --date YYYY-MM-DD --from-file <path> [--prompt <name>]
        The ship_* hook: write complete/<YYYY>/<MM>/<slug>.md from the rich
        completion body in <path> (drafted by the ship skill), folding and
        removing the active/ prompt. Run `index --apply` afterwards.

  index [--apply | --check]
        Generate complete/index.md (token-light navigation over the records);
        --check fails if it is stale (CI).

  dates [--write | --check]
        The date on every active/issued task: report what carries none, or
        --write to backfill it from git history (the commit that introduced
        the entry / moved the prompt into active/). See "task dates" below.

  check
        Drift guard (mirrors repos_sync.py --check; non-zero exit on drift):
          * no active.md slug has a complete/ record (finished but still active)
          * no file lives in two states at once
          * every registry `prompt:` path resolves, exactly rather than by
            fallback, and into the state folder its registry implies
          * no slug is listed in two registries at once
          * no active/ prompt is left unclaimed by every registry
          * nothing lives under active/ except top-level prompt .md files
            (subdirectories and scripts are invisible to every other guard)
        Wire into /health and CI.

  orphans
        The focused view of `check`'s last leg: active/ prompts that no registry
        entry claims. `check` grades this too — this lists only them.

  issues
        The ONLINE leg (needs network — `gh` when installed, else plain HTTPS
        with an optional GITHUB_TOKEN; deliberately not part of `check`, which
        stays hermetic): every registry entry's tracking issue AND every
        `status: pr-open` PR cross-checked against GitHub. Catches finished
        work still listed as pending — including the crashed-ship case where
        the PR merged but the session died before closing the issue, so the
        issue leg alone stays green. Run daily by registry_reconcile.yml
        (instance automation — deliberately not part of the shipped
        lifecycle_drift.yml, which must stay schedule-free per spawn rule 9).

This file is intentionally stdlib-only (no PyAuto imports) so it runs in any
environment, including a bare template checkout.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ACTIVE_DIR = ROOT / "active"
COMPLETE_DIR = ROOT / "complete"
# complete/archive/ holds non-record material (retired epic trackers, shelved
# prompts) — NOT dated task records, so check/index skip it.
ARCHIVE_DIR = COMPLETE_DIR / "archive"
DRAFT_DIR = ROOT / "draft"
ACTIVE_MD = ROOT / "active.md"

H2_RE = re.compile(r"^##\s+(.+?)\s*$")


def _slugify_h2(heading: str) -> str:
    """First token of an H2 heading is the task slug: `## slug (parenthetical)`."""
    return heading.split("(")[0].strip()


def safe_name(slug: str) -> str:
    """Kebab-case filename stem safe for the filesystem (no spaces/slashes).

    Used for BOTH writing complete/ filenames and comparing them back in
    `check`, so the round-trip is consistent (a raw H2 slug may carry spaces,
    `/`, em-dashes, etc.)."""
    s = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")
    return s or "untitled"


def ledger_slugs(path: Path) -> "set[str]":
    """H2 task slugs recorded in a ledger file (active.md)."""
    slugs = set()
    if not path.exists():
        return slugs
    for line in path.read_text(errors="replace").splitlines():
        m = H2_RE.match(line)
        if m:
            slugs.add(_slugify_h2(m.group(1)))
    return slugs


# --------------------------------------------------------------------------- #
# registry integrity
#
# The registry files are the first thing a task-selection pass reads, so a wrong
# entry costs a whole session before it is noticed. `check` used to ignore them
# entirely — it never opened planned.md or parked.md and never resolved a single
# `prompt:` path, so it printed OK over a planned.md in which 8 of 12 entries
# were wrong (2026-08-08 audit).
# --------------------------------------------------------------------------- #
REGISTRY_FILES = ("active.md", "planned.md", "parked.md")

# A field is a ZERO-INDENT `- key: value`. Nested two-space bullets are values
# of their parent key (`  - SomeRepo: some-branch` under `repos:`), NOT fields —
# reading them as fields would invent keys out of branch names.
FIELD_RE = re.compile(r"^-\s*([^:\s][^:]*?):\s*(.*)$")

# Which state folder(s) each registry's prompts may live in. parked.md takes
# BOTH: it holds tasks that were merely scoped (prompt still in draft/) and
# tasks that were started and then parked (prompt already advanced to active/).
EXPECTED_STATE = {
    "active.md": {"active"},
    "planned.md": {"draft"},
    "parked.md": {"draft", "active"},
}


def registry_entries(path: Path) -> "list[tuple[str, dict]]":
    """[(slug, {key: value})] for each `## slug` section of a registry file.

    First occurrence of a key wins, matching how a reader scans the block."""
    entries: "list[tuple[str, dict]]" = []
    if not path.exists():
        return entries
    fields: "dict[str, str]" = {}
    slug = None
    for line in path.read_text(errors="replace").splitlines():
        m = H2_RE.match(line)
        if m:
            if slug is not None:
                entries.append((slug, fields))
            slug, fields = _slugify_h2(m.group(1)), {}
            continue
        if slug is None:
            continue
        f = FIELD_RE.match(line)
        if f:
            fields.setdefault(f.group(1).strip(), f.group(2).strip())
    if slug is not None:
        entries.append((slug, fields))
    return entries


def resolve_prompt(root: Path, raw: str) -> "tuple[Path | None, str | None]":
    """(path, state) for a registry `prompt:` value, else (None, None).

    Mirrors the fallback chain AGENTS.md documents for `$start-dev`: the literal
    path, the pre-lifecycle `PyAutoMind/<work-type>/<target>/` and bare
    `<work-type>/<target>/` forms under draft/, and the bare filename in active/
    or as a complete/ record. `state` is the state folder the file ACTUALLY sits
    in, which is what makes a state contradiction visible — resolving is not the
    same as being in the right place."""
    rel = raw[len("PyAutoMind/"):] if raw.startswith("PyAutoMind/") else raw
    stripped = rel[len("draft/"):] if rel.startswith("draft/") else rel
    name = Path(rel).name

    candidates = [root / rel, root / "draft" / stripped, root / "active" / name]
    complete = root / "complete"
    if complete.is_dir():
        candidates += [
            f for f in sorted(complete.rglob(name))
            if (complete / "archive") not in f.parents
        ]

    for cand in candidates:
        if cand.is_file():
            try:
                top = cand.resolve().relative_to(root.resolve()).parts[0]
            except ValueError:
                return cand, "outside"
            return cand, top if top in ("draft", "active", "complete") else "other"
    return None, None


def registry_problems(root: Path) -> "list[str]":
    """Drift across active.md / planned.md / parked.md."""
    problems: "list[str]" = []
    seen: "dict[str, str]" = {}

    for reg in REGISTRY_FILES:
        for slug, fields in registry_entries(root / reg):
            key = safe_name(slug)
            if key in seen and seen[key] != reg:
                problems.append(
                    f"slug listed in two registries: {slug} ({seen[key]} + {reg})"
                )
            seen.setdefault(key, reg)

            raw = fields.get("prompt")
            if not raw:
                continue
            # Entries annotate the path with a trailing parenthetical
            # ("... .md (carries the phase-1 record)") — the path is the first
            # token, the rest is prose for a human.
            raw = raw.split()[0]
            resolved, state = resolve_prompt(root, raw)
            if resolved is None:
                problems.append(f"{reg}: {slug}: prompt path does not resolve: {raw}")
                continue

            rel = resolved.relative_to(root).as_posix()
            expected = EXPECTED_STATE[reg]
            if state == "complete":
                problems.append(
                    f"{reg}: {slug}: prompt is a complete/ record (shipped but "
                    f"still listed): {rel}"
                )
            elif state not in expected:
                want = "/ or ".join(sorted(expected))
                problems.append(
                    f"{reg}: {slug}: prompt is in {state}/ but {reg} implies "
                    f"{want}/: {rel}"
                )
            elif rel != raw:
                problems.append(
                    f"{reg}: {slug}: legacy prompt path, resolves only via "
                    f"fallback: {raw} -> {rel}"
                )
    return problems


# --------------------------------------------------------------------------- #
# task dates
#
# Until 2026-08-23 the Mind dated only what it FINISHED: every complete/ record
# carries `completed:`, but a task that had merely been picked up carried no
# date at all. active.md rows said it in prose when a session remembered to
# ("- issue: …/1501 (issued 2026-08-19)"), which nothing could read back — so
# the Mind could answer "what shipped in July?" and not "what did we start?".
#
# The convention: every registry entry carries ONE zero-indent date field, and
# every issued prompt an `Issued:` header line. The KEY names the event, so the
# date reads as something that happened rather than a bare timestamp:
#
#     active.md    - issued: YYYY-MM-DD    the day the task got its issue
#     planned.md   - filed:  YYYY-MM-DD    the day it was scoped
#     parked.md    - parked: YYYY-MM-DD    the day it stopped
#     active/*.md  Issued: YYYY-MM-DD      the prompt's own copy (survives a
#                                          registry row going missing)
#
# `dates` reports what carries none; `dates --write` backfills from git — the
# commit that first introduced the entry, or that moved the prompt into
# active/. Retroactive by construction: the history already knows the dates,
# they were simply never written down where a reader could see them.
# --------------------------------------------------------------------------- #
ISO_DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")

# Date keys a registry entry may carry, most task-authoritative first. The
# first one present wins, so an entry that was filed, then issued, dates from
# the issue — the later, more specific event.
DATE_KEYS = ("issued", "registered", "started", "planned", "filed", "parked",
             "found", "completed", "shipped")

# The key each registry's entries SHOULD carry — what `--write` inserts.
REGISTRY_DATE_KEY = {"active.md": "issued", "planned.md": "filed",
                     "parked.md": "parked"}

# The prompt-header form. These join the light header convention (REFERENCE.md
# "Prompt file format") — optional like every other key, and never YAML. The
# key names the state the prompt was in when the date happened, so the two
# never have to be told apart by which folder the file currently sits in:
#
#   draft/   Filed:  YYYY-MM-DD   the day the prompt was written
#   active/  Issued: YYYY-MM-DD   the day it got its GitHub issue
#
# The backlog is the LARGEST pool of tasks the Mind holds — 150 prompts against
# a handful of live rows — so leaving `draft/` undated left the recent feed
# unable to see most of the work (2026-08-23).
PROMPT_DATE_KEY = {"draft": "Filed", "active": "Issued"}
PROMPT_DATE_KEYS = tuple(PROMPT_DATE_KEY.values())
_HEADER_FIELD_RE = re.compile(
    r"^(Type|Target|Repos|Difficulty|Autonomy|Priority|Status|Issued|Filed|"
    r"Epic|Phase|Blocked-by|Closes-when):", re.IGNORECASE)


def entry_date(fields: "dict[str, str]") -> "tuple[str | None, str | None]":
    """(date, key) for a registry entry, or (None, None) when it carries none.

    Only a key from DATE_KEYS counts. A date sitting in some other field's
    prose is invisible on purpose — `- issue: …/1501 (issued 2026-08-19)` is
    exactly the un-machine-readable habit this convention replaces (backfill
    still mines it, see `_prose_date`)."""
    for key in DATE_KEYS:
        value = fields.get(key)
        if not value:
            continue
        m = ISO_DATE_RE.search(value)
        if m:
            return m.group(1), key
    return None, None


def prompt_date(text: str) -> "tuple[str | None, str | None]":
    """(date, key) from a prompt's `Filed:` / `Issued:` header, else (None, None).

    Header only (first 30 lines), matching how every other prompt field is
    read — a date deep in the prose is prose. `Issued:` wins when a prompt
    carries both: it is the later, more specific event, and an issued prompt
    keeps the `Filed:` it had as a draft."""
    found = {}
    for line in text.splitlines()[:30]:
        m = re.match(r"(Issued|Filed):\s*(\S.*)", line.strip(), re.IGNORECASE)
        if m:
            d = ISO_DATE_RE.search(m.group(2))
            if d:
                found.setdefault(m.group(1).capitalize(), d.group(1))
    for key in ("Issued", "Filed"):
        if key in found:
            return found[key], key
    return None, None


def prompt_issued_date(text: str) -> "str | None":
    """Back-compat shim: the prompt's header date, whichever key carries it."""
    return prompt_date(text)[0]


def _prose_date(fields: "dict[str, str]") -> "str | None":
    """Earliest ISO date anywhere in an entry's field values.

    The backfill's second source: entries that DID record when they started,
    just not where `entry_date` looks. Earliest wins because the later dates
    in an entry are progress notes, and the entry's own date is its first."""
    found = sorted(m for v in fields.values() for m in ISO_DATE_RE.findall(v))
    return found[0] if found else None


def _git(root: Path, args: "list[str]") -> "list[str]":
    """`git` output lines, or [] on any failure.

    Empty on no git, not a repo, a fresh template checkout — the backfill
    degrades to its other sources rather than dying."""
    import subprocess
    try:
        out = subprocess.run(["git", "-C", str(root), *args],
                             capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return []
    if out.returncode != 0:
        return []
    return [ln.strip() for ln in out.stdout.splitlines() if ln.strip()]


def _shallow_boundary(root: Path) -> "str | None":
    """Date of the oldest commit a SHALLOW clone can see, else None.

    A shallow checkout (CI, a cloud session) has no history before its
    boundary, so `git log` reports the boundary commit as the day everything
    older was "introduced" — every backfill in one clone would come out the
    same wrong date. Anything at or before the boundary is therefore not
    evidence, and the caller falls through to a slower but honest source."""
    if _git(root, ["rev-parse", "--is-shallow-repository"])[:1] != ["true"]:
        return None
    dates = _git(root, ["log", "--format=%ad", "--date=short"])
    return dates[-1] if dates else None


def _git_dates(root: Path, args: "list[str]") -> "list[str]":
    """`git log` short author dates for a pathspec/pickaxe, newest first."""
    return _git(root, ["log", "--format=%ad", "--date=short", *args])


def _oldest(dates: "list[str]", boundary: "str | None") -> "str | None":
    """The oldest date in a `git log` answer, unless the clone truncates it."""
    if not dates:
        return None
    oldest = dates[-1]
    return None if boundary and oldest <= boundary else oldest


def git_entry_date(root: Path, registry: str, slug: str,
                   boundary: "str | None" = None) -> "str | None":
    """The day this entry's `## slug` heading first appeared in its registry."""
    return _oldest(_git_dates(root, [f"-S## {slug}", "--", registry]), boundary)


def git_prompt_date(root: Path, rel: str, state: str,
                    boundary: "str | None" = None) -> "str | None":
    """The day a prompt reached the state its folder says it is in.

    The two states want opposite readings of the same history, and the switch
    is `--follow`:

    * `active/` — the day it ARRIVED there, i.e. was issued. `git mv` from
      draft/ records as an add at the new path, which is exactly that event,
      so following the rename back would report the wrong day.
    * `draft/` — the day the prompt was WRITTEN, wherever it lived then. The
      2026-07-13 lifecycle migration `git mv`-ed 42 prompts in one commit;
      without `--follow` all 42 date from the migration rather than from
      themselves, which is a fact about the repo's plumbing, not the work.
    """
    args = ["--diff-filter=A", "--", rel]
    if state == "draft":
        args = ["--follow"] + args
    return _oldest(_git_dates(root, args), boundary)


def _insert_registry_date(lines: "list[str]", start: int, key: str,
                          date: str) -> "list[str]":
    """Insert `- key: date` into the entry whose `## ` heading is at `start`.

    Placed after the `- issue:` field (and its wrapped continuation lines) when
    there is one, so an entry reads identity-then-date; otherwise it becomes
    the entry's first field."""
    i = start + 1
    at = i
    while i < len(lines) and not H2_RE.match(lines[i]):
        f = FIELD_RE.match(lines[i])
        if f and f.group(1).strip() == "issue":
            i += 1
            while i < len(lines) and lines[i][:1].isspace() and lines[i].strip():
                i += 1
            at = i
            break
        if f:
            at = i
            break
        i += 1
    return lines[:at] + [f"- {key}: {date}"] + lines[at:]


def _insert_prompt_date(text: str, date: str, key: str = "Issued") -> str:
    """Insert `<key>: <date>` into a prompt's light metadata header.

    After the last header field (skipping the bullet list a `Repos:` field
    owns) when there is a header; else under the title heading; else at the
    very top. Every existing line survives verbatim, including line endings —
    the prompt body is the human's, not the tool's."""
    lines = text.splitlines()
    head = lines[:30]
    last = max((i for i, ln in enumerate(head) if _HEADER_FIELD_RE.match(ln.strip())),
               default=None)
    if last is not None:
        # A header field's value may run on: the bullet list a `Repos:` field
        # owns, an indented wrap, or a bare continuation line ("Status: issued
        # … / (do not start dev)"). The header block ends at the first blank
        # line, so append there rather than splitting somebody's value in two.
        at = last + 1
        while at < len(lines) and lines[at].strip():
            at += 1
        new = lines[:at] + [f"{key}: {date}"] + lines[at:]
    else:
        first = next((i for i, ln in enumerate(lines) if ln.strip()), 0)
        if lines and lines[first].lstrip().startswith("#"):
            new = (lines[:first + 1] + ["", f"{key}: {date}"]
                   + lines[first + 1:])
        else:
            new = [f"{key}: {date}", ""] + lines
    nl = "\r\n" if "\r\n" in text else "\n"
    return nl.join(new) + (nl if text.endswith("\n") else "")


def undated_entries(root: Path) -> "list[dict]":
    """Registry entries carrying no DATE_KEYS date."""
    out = []
    for reg in REGISTRY_FILES:
        for slug, fields in registry_entries(root / reg):
            date, _ = entry_date(fields)
            if date is None:
                out.append({"registry": reg, "slug": slug, "fields": fields})
    return out


def state_prompts(root: Path) -> "list[tuple[Path, str]]":
    """Every prompt the Mind holds as (path, state) — `draft/` and `active/`.

    `complete/` is excluded: a record is already dated by definition, and its
    date is the ledger's job, not this one's."""
    out = []
    active = root / "active"
    if active.is_dir():
        out += [(f, "active") for f in sorted(active.glob("*.md"))]
    drafts = root / "draft"
    if drafts.is_dir():
        out += [(f, "draft") for f in sorted(drafts.rglob("*.md"))
                if f.name != "README.md"]
    return out


def undated_prompts(root: Path) -> "list[Path]":
    """Prompts carrying no date header, in either state folder."""
    return [f for f, _state in state_prompts(root)
            if prompt_date(f.read_text(errors="replace"))[0] is None]


# The Intake Agent stamps every prompt it files with a trailer naming the day
# ("<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from … -->").
# 53 of the backlog's 150 prompts carry one — the prompt's own claim about when
# it was conceived, and the fallback when git cannot see far enough back.
_INTAKE_TRAILER = re.compile(
    r"Intake \(Conception\) Agent on\s+(\d{4}-\d{2}-\d{2})")


def intake_trailer_date(text: str) -> "str | None":
    m = _INTAKE_TRAILER.search(text)
    return m.group(1) if m else None


# A backfilled date is INFERRED, and says so in the file. A writer that knows
# the date (create_issue, at the moment it opens the issue) writes a bare
# `Issued: 2026-08-19`; anything reconstructed afterwards carries its source,
# so a reader can tell "this is when it happened" from "this is our best
# reconstruction of when it happened" without going back to git.
BACKFILL_NOTE = "(backfilled from {source})"


def _registry_claim(root: Path) -> "dict[str, tuple[str, str, str]]":
    """{prompt path -> (date, key, registry)} for every dated registry entry.

    The Mind's own record of when a task changed state — the best evidence
    left for a prompt whose issue date pre-dates what this clone can see."""
    out = {}
    for reg in REGISTRY_FILES:
        for _slug, fields in registry_entries(root / reg):
            raw = (fields.get("prompt") or "").split()
            date, key = entry_date(fields)
            if raw and date:
                out.setdefault(raw[0], (date, key, reg))
    return out


def backfill_dates(root: Path, apply: bool = False) -> "list[dict]":
    """Date every undated registry entry and issued prompt, retroactively.

    Read-only unless `apply`. Each result records where the date came from, so
    a backfill is auditable rather than anonymous, and every inferred date is
    annotated in the file it lands in:

      `git`         the commit that introduced the entry / the active/ prompt
      `<registry>`  the dated registry entry that claims this prompt
      `prose`       a date the entry or prompt already stated in its own text
      `unknown`     nothing to go on — reported, never guessed

    A shallow clone cannot see far enough back for the `git` source (see
    `_shallow_boundary`); the chain then falls through to the Mind's own
    records, which is why they are consulted at all.
    """
    results = []
    boundary = _shallow_boundary(root)

    for reg in REGISTRY_FILES:
        path = root / reg
        if not path.exists():
            continue
        key = REGISTRY_DATE_KEY[reg]
        pending = []
        for slug, fields in registry_entries(path):
            if entry_date(fields)[0] is not None:
                continue
            date, source = git_entry_date(root, reg, slug, boundary), "git"
            if date is None:
                date, source = _prose_date(fields), "prose"
            if date is None:
                source = "unknown"
            results.append({"what": f"{reg}: {slug}", "key": key,
                            "date": date, "source": source})
            if date:
                pending.append((slug, date, source))
        if not (apply and pending):
            continue
        lines = path.read_text(errors="replace").splitlines()
        # Bottom-up: inserting into a later entry cannot shift an earlier
        # entry's heading index out from under the next insert.
        by_slug = {s: (d, src) for s, d, src in pending}
        heads = [(i, _slugify_h2(m.group(1)))
                 for i, ln in enumerate(lines) if (m := H2_RE.match(ln))]
        for i, slug in reversed(heads):
            if slug in by_slug:
                date, source = by_slug[slug]
                value = f"{date} {BACKFILL_NOTE.format(source=source)}"
                lines = _insert_registry_date(lines, i, key, value)
        path.write_text("\n".join(lines) + "\n")

    claims = _registry_claim(root)
    for f, state in state_prompts(root):
        text = f.read_text(errors="replace")
        if prompt_date(text)[0] is not None:
            continue
        rel = f.relative_to(root).as_posix()
        key = PROMPT_DATE_KEY[state]
        date, source = git_prompt_date(root, rel, state, boundary), "git"
        if date is None:
            trailer = intake_trailer_date(text)
            if trailer:
                date, source = trailer, "the prompt's intake trailer"
        if date is None and rel in claims:
            claimed, claim_key, claim_reg = claims[rel]
            date, source = claimed, f"{claim_reg} `{claim_key}:`"
        if date is None:
            m = ISO_DATE_RE.search(text)
            date, source = (m.group(1), "prose") if m else (None, "unknown")
        results.append({"what": rel, "key": key, "date": date,
                        "source": source})
        if date and apply:
            value = f"{date} {BACKFILL_NOTE.format(source=source)}"
            f.write_text(_insert_prompt_date(text, value, key))

    return results


# --------------------------------------------------------------------------- #
# the online leg — tracking-issue state
#
# The offline checks catch STRUCTURAL rot (bad paths, state contradictions).
# They cannot catch the class that costs most: an entry describing work that is
# finished. The 2026-08-08 audit found six such entries, including the whole
# M0-M3 release-validation chain, and not one was locally detectable — every one
# had correct upstream state (a closed issue, a merged PR, a capability live on
# main) that the Mind simply never read back. This is that read-back.
#
# Deliberately NOT part of `check`: it needs the network and `gh` credentials,
# and `check` is wired into CI where it must stay hermetic.
# --------------------------------------------------------------------------- #
# Only TRACKING refs. A task's `library-pr:`/`workspace-pr:` are merged by
# definition once it ships, so reporting those as closed would be pure noise.
ISSUE_FIELDS = ("issue", "epic")
ISSUE_URL_RE = re.compile(r"https://github\.com/([\w.-]+)/([\w.-]+)/issues/(\d+)")

# The one PR reference that IS tracking state: a `status:` field declaring the
# task is waiting on an open PR. When that PR merges, the ship bookkeeping
# (record + retire + issue close) is owed — and if the shipping session dies
# first, the entry goes stale with its tracking ISSUE still open, which is
# exactly the case the issue leg above cannot see. (version-stamp-sync-guards,
# 2026-08-17: six PRs merged, session died after the "Shipped" comment; found
# two days later only by a manual sweep.)
PR_URL_RE = re.compile(r"https://github\.com/([\w.-]+)/([\w.-]+)/pull/(\d+)")
PR_OPEN_TOKEN = "pr-open"


class GhUnavailable(RuntimeError):
    """`gh` is not installed. Distinct from "gh ran and said no" so the command
    can report "could not run" instead of the far worse "nothing to report"."""


def registry_issue_refs(root: Path) -> "list[tuple[str, str, str]]":
    """(registry, slug, issue_url) for every entry carrying a tracking issue.

    Entries legitimately carry prose instead of a URL ("(no issue — a
    human-authorized release drive)", "NEEDS A FRESH ISSUE — ..."); those have
    nothing to query and are skipped rather than reported."""
    refs = []
    for reg in REGISTRY_FILES:
        for slug, fields in registry_entries(root / reg):
            for key in ISSUE_FIELDS:
                m = ISSUE_URL_RE.search(fields.get(key, ""))
                if m:
                    refs.append((reg, slug, m.group(0)))
    return refs


def _http_api_state(owner: str, repo: str, kind: str, num: str) -> str:
    """One GitHub REST read via stdlib urllib — the gh-free fallback path.

    `kind` is "issues" or "pulls". Sends `GITHUB_TOKEN`/`GH_TOKEN` when set
    (CI runners always have one; anonymous works for public repos, rate-limited).
    Returns "merged" for a merged PR, else the API `state`, else "unreadable: …"
    — never raises, so one dead URL cannot sink the whole report."""
    import json
    import os
    import urllib.error
    import urllib.request

    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}/{kind}/{num}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "pyautomind-lifecycle",
        },
    )
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        return f"unreadable: HTTP {e.code}"
    except Exception as e:  # URLError, timeout, bad JSON — report, don't crash
        return f"unreadable: {e.__class__.__name__}"
    if kind == "pulls" and data.get("merged_at"):
        return "merged"
    return data.get("state", "unknown")


def _states_via_gh_or_http(urls: "list[str]", url_re: "re.Pattern",
                           kind: str, jq: str) -> "dict[str, str]":
    """{url: state} via the `gh` CLI, falling back to plain HTTPS when gh is
    not installed (cloud/web sessions, bare CI images). Online leg only."""
    import subprocess

    states: "dict[str, str]" = {}
    gh_missing = False
    for url in urls:
        m = url_re.match(url)
        if not m:
            continue
        owner, repo, num = m.groups()
        if gh_missing:
            states[url] = _http_api_state(owner, repo, kind, num)
            continue
        try:
            r = subprocess.run(
                ["gh", "api", f"repos/{owner}/{repo}/{kind}/{num}", "--jq", jq],
                capture_output=True, text=True,
            )
        except FileNotFoundError:
            gh_missing = True
            states[url] = _http_api_state(owner, repo, kind, num)
            continue
        if r.returncode != 0:
            tail = (r.stderr.strip().splitlines() or ["error"])[-1]
            states[url] = f"unreadable: {tail}"
            continue
        states[url] = r.stdout.strip()
    return states


def _gh_issue_states(urls: "list[str]") -> "dict[str, str]":
    return _states_via_gh_or_http(urls, ISSUE_URL_RE, "issues", ".state")


def _gh_pr_states(urls: "list[str]") -> "dict[str, str]":
    return _states_via_gh_or_http(
        urls, PR_URL_RE, "pulls",
        'if .merged_at then "merged" else .state end')


def issue_problems(root: Path, fetch=None) -> "list[str]":
    """Registry entries whose tracking issue is CLOSED — i.e. finished work
    still listed as pending.

    `fetch` maps urls -> {url: state}; injectable so the logic is testable
    without a network."""
    refs = registry_issue_refs(root)
    if not refs:
        return []
    fetch = fetch or _gh_issue_states
    states = fetch([url for _, _, url in refs])

    problems = []
    for reg, slug, url in refs:
        state = states.get(url, "unknown")
        if state == "closed":
            problems.append(
                f"{reg}: {slug}: tracking issue is CLOSED but the entry is still "
                f"listed as pending: {url}"
            )
        elif state != "open":
            problems.append(f"{reg}: {slug}: could not read issue state ({state}): {url}")
    return problems


def registry_pr_refs(root: Path) -> "list[tuple[str, str, str]]":
    """(registry, slug, pr_url) for every entry whose `status:` declares an
    open PR. Only the `status:` field is read — a PR URL anywhere else in the
    entry (prose, `library-pr:` history) is not a claim of in-flight state."""
    refs = []
    for reg in REGISTRY_FILES:
        for slug, fields in registry_entries(root / reg):
            status = fields.get("status", "")
            if PR_OPEN_TOKEN not in status:
                continue
            for m in PR_URL_RE.finditer(status):
                refs.append((reg, slug, m.group(0)))
    return refs


def pr_problems(root: Path, fetch=None) -> "list[str]":
    """Registry entries whose `status: pr-open` PR is no longer open.

    The complement of `issue_problems`: when a shipping session dies between
    the merge and the bookkeeping, the tracking issue is never closed — so the
    issue leg stays green while the entry rots. The merged PR is the one
    signal that survives the crash. `fetch` is injectable for tests."""
    refs = registry_pr_refs(root)
    if not refs:
        return []
    fetch = fetch or _gh_pr_states
    states = fetch([url for _, _, url in refs])

    problems = []
    for reg, slug, url in refs:
        state = states.get(url, "unknown")
        if state == "merged":
            problems.append(
                f"{reg}: {slug}: status says pr-open but the PR is MERGED — "
                f"the ship bookkeeping (record + retire + issue close) was "
                f"never done: {url}"
            )
        elif state == "closed":
            problems.append(
                f"{reg}: {slug}: status says pr-open but the PR was CLOSED "
                f"without merging: {url}"
            )
        elif state != "open":
            problems.append(f"{reg}: {slug}: could not read PR state ({state}): {url}")
    return problems


# --------------------------------------------------------------------------- #
# the PR ledger
#
# `library-pr:` / `workspace-pr:` were written by ship_library and read by /prm
# for months before anything validated them: they were absent from the
# `active.md` schema, so a row could declare `status: awaiting-merge` and name
# no PR at all, and /prm would have nothing to merge. The keys are REPEATABLE —
# one task may open several PRs of a kind — which is why they need their own
# parse: `registry_entries` keeps the first occurrence of a key, matching how a
# reader scans a block, and would silently drop the rest.
#
# The chain these keys carry is documented once in REFERENCE.md ("The PR keys"
# and "The pending-release chain"); this module only enforces it.
# --------------------------------------------------------------------------- #
PR_KEYS = ("library-pr", "workspace-pr")

# A `status:` containing any of these declares the PRs exist, so the row must
# say where they are. Matched case-insensitively against the status line only.
SHIP_STATUS_TOKENS = ("awaiting-merge", "pr open", "pr-open", "shipped")

# How long a `complete/` record may keep an uncleared `pending-release:` before
# the check mentions it. A warning, never an error: the library may simply not
# have been released yet, which is the normal state of the key.
PENDING_RELEASE_STALE_DAYS = 30

PENDING_RELEASE_RE = re.compile(r"^([\w.-]+)@(\S+)$")


def registry_multi(path: Path) -> "list[tuple[str, dict[str, list[str]]]]":
    """[(slug, {key: [value, ...]})] — every occurrence of every key.

    The repeat-tolerant twin of `registry_entries`. Used only where a key is
    legitimately repeatable (the PR keys, `pending-release:`, `release-gate:`);
    everything else should keep reading `registry_entries`, whose first-wins
    rule matches how a human scans the block."""
    entries: "list[tuple[str, dict[str, list[str]]]]" = []
    if not path.exists():
        return entries
    fields: "dict[str, list[str]]" = {}
    slug = None
    for line in path.read_text(errors="replace").splitlines():
        m = H2_RE.match(line)
        if m:
            if slug is not None:
                entries.append((slug, fields))
            slug, fields = _slugify_h2(m.group(1)), {}
            continue
        if slug is None:
            continue
        f = FIELD_RE.match(line)
        if f:
            fields.setdefault(f.group(1).strip(), []).append(f.group(2).strip())
    if slug is not None:
        entries.append((slug, fields))
    return entries


def pr_urls(values: "list[str]") -> "list[str]":
    """Every PR URL across a repeated key's values.

    Both written forms collapse here: one line per URL (the schema's preferred
    shape) and the older single line of `<url>, <url>`. Trailing prose is
    ignored — the URLs are matched, not the field."""
    out: "list[str]" = []
    for value in values:
        for m in PR_URL_RE.finditer(value):
            if m.group(0) not in out:
                out.append(m.group(0))
    return out


def pr_key_problems(root: Path) -> "list[str]":
    """`active.md` rows that declare open/shipped PRs and name none.

    The row says `/prm` has work to do and then withholds the only thing it
    needs — a contradiction inside one entry, which is exactly what this check
    is for, so it is drift and not a warning."""
    problems: "list[str]" = []
    for slug, multi in registry_multi(root / "active.md"):
        status = " ".join(multi.get("status", [])).lower()
        if not any(tok in status for tok in SHIP_STATUS_TOKENS):
            continue
        if any(pr_urls(multi.get(key, [])) for key in PR_KEYS):
            continue
        problems.append(
            f"active.md: {slug}: status declares open/shipped PRs but the row "
            f"carries no `library-pr:`/`workspace-pr:` — /prm has nothing to "
            f"merge (REFERENCE.md \"The PR keys\")"
        )
    return problems


def _record_fields(path: Path) -> "dict[str, list[str]]":
    """The record's own fields — everything above `## Original prompt`.

    `lifecycle.py record` appends the task's starting prompt verbatim, and that
    prompt may itself quote `library-pr:` lines from some other task. Reading
    past the boundary would attribute them to this record."""
    text = path.read_text(errors="replace")
    head = re.split(r"^##\s+Original prompt\s*$", text, maxsplit=1,
                    flags=re.M | re.I)[0]
    fields: "dict[str, list[str]]" = {}
    for line in head.splitlines():
        f = FIELD_RE.match(line)
        if f:
            fields.setdefault(f.group(1).strip(), []).append(f.group(2).strip())
    return fields


def pending_release_problems(root: Path,
                             today: "str | None" = None) -> "list[str]":
    """`complete/` records whose `pending-release:` is long uncleared.

    A warning by construction: the key means "merged, not yet on PyPI", which
    is a legitimate state for as long as the release takes. What it stops being
    legitimate at is a month — by then either the release happened and
    `/review_release` never swept the ledger, or the release is itself the
    problem."""
    complete = root / "complete"
    archive = complete / "archive"
    if not complete.is_dir():
        return []
    now = _dt.date.fromisoformat(today) if today else _dt.date.today()
    problems: "list[str]" = []
    for f in sorted(complete.rglob("*.md")):
        if archive in f.parents or f.name == "index.md":
            continue
        fields = _record_fields(f)
        links = fields.get("pending-release") or []
        if not links:
            continue
        dates = fields.get("completed") or []
        m = ISO_DATE_RE.search(dates[0]) if dates else None
        if not m:
            continue
        age = (now - _dt.date.fromisoformat(m.group(1))).days
        if age < PENDING_RELEASE_STALE_DAYS:
            continue
        problems.append(
            f"{f.relative_to(root)}: `pending-release:` still uncleared "
            f"{age}d after completion ({', '.join(links)}) — if the release "
            f"happened, /review_release never swept the ledger"
        )
    return problems


def draft_issue_refs(root: Path) -> "list[tuple[str, str]]":
    """(draft_path, issue_url) for draft prompts citing a GitHub issue.

    Only a handful do — drafts are pre-issue by definition — but `draft/` is
    backlog no check grades, and it carries shipped work too (the 2026-08-08
    sweep found `minimum_library_version_adoption` fully delivered across all
    seven repos while still sitting in draft/)."""
    draft = root / "draft"
    if not draft.is_dir():
        return []
    refs = []
    for f in sorted(draft.rglob("*.md")):
        m = ISSUE_URL_RE.search(f.read_text(errors="replace"))
        if m:
            refs.append((str(f.relative_to(root)), m.group(0)))
    return refs


def draft_issue_notes(root: Path, fetch=None) -> "list[str]":
    """ADVISORY notes on drafts whose cited issue is closed.

    Deliberately weaker than `issue_problems`, and deliberately not drift. A
    registry entry's `issue:` is its OWN tracking issue, so closed means done. A
    draft usually cites an issue as CONTEXT — "Once #480 is fixed…", "Follow-up
    to #57" — so closed can mean the draft is newly UNBLOCKED rather than
    finished. Both readings are worth a human look; neither is a gate.

    For the drafts that DO state which reading applies, see `draft_gate_notes`:
    an explicit `Closes-when:` / `Blocked-by:` header removes exactly this
    ambiguity, and those drafts are reported there instead of here."""
    gated = {path for path, _, _ in draft_gate_refs(root)}
    refs = [(p, u) for p, u in draft_issue_refs(root) if p not in gated]
    if not refs:
        return []
    fetch = fetch or _gh_issue_states
    states = fetch([url for _, url in refs])
    return [
        f"{path}: cited issue is closed — shipped, or newly unblocked? {url}"
        for path, url in refs
        if states.get(url) == "closed"
    ]


# --------------------------------------------------------------------------- #
# draft gates
#
# The 2026-08-09 draft/ sweep found five prompts whose stated gate had since
# closed, and the two readings are OPPOSITE: `test_mode_representative_outputs`
# said "EPIC CLOSES when #70 ships its recipe leg" (gate closed => the prompt is
# DONE), while `unpark_imaging_scaling_relation_slam` said "BLOCKED until
# PyAutoArray PR#431 merges" (gate closed => the prompt is READY TO START).
# Prose cannot be graded, so `--drafts` had to lump both into one "shipped, or
# newly unblocked?" note. These keys let a prompt say which it means.
# --------------------------------------------------------------------------- #
GATE_FIELDS = ("closes-when", "blocked-by")
#: `Repo#123` shorthand as well as full URLs — prompts overwhelmingly write the
#: former, and a URL-only extractor found 2 refs across the backlog where the
#: shorthand form found 8 (2026-08-09 measurement).
GATE_REF_RE = re.compile(
    r"https://github\.com/([\w.-]+)/([\w.-]+)/(?:issues|pull)/(\d+)"
    r"|(?<![\w/])([A-Za-z_][\w.]*)#(\d+)\b"
)
_GATE_KEY_RE = re.compile(r"^\s*(closes-when|blocked-by)\s*:\s*(.+?)\s*$", re.I)
DEFAULT_GATE_OWNER = "PyAutoLabs"


def _gate_url(match: "re.Match") -> "str | None":
    """Normalise either GATE_REF_RE alternative to a canonical issues URL.

    `Repo#123` cannot say whether 123 is an issue or a PR, and the GitHub API
    resolves an issues URL for both (a PR *is* an issue), so the issues form is
    the safe canonical shape."""
    owner, repo, num, short_repo, short_num = match.groups()
    if owner:
        return f"https://github.com/{owner}/{repo}/issues/{num}"
    if short_repo:
        return f"https://github.com/{DEFAULT_GATE_OWNER}/{short_repo}/issues/{short_num}"
    return None


def draft_gate_refs(root: Path) -> "list[tuple[str, str, str]]":
    """(draft_path, gate_kind, url) for drafts carrying a gate header key.

    `gate_kind` is `closes-when` or `blocked-by` — the two opposite readings.
    A key may list several refs; each becomes its own entry, because a prompt
    blocked on three PRs is only unblocked when the last one lands."""
    draft = root / "draft"
    if not draft.is_dir():
        return []
    refs = []
    for f in sorted(draft.rglob("*.md")):
        rel = str(f.relative_to(root))
        in_fence = False
        for line in f.read_text(errors="replace").splitlines():
            # Fenced blocks are documentation, not declarations. Prompts that
            # *describe* these keys (this feature's own prompt does, in a
            # ```markdown example) must not be read as declaring them.
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            m = _GATE_KEY_RE.match(line)
            if not m:
                continue
            kind = m.group(1).lower()
            for ref in GATE_REF_RE.finditer(m.group(2)):
                url = _gate_url(ref)
                if url:
                    refs.append((rel, kind, url))
    return refs


def draft_gate_notes(root: Path, fetch=None) -> "dict[str, list[str]]":
    """Drafts whose declared gate has closed, split by what that MEANS.

    Returns `{"shipped": [...], "unblocked": [...], "partial": [...],
    "unreadable": [...]}`. Unlike `draft_issue_notes` these are unambiguous —
    the prompt author said which reading applies — so each line states the
    action rather than asking a question.

    Aggregated PER PROMPT, not per reference: a prompt blocked on three PRs is
    unblocked only when the last one lands, so reporting each ref separately
    would claim "ready to start" three times while it is still blocked. A
    partially-satisfied `Blocked-by:` is reported in its own weaker band, which
    is the real state of `ep_analytic_updates` (its WP1 gate merged; the WP3/WP4
    gates are open).

    Still advisory, and deliberately so: a satisfied `Closes-when:` is strong
    evidence the work is done, but retiring a prompt writes to `complete/` and
    stays a human act (the same contract `intake reconcile` keeps)."""
    refs = draft_gate_refs(root)
    out = {"shipped": [], "unblocked": [], "partial": [], "unreadable": []}
    if not refs:
        return out
    fetch = fetch or _gh_issue_states
    states = fetch(sorted({url for _, _, url in refs}))

    grouped: "dict[tuple[str, str], list[str]]" = {}
    for path, kind, url in refs:
        grouped.setdefault((path, kind), []).append(url)

    for (path, kind), urls in sorted(grouped.items()):
        got = [(u, states.get(u, "unknown")) for u in urls]
        bad = [f"{u} ({s})" for u, s in got if s not in ("open", "closed")]
        if bad:
            out["unreadable"].append(
                f"{path}: could not read {len(bad)} declared gate(s): "
                + ", ".join(bad))
            continue
        closed = [u for u, s in got if s == "closed"]
        if not closed:
            continue
        joined = ", ".join(closed)
        if len(closed) < len(got):
            still = ", ".join(u for u, s in got if s == "open")
            out["partial"].append(
                f"{path}: {len(closed)} of {len(got)} `{kind}:` gates closed — "
                f"partly ready; still open: {still}")
        elif kind == "closes-when":
            out["shipped"].append(
                f"{path}: every `Closes-when:` gate is CLOSED — the prompt's own "
                f"exit condition is met, so this is very likely shipped: {joined}")
        else:
            out["unblocked"].append(
                f"{path}: every `Blocked-by:` gate is CLOSED — ready to start, "
                f"not blocked: {joined}")
    return out


def cmd_issues(args) -> int:
    """Cross-check every registry entry's tracking issue AND every
    `status: pr-open` PR against GitHub."""
    try:
        problems = issue_problems(ROOT) + pr_problems(ROOT)
    except GhUnavailable:
        print(
            "lifecycle issues: cannot run — the `gh` CLI is not installed.\n"
            "  This leg needs GitHub; it is deliberately separate from `check`,\n"
            "  which stays hermetic for CI. Install gh, or run this from a\n"
            "  session that has it.",
            file=sys.stderr,
        )
        return 2
    n_refs = len(registry_issue_refs(ROOT)) + len(registry_pr_refs(ROOT))
    if problems and n_refs and all("could not read" in p for p in problems) \
            and len(problems) == n_refs:
        print(
            "lifecycle issues: cannot run — GitHub is unreachable from here\n"
            "  (every state read failed). Run from a session with GitHub\n"
            "  access, or set GITHUB_TOKEN for the HTTPS fallback.",
            file=sys.stderr,
        )
        for line in problems[:3]:
            print(f"    e.g. {line}", file=sys.stderr)
        return 2
    notes = []
    gates = {"shipped": [], "unblocked": [], "partial": [], "unreadable": []}
    if getattr(args, "drafts", False):
        try:
            gates = draft_gate_notes(ROOT)
            notes = draft_issue_notes(ROOT)
        except GhUnavailable:
            pass  # unreachable: issue_problems above would already have raised

    if problems:
        print("lifecycle issues: DRIFT")
        for line in problems:
            print(f"  - {line}")
    else:
        print(
            f"lifecycle issues: OK ({len(registry_issue_refs(ROOT))} tracking "
            f"issue(s) open, {len(registry_pr_refs(ROOT))} pr-open PR(s) open)")

    # Declared gates first: the prompt author said which reading applies, so
    # these are actionable rather than a question. Still advisory — retiring a
    # prompt writes to complete/ and stays human.
    if gates["shipped"]:
        print(f"\nGATE MET — {len(gates['shipped'])} draft(s) whose `Closes-when:` "
              f"has closed (likely shipped; verify, then retire):")
        for line in gates["shipped"]:
            print(f"  ! {line}")
    if gates["unblocked"]:
        print(f"\nUNBLOCKED — {len(gates['unblocked'])} draft(s) whose `Blocked-by:` "
              f"has closed (ready to start):")
        for line in gates["unblocked"]:
            print(f"  > {line}")
    if gates["partial"]:
        print(f"\npartly unblocked — {len(gates['partial'])} draft(s) with some "
              f"gates closed:")
        for line in gates["partial"]:
            print(f"  ~ {line}")
    if gates["unreadable"]:
        print(f"\nunreadable — {len(gates['unreadable'])} declared gate(s):")
        for line in gates["unreadable"]:
            print(f"  ? {line}")

    # Advisory only — never affects the exit code. A draft citing a closed issue
    # with no declared gate may be shipped OR newly unblocked; that is a
    # judgement, not drift. Drafts that DO declare a gate are reported above
    # instead, so this list is the genuinely-ambiguous remainder.
    if notes:
        print(f"\nadvisory — {len(notes)} undeclared draft(s) citing a closed issue:")
        for line in notes:
            print(f"  ? {line}")

    return 1 if problems else 0


def active_strays(root: Path) -> "list[Path]":
    """Files under active/ the lifecycle tooling cannot see.

    `check`, `orphans` and the dashboard all scan `active/*.md` — top level
    only. Anything else under active/ (a pre-migration `active/<target>/`
    subdirectory, a stray script) is therefore invisible to every guard, which
    is how five completed leftovers sat there for a month+ until the
    2026-08-19 sweep: three prompts whose completion records had existed since
    May/July, and two retired ground-truth scripts. A prompt belongs at
    `active/<name>.md`; anything else belongs in another state folder or in
    `complete/archive/`."""
    active_dir = root / "active"
    if not active_dir.is_dir():
        return []
    strays = []
    for f in sorted(active_dir.rglob("*")):
        if f.is_dir():
            continue
        if f.parent == active_dir and f.suffix == ".md":
            continue
        strays.append(f)
    return strays


def orphan_prompts(root: Path) -> "list[Path]":
    """active/*.md that no registry entry claims — the mirror of registry_problems().

    `check` validates registry -> prompt. This is prompt -> registry: a prompt
    sitting in active/ that nothing lists is work whose state nobody is
    tracking, which is how the M0-M3 release-validation chain shipped without a
    single entry being retired.

    A prompt counts as claimed either by a registry `prompt:` path that resolves
    to it, or by an entry whose slug matches its filename stem — many entries
    predate the `prompt:` convention and identify their file by name alone.
    """
    active_dir = root / "active"
    if not active_dir.is_dir():
        return []

    claimed: "set[Path]" = set()
    slugs: "set[str]" = set()
    for reg in REGISTRY_FILES:
        for slug, fields in registry_entries(root / reg):
            slugs.add(safe_name(slug))
            raw = fields.get("prompt")
            if not raw:
                continue
            resolved, _ = resolve_prompt(root, raw.split()[0])
            if resolved is not None:
                claimed.add(resolved.resolve())

    orphans = []
    for f in sorted(active_dir.glob("*.md")):
        if f.resolve() in claimed or safe_name(f.stem) in slugs:
            continue
        orphans.append(f)
    return orphans


def cmd_orphans(args) -> int:
    """Report active/ prompts no registry claims.

    This condition is now part of `check` (it became a gate on 2026-08-08, once
    the 8-prompt backlog the audit found was triaged to zero). The subcommand
    stays as the focused view — `check` reports orphans alongside everything
    else, this lists only them.
    """
    orphans = orphan_prompts(ROOT)
    if not orphans:
        print("lifecycle orphans: none")
        return 0
    print(f"lifecycle orphans: {len(orphans)} active/ prompt(s) no registry claims")
    for f in orphans:
        print(f"  - {f.relative_to(ROOT)}")
    return 1



# --------------------------------------------------------------------------- #
# epics — retire shipped entries out of epics.md
#
# epics.md is a live board: the dashboard renders every entry under "Epics"
# with a resume prompt. Nothing ever took an entry off it, so a programme that
# had shipped months ago still invited a session to continue it. An entry whose
# `status:` OPENS with SHIPPED or COMPLETE is done (a status that merely
# MENTIONS a shipped phase — "phase 2 SHIPPED; phase 3 open" — is not), and its
# text is preserved under complete/archive/epics/ rather than deleted.
# --------------------------------------------------------------------------- #
# Anchored, deliberately: the whole point is that a status naming one shipped
# phase mid-sentence does not retire a still-running epic.
DONE_STATUS_RE = re.compile(r"^(shipped|complete)", re.IGNORECASE)


def epic_blocks(path: Path) -> "tuple[list[str], list[tuple[str, list[str]]]]":
    """(header lines, [(slug, block lines)]) for epics.md, verbatim.

    A block runs from its `## <slug>` heading to the line before the next `##`
    (or EOF); everything before the first heading is the file's header."""
    if not path.exists():
        return [], []
    header: "list[str]" = []
    blocks: "list[tuple[str, list[str]]]" = []
    slug: "str | None" = None
    cur: "list[str]" = []
    for line in path.read_text(errors="replace").splitlines():
        m = H2_RE.match(line)
        if m:
            if slug is not None:
                blocks.append((slug, cur))
            slug, cur = _slugify_h2(m.group(1)), [line]
            continue
        (cur if slug is not None else header).append(line)
    if slug is not None:
        blocks.append((slug, cur))
    return header, blocks


def epic_fields(block: "list[str]") -> "dict[str, str]":
    """`- key: value` fields of one epic block; first occurrence of a key wins."""
    fields: "dict[str, str]" = {}
    for line in block[1:]:
        f = FIELD_RE.match(line)
        if f:
            fields.setdefault(f.group(1).strip(), f.group(2).strip())
    return fields


def epic_is_done(fields: "dict[str, str]") -> bool:
    """True when `status:` OPENS with SHIPPED or COMPLETE (prefix, not search)."""
    return bool(DONE_STATUS_RE.match(fields.get("status", "").strip()))


def _git_ok(root: Path, args: "list[str]") -> bool:
    """True when `git <args>` succeeds. `_git` cannot say: it returns [] both
    for a failure and for a command with no output (`git mv`)."""
    import subprocess
    try:
        out = subprocess.run(["git", "-C", str(root), *args],
                             capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return False
    return out.returncode == 0


def _epic_archive_dest(root: Path, slug: str, fields: "dict[str, str]") -> "tuple[Path, Path | None]":
    """(archive file the entry text is appended to, ledger file to move | None).

    A ledger still under `draft/` or `active/` follows its epic into
    `complete/archive/epics/`; one already archived there is left alone and
    receives the text; anything else (a dated `complete/YYYY/MM/` record, a file
    in another repo) is not ours to move, so the text lands in `<slug>.md`."""
    archive_dir = root / "complete" / "archive" / "epics"
    raw = fields.get("ledger", "").strip()
    if raw and not raw.startswith(("http://", "https://")):
        rel = raw.split("#", 1)[0].strip()
        cand = (root / rel)
        try:
            inside = cand.resolve().relative_to(root.resolve())
        except ValueError:
            inside = None
        if inside is not None:
            if inside.parts[:1] in (("draft",), ("active",)) and cand.is_file():
                return archive_dir / cand.name, cand
            if str(inside.parent).replace("\\", "/") == "complete/archive/epics":
                return archive_dir / cand.name, None
    return archive_dir / f"{safe_name(slug)}.md", None


def _append_retired(dest: Path, title: str, block: "list[str]", day: str) -> None:
    """Append one epics.md entry verbatim under a dated retirement heading."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join(block).rstrip("\n")
    if dest.exists():
        existing = dest.read_text(errors="replace")
        if existing and not existing.endswith("\n"):
            existing += "\n"
    else:
        existing = f"# {title}\n"
    dest.write_text(f"{existing}\n## Retired from epics.md ({day})\n\n{body}\n")


def retire_epics(root: Path, apply: bool = False,
                 day: "str | None" = None) -> "list[dict]":
    """Report (or, with apply, perform) the retirement of every done entry."""
    import datetime
    if day is None:
        day = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    path = root / "epics.md"
    header, blocks = epic_blocks(path)
    done: "list[dict]" = []
    keep: "list[tuple[str, list[str]]]" = []
    for slug, block in blocks:
        fields = epic_fields(block)
        if not epic_is_done(fields):
            keep.append((slug, block))
            continue
        dest, move = _epic_archive_dest(root, slug, fields)
        done.append({
            "slug": slug,
            "ledger": fields.get("ledger", "").strip() or "(no ledger)",
            "archive": str(dest.relative_to(root)),
            "title": fields.get("title", "").strip() or slug,
            "move": move,
            "block": block,
        })
    if not apply or not done:
        return done

    for item in done:
        dest = root / item["archive"]
        move = item["move"]
        if move is not None:
            dest.parent.mkdir(parents=True, exist_ok=True)
            src_rel = str(move.relative_to(root))
            dst_rel = str(dest.relative_to(root))
            if not (_git_ok(root, ["ls-files", "--error-unmatch", "--", src_rel])
                    and _git_ok(root, ["mv", src_rel, dst_rel])):
                move.replace(dest)
        _append_retired(dest, item["title"], item["block"], day)

    out = list(header)
    for _, block in keep:
        out.extend(block)
    path.write_text("\n".join(out).rstrip("\n") + "\n")
    return done


def cmd_epics(args) -> int:
    done = retire_epics(ROOT, apply=args.retire)
    if not done:
        print("epics: nothing to retire")
        return 0
    for item in done:
        if args.retire:
            print(f"retired {item['slug']}: ledger -> {item['archive']}")
        else:
            print(f"{item['slug']} \u2014 {item['ledger']}")
    return 0


def _prune_ledger_section(path: Path, slug: str) -> bool:
    """Drop the `## <slug>` H2 section (heading through the line before the
    next H2, or EOF) from a ledger file. Returns True if a section was removed."""
    if not path.exists():
        return False
    want = safe_name(slug)
    lines = path.read_text(errors="replace").splitlines()
    out: "list[str]" = []
    i = 0
    removed = False
    while i < len(lines):
        m = H2_RE.match(lines[i])
        if m and safe_name(_slugify_h2(m.group(1))) == want:
            removed = True
            i += 1
            while i < len(lines) and not H2_RE.match(lines[i]):
                i += 1
            while out and not out[-1].strip():
                out.pop()
            if i < len(lines):
                out.append("")
            continue
        out.append(lines[i])
        i += 1
    if removed:
        path.write_text("\n".join(out).rstrip("\n") + "\n")
    return removed


def complete_bucket(date: "tuple[str, str] | None") -> Path:
    if date is None:
        return COMPLETE_DIR / "unknown"
    return COMPLETE_DIR / date[0] / date[1]


def _parse_date(arg: str) -> "tuple[str, str] | None":
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", arg)
    return (m.group(1), m.group(2)) if m else None


def _record_bucket_for(name: str) -> "Path | None":
    """Bucket of an existing dated record whose slug matches <name>, if any."""
    want = safe_name(name)
    for _, slug, path in _all_records():
        if safe_name(slug) == want:
            return path.parent
    return None


# --------------------------------------------------------------------------- #
# move
# --------------------------------------------------------------------------- #
def cmd_move(args) -> int:
    name = args.name
    if name.endswith(".md"):
        name = name[:-3]
    src = ACTIVE_DIR / f"{name}.md"
    if not src.exists():
        print(f"lifecycle move: not found in active/: {src.name}", file=sys.stderr)
        return 1

    if args.date:
        date = _parse_date(args.date)
        if date is None:
            print(f"lifecycle move: bad --date {args.date!r}", file=sys.stderr)
            return 1
        bucket = complete_bucket(date)
    else:
        bucket = _record_bucket_for(name)
        if bucket is None:
            print(
                f"lifecycle move: no --date and no existing record for {name!r}; "
                f"pass --date",
                file=sys.stderr,
            )
            return 1

    dest = bucket / src.name
    print(f"active/{src.name} -> {dest.relative_to(ROOT)}")
    if not args.apply:
        print("(dry run; pass --apply)")
        return 0
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Prefer git mv to preserve history; fall back to a plain rename.
    import subprocess

    r = subprocess.run(
        ["git", "-C", str(ROOT), "mv", str(src), str(dest)],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        src.rename(dest)
    return 0


# --------------------------------------------------------------------------- #
# record  (single-entry: the go-forward ship_* hook)
# --------------------------------------------------------------------------- #
def cmd_record(args) -> int:
    """Write ONE dated record from the rich completion body the ship skill
    drafted (--from-file), folding + removing the active/ prompt. The record is
    the sole completion ledger — regenerate complete/index.md afterwards."""
    src = Path(args.from_file)
    if not src.is_file():
        print(f"lifecycle record: --from-file not found: {src}", file=sys.stderr)
        return 1
    date = _parse_date(args.date)
    if date is None:
        print(f"lifecycle record: bad --date {args.date!r}", file=sys.stderr)
        return 1

    dest = complete_bucket(date) / f"{safe_name(args.slug)}.md"
    body = src.read_text(errors="replace").rstrip() + "\n"
    # fold the original active/ prompt (explicit --prompt, else guess from slug)
    prompt = None
    if args.prompt:
        p = ACTIVE_DIR / args.prompt
        if p.exists():
            prompt = p
    if prompt is None:
        guess = ACTIVE_DIR / f"{safe_name(args.slug).replace('-', '_')}.md"
        if guess.exists():
            prompt = guess
    if prompt is not None:
        body += "\n## Original prompt\n\n" + prompt.read_text(errors="replace")

    print(f"record: {dest.relative_to(ROOT)}"
          + (f"  (+folds active/{prompt.name})" if prompt else ""))
    slug_in_active_md = safe_name(args.slug) in {
        safe_name(s) for s in ledger_slugs(ACTIVE_MD)
    }
    if slug_in_active_md:
        print(f"active.md: will remove section for {safe_name(args.slug)!r}")
    if not args.apply:
        print("(dry run; pass --apply)")
        return 0
    import subprocess

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(body)
    subprocess.run(["git", "-C", str(ROOT), "add", str(dest)],
                   capture_output=True, text=True)
    if prompt is not None:
        r = subprocess.run(["git", "-C", str(ROOT), "rm", "-q", str(prompt)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            prompt.unlink(missing_ok=True)

    # Freshen complete/index.md in the same step so a shipped record never
    # leaves it stale — the Lifecycle Drift guard runs `index --check` on every
    # push to main touching complete/**, and the separate `index --apply` step
    # was easy to forget (failing runs + maintainer emails). Same effect as
    # cmd_index --apply, folded in so the two can't drift apart.
    INDEX_MD.write_text(_render_index(_existing_curated()))
    subprocess.run(["git", "-C", str(ROOT), "add", str(INDEX_MD)],
                   capture_output=True, text=True)
    print(f"index: refreshed {INDEX_MD.relative_to(ROOT)} "
          f"({len(_all_records())} records)")

    # Prune the task's `## <slug>` section from the active.md registry in the
    # same step — `check` fails ("finished but still active") on every later
    # push to main while a shipped slug lingers there, and the manual registry
    # edit in the ship skills was easy to forget (2026-07-30 email storm).
    if _prune_ledger_section(ACTIVE_MD, args.slug):
        subprocess.run(["git", "-C", str(ROOT), "add", str(ACTIVE_MD)],
                       capture_output=True, text=True)
        print(f"active.md: removed shipped section {safe_name(args.slug)!r}")
    return 0


# --------------------------------------------------------------------------- #
# index  (token-light navigation over the complete/ archive)
# --------------------------------------------------------------------------- #
INDEX_MD = COMPLETE_DIR / "index.md"
CURATED_START = "<!-- CURATED:START -->"
CURATED_END = "<!-- CURATED:END -->"
GEN_START = "<!-- GENERATED:START — edit records, not this block; regenerate with `lifecycle.py index --apply` -->"
GEN_END = "<!-- GENERATED:END -->"


def _record_hook(path: Path) -> str:
    """One-line hook for a record: the H2 parenthetical, else the summary snippet."""
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return ""
    first = text.splitlines()[0] if text else ""
    m = re.search(r"\((.*)\)\s*$", first)
    hook = m.group(1).strip() if m else ""
    # a bare date / trivial paren is no hook — fall back to the summary line
    if not hook or re.fullmatch(r"[\d\-/ ]+|MERGED|complete|done", hook, re.I):
        sm = re.search(r"^-\s*summary:\s*(.+)$", text, re.MULTILINE)
        if sm:
            hook = sm.group(1)
    hook = re.sub(r"\s+", " ", hook).strip(" |")
    return (hook[:110] + "…") if len(hook) > 111 else hook


def _all_records() -> "list[tuple[str, str, Path]]":
    """(bucket, slug, path) for every complete/ record, newest bucket first."""
    if not COMPLETE_DIR.exists():
        return []
    recs = []
    for f in COMPLETE_DIR.rglob("*.md"):
        if f.name in ("index.md", "AGENTS.md") or ARCHIVE_DIR in f.parents:
            continue
        bucket = "/".join(f.relative_to(COMPLETE_DIR).parts[:-1]) or "unknown"
        recs.append((bucket, f.stem, f))

    def _key(r):
        b = r[0]
        if b == "unknown":
            return (1, 0, 0, r[1])          # unknown bucket sorts last
        parts = b.split("/")
        y = int(parts[0])
        m = int(parts[1]) if len(parts) > 1 else 0
        return (0, -y, -m, r[1])            # dated: reverse-chronological, then slug

    recs.sort(key=_key)
    return recs


def _render_index(curated: str) -> str:
    recs = _all_records()
    from collections import OrderedDict
    by_bucket: "OrderedDict[str, list]" = OrderedDict()
    for bucket, slug, path in recs:
        by_bucket.setdefault(bucket, []).append((slug, path))
    lines = [
        "# complete/ — finished-work archive index",
        "",
        "Token-light navigation over the finished-work records (schema:",
        "[`AGENTS.md`](AGENTS.md)). **Generated** from the records by",
        "`scripts/lifecycle.py index` — read this, follow one or two links, and",
        "only then grep a dated bucket. Curators: edit the band between the CURATED",
        "markers; everything below GENERATED is rebuilt.",
        "",
        f"{len(recs)} records across {len(by_bucket)} buckets.",
        "",
        CURATED_START,
        curated.strip() or "## Highlights\n\n_(curate hard-won records here — survives regeneration.)_",
        CURATED_END,
        "",
        GEN_START,
        "",
    ]
    for bucket, items in by_bucket.items():
        lines.append(f"## {bucket}")
        lines.append("")
        for slug, path in sorted(items):
            hook = _record_hook(path)
            rel = path.relative_to(COMPLETE_DIR).as_posix()
            lines.append(f"- [{slug}]({rel})" + (f" — {hook}" if hook else ""))
        lines.append("")
    lines.append(GEN_END)
    return "\n".join(lines).rstrip() + "\n"


def _existing_curated() -> str:
    if not INDEX_MD.exists():
        return ""
    text = INDEX_MD.read_text(errors="replace")
    if CURATED_START in text and CURATED_END in text:
        return text.split(CURATED_START, 1)[1].split(CURATED_END, 1)[0].strip()
    return ""


def cmd_index(args) -> int:
    rendered = _render_index(_existing_curated())
    if args.check:
        current = INDEX_MD.read_text(errors="replace") if INDEX_MD.exists() else ""
        if current != rendered:
            print("lifecycle index: DRIFT — complete/index.md is stale; "
                  "run `lifecycle.py index --apply`", file=sys.stderr)
            return 1
        print("lifecycle index: OK")
        return 0
    if args.apply:
        INDEX_MD.write_text(rendered)
        print(f"wrote {INDEX_MD.relative_to(ROOT)} ({len(_all_records())} records)")
    else:
        print(rendered)
    return 0


# --------------------------------------------------------------------------- #
# check
# --------------------------------------------------------------------------- #
def cmd_dates(args) -> int:
    """Report — and with --write, backfill — the dates on active/issued tasks."""
    root = ROOT
    if args.write:
        results = backfill_dates(root, apply=True)
        wrote = [r for r in results if r["date"]]
        for r in wrote:
            print(f"  + {r['what']}: {r['key']}: {r['date']}  ({r['source']})")
        unknown = [r for r in results if not r["date"]]
        for r in unknown:
            print(f"  ? {r['what']}: no date in git history or prose — date it by hand")
        print(f"dates: wrote {len(wrote)}, undatable {len(unknown)}")
        return 0

    missing = undated_entries(root)
    prompts = [(f, s) for f, s in state_prompts(root)
               if prompt_date(f.read_text(errors="replace"))[0] is None]
    for e in missing:
        key = REGISTRY_DATE_KEY[e["registry"]]
        print(f"  - {e['registry']}: {e['slug']}: no `{key}:` date")
    for f, state in prompts:
        print(f"  - {f.relative_to(root)}: no "
              f"`{PROMPT_DATE_KEY[state]}:` header")
    if not (missing or prompts):
        print("dates: OK — every registry entry and prompt is dated")
        return 0
    print(f"dates: {len(missing) + len(prompts)} undated "
          f"(run `lifecycle.py dates --write` to backfill from git history)")
    return 1 if args.check else 0


def cmd_check(args) -> int:
    problems: "list[str]" = []
    a_slugs = {safe_name(s) for s in ledger_slugs(ACTIVE_MD)}
    rec_by_slug: "dict[str, Path]" = {}
    for _, slug, path in _all_records():
        rec_by_slug.setdefault(safe_name(slug), path)

    for s in sorted(a_slugs & set(rec_by_slug)):
        problems.append(
            f"active.md slug has a complete/ record (finished but still "
            f"active?): {s} -> {rec_by_slug[s].relative_to(ROOT)}"
        )

    # a file should not exist in two state dirs at once
    if ACTIVE_DIR.exists() and COMPLETE_DIR.exists():
        active_names = {f.name for f in ACTIVE_DIR.glob("*.md")}
        for f in COMPLETE_DIR.rglob("*.md"):
            if ARCHIVE_DIR in f.parents:
                continue
            if f.name in active_names:
                problems.append(f"file in both active/ and complete/: {f.name}")

    problems.extend(registry_problems(ROOT))
    problems.extend(
        f"active/ prompt no registry entry claims: {f.relative_to(ROOT)}"
        for f in orphan_prompts(ROOT)
    )
    problems.extend(
        f"active/ stray the lifecycle tooling cannot see (retire, or re-home "
        f"to a state folder): {f.relative_to(ROOT)}"
        for f in active_strays(ROOT)
    )

    # A row that declares its PRs are open and names none contradicts itself,
    # so it is drift like the rest. An uncleared `pending-release:` does not:
    # the key MEANS "not released yet", and a library can legitimately sit
    # unreleased for weeks — reported, exit code untouched.
    problems.extend(pr_key_problems(ROOT))
    warnings: "list[str]" = list(pending_release_problems(ROOT))

    if problems:
        print("lifecycle check: DRIFT")
        for p in problems:
            print(f"  - {p}")
        for w in warnings:
            print(f"  ! warning: {w}")
        return 1
    if warnings:
        print(f"lifecycle check: OK ({len(warnings)} warning(s))")
        for w in warnings:
            print(f"  ! warning: {w}")
        return 0
    print("lifecycle check: OK")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="PyAutoMind prompt-file lifecycle engine")
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("move", help="advance active/<name> -> complete/YYYY/MM/")
    m.add_argument("name")
    m.add_argument("--date", help="completion date YYYY-MM-DD (else from the matching record)")
    m.add_argument("--apply", action="store_true")
    m.set_defaults(func=cmd_move)

    r = sub.add_parser("record", help="write one dated record from a completion body (ship_* hook)")
    r.add_argument("slug", help="the task slug for the shipped task")
    r.add_argument("--date", required=True, help="completion date YYYY-MM-DD")
    r.add_argument("--from-file", required=True, dest="from_file",
                   help="path to the rich completion body drafted by the ship skill")
    r.add_argument("--prompt", help="active/ prompt filename to fold + remove")
    r.add_argument("--apply", action="store_true")
    r.set_defaults(func=cmd_record)

    ix = sub.add_parser("index", help="generate complete/index.md (token-light archive navigation)")
    ix.add_argument("--apply", action="store_true", help="write complete/index.md")
    ix.add_argument("--check", action="store_true", help="fail if index.md is stale (CI)")
    ix.set_defaults(func=cmd_index)

    c = sub.add_parser("check", help="drift guard (non-zero exit on drift)")
    c.set_defaults(func=cmd_check)

    d = sub.add_parser(
        "dates",
        help="report (or --write to backfill from git) the date on every "
             "registry entry and issued prompt",
    )
    d.add_argument("--write", action="store_true",
                   help="insert the missing date fields in place")
    d.add_argument("--check", action="store_true",
                   help="non-zero exit when anything is undated (CI)")
    d.set_defaults(func=cmd_dates)

    iss = sub.add_parser(
        "issues",
        help="cross-check registry tracking issues + pr-open PRs against "
             "GitHub (needs gh, or network + optional GITHUB_TOKEN)",
    )
    iss.add_argument("--drafts", action="store_true",
                     help="also flag draft/ prompts citing a closed issue (advisory)")
    iss.set_defaults(func=cmd_issues)

    o = sub.add_parser("orphans", help="report active/ prompts no registry claims")
    o.set_defaults(func=cmd_orphans)

    e = sub.add_parser(
        "epics",
        help="report (or --retire) epics.md entries whose status is SHIPPED/COMPLETE",
    )
    e.add_argument("--retire", action="store_true",
                   help="archive the entry text (and a draft/active ledger) and "
                        "delete the entry from epics.md")
    e.set_defaults(func=cmd_epics)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
