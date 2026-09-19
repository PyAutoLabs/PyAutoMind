#!/usr/bin/env python3
"""Classify a PyAutoMind branch diff as *ledger* or *code*.

WHY THIS EXISTS. PyAutoMind's own work strands. A branch-scoped session (the
phone, claude.ai/code, any `claude/**` or `codex/**` flow) pushes its Mind changes to a
feature branch — `prompt_sync.sh` pushes HEAD deliberately, so a cloud session
cannot bypass review — and then nothing moves them. No workflow even *looks* at
a `claude/**` or `codex/**` push: `lifecycle_drift`, `dashboard_refresh`, `firewall_gate` and
`spawn_drift` all trigger on `push: main` or `pull_request` only. The branch
sits there until a human writes an explicit "merge this" prompt.

Almost all of what strands is *ledger*: a prompt filed under `draft/`, a task
moved `active/` → `complete/`, a registry line, a regenerated dashboard. It is
the organism's own bookkeeping, it is generated or template-shaped, its drift
checks are already automated, and a human reviewing it adds nothing. The
minority that is *code* — `scripts/`, `tests/`, `.github/`, `skills/`,
`policy/`, `repos.yaml`, the doc pages — is exactly what review is for.

So this script draws that line, and `mind_ledger_merge.yml` merges only what
falls on the ledger side of it. The gate is a script, not workflow YAML, so it
is testable and so a session can predict the verdict before it pushes.

DEFAULT DENY. A path is ledger only by matching a rule below; an unrecognised
one — a new root file, a new top-level folder — is code. Getting that backwards
would auto-merge the next thing nobody thought about.

Usage:
    python3 scripts/ledger_merge.py classify --base origin/main   # diff HEAD vs base
    python3 scripts/ledger_merge.py classify path/one path/two    # explicit paths
    ... < paths-on-stdin
    python3 scripts/ledger_merge.py merge-entries BASE OURS THEIRS [--write PATH]
    python3 scripts/ledger_merge.py resolve      # inside a conflicted `git merge`

CONFLICTS ARE SETTLED BY THE FILE'S GRAMMAR, NOT BY A HUMAN. Every ledger
branch rewrites the same few files — the `## slug` registries and the
generated renders — so git's line merge stops on two branches that never
touched the same entry (24 of 100 runs in the week to 2026-09-17, six
completion records stranded, nobody told). `merge-entries` is a three-way
merge at entry granularity; `resolve` applies it to the registries of an
in-progress merge, takes main's copy of the renders (they are regenerated on
the merged tree), and leaves only a genuine both-sides edit of one slug — or
a path the grammar does not cover — for a human.

Sources take precedence in that order: explicit paths, then `--base`, then
stdin. Stdin is read only when neither of the others is given, so a `--base`
run never blocks on a stdin that stays open (a harness socket).

Exit codes: 0 = ledger-only (safe to auto-merge) · 1 = holds code (a human's
call) · 2 = the script could not run. The caller must distinguish 1 from 2:
"a human should look" and "the gate is broken" are not the same answer.
"""

from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path

# Directories holding nothing but the task ledger: prompts, in-flight state and
# the completion records. Their whole contents are ledger (subject to the
# EXCLUDED_NAMES guard below).
LEDGER_DIRS = ("draft/", "active/", "complete/", "batches/")

# `batches/` joins the state folders (2026-08-30): a batch record is the ledger
# of what was dispatched into one shift and what came back — the same genre as
# `complete/`, written by the workflow, read by the next slot. It has to land
# without a human, or the unattended system cannot record its own history
# unattended.
#
# Root files that are registry state or a generated render of it. Deliberately
# NOT here: README.md, AGENTS.md, CLAUDE.md, REFERENCE.md, ROUTING.md,
# CONTRIBUTING.md, AI_POLICY.md, repos.yaml, themes.md — prose and
# configuration a human reads, changed rarely and on purpose. `themes.md` sits
# with repos.yaml rather than with the registries it resembles: it is a
# CONTROLLED vocabulary, and the control is the human. A keyword added without
# review is a grouping key nobody chose, and the dashboard reads it on every
# render.
LEDGER_FILES = (
    "active.md",
    "planned.md",
    "parked.md",
    "condemned.md",
    "epics.md",
    "bundles.md",
    "ideas.md",
    "autonomy_log.md",
    "dashboard.md",
    "dashboard.html",
    "queue.md",
)

