#!/usr/bin/env python3
"""spawn — stamp fresh-slate template repos from the live Mind and Memory.

Implements docs/pyautobrain/spawn_spec.md (the partition rules are data
below; change the spec first, then mirror it here). Same doctrine as
repos_sync.py: single source (the live repos) -> generated view (the
templates), re-runnable, drift-checked.

Usage:
    python3 scripts/spawn.py                     # dry-run: print the file plan
    python3 scripts/spawn.py --write DIR         # materialise templates under DIR
    python3 scripts/spawn.py --check DIR         # regenerate + diff (CI; exit 1 on drift)
    python3 scripts/spawn.py --stamp-family DIR  # stamp mechanical layers into family checkouts
    python3 scripts/spawn.py --root DIR          # override the workspace root

spawn never mutates a live repo. Only tracked files (git ls-files) are read.
Every file is assigned by the FIRST matching rule; unmatched files are
DROP + WARN and the run fails on any WARN (extend the spec's tables via a
human decision, then mirror here).
"""

import argparse
import filecmp
import fnmatch
import shutil
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

# --------------------------------------------------------------------------
# Partition rules (spawn_spec.md — first match wins)
# Actions: KEEP | KEEP_SUB (owner substitution) | EMPTY | SKELETON | DROP | SPECIAL
# --------------------------------------------------------------------------

OWNER_PLACEHOLDER = "YOURORG"

# --check exit codes. The split exists so the Spawn Drift self-heal can tell
# "the templates are stale" from "the generator produced something unsafe":
#
#   CLEAN  0  published templates match the regenerated tree
#   DRIFT  1  content differs — mechanical, safe to PROPOSE as a PR
#   UNSAFE 2  UNMATCHED file class or canary hit — a HUMAN DECISION
#   CRASH  3  unhandled exception — NOT drift (see the __main__ guard)
#
# EXIT_UNSAFE must never be auto-healed. A canary hit means the generated tree
# contains live instance content, so opening a sync PR would be proposing to
# publish a leak — exactly the #118 failure, automated.
#
# EXIT_CRASH exists because Python exits 1 on an unhandled exception, which is
# indistinguishable from EXIT_DRIFT — a crash would otherwise read as "the
# templates are stale" and the self-heal would propose a PR from whatever
# partial tree the crash left. All of these stay non-zero, so anything treating
# the check as a boolean is unaffected.
EXIT_CLEAN, EXIT_DRIFT, EXIT_UNSAFE, EXIT_CRASH = 0, 1, 2, 3

MIND_WORK_TYPES = (
    "feature", "bug", "refactor", "docs", "test", "release",
    "maintenance", "research", "experiment", "human_review", "triage",
)

