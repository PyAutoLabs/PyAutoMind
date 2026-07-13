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
from pathlib import Path

# --------------------------------------------------------------------------
# Partition rules (spawn_spec.md — first match wins)
# Actions: KEEP | KEEP_SUB (owner substitution) | EMPTY | SKELETON | DROP | SPECIAL
# --------------------------------------------------------------------------

OWNER_PLACEHOLDER = "YOURORG"

MIND_WORK_TYPES = (
    "feature", "bug", "refactor", "docs", "test", "release",
    "maintenance", "research", "experiment", "triage",
)

MIND_RULES = [
    ("scripts/*", "KEEP"),
    ("REFERENCE.md", "KEEP"), ("AGENTS.md", "KEEP"), ("CLAUDE.md", "KEEP"),
    ("LICENSE", "KEEP"), ("CONTRIBUTING.md", "KEEP"), ("ROUTING.md", "KEEP"),
    (".gitignore", "KEEP"),
    ("README.md", "KEEP"),
    ("repos.yaml", "SPECIAL:body_map"),
    ("active.md", "EMPTY"), ("planned.md", "EMPTY"), ("complete.md", "EMPTY"),
    ("parked.md", "EMPTY"), ("condemned.md", "EMPTY"), ("ideas.md", "EMPTY"), ("queue.md", "EMPTY"),
    ("autonomy_log.md", "SPECIAL:autonomy_log"),
    # Prompt-file lifecycle (issue #71): draft/ (not-started) -> active/
    # (in-flight) -> complete/YYYY/MM (shipped). A fresh template ships an empty
    # draft/ skeleton; active/ + complete/ records are instance state (DROP),
    # but the complete/ archive SCHEMA is template content (KEEP, first-match).
    ("draft/*", "SKELETON"),
    ("complete/AGENTS.md", "KEEP"),
    ("active/*", "DROP"), ("complete/*", "DROP"),
    ("z_features/*", "DROP"), ("z_vault/*", "DROP"),
    ("autoprompt/*", "DROP"), ("docs/*", "DROP"),
    # Instance root docs + legacy pre-migration prompt dirs:
    ("dashboard.md", "DROP"), ("overview.md", "DROP"), ("autolens/*", "DROP"),
    ("skills/*", "KEEP"), ("policy/*", "KEEP"),
    (".github/*", "KEEP_SUB"),
    # Agent-discovery symlinks are install artifacts (recreated by the
    # PyAutoBrain installer), not source content — drop them from the template.
    (".claude/*", "DROP"), (".codex/*", "DROP"),
]

MEMORY_RULES = [
    ("bibliography/*.py", "KEEP"), ("bibliography/README.md", "KEEP"),
    ("scripts/*", "KEEP"), ("tests/*", "KEEP"),
    ("Makefile", "KEEP"), ("LICENSE", "KEEP"), ("CONTRIBUTING.md", "KEEP"),
    ("AGENTS.md", "KEEP"), ("CLAUDE.md", "KEEP"), (".gitignore", "KEEP"),
    ("bibliography/*", "EMPTY"),
    ("*_wiki/*", "DROP"),
    ("index.md", "SPECIAL:memory_index"),
    ("reading-queue.md", "EMPTY"),
    ("README.md", "SPECIAL:memory_readme"),
    ("*.bib", "DROP"),
    # Legacy paper-notes families predating the sub-wikis:
    ("CTI/*", "DROP"), ("DarkMatterModels/*", "DROP"), ("Medical/*", "DROP"),
    ("LightProFFits/*", "DROP"), ("euclid.sty", "DROP"), ("cticomments", "DROP"),
    ("Hubble1926*", "DROP"), ("devaucoleurs1948*", "DROP"),
]

# Instance-content tokens that must NEVER appear in a generated template.
# Chosen to be absent from every KEEP-verbatim file (verified at run time —
# the scan covers the whole output tree, so a canary in a kept file fails
# the run and forces the list or the rules to be reconsidered).
CANARY_TOKENS = ("slacs", "b1938", "cosmos_web_ring", "smbh_binary", "arctic")

# --------------------------------------------------------------------------
# Generated assets
# --------------------------------------------------------------------------

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
  PyAutoBuild:
    github: YOURORG/PyAutoBuild
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
and follows the schema defined in `example_wiki/CLAUDE.md`.

| Wiki | Covers |
|------|--------|
| [`example_wiki/`](example_wiki/index.md) | An empty example — copy it to start your first real sub-wiki. |

Add sub-wikis beside `example_wiki/` following the same schema, and give
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
| `example_wiki/` | An empty sub-wiki demonstrating the schema — copy it per domain. |
| `bibliography/` | Canonical BibTeX metadata every wiki claim cites against. |
| `reading-queue.md` | What is waiting to be read and filed. |

New knowledge updates the metadata and the claim support together, then
passes `make validate-literature-citations`. The wiki schema is defined in
`example_wiki/CLAUDE.md` and inherited by every sub-wiki. How agents should
read this repo: [AGENTS.md](AGENTS.md).

This repo was generated by `spawn` from the live PyAutoScientist organism —
see <https://pyautoscientist.readthedocs.io>.
"""

GENERIC_WIKI_SCHEMA = """\
# example_wiki — schema + usage rules

This sub-wiki gives an AI assistant broad context for one domain. It follows
Karpathy's "LLM Wiki" pattern: concise, cross-linked pages read at query
time, while canonical citation metadata lives separately in
`../bibliography/`. Copy this folder to start a real sub-wiki; every sibling
wiki inherits this schema.

## Layout

