# Rename `PyAutoHands/autobuild` to `PyAutoHands/autohands`

Type: refactor
Target: PyAutoHands
Repos:
- PyAutoHands
- PyAutoBrain
- PyAutoHeart
- autolens_workspace
- autogalaxy_workspace
- autofit_workspace
- autolens_workspace_test
- autogalaxy_workspace_test
- autofit_workspace_test
- autocti_workspace_test
- HowToLens
- HowToGalaxy
- HowToFit
- autolens_assistant
- autofit_assistant
- autocti_assistant
- admin_jammy
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

## Original request (verbatim)

> rename - PyAutoHands/autobuild to - PyAutoHands/autohands and make sure this
> new word is used throughout

## Why

The Hands repo was renamed `PyAutoBuild` → `PyAutoHands`, but its payload
package and CLI kept the old `autobuild` name. The organ and its package now
disagree, which is the one naming seam the rename left behind.

## Scope

Rename the package directory, the CLI, and every **live** reference to the new
word across the organism.

- **PyAutoHands** (primary): `autobuild/` → `autohands/` (27 modules +
  `config/workspaces.yaml`), `bin/autobuild` → `bin/autohands` (and its internal
  `AUTOBUILD_DIR` / help text / alias suggestion), `pre_build.sh`, `tests/`
  (including the dotted imports `from autobuild.build_util import …`), `docs/`,
  `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `.github/workflows/`.
- **PyAutoHeart**: `.github/workflows/workspace-validation.yml` invokes
  `PyAutoHands/autobuild/*.py` by path in five places; also
  `heart/checks/*.py` comments and `scripts/health_release.sh`.
- **PyAutoBrain**: `config/policy.yaml` (`extra_organism_targets`, alias map),
  `agents/_common.sh` (`resolve_autobuild`), the intake/bug repo maps, the
  build-conductor docs and `build.sh` dispatch.
- **Workspaces / HowTos / assistants**: `AGENTS.md` generate commands
  (`PYTHONPATH=../PyAutoHands/autobuild …`), `.github/scripts/run_smoke.py`
  (`sys.path.insert(… "autobuild")`), `.github/workflows/navigator_check.yml`
  comments, `config/build/visualise_notebooks.yaml` header comments,
  `.claude/skills/*/SKILL.md`.

## Guardrails

- **No back-compat shim.** Land atomically, library-first: the directory move
  breaks PyAutoHeart's `workspace-validation.yml` and every workspace's
  `run_smoke.py` the moment it merges, so all PRs must be merged in one pass
  before the next nightly.
- **Preserve historical old-name references.** Do *not* rewrite `PyAutoBuild#NNN`
  issue citations, `rhayes777/PyAutoBuild` URL-fixup patterns in
  `PyAutoHeart/config/url_fixups.yaml` / `url_check.sh`, or the back-compat
  alias `pyautobuild: pyautohands` in `PyAutoBrain/config/policy.yaml`. These
  point at real historical artifacts; rewriting them makes them wrong.
- **Leave PyAutoMind historical records untouched** (~150 files under
  `complete/`, `active/`, `draft/`, `issued/`, records) — dated records of past
  work. Two further exclusions of the same kind: `planned.md:121` and
  `dashboard.md:92` reference Mind *prompt paths* (`feature/pyautobuild/…`,
  `research/autobuild/git_docs.md`); those are registry pointers to real files
  on disk, so rewriting the string without moving the files breaks the link.
- **But PyAutoMind has two LIVE exceptions that must change** (found on the
  deep sweep; they are code and routing, not records):
  - `scripts/repos_sync.py:558-570` — a hard-coded dict keyed by
    `PyAutoHands/autobuild/<module>.py` paths. `repos_sync.py --write`
    regenerates the AGENTS.md repo tables and breaks silently without this.
  - `ROUTING.md:38` — lists `autobuild` as a routing target.
- Confirmed absent, do not go hunting again: no root-level `PyAutoLabs/*.md`
  references, and no `auto_build` / `autoBuild` / `Autobuild` spelling variants
  anywhere in the workspace.
- Two import styles must both keep working: dotted (`from autobuild.build_util
  import …`, PyAutoHands' own tests) and flat-on-`PYTHONPATH`
  (`from build_util import …`, workspaces — only the `sys.path` string changes).
- Use `git mv` so history follows the files.
- No `setup.py`/`pyproject.toml` exists, so no PyPI package name is at stake.

## Run conditions (recorded at launch, 2026-07-23)

- **Phasing override.** The Brain Feature Agent scored this `too-large (37)` and
  recommended `split-into-phases` (design / core-api / workspace-examples /
  docs). Not taken, with the human's approval: the score is driven by repo count
  (16), not conceptual complexity; there is no design phase in a mechanical
  rename; and sequential phases would violate the atomic-landing guardrail above
  by leaving a window where Hands has moved and Heart's CI still points at the
  old path. The work is still ~18 PRs (one per repo) sharing one branch name.
- **Heart was RED (score 0) at launch** — 13 test failures, 33 stale parked
  scripts, release validation `integrate:fail`. None caused by this task, and
  the corrective-PR exception does not apply (this rename repairs no RED
  reason). Per `AUTONOMY.md`, RED forbids commit/push/PR-open at every autonomy
  level, so this run is expected to park at the ship gate. Effective autonomy
  = min(`supervised` header, `safe` refactor cap) = **supervised**.

<!-- authored by start_dev from a direct user request on 2026-07-23; scope
     decisions (all live code + docs / preserve historical refs / no shim)
     confirmed with the user before planning -->