MIND_RULES = [
    ("scripts/*", "KEEP"),
    # Generator machinery, same class as scripts/ (spec rule 1b; MEMORY_RULES
    # already keeps tests/). The privacy test must travel with the generator it
    # guards, or a spawned org can reintroduce the rule-5 leak (#118) silently.
    ("tests/*", "KEEP"),
    ("REFERENCE.md", "KEEP"), ("AGENTS.md", "KEEP"), ("CLAUDE.md", "KEEP"),
    ("LICENSE", "KEEP"), ("ROUTING.md", "KEEP"),
    (".gitignore", "KEEP"),
    ("README.md", "KEEP"),
    # Org-wide pointer docs. Generic prose, but each names the owning org and
    # links the canonical copy in that org's PyAutoScientist — so they take the
    # same owner substitution .github/** does rather than a verbatim KEEP.
    # Verbatim would stamp "Contributing to PyAutoLabs" into a fresh-slate
    # template spawned for somebody else's org. They live under .github/ (the
    # 2026-08 root declutter, #248) — GitHub resolves community-health files
    # there, and the Mind's root stays the task ledger.
    ("AI_POLICY.md", "KEEP_SUB"), ("CONTRIBUTING.md", "KEEP_SUB"),
    ("repos.yaml", "SPECIAL:body_map"),
    ("active.md", "EMPTY"), ("planned.md", "EMPTY"), ("epics.md", "EMPTY"),
    ("bundles.md", "EMPTY"),
    # `themes.md` is the `Themes:` vocabulary the dashboard groups bundles on.
    # EMPTY rather than KEEP: the keyword list is this org's science and
    # tooling domains ("mge", "cti", "docs-hub"), so shipping it verbatim would
    # stamp our subject matter into somebody else's fresh-slate Mind. An empty
    # vocabulary simply disables the unknown-keyword warning until they write
    # their own (see PyAutoBrain `parse_themes`).
    ("themes.md", "EMPTY"),
    ("parked.md", "EMPTY"), ("condemned.md", "EMPTY"), ("ideas.md", "EMPTY"), ("queue.md", "EMPTY"),
    ("autonomy_log.md", "SPECIAL:autonomy_log"),
    # Prompt-file lifecycle (issue #71): draft/ (not-started) -> active/
    # (in-flight) -> complete/YYYY/MM (shipped). A fresh template ships an empty
    # draft/ skeleton; active/ + complete/ records are instance state (DROP),
    # but the complete/ archive SCHEMA is template content (KEEP, first-match).
    # `batches/` is the same shape one step further on: a batch record is what
    # one dispatched shift did, which is instance state, while the schema that
    # says how to write one is template content. Same split, same first-match
    # ordering, same reason.
    ("draft/*", "SKELETON"),
    ("complete/AGENTS.md", "KEEP"), ("batches/AGENTS.md", "KEEP"),
    ("active/*", "DROP"), ("complete/*", "DROP"), ("batches/*", "DROP"),
    ("docs/*", "DROP"),
    # `dashboard.md` is EMPTY rather than DROP: README.md ships verbatim and
    # links it, so dropping it would hand every spawned org a broken
    # front-page link. The emptied page carries the regenerate command, which
    # is the whole of what a fresh Mind can truthfully say.
    ("dashboard.md", "EMPTY"),
    # `dashboard.html` is the Pages twin of dashboard.md, generated by the same
    # `pyauto-brain intake --apply dashboard` run. DROP rather than EMPTY: no
    # shipped file links it (README links neither page directly), and its
    # publisher — pages_dashboard.yml — is dropped by rule 9c, so a fresh org
    # has nothing that reads it until it regenerates the pair itself.
    ("dashboard.html", "DROP"),
    ("skills/*", "KEEP"), ("policy/*", "KEEP"),
    # .github is decided PER FILE by the spec's fresh-repo invariant (rule 9):
    # a shipped workflow must succeed on a freshly-spawned repo with no secrets
    # and no sibling repos. Owner substitution alone does NOT achieve that —
    # YOURORG is a literal placeholder, and the template's own spawn_drift run
    # failed with `repository 'https://github.com/YOURORG/PyAutoMind/' not
    # found`. Anything cloning or querying a sibling repo is broken on arrival.
    #
    # Ordered before the .github/scripts DROP and each other; first match wins.
    (".github/workflows/lifecycle_drift.yml", "KEEP"),          # 9a: self-contained
    # 9b: DROP (revised in #125). The self-heal makes this workflow depend on
    # secrets.PAT_PYAUTOLABS and on published *-template repos; a fresh org has
    # neither, so every path in it is unrunnable there and the secret reference
    # alone breaks rule 9's no-configured-secret condition.
    (".github/workflows/spawn_drift.yml", "DROP"),
    # 9c — instance automation: sibling repo lists, organ-specific workflow
    # names, org secrets, strong-lensing vocabulary. Every one of the 13 failing
    # runs in the published template came from these.
    # 9c also: the dashboard is rendered by PyAutoBrain, so this workflow
    # checks out a sibling repo by name. A fresh org has no such sibling (and
    # under owner substitution the name is the literal YOURORG placeholder), so
    # every run of it there fails on checkout.
    (".github/workflows/dashboard_refresh.yml", "DROP"),
    # 9c also: the online lifecycle leg — scheduled, and it reads sibling-repo
    # issue/PR state across the org. A fresh org has neither the schedule
    # tolerance (rule 9's no-unattended-trigger condition) nor the siblings.
    (".github/workflows/registry_reconcile.yml", "DROP"),
    (".github/workflows/morning_status.yml", "DROP"),
    (".github/workflows/morning_health.yml", "DROP"),
    (".github/workflows/arxiv_papers.yml", "DROP"),
    # rule 9c, same as its sibling above: scheduled, needs the papers
    # webhook-less cross-repo PAT, and pushes to another org repo.
    (".github/workflows/arxiv_interests.yml", "DROP"),
    # 9c also: the tenant-firewall gate checks out three sibling organ repos by
    # name (PyAutoBrain/PyAutoHeart/PyAutoHands). A fresh org has none of them,
    # and owner substitution only turns those into YOURORG/... placeholders —
    # the same failure mode as dashboard_refresh.yml.
    (".github/workflows/firewall_gate.yml", "DROP"),
    # 9c also: the SessionStart-hook propagator. It clones every sibling repo
    # in the manifest with secrets.PAT_PYAUTOLABS and pushes bot commits into
    # them by name — firewall_gate.yml's org-coupled shape, multiplied by
    # thirty, plus rule 9's no-configured-secret condition. A fresh org has no
    # siblings to propagate into and no such secret to do it with.
    (".github/workflows/session_hook_propagate.yml", "DROP"),
    # 9c also: the Pages publisher. It needs a GitHub Pages site the default
    # token cannot create on a fresh repo (the Hands lesson, already recorded
    # for Memory's knowledge_board.yml) and takes pages:write + id-token:write,
    # so it is unrunnable on arrival. scripts/ and the renderer still travel;
    # an adopter re-adds the publisher deliberately.
    (".github/workflows/pages_dashboard.yml", "DROP"),
    # 9c also: the branch sweep checks out PyAutoLabs/PyAutoBrain for its logic
    # (dashboard_refresh.yml's failure mode again — YOURORG/PyAutoBrain does not
    # exist), and carries a weekly cron, which rule 9's no-unattended-trigger
    # condition rejects on its own. Worth re-adding deliberately once an
    # adopter has a Brain; not worth inheriting a scheduled job that fails on
    # checkout every Sunday.
    (".github/workflows/branch_sweep.yml", "DROP"),
    # 9c also: the ledger auto-merge. It MERGES TO MAIN with the workflow
    # token and checks out PyAutoLabs/PyAutoBrain for the dashboard render
    # (dashboard_refresh.yml's failure mode again). A fresh org should inherit
    # neither unasked: an adopter re-adds it once they have a Brain and have
    # decided for themselves which of their paths are ledger.
    (".github/workflows/mind_ledger_merge.yml", "DROP"),
    (".github/scripts/*", "DROP"),
    # NO `.github/*` catch-all, deliberately. A catch-all is fail-OPEN: a new
    # Mind workflow would ride it into the template carrying whatever schedule
    # and secrets it has — the exact defect this rule exists to fix. With no
    # fallback, a new .github file is UNMATCHED, spawn fails, and a human adds
    # an explicit rule 9 entry. Same doctrine as every other new file class:
    # "extend the spec's tables, then mirror here", never classify ad hoc.
    # Agent-discovery symlinks are install artifacts (recreated by the
    # PyAutoBrain installer), not source content — drop them from the template.
    (".claude/*", "DROP"), (".codex/*", "DROP"),
    # Instance branding:
    ("logo.png", "DROP"),
]

