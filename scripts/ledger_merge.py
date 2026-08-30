#!/usr/bin/env python3
"""Classify a PyAutoMind branch diff as *ledger* or *code*.

WHY THIS EXISTS. PyAutoMind's own work strands. A branch-scoped session (the
phone, claude.ai/code, any `claude/**` flow) pushes its Mind changes to a
feature branch — `prompt_sync.sh` pushes HEAD deliberately, so a cloud session
cannot bypass review — and then nothing moves them. No workflow even *looks* at
a `claude/**` push: `lifecycle_drift`, `dashboard_refresh`, `firewall_gate` and
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


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    cls = sub.add_parser("classify", help="ledger-only, or does it hold code?")
    cls.add_argument("paths", nargs="*", help="repo-relative paths (else stdin, else --base)")
    cls.add_argument("--base", help="diff HEAD against the merge base with this ref")
    cls.add_argument("--head", default="HEAD", help="the branch tip to judge (default HEAD)")
    args = parser.parse_args(argv)

    if args.paths:
        paths = args.paths
    elif not sys.stdin.isatty():
        paths = sys.stdin.read().splitlines()
    elif args.base:
        paths = []
    else:
        parser.error("give paths, pipe them in, or pass --base")
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
