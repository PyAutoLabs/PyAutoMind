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

  check
        Drift guard (mirrors repos_sync.py --check; non-zero exit on drift):
          * no active.md slug has a complete/ record (finished but still active)
          * no file lives in two states at once
          * every registry `prompt:` path resolves, exactly rather than by
            fallback, and into the state folder its registry implies
          * no slug is listed in two registries at once
          * no active/ prompt is left unclaimed by every registry
        Wire into /health and CI.

  orphans
        The focused view of `check`'s last leg: active/ prompts that no registry
        entry claims. `check` grades this too — this lists only them.

  issues
        The ONLINE leg (needs `gh` + network, so deliberately not part of
        `check`): every registry entry's tracking issue cross-checked against
        GitHub. Catches finished work still listed as pending — the class no
        offline check can see.

This file is intentionally stdlib-only (no PyAuto imports) so it runs in any
environment, including a bare template checkout.
"""
from __future__ import annotations

import argparse
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


def _gh_issue_states(urls: "list[str]") -> "dict[str, str]":
    """{url: state} via the `gh` CLI. Requires gh + network; online leg only."""
    import subprocess

    states: "dict[str, str]" = {}
    for url in urls:
        m = ISSUE_URL_RE.match(url)
        if not m:
            continue
        owner, repo, num = m.groups()
        try:
            r = subprocess.run(
                ["gh", "api", f"repos/{owner}/{repo}/issues/{num}", "--jq", ".state"],
                capture_output=True, text=True,
            )
        except FileNotFoundError:
            raise GhUnavailable
        if r.returncode != 0:
            tail = (r.stderr.strip().splitlines() or ["error"])[-1]
            states[url] = f"unreadable: {tail}"
            continue
        states[url] = r.stdout.strip()
    return states


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
    """Cross-check every registry entry's tracking issue against GitHub."""
    try:
        problems = issue_problems(ROOT)
    except GhUnavailable:
        print(
            "lifecycle issues: cannot run — the `gh` CLI is not installed.\n"
            "  This leg needs GitHub; it is deliberately separate from `check`,\n"
            "  which stays hermetic for CI. Install gh, or run this from a\n"
            "  session that has it.",
            file=sys.stderr,
        )
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
        print(f"lifecycle issues: OK ({len(registry_issue_refs(ROOT))} tracking issue(s) open)")

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

    if problems:
        print("lifecycle check: DRIFT")
        for p in problems:
            print(f"  - {p}")
        return 1
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

    iss = sub.add_parser(
        "issues", help="cross-check registry tracking issues against GitHub (needs gh)"
    )
    iss.add_argument("--drafts", action="store_true",
                     help="also flag draft/ prompts citing a closed issue (advisory)")
    iss.set_defaults(func=cmd_issues)

    o = sub.add_parser("orphans", help="report active/ prompts no registry claims")
    o.set_defaults(func=cmd_orphans)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