MEMORY_RULES = [
    ("bibliography/README.md", "KEEP"),
    ("scripts/*", "KEEP"), ("tests/*", "KEEP"),
    ("Makefile", "KEEP"), ("LICENSE", "KEEP"),
    ("AGENTS.md", "KEEP"), ("CLAUDE.md", "KEEP"), (".gitignore", "KEEP"),
    # Same org-wide pointer docs as MIND_RULES — owner substitution; under
    # .github/ since the 2026-08 root declutter (all five organs match).
    ("AI_POLICY.md", "KEEP_SUB"), ("CONTRIBUTING.md", "KEEP_SUB"),
    ("bibliography/*", "EMPTY"),
    # Same fail-closed discipline as MIND_RULES (spec rule 9d). validate.yml is
    # self-contained — no schedule, no secrets, no sibling repos — so it clears
    # the fresh-repo invariant and ships. No catch-all: a new Memory workflow is
    # UNMATCHED and gets an explicit decision.
    (".github/workflows/validate.yml", "KEEP_SUB"),
    # DROP: the knowledge-board publisher needs a GitHub Pages site the default
    # token cannot create on a fresh repo (the Hands lesson) and a schedule —
    # both break the fresh-repo invariant. scripts/board.py itself SHIPS via
    # the scripts/* KEEP above (it is generic: everything derives from the
    # checkout + git remote), so an adopter re-adds the workflow deliberately.
    (".github/workflows/knowledge_board.yml", "DROP"),
    # DROP: the queue-actions processor mutates the instance reading queue from
    # `queue-read` issues and needs the repo's labels — instance machinery, not
    # template content. scripts/queue_mark_done.py SHIPS via scripts/*, so an
    # adopter re-adds the workflow deliberately, like the board publisher.
    (".github/workflows/queue_actions.yml", "DROP"),
    # DROP: the claude-action filing workflow needs the instance's Claude OAuth
    # secret, labels and reading queue — instance machinery like the two above.
    (".github/workflows/queue_filing.yml", "DROP"),
    # DROP: the arXiv-ref backfill is generic (no secrets, no sibling repos) but
    # runs on a schedule and pushes to main, which breaks the fresh-repo
    # invariant exactly as the board publisher does. scripts/arxiv_refs.py and
    # scripts/backfill_arxiv_refs.py SHIP via scripts/*, so an adopter with a
    # populated reading queue re-adds the workflow deliberately.
    (".github/workflows/arxiv_refs.yml", "DROP"),
    # The shared wiki schema is template content; the sub-wikis are instance
    # content (the generator stamps an empty wiki/example/ instead).
    ("wiki/CLAUDE.md", "KEEP"),
    ("wiki/*", "DROP"),
    # Instance branding:
    ("logo.png", "DROP"),
    ("index.md", "SPECIAL:memory_index"),
    ("reading-queue.md", "EMPTY"),
    # EMPTY, same class as the reading queue: the inbox format is template
    # content, the instance's overnight suggestions are not. A fresh repo gets
    # the header and no papers; PyAutoMemory#57.
    ("arxiv-inbox.md", "EMPTY"),
    # EMPTY for the same reason: the day-batch format is template content, the
    # instance's backlog of recommendations is not.
    ("arxiv-interests.md", "EMPTY"),
    ("README.md", "SPECIAL:memory_readme"),
]

# Instance-content tokens that must NEVER appear in a generated template.
# Chosen to be absent from every KEEP-verbatim file (verified at run time —
# the scan covers the whole output tree, so a canary in a kept file fails
# the run and forces the list or the rules to be reconsidered).
# Dataset names catch leaked science content; person names catch leaked task
# slugs and prompt lines (the spec's example list names `Nightingale`).
CANARY_TOKENS = (
    "slacs", "b1938", "cosmos_web_ring", "smbh_binary", "arctic",
    "nightingale", "rhayes",
)