# Names that are ledger by location but executable by collection. The ledger
# dirs do carry inert assets — a prompt's reproduction script under
# `draft/bug/autofit/*_assets/`, say — and those are fine. A file pytest would
# *collect*, though, runs in CI from anywhere in the tree, so it is code
# wherever it sits.
EXCLUDED_NAMES = ("conftest.py", "test_*.py", "*_test.py")


def is_ledger_path(path: str) -> bool:
    """True if `path` (repo-relative, POSIX separators) is ledger material."""
    # Normalise away "./" and any "..", so a traversal cannot smuggle a code
    # path in behind a ledger prefix.
    parts = [p for p in path.replace("\\", "/").split("/") if p not in ("", ".")]
    if not parts or ".." in parts:
        return False
    # A dot-directory or dot-file anywhere is never ledger: `.github/`,
    # `.claude/`, `.codex/`, `.gitignore` all carry behaviour.
    if any(p.startswith(".") for p in parts):
        return False
    name = parts[-1]
    if any(fnmatch.fnmatch(name, pattern) for pattern in EXCLUDED_NAMES):
        return False
    normalised = "/".join(parts)
    if len(parts) == 1:
        return normalised in LEDGER_FILES
    return any(normalised.startswith(d) for d in LEDGER_DIRS)


def classify(paths):
    """Split `paths` into (ledger, blocked), preserving order and dropping dupes."""
    ledger, blocked, seen = [], [], set()
    for path in paths:
        path = path.strip()
        if not path or path in seen:
            continue
        seen.add(path)
        (ledger if is_ledger_path(path) else blocked).append(path)
    return ledger, blocked


def changed_paths(base: str, head: str = "HEAD"):
    """Paths changed by `head` relative to its merge base with `base`.

    Three-dot: a branch that merged main into itself must be judged on what it
    *adds*, not on everything main moved underneath it, or every long-running
    branch reads as code the moment someone else touches `scripts/`.
    """
    proc = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...{head}"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parents[1],
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit(2)
    return [line for line in proc.stdout.splitlines() if line.strip()]


# --- merge-entries: a three-way merge at ENTRY granularity ---------------------
#
# WHY. The registry files (`active.md`, `planned.md`, `parked.md`,
# `condemned.md`, `epics.md`) are lists of `## <slug>` entries, and every
# session edits them: a task issued adds one, a status change rewrites one, a
# close-out deletes one. Two branches in flight touch the same FILE almost
# every time and the same ENTRY almost never — yet git's line merge sees two
# edits near the same lines and stops, and `mind_ledger_merge.yml` then leaves
# the branch for a human who never comes (24 of 100 runs failed in the week to
# 2026-09-17; six completion records were stranded). Merging by entry is the
# merge git would do if it knew the file's grammar: an entry is one unit,
# changed by at most one side, and only a genuine both-sides edit of the SAME
# slug is a conflict.
#
# The preamble (everything before the first `## `, including the generated
# `<!-- toc:start -->` block) is taken from OURS; the caller regenerates the
# contents block (`registry_toc.py --write`) after the merge.

ENTRY_MERGED_FILES = ("active.md", "planned.md", "parked.md", "condemned.md", "epics.md")


def split_entries(text: str):
    """(preamble, [(slug, entry_text), ...]) — an entry runs from its `## `
    heading to the next heading; the trailing newline stays with the entry."""
    lines = text.splitlines(keepends=True)
    preamble, entries, current = [], [], None
    for line in lines:
        if line.startswith("## "):
            current = [line.rstrip("\n").strip(), [line]]
            entries.append(current)
        elif current is None:
            preamble.append(line)
        else:
            current[1].append(line)
    # An entry's trailing blank lines are layout, not content: the last entry
    # of a file has none and gains one the moment something is appended after
    # it, which must not read as "both sides changed it". Normalise every entry
    # to end in exactly one blank line; `join_entries` fixes the file's tail.
    return "".join(preamble), [(slug, "".join(body).rstrip("\n") + "\n\n") for slug, body in entries]