```
PyAutoMemory/
├── example_wiki/             # one domain — the compiled wiki (in git)
│   ├── CLAUDE.md             # this file — schema + usage rules
│   ├── index.md              # the wiki's own navigation
│   ├── concepts/             # one topic per page — the science
│   ├── entities/             # named things: surveys, instruments, software
│   └── sources/              # compact claim support (one source = one section)
└── bibliography/             # canonical BibTeX, aliases, citation tooling
```

Sources are the ground truth; wiki pages are syntheses. If they disagree,
update the wiki and log the change.

## Page types

| Type    | Folder      | Scope                                            |
|---------|-------------|--------------------------------------------------|
| Concept | `concepts/` | One idea per page — split pages that cover two   |
| Entity  | `entities/` | One named thing (survey, instrument, code, team) |
| Sources | `sources/`  | Claim support for one topic, one section/source  |
| Index   | root        | Navigation and provenance                        |

## Conventions

- File names are lowercase kebab-case; one concept per concept page.
- Wiki-internal links use `[[page-slug]]`; a link with no target yet is
  fine — it marks a future page.
- External references use verified DOI/arXiv/journal metadata, never a
  local path; canonical keys live in `../bibliography/` and are validated
  by `make validate-literature-citations`.
- Every page starts with YAML frontmatter: `title`, `type`
  (concept | entity | sources | meta), `topics`, optional `sources`, and
  `status` (stub | drafted | reviewed).

## Concept page structure

`# Title` → `## TL;DR` (one quotable paragraph) → `## What it is` →
`## Why it matters for your project` → `## Key results from the
literature` (each bullet ends with a `([[source-slug]])` link) →
`## See also`.

## Source-collection page structure

One H2 section per source: the canonical BibTeX key, the reference, the
concepts it supports, a short **Supports:** bullet list, and **Use when /
Do not use for** guidance. Keep entries to 2–5 support bullets; never copy
abstracts or infer claims from filenames — add a TODO when support is
unverified.

## How an assistant should use this wiki

Open `index.md` first; follow the relevant concept/entity page; follow the
source entry for claim scope and its canonical key for metadata; if
support is unclear, read the public source and add a TODO rather than
guessing.
"""

EXAMPLE_WIKI_INDEX = """\
# example_wiki — index

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


def empty_body(src):
    try:
        first = src.read_text(errors="replace").splitlines()[0]
    except IndexError:
        first = ""
    return first + "\n\n<!-- emptied by spawn; schema: REFERENCE.md -->\n"


def autonomy_log_body(src):
    lines = src.read_text(errors="replace").splitlines()
    kept = []
    for line in lines:
        kept.append(line)
        if line.startswith("|---"):
            break
    return "\n".join(kept) + "\n"


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
            dest.write_text(empty_body(src))
        elif action == "SPECIAL:autonomy_log":
            dest.write_text(autonomy_log_body(src))
        elif action == "SPECIAL:body_map":
            dest.write_text(BODY_MAP_TEMPLATE)
        elif action == "GENERATE:":
            dest.write_text("")
    readme = out_dir / "README.md"
    if readme.exists():
        readme.write_text(TEMPLATE_README_BANNER + readme.read_text())
    return warns


def generate_memory(memory_root, out_dir):
    plan, warns = plan_repo(memory_root, MEMORY_RULES)
    for rel, (action, src) in sorted(plan.items()):
        dest = out_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if action == "KEEP":
            shutil.copy2(src, dest)
        elif action == "EMPTY":
            dest.write_text(empty_body(src))
        elif action == "SPECIAL:memory_index":
            dest.write_text(MEMORY_INDEX_TEMPLATE)
        elif action == "SPECIAL:memory_readme":
            dest.write_text(TEMPLATE_README_BANNER + MEMORY_README_TEMPLATE)
    wiki = out_dir / "example_wiki"
    wiki.mkdir(parents=True, exist_ok=True)
    (wiki / "CLAUDE.md").write_text(GENERIC_WIKI_SCHEMA)
    (wiki / "index.md").write_text(EXAMPLE_WIKI_INDEX)
    (wiki / "sources").mkdir(exist_ok=True)
    (wiki / "sources" / "EXAMPLE_stub.md").write_text(EXAMPLE_WIKI_STUB)
    return warns


def canary_scan(out_dir):
    hits = []
    for path in sorted(out_dir.rglob("*")):
        if not path.is_file():
            continue
        # spawn.py itself defines CANARY_TOKENS; its token list is generator
        # machinery, not instance content, so exclude it from its own scan.
        if path.relative_to(out_dir).as_posix() == "scripts/spawn.py":
            continue
        text = path.read_text(errors="replace").lower()
        for token in CANARY_TOKENS:
            if token in text:
                hits.append(f"{path.relative_to(out_dir)}: '{token}'")
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
        (ws / "config" / "build" / "copy_files.yaml").write_text(
            "# Files copied verbatim into notebooks/ (not converted) by the notebook\n"
            "# build (PyAutoBuild generate.py reads this workspace-local list). List\n"
            "# paths relative to scripts/, e.g.:\n"
            "#\n"
            "# - util/helpers.py\n"
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
        failed = report(results)

        if args.check and not failed:
            for name in results:
                problems = diff_trees(out_root / name, Path(args.check) / name)
                # SPAWNED_FROM records the source commit, which legitimately
                # advances between regenerations; content drift is what matters.
                problems = [p for p in problems if not p.endswith("SPAWNED_FROM")]
                status = "OK" if not problems else f"{len(problems)} drift(s)"
                print(f"check {name}: {status}")
                for p in problems:
                    failed = True
                    print(f"  ✗ {p}")

        if args.write and not failed:
            print(f"written: {out_root}")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