# Titles for EMPTY-ruled files, keyed by their path RELATIVE TO THE REPO ROOT
# (spawn_spec.md rules 5 + 6: "header line + schema pointer comment only").
# These are GENERATED, never read from the live file: some registry files carry
# no H1 at all, so their first line is a live registry entry, and a
# heading-shape test cannot save us either — a task slug written as an H2 is a
# structurally valid heading. Copying any source byte here breaks the privacy
# invariant (spawn_spec.md).
#
# Keyed by relative path, not basename, so a glob-matched file that merely
# SHARES a name (e.g. Memory's `bibliography/active.md`, caught by the broad
# `bibliography/*` EMPTY rule) does not silently inherit a root file's title.
EMPTY_TITLES = {
    "dashboard.md": "# PyAutoMind Dashboard",
    "active.md": "# Active Tasks",
    "epics.md": "# Epics",
    "bundles.md": "# Bundles",
    "themes.md": "# Themes",
    "planned.md": "# Planned",
    "parked.md": "# Parked tasks",
    "condemned.md": "# Condemned material",
    "ideas.md": "# Ideas",
    "queue.md": "# Queue",
    "reading-queue.md": "# Reading queue",
    "arxiv-inbox.md": "# arXiv inbox",
    "arxiv-interests.md": "# arXiv interests",
}

# Generated header comments for EMPTY files matched by a glob rather than by
# name (Memory's `bibliography/*` — arbitrary filenames, so no title map).
# spawn_spec.md rule 2 already specifies a generated header comment here.
EMPTY_COMMENTS = {
    ".bib": "% Canonical BibTeX metadata — populated by your literature.",
    ".yaml": "# Populated by your literature.",
    ".yml": "# Populated by your literature.",
}

# --------------------------------------------------------------------------
# Generated assets
# --------------------------------------------------------------------------

# The autonomy ledger's schema header, GENERATED rather than parsed out of the
# live file (spec rule 5; issue #123). The old implementation copied lines
# until one started with "|---", which leaked two ways: a row inserted above
# the separator was copied, and a cosmetically reformatted separator
# ("| --- |") meant the break never fired — 231 live task records into a
# public repo. The canary scan does not cover this; a leaked row with no
# dataset or person token scans clean.
#
# Byte-identical to what the parse produced for the current ledger, so
# adopting it introduces no template drift.
AUTONOMY_LOG_TEMPLATE = """\
# Autonomy calibration log

Append-only record of `--auto` workflow runs — the evidence base for raising
or lowering the per-work-type autonomy caps in `PyAutoBrain/AUTONOMY.md` (the
autonomy contract). One row per run, appended at PR-open or on parking.

Outcome ∈ `merged-unchanged` / `amended` / `rejected` / `parked` /
`corrective`.

| date | task | effective level | gates (tests/smoke/review/heart) | outcome |
|------|------|-----------------|----------------------------------|---------|
"""

BODY_MAP_TEMPLATE = """\
# repos.yaml — the body map: the single source of repo IDENTITY.
#
# This is the template body map: the five organs + the PyAutoProject
# satellite family. Replace YOURORG with your GitHub owner and the
# autoproject rows with your science repos, then run:
#
#   python3 scripts/repos_sync.py --write

categories:
  organ: {}
  library: {}
  workspace: {}
  workspace_test: {}
  assistant: {}

repos:
  PyAutoMind:
    github: YOURORG/PyAutoMind
    category: organ
    role: "Intent, goals, priorities, workflow state; every task starts as a markdown prompt here."
  PyAutoBrain:
    github: YOURORG/PyAutoBrain
    category: organ
    role: "Reasoning/orchestration layer; how work is decomposed and routed; the specialist agents."
  PyAutoHands:
    github: YOURORG/PyAutoHands
    category: organ
    role: "Packaging, tagging, notebook generation, release execution."
  PyAutoHeart:
    github: YOURORG/PyAutoHeart
    category: organ
    role: "Health/readiness — the authoritative \\"is it safe to release?\\" verdict."
  PyAutoMemory:
    github: YOURORG/PyAutoMemory
    category: organ
    role: "Long-term scientific/software/project knowledge."

  PyAutoProject:
    github: YOURORG/PyAutoProject
    category: library
    role: "Your science library — model + analysis on the PyAutoFit engine."
  autoproject_workspace:
    github: YOURORG/autoproject_workspace
    category: workspace
    role: "End-to-end example scripts that build to notebooks."
  autoproject_workspace_test:
    github: YOURORG/autoproject_workspace_test
    category: workspace_test
    role: "Regression, smoke and parity scripts (code-heavy, doc-light)."

  # Uncomment when the clone agent seeds your assistant:
  # autoproject_assistant:
  #   github: YOURORG/autoproject_assistant
  #   category: assistant
"""

MEMORY_INDEX_TEMPLATE = """\
# PyAutoMemory — index

Top-level navigation across the sub-wikis. Every sub-wiki is self-contained
and follows the schema defined in `wiki/CLAUDE.md`.

| Wiki | Covers |
|------|--------|
| [`wiki/example/`](wiki/example/index.md) | An empty example — copy it to start your first real sub-wiki. |

Add sub-wikis beside `wiki/example/` following the same schema, and give
each a row here.
"""