def join_entries(preamble: str, entries) -> str:
    """The inverse of `split_entries` up to trailing-blank-line layout."""
    text = preamble + "".join(body for _, body in entries)
    return text.rstrip("\n") + "\n" if entries else preamble


def merge_entries(base: str, ours: str, theirs: str):
    """Three-way merge of entry lists. Returns (merged_text, conflicts) where
    conflicts is the list of slugs both sides changed differently; when it is
    non-empty merged_text is None."""
    base_pre, base_entries = split_entries(base)
    ours_pre, ours_entries = split_entries(ours)
    theirs_pre, theirs_entries = split_entries(theirs)
    b = dict(base_entries)
    o = dict(ours_entries)
    t = dict(theirs_entries)
    ours_order = [slug for slug, _ in ours_entries]
    theirs_order = [slug for slug, _ in theirs_entries]

    conflicts: list[str] = []
    result: dict[str, str | None] = {}  # slug -> text, or None when dropped
    for slug in set(b) | set(o) | set(t):
        in_b, in_o, in_t = slug in b, slug in o, slug in t
        if in_b:
            ours_changed = (not in_o) or o[slug] != b[slug]
            theirs_changed = (not in_t) or t[slug] != b[slug]
            if not theirs_changed:
                result[slug] = o.get(slug)            # ours wins, deletion included
            elif not ours_changed:
                result[slug] = t.get(slug)            # theirs wins, deletion included
            elif o.get(slug) == t.get(slug):
                result[slug] = o.get(slug)            # both made the same change
            else:
                conflicts.append(slug)
        else:
            if in_o and in_t and o[slug] != t[slug]:
                conflicts.append(slug)
            else:
                result[slug] = o.get(slug) if in_o else t[slug]
    if conflicts:
        return None, sorted(conflicts)

    # Order: ours' order, with theirs' additions inserted after the entry that
    # precedes them in theirs (or at the end when nothing precedes).
    order = [slug for slug in ours_order if result.get(slug) is not None]
    for i, slug in enumerate(theirs_order):
        if slug in order or result.get(slug) is None:
            continue
        prev = next((p for p in reversed(theirs_order[:i]) if p in order), None)
        order.insert(order.index(prev) + 1 if prev else len(order), slug)
    return join_entries(ours_pre, [(slug, result[slug]) for slug in order]), []


# Renders of the ledger, never sources: on a conflict they take main's side and
# are regenerated on the merged tree by the caller.
GENERATED_FILES = ("dashboard.md", "dashboard.html", "complete/index.md")


def _git(*args, cwd):
    return subprocess.run(["git", *args], capture_output=True, text=True, cwd=cwd)


def resolve_conflicts(cwd=None) -> tuple[list[str], list[str]]:
    """Resolve the unmerged paths of an in-progress `git merge` that the ledger
    grammar can settle, and stage them. Returns (resolved, unresolved):
    generated renders take OURS (main) and are re-rendered afterwards; the
    `## slug` registries merge by entry; anything else — or an entry both
    sides changed — is left unmerged for a human."""
    root = Path(cwd) if cwd else Path(__file__).resolve().parents[1]
    unmerged = [p for p in _git("diff", "--name-only", "--diff-filter=U", cwd=root).stdout.splitlines() if p]
    resolved, unresolved = [], []
    for path in unmerged:
        if path in GENERATED_FILES:
            _git("checkout", "--ours", "--", path, cwd=root)
            _git("add", "--", path, cwd=root)
            resolved.append(f"{path} (render: main's copy, regenerated after the merge)")
        elif path in ENTRY_MERGED_FILES:
            stages = [_git("show", f":{n}:{path}", cwd=root) for n in (1, 2, 3)]
            if any(s.returncode != 0 for s in stages):
                unresolved.append(f"{path} (added on both sides, or deleted on one)")
                continue
            merged, conflicts = merge_entries(*(s.stdout for s in stages))
            if conflicts:
                unresolved.append(f"{path} (both sides changed {', '.join(conflicts)})")
                continue
            (root / path).write_text(merged, encoding="utf-8")
            _git("add", "--", path, cwd=root)
            resolved.append(f"{path} (merged by entry)")
        else:
            unresolved.append(path)
    return resolved, unresolved


