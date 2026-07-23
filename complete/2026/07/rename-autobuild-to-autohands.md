- summary: renamed the Hands payload package and CLI `autobuild` -> `autohands`, closing the seam left by the earlier PyAutoBuild -> PyAutoHands repo rename. 18 PRs across 18 repos, all merged 2026-07-23 in the required order (PyAutoHands#179 -> PyAutoHeart#99 -> PyAutoBrain#152 -> 15 others). `git mv` throughout so history follows. Landed ATOMICALLY with no back-compat shim, by explicit human choice.
- scope: PyAutoHands (54 files: autobuild/ -> autohands/, bin/autobuild -> bin/autohands, AUTOHANDS_DIR, dotted test imports, pre_build.sh, docs, workflows); PyAutoHeart (12: workspace-validation.yml's five hard-coded PyAutoHands/autobuild/*.py invocations, health_release.sh, check comments); PyAutoBrain (19: _common.sh resolve_autobuild -> resolve_autohands, policy.yaml, build/release/intake/bug/clone conductors, organ docs, test_policy_seams.py); 13 workspace/HowTo/assistant repos (AGENTS.md generate commands, run_smoke.py sys.path.insert, SKILL.md, config/workflow header comments); PyAutoMind (2 LIVE files only); admin_jammy (1 stale PyAutoBuild/skills/ path).
- preserved: PyAutoBuild#NNN issue citations, rhayes777/PyAutoBuild url_fixups patterns, the `pyautobuild: pyautohands` policy alias, pyautobuild_boundary_audit.md (a real filename), ~150 Mind historical records, planned.md/dashboard.md prompt-path pointers, the two gitignored settings.local.json allowlists, and the PYAUTOBUILD_DIR docstring describing a shim that no longer exists. Implemented with perl lookbehind guards `(?<!py)autobuild` / `(?<!PY)AUTOBUILD` so the preserved repo-name token survived all 111 edited files. `autobuild` was additionally KEPT as a back-compat ROUTER KEYWORD in policy.yaml/_intake.py/_bug.py — typed keywords, not paths, so old prompts still route to Hands at zero cost.
- key finding 1 (THE DEEP SWEEP EARNED ITS KEEP): PyAutoMind/scripts/repos_sync.py:558-570 held a hard-coded FIREWALL_ALLOWLIST dict keyed by `PyAutoHands/autobuild/<module>.py`. Missed by the first repo-level pass because PyAutoMind had been excluded wholesale as "historical" — too coarse. The allowlist is keyed by REAL FILE PATH, so missing it would have turned all 13 moved modules into "unlisted file" firewall violations, and `repos_sync.py --write` would have broken SILENTLY. ROUTING.md:38 was the only other live Mind file.
- key finding 2 (RE-SWEEP AFTER EVERY MERGE FROM MAIN): on a rename this wide, new references keep ARRIVING mid-flight. Twice: (a) PR#178 (clone-skill-prefix-corruption) landed tests/test_clone_seed_substitute.py importing `from autobuild.clone_seed import substitute` — git rename-detection correctly carried main's edits onto autohands/clone_seed.py but is STRUCTURALLY BLIND to a NEW file written against the old name; (b) the no_run config cleanup then added 3 more `PyAutoHands/autobuild/build_util.py` comments (autolens_workspace, HowToLens, HowToGalaxy). Both caught ONLY because main was merged in early and the sweep re-run — deferring the merge to ship time would have surfaced them as red CI across an 18-PR wave.
- key finding 3 (STALE __pycache__ CAN MASK A MISSED RENAME): after merge, PyAutoHands/autobuild/ survived as untracked cruft containing only __pycache__. In Python 3 a directory WITHOUT __init__.py is still importable as a NAMESPACE PACKAGE, so `import autobuild` would have silently succeeded instead of failing loudly. Removed, then asserted via importlib.util.find_spec that autobuild is NOT importable and autohands IS.
- key finding 4 (THE RED WAS STALE EVIDENCE): the task parked twice at the ship gate on Heart RED (score 0). Investigation showed `release validation FAILED (stage integrate)` traced to run 29912642195 with 3 script failures — cluster/start_here.py TIMEOUT@1800s and interferometer/features/potential_correction/{start_here,likelihood_function}.py both raising "The dpsi grid is too sparse" (mesh.py:132) because PYAUTO_SMALL_DATASETS=1 caps masks to 15x15 and the `interferometer/start_here` override is a SUBSTRING match that never reaches interferometer/features/potential_correction/*. THAT FIX WAS ALREADY MERGED (autolens_workspace f582fb7f5, 2026-07-22 19:26) NINE HOURS AFTER the failing run started (10:40). The "13 failed" reason was dated 2026-07-21, also pre-fix. Refreshing stale local checkouts alone moved Heart 0 -> 40; Heart's readiness reads a CACHED tick, so a forced `pyauto-heart tick` was needed to see it. No re-run was performed — human directed not to.
- process: Brain Feature Agent scored too-large(37) and recommended split-into-phases; OVERRIDDEN with human approval — the score is repo-count-driven, there is no design phase in a mechanical rename, and sequential phases would have violated the atomic-landing guardrail.
- followup: `manifest drift: tenant firewall (organ code) — 4 mismatch(es)` NOT fixed here, deliberately unbundled to keep the rename diff clean. 2 of the 4 are PR#178 fallout (test_clone_seed_substitute.py absent from FIREWALL_ALLOWLIST; _clone.py:417 autocti_assistant). Fix = one-line allowlist addition in PyAutoMind/scripts/repos_sync.py, same treatment as the already-allowlisted sibling test_clone_conductor.py.
- verification (on merged main): PyAutoHands 148 passed; PyAutoBrain 152 passed / 1 failed (test_skill_install `sizing` wrapper — PRE-EXISTING on main, verified before the work started); autohands help renders; repos_sync.py --check clean; zero lowercase autobuild outside the preserve-list; autobuild not importable, autohands importable.

## Original prompt

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