MEMORY_README_TEMPLATE = """\
# PyAutoMemory

The long-term memory of your PyAutoScientist organism: what it has learned,
distilled into cross-linked LLM wikis — literature summaries, domain
concepts, and the citation metadata to verify them. Start at
[`index.md`](index.md).

| Piece | What it is |
|-------|------------|
| `wiki/example/` | An empty sub-wiki demonstrating the schema — copy it per domain. |
| `wiki/CLAUDE.md` | The shared schema every sub-wiki inherits. |
| `bibliography/` | Canonical BibTeX metadata every wiki claim cites against. |
| `reading-queue.md` | What is waiting to be read and filed. |

New knowledge updates the metadata and the claim support together, then
passes `make validate`. The wiki schema is defined in
`wiki/CLAUDE.md` and inherited by every sub-wiki. How agents should
read this repo: [AGENTS.md](AGENTS.md).

This repo was generated by `spawn` from the live PyAutoScientist organism —
see <https://pyautoscientist.readthedocs.io>.
"""

EXAMPLE_WIKI_CLAUDE = """\
# example wiki — scope

An empty sub-wiki demonstrating the layout. Copy `wiki/example/` to
`wiki/<your-domain>/` to start a real sub-wiki. All schema rules — page
types, naming, `[[wiki-links]]`, frontmatter, page structures, status
flags — are defined once in [`../CLAUDE.md`](../CLAUDE.md) and inherited;
a sub-wiki's own `CLAUDE.md` (this file) records only its scope: what the
domain covers, and which adjacent topics link out to sibling wikis.
"""

EXAMPLE_WIKI_INDEX = """\
# example wiki — index

The sub-wiki's own navigation. Sources are summarised under `sources/`
(one page per paper/resource, see the stub); concept pages live beside
this index and link the sources that support each claim.

## Sources

*(none yet — see `sources/EXAMPLE_stub.md` for the format)*
"""

EXAMPLE_WIKI_STUB = """\
# EXAMPLE, Author et al. (YYYY) — stub

**Status: stub** — filed, not yet read/summarised.

- **Citation key:** `AuthorYYYY` (must exist in `bibliography/`)
- **What it is:** one line on why this source is in the wiki.
- **Claims it will support:** bullet the concept pages that will cite it.

Upgrade to `drafted` by replacing this with a Karpathy-style summary of
what the source actually says and which claims it supports.
"""

TEMPLATE_README_BANNER = (
    "> **Generated repository.** This template is stamped from the live\n"
    "> PyAutoScientist organism by `scripts/spawn.py` — do not PR it; PR the\n"
    "> generator. History may be force-synced on regeneration.\n\n"
)

CONTRIBUTING_FAMILY = """\
# Contributing

{repo} is part of the **PyAutoScientist template family** — a seed you copy
("Use this template"), not a library you track. Upstream churn lands
through the `autoconf`/`autofit` packages and reusable workflows, not
through this repo. Issues about the template itself are welcome at
[PyAutoBrain](https://github.com/PyAutoLabs/PyAutoBrain); the adoption model
is documented at <https://pyautoscientist.readthedocs.io>.
"""

# --------------------------------------------------------------------------

FAMILY_SMOKE_CALLER = """name: Smoke Tests

# Thin caller for the reusable smoke-test workflow (owned by your Heart
# fork). The chain is just your own library: its dependencies (autoconf,
# autofit) install from PyPI via pip in smoke_install.sh.

on: [push, pull_request]

jobs:
  smoke:
    uses: {owner}/PyAutoHeart/.github/workflows/smoke-tests.yml@main
    with:
      chain: "PyAutoProject"
    secrets: inherit
"""

FAMILY_SMOKE_INSTALL = """#!/usr/bin/env bash
# Workspace-owned install epilogue for the reusable Smoke Tests workflow.
# The template library's dependencies (autoconf, autofit) come from PyPI.
set -e

pip install ./PyAutoProject
"""

FAMILY_RUN_SMOKE = '''#!/usr/bin/env python3
"""Minimal smoke runner: execute every script listed in smoke_tests.txt
(repo-root-relative, one per line, # comments allowed); fail on the first
nonzero exit. The reusable Smoke Tests workflow invokes this."""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIMEOUT = int(os.environ.get("SMOKE_TIMEOUT_SECS", "600"))

env = dict(os.environ, MPLBACKEND="Agg")
scripts = [
    line.strip()
    for line in (ROOT / "smoke_tests.txt").read_text().splitlines()
    if line.strip() and not line.strip().startswith("#")
]
for script in scripts:
    print(f"== smoke: {script}", flush=True)
    result = subprocess.run(
        [sys.executable, script], cwd=ROOT, env=env, timeout=TIMEOUT
    )
    if result.returncode != 0:
        sys.exit(f"smoke FAILED: {script} (exit {result.returncode})")
print(f"smoke OK: {len(scripts)} script(s)")
'''


def tracked_files(repo):
    out = subprocess.run(
        ["git", "-C", str(repo), "ls-files"],
        capture_output=True, text=True, check=True,
    )
    return [Path(line) for line in out.stdout.splitlines() if line]


def head_sha(repo):
    out = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def match_rule(rel, rules):
    posix = rel.as_posix()
    for pattern, action in rules:
        if fnmatch.fnmatch(posix, pattern) or (
            pattern.endswith("/*") and posix.startswith(pattern[:-1])
        ):
            return pattern, action
    return None, None