def _resolve_cli(args) -> int:
    resolved, unresolved = resolve_conflicts(args.root)
    for line in resolved:
        print(f"resolved: {line}")
    for line in unresolved:
        print(f"unresolved: {line}")
    if not resolved and not unresolved:
        print("nothing to resolve")
    return 1 if unresolved else 0


def _merge_entries_cli(args) -> int:
    base = Path(args.base_file).read_text(encoding="utf-8")
    ours = Path(args.ours_file).read_text(encoding="utf-8")
    theirs = Path(args.theirs_file).read_text(encoding="utf-8")
    merged, conflicts = merge_entries(base, ours, theirs)
    if conflicts:
        print("conflict: both sides changed " + ", ".join(conflicts))
        return 1
    if args.write:
        Path(args.write).write_text(merged, encoding="utf-8")
        print(f"merged by entry -> {args.write}")
    else:
        sys.stdout.write(merged)
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    cls = sub.add_parser("classify", help="ledger-only, or does it hold code?")
    cls.add_argument("paths", nargs="*", help="repo-relative paths (else --base, else stdin)")
    cls.add_argument("--base", help="diff HEAD against the merge base with this ref")
    cls.add_argument("--head", default="HEAD", help="the branch tip to judge (default HEAD)")
    mrg = sub.add_parser("merge-entries",
                         help="three-way merge a `## slug` registry file by entry")
    mrg.add_argument("base_file")
    mrg.add_argument("ours_file")
    mrg.add_argument("theirs_file")
    mrg.add_argument("--write", metavar="PATH", help="write the merge here (else stdout)")
    res = sub.add_parser("resolve", help="settle the ledger-grammar conflicts of an in-progress "
                                         "git merge (renders take main, registries merge by entry)")
    res.add_argument("--root", help="the repo with the merge in progress (default: this one)")
    args = parser.parse_args(argv)
    if args.command == "merge-entries":
        return _merge_entries_cli(args)
    if args.command == "resolve":
        return _resolve_cli(args)

    # Source precedence: explicit paths, then --base, then stdin. `--base` must
    # never read stdin: a Claude Code web/mobile session runs commands with a
    # stdin that is not a TTY and never closes (a harness socket, not a pipe),
    # so an `isatty()` test that falls through to `sys.stdin.read()` blocks
    # forever, and `classify --base origin/main` hung there twice before this
    # order was fixed (2026-09-17). Stdin is read only when it is the sole
    # source left — the documented `... < paths` usage — where a caller that
    # pipes nothing has asked for exactly the wait it gets, as with `cat`.
    if args.paths:
        paths = args.paths
    elif args.base:
        paths = []
    elif not sys.stdin.isatty():
        paths = sys.stdin.read().splitlines()
    else:
        parser.error("give paths, pass --base, or pipe paths in")
        return 2
    # Strip blanks BEFORE the emptiness check, not inside classify(): a stdin
    # of "\n" is one empty string, which is a truthy list, and an unfiltered
    # check would call that "0 ledger paths" and exit 0 — fail-open, on the one
    # question this gate exists to answer.
    paths = [p.strip() for p in paths if p.strip()]
    if args.base and not paths:
        paths = changed_paths(args.base, args.head)

    if not paths:
        # Nothing changed is not "safe to merge" — there is nothing to merge,
        # and the caller must not read exit 0 as "go". Say so and block.
        print("no changed paths — nothing to merge")
        return 1

    ledger, blocked = classify(paths)
    if blocked:
        print(f"code: {len(blocked)} of {len(ledger) + len(blocked)} path(s) need a human")
        for path in blocked:
            print(f"  {path}")
        return 1
    print(f"ledger-only: {len(ledger)} path(s)")
    for path in ledger:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