def empty_body(src, rel=None):
    """Generate the EMPTY body for `rel` WITHOUT reading the source.

    The source is never opened: an EMPTY output is a generated title plus a
    schema pointer, so no live registry entry, idea line or bibliography entry
    can reach a template (the spawn_spec.md privacy invariant).

    `rel` is the path relative to the repo root and is what EMPTY_TITLES is
    keyed on. It defaults to the basename only so direct callers (tests) stay
    ergonomic; the generators always pass the real relative path.
    """
    key = Path(rel).as_posix() if rel is not None else src.name
    header = EMPTY_TITLES.get(key)
    if header is None:
        header = EMPTY_COMMENTS.get(src.suffix)
    if header is None:
        # Same doctrine as UNMATCHED: a new EMPTY file class is a human
        # decision — add it to the spec's tables and mirror it here. Guessing
        # a header from the live file is what leaked instance content before.
        raise SystemExit(
            f"spawn: EMPTY file '{key}' has no generated header.\n"
            f"  Add it to EMPTY_TITLES (named registry files) or EMPTY_COMMENTS\n"
            f"  (glob-matched files), updating docs/pyautobrain/spawn_spec.md first."
        )
    if src.suffix in {".yaml", ".yml", ".bib"}:
        # YAML/BibTeX consumers parse every non-comment line — an HTML comment
        # would read as content (e.g. a bibkey alias with a missing target).
        marker = "# emptied by spawn; schema: REFERENCE.md"
        if src.suffix == ".bib":
            marker = "% emptied by spawn; schema: REFERENCE.md"
        return header + "\n\n" + marker + "\n"
    return header + "\n\n<!-- emptied by spawn; schema: REFERENCE.md -->\n"


def autonomy_log_body(src=None):
    """Return the autonomy ledger's schema header WITHOUT reading the source.

    `src` is accepted and ignored so the generator's dispatch stays uniform;
    the whole point is that no live byte reaches the template.

    The previous implementation copied lines until one started with `|---`,
    which leaked two ways (issue #123, both reproduced against the real
    ledger): a row inserted above the separator was copied, and a cosmetically
    reformatted separator (`| --- |`) meant the break never fired at all —
    231 live task records into a public repo. The canary scan is no backstop
    here: a leaked row with no dataset or person token scans clean.

    Same fix as the EMPTY ledgers (#118): generate, never parse.
    """
    return AUTONOMY_LOG_TEMPLATE


def substitute_owner(text):
    return text.replace("PyAutoLabs", OWNER_PLACEHOLDER)


def plan_repo(repo, rules):
    """Return (plan, warns): plan maps output rel-path -> (action, source)."""
    plan, warns, skeleton_dirs = {}, [], set()
    for rel in tracked_files(repo):
        pattern, action = match_rule(rel, rules)
        if action is None:
            warns.append(rel.as_posix())
            continue
        if action == "DROP":
            continue
        if action == "SKELETON":
            skeleton_dirs.add(rel.as_posix().split("/")[0])
            continue
        plan[rel] = (action, repo / rel)
    for d in sorted(skeleton_dirs):
        plan[Path(d) / ".gitkeep"] = ("GENERATE:", "")
    return plan, warns


def generate_mind(mind_root, out_dir):
    plan, warns = plan_repo(mind_root, MIND_RULES)
    for rel, (action, src) in sorted(plan.items()):
        dest = out_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if action == "KEEP":
            shutil.copy2(src, dest)
        elif action == "KEEP_SUB":
            dest.write_text(substitute_owner(src.read_text(errors="replace")))
        elif action == "EMPTY":
            dest.write_text(empty_body(src, rel))
        elif action == "SPECIAL:autonomy_log":
            dest.write_text(autonomy_log_body(src))
        elif action == "SPECIAL:body_map":
            dest.write_text(BODY_MAP_TEMPLATE)
        elif action == "GENERATE:":
            dest.write_text("")
    readme = out_dir / "README.md"
    if readme.exists():
        readme.write_text(TEMPLATE_README_BANNER + readme.read_text())
    stamp_complete_index(out_dir)
    return warns


def stamp_complete_index(out_dir):
    """Stamp the template's empty-archive `complete/index.md` (spec rule 6c).

    Runs the GENERATED tree's own `scripts/lifecycle.py`, which resolves its
    root from `__file__` — so the index is produced by the same code, over the
    same (empty) archive, as the template's own lifecycle self-heal.

    Without this the template is permanently drifted: it ships
    `lifecycle_drift.yml`, whose self-heal (PyAutoMind#116) regenerates this
    file on every push to the template's `main`. Each spawn sync was therefore
    followed within seconds by a bot commit creating a file spawn did not
    produce, which the next `--check` reported as drift — forever.

    Deliberately NOT a constant here: `lifecycle.py` owns the index format, and
    a second copy of that text would drift from it.
    """
    # Absolute, deliberately: the script path is resolved by the child AFTER it
    # chdir's to `cwd`, so a relative --write DIR (e.g. `--write regenerated`,
    # which is what a CI step naturally passes) made the path unresolvable from
    # inside the new cwd and the child died with "can't open file". Every
    # invocation to date happened to use an absolute path, so it stayed latent.
    out_dir = out_dir.resolve()
    lifecycle = out_dir / "scripts" / "lifecycle.py"
    if not lifecycle.exists():          # rules changed; nothing to stamp
        return
    (out_dir / "complete").mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, str(lifecycle), "index", "--apply"],
        cwd=out_dir, check=True, capture_output=True,
    )


def generate_memory(memory_root, out_dir):
    plan, warns = plan_repo(memory_root, MEMORY_RULES)
    for rel, (action, src) in sorted(plan.items()):
        dest = out_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if action == "KEEP":
            shutil.copy2(src, dest)
        elif action == "KEEP_SUB":
            dest.write_text(substitute_owner(src.read_text(errors="replace")))
        elif action == "EMPTY":
            dest.write_text(empty_body(src, rel))
        elif action == "SPECIAL:memory_index":
            dest.write_text(MEMORY_INDEX_TEMPLATE)
        elif action == "SPECIAL:memory_readme":
            dest.write_text(TEMPLATE_README_BANNER + MEMORY_README_TEMPLATE)
    wiki = out_dir / "wiki" / "example"
    wiki.mkdir(parents=True, exist_ok=True)
    (wiki / "CLAUDE.md").write_text(EXAMPLE_WIKI_CLAUDE)
    (wiki / "index.md").write_text(EXAMPLE_WIKI_INDEX)
    (wiki / "sources").mkdir(exist_ok=True)
    (wiki / "sources" / "EXAMPLE_stub.md").write_text(EXAMPLE_WIKI_STUB)
    return warns


# Paths where a specific canary token is legitimate rather than leaked.
# Deliberately narrow: each entry names the exact file AND the exact tokens
# excused there, so a new leak elsewhere still fails the scan.
CANARY_EXEMPT = {
    # spawn.py DEFINES CANARY_TOKENS; that literal list is generator machinery.
    # This is the ONLY unavoidable exemption: the token list has to exist
    # somewhere, and this is where. Everything else must earn its place —
    # `tests/` deliberately has NO entry here. The privacy test derives every
    # token from CANARY_TOKENS at run time and uses fictional fixtures, so it
    # scans clean on its own merits. Exempting it instead would let the test
    # smuggle the very strings it exists to keep out (both spawn.py and
    # tests/ are KEEP-copied verbatim into the public template).
    "scripts/spawn.py": set(CANARY_TOKENS),
    # The licence attributes copyright to a named human — that is the point of
    # a licence, not leaked instance content.
    "LICENSE": {"nightingale"},
}


def canary_scan(out_dir):
    hits = []
    for path in sorted(out_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(out_dir).as_posix()
        exempt = CANARY_EXEMPT.get(rel, set())
        text = path.read_text(errors="replace").lower()
        for token in CANARY_TOKENS:
            if token in exempt:
                continue
            if token in text:
                hits.append(f"{rel}: '{token}'")
    return hits


def generate_all(root, out_root):
    mind_root = root / "PyAutoMind"
    memory_root = root / "PyAutoMemory"
    results = {}
    for name, gen, src in (
        ("PyAutoMind-template", generate_mind, mind_root),
        ("PyAutoMemory-template", generate_memory, memory_root),
    ):
        out_dir = out_root / name
        if out_dir.exists():
            shutil.rmtree(out_dir)
        warns = gen(src, out_dir)
        (out_dir / "SPAWNED_FROM").write_text(
            f"{src.name} @ {head_sha(src)}\ngenerated by scripts/spawn.py\n"
        )
        hits = canary_scan(out_dir)
        results[name] = (warns, hits)
    return results


def diff_trees(a, b):
    problems = []

    def walk(dc):
        for name in dc.left_only:
            problems.append(f"only in regenerated: {Path(dc.left) / name}")
        for name in dc.right_only:
            if name == ".git":
                continue
            problems.append(f"only in published: {Path(dc.right) / name}")
        for name in dc.diff_files:
            problems.append(f"differs: {Path(dc.right) / name}")
        for sub in dc.subdirs.values():
            walk(sub)

    walk(filecmp.dircmp(str(a), str(b), ignore=[".git"]))
    return problems


def stamp_family(root, family_dir):
    """Stamp the family's mechanical layers (spec: workflows deferred to the
    reusable-smoke work; the workspace pin stamps the family's own version)."""
    license_text = (root / "PyAutoMind" / "LICENSE").read_text()
    stamped = []
    for repo in ("PyAutoProject", "autoproject_workspace", "autoproject_workspace_test"):
        rdir = family_dir / repo
        if not rdir.is_dir():
            print(f"stamp-family: skipping {repo} (not checked out under {family_dir})")
            continue
        (rdir / "LICENSE").write_text(license_text)
        (rdir / "CONTRIBUTING.md").write_text(CONTRIBUTING_FAMILY.format(repo=repo))
        stamped.append(repo)
    for repo, smoke_seed in (
        ("autoproject_workspace", "scripts/start_here.py"),
        ("autoproject_workspace_test", "scripts/fit_quick.py"),
    ):
        rdir = family_dir / repo
        if not rdir.is_dir():
            continue
        wf = rdir / ".github" / "workflows"
        sc = rdir / ".github" / "scripts"
        wf.mkdir(parents=True, exist_ok=True)
        sc.mkdir(parents=True, exist_ok=True)
        (wf / "smoke_tests.yml").write_text(
            FAMILY_SMOKE_CALLER.format(owner="PyAutoLabs")
        )
        (sc / "smoke_install.sh").write_text(FAMILY_SMOKE_INSTALL)
        (sc / "smoke_install.sh").chmod(0o755)
        (sc / "run_smoke.py").write_text(FAMILY_RUN_SMOKE)
        (sc / "run_smoke.py").chmod(0o755)
        smoke_txt = rdir / "smoke_tests.txt"
        if not smoke_txt.exists():
            smoke_txt.write_text(smoke_seed + "\n")

    ws = family_dir / "autoproject_workspace"
    if ws.is_dir():
        (ws / "config").mkdir(exist_ok=True)
        (ws / "config" / "general.yaml").write_text(
            "version:\n"
            "  # The workspace pins the library version it was written against. The\n"
            "  # organism's health layer (PyAutoHeart version_skew) and the autoconf\n"
            "  # runtime handshake both read this key; keep it in step with your\n"
            "  # library's __version__ when you release.\n"
            "  workspace_version: 0.1.0\n"
        )
        (ws / "config" / "build").mkdir(exist_ok=True)
        (ws / "config" / "build" / "no_run.yaml").write_text(
            "# Scripts/notebooks the build must NOT execute (PyAutoHands run.py\n"
            "# reads this workspace-local list). Every workspace must own this\n"
            "# file — run.py raises if it is missing — but an empty list is valid\n"
            "# and skips nothing. List paths relative to scripts/, e.g.:\n"
            "#\n"
            "# - gui/mask  # GUI scripts cannot be run headless\n"
            "[]\n"
        )
    return stamped


def report(results):
    failed = False
    for name, (warns, hits) in results.items():
        print(f"== {name}")
        if warns:
            failed = True
            print(f"  UNMATCHED ({len(warns)}) — extend the spec's tables, then mirror here:")
            for w in warns:
                print(f"    ✗ {w}")
        else:
            print("  unmatched: none")
        if hits:
            failed = True
            print(f"  CANARY HITS ({len(hits)}):")
            for h in hits:
                print(f"    ✗ {h}")
        else:
            print("  canary scan: clean")
    return failed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", metavar="DIR")
    parser.add_argument("--check", metavar="DIR")
    parser.add_argument("--stamp-family", metavar="DIR")
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args()

    mind_root = Path(__file__).resolve().parents[1]
    root = args.root or mind_root.parent

    if args.stamp_family:
        stamped = stamp_family(root, Path(args.stamp_family))
        print(f"stamped: {', '.join(stamped) if stamped else 'nothing'}")
        return

    with tempfile.TemporaryDirectory(prefix="spawn_") as tmp:
        out_root = Path(args.write) if args.write else Path(tmp)
        out_root.mkdir(parents=True, exist_ok=True)
        results = generate_all(root, out_root)
        # UNSAFE: the generated tree itself cannot be trusted — an unclassified
        # file class (UNMATCHED) or leaked instance content (canary). Kept
        # strictly apart from DRIFT below; see EXIT_* for why that matters.
        unsafe = report(results)
        drifted = False

        if args.check and not unsafe:
            for name in results:
                problems = diff_trees(out_root / name, Path(args.check) / name)
                # SPAWNED_FROM records the source commit, which legitimately
                # advances between regenerations; content drift is what matters.
                problems = [p for p in problems if not p.endswith("SPAWNED_FROM")]
                status = "OK" if not problems else f"{len(problems)} drift(s)"
                print(f"check {name}: {status}")
                for p in problems:
                    drifted = True
                    print(f"  ✗ {p}")

        if args.write and not unsafe:
            print(f"written: {out_root}")

    if unsafe:
        sys.exit(EXIT_UNSAFE)
    sys.exit(EXIT_DRIFT if drifted else EXIT_CLEAN)


if __name__ == "__main__":
    try:
        main()
    except SystemExit as exc:
        # main() exits with an explicit EXIT_* code. Anything else raising
        # SystemExit is a fail-closed generator path — `empty_body()` on an
        # unmapped EMPTY file, say — which passes a STRING, and Python turns a
        # string exit into code 1: indistinguishable from EXIT_DRIFT. Those are
        # human decisions, exactly like UNMATCHED, so map them to EXIT_UNSAFE
        # rather than letting the self-heal read them as "templates are stale".
        if isinstance(exc.code, int) or exc.code is None:
            raise
        print(exc.code, file=sys.stderr)
        sys.exit(EXIT_UNSAFE)
    except BaseException:
        # An unhandled exception would otherwise exit 1 — INDISTINGUISHABLE
        # from EXIT_DRIFT, so the Spawn Drift self-heal would read a crash as
        # "the templates are stale" and try to propose a sync PR from whatever
        # partial tree the crash left behind. Exit on a code no caller treats
        # as actionable instead; the workflow's catch-all rejects it.
        traceback.print_exc()
        sys.exit(EXIT_CRASH)
