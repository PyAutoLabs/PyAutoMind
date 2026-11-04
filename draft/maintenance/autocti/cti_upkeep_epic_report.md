# CTI upkeep parity — survey report (2026-11-04)

Companion to `cti_upkeep_epic.md`. Read-only survey of the live checkouts
under `~/Code/PyAutoLabs`, GitHub (`gh api`), PyPI and Read the Docs, taken
2026-11-04 by the Fable architect session. Nothing was edited. Each row is a
fact a phase can be checked against; re-verify on the day a phase opens.

## 1. Repos and activity

| Repo | Last main commit | CI on main (last runs) |
|---|---|---|
| PyAutoCTI | 2026-10-08 (#116, search-ext A1 declare gate) | `Tests` (Heart lib-tests, 3.12+3.13) green; `Dependency Graph` green |
| autocti_workspace | 2026-11-01 (#39) | `Smoke Tests` + `Navigator Check` green |
| autocti_workspace_test | 2026-10-07 | `Smoke Tests` green |
| autocti_visualization | 2026-10-23 (re-render on PyAutoCTI main@2a91ff5) | `render` green (mains mode), `lint` green |
| autocti_assistant | 2026-10-26 (#39, colab-gemini phase 3) | `wiki-currency`, `colab-contexts`, `clone-boundary` green |

Heart polls all five (config/repos.yaml) with the same `required_workflows`
as the lens siblings; the only CTI special case is `release_gate: false` on
PyAutoCTI (`heart/readiness.py load_release_gate_names`).

## 2. Release train (the root gap)

- PyPI `autocti`: newest `2024.11.13.2`; git tags end at `2024.11.13.2`. The
  five train libraries are at `2026.11.1.1` (PyAutoHands README strip).
- `autocti/__init__.py` has `__version__ = "2024.11.13.2"` and no
  `check_version` call (PyAutoLens has both at `2026.8.17.1`, stamped by Hands).
- The PyPI wheel carries exact pins `autofit==2024.11.13.2` /
  `autoarray==2024.11.13.2` (memory `project_intra_family_dep_floors`:
  PyAutoCTI#104 put `>=2026.7.29.2` floors in source only, never republished).
- Hands omissions: `autohands/tag_and_merge.sh` `LIB_PROJECTS=(PyAutoNerves
  PyAutoFit PyAutoArray PyAutoLens PyAutoGalaxy)`; `release.yml` checks out the
  same five (lines ~95–107 and ~453–465) and the App-token repo lists;
  `python_matrix.yml` `unit_tests` (3.12/3.13/3.14) lists five libraries and
  `smoke_tests` three workspaces; `pre_build.sh` `WORKSPACE_SPECS` has no
  autocti rows; `build_util.COLAB_PROJECTS` = autofit/autogalaxy/autolens +
  HowTo; `generate_release_notes.py`, `slack_release_notes.py`,
  `aggregate_results.py` repo maps are five-library; `release.yml` ~line 1241
  explicitly says autocti_assistant's wiki-currency is NOT wired "until the CTI
  release train is wired". `autohands/config/workspaces.yaml` `colab_gemini`
  DOES already have an `autocti` row.
- Nerves `autonerves/setup_colab.py` `_PROJECTS` has autofit/autogalaxy/
  autolens only; an `autocti` entry needs an arcticpy pre-install step.
- Heart omissions: `release-integrate.yml` and `workspace-validation.yml`
  (six doc workspaces: autofit/autogalaxy/autolens + three HowTo) have no CTI
  rows; `docs-build.yml` package map has no `autocti`.
- Consequences visible today: autocti_workspace notebooks — 79 scripts ↔ 79
  notebooks, 0 Colab setup cells, 18 `Finish.` markdown cells, 4 code cells
  containing a literal `# %%`/`'''` (counted 2026-11-04;
  `autocti_workspace/AGENTS.md` line 166 documents the regeneration as blocked);
  PyAutoEyes dashboard row `PyAutoCTI | 135 | 2024.11.13.2 | Current`;
  autocti_visualization `render.yml` renders from mains since #8;
  autocti_assistant `version.txt` = `2026.7.9.1`, `PENDING.md` 390 lines.
- Existing prompt for this: `draft/release/autocti/cti_release_train_wiring.md`
  (filed 2026-07-17, formalised, human-required, medium) — now phase 1.

## 3. arcticpy

- Organism pin: `arcticpy==2.6`, single home
  `PyAutoHeart/.github/actions/install-arcticpy/install_arcticpy.sh`
  (`ARCTICPY_VERSION`), consumed by the composite action (lib-tests for
  `autocti`, both CTI smoke callers via `arcticpy: true`) and by
  `heart/smoke.py` locally. `arcticpy-action.yml` + `arcticpy_smoke.py` prove
  a clocked trail.
- PyPI `arcticpy` releases: 2.0 2022-10-19 … 2.5 2023-09-16, 2.6 2023-12-19;
  `requires_python >=3.8`, `requires_dist None`, source-only (no wheels).
  `arcticpy_no_gsl` 2.6 also exists.
- Upstream `jkeger/arctic` (default `main`, pushed 2026-04-06): PR #71
  2026-04-06 "CCD well filling model updated to match Euclid DR2", #70
  2026-03-30 "Euclid well-filling model", #69 2026-02-13 "Update pixel_bounce
  model", #68 2025-08-28 "Version history reporting for new paper submission",
  #67 2024-09-07 "Reflect move of wrapper from autoarray to autocti". No tags,
  no GitHub releases. `pyproject.toml` on main: `version = "2.5"`,
  `build-system.requires` = `setuptools_scm==7.0.5`, `numpy ~=1.21`,
  `Cython==0.29.36`; `dependencies = ["numpy ~=1.21"]`. Open issues include #72
  (2026-07-13) "Multi-phase CCD causes ArCTIc to crash".
- Install traps (PyAutoCTI/AGENTS.md "arcticpy"): needs `libgsl-dev`; naive
  `pip install arcticpy` downgrades numpy below 2.0; `--no-build-isolation`
  requires setuptools/numpy/cython preinstalled; `--no-deps` requires scipy +
  matplotlib preinstalled; `pip check` always reports
  `arcticpy 2.6 has requirement numpy~=1.21` (Heart `heart/smoke.py` ~line 364
  carries a permanent exception).
- Local: `~/venv/PyAuto313` has arcticpy 2.6 built for cp313 and imports.
- PyAutoCTI docs still wrong: `docs/installation/pip.rst` and `conda.rst` say
  `pip install arcticpy`; `arctic.rst` shows a 2023 `/mnt/c/Users/Jammy/Code/
  PyAuto/arctic/python` location; `troubleshooting.rst` points at
  `arcticpy_no_gsl`.
- `autocti/__init__.py` imports ROE, ROEChargeInjection, CCD, CCDPhase, the
  four Trap classes and PixelBounce from arcticpy at import time;
  `clocker/one_d.py` imports `add_cti`. So `import autocti` needs the C++ build.
- DNA: `PyAutoDNA/dna/inventory.py` `PUBLIC_PACKAGES` has no `arcticpy`;
  `stacks/` and `campaigns/` hold only READMEs.

## 4. Integration testing

| Surface | PyAutoLens side | PyAutoCTI side |
|---|---|---|
| Library unit tests | Heart lib-tests 3.12+3.13 | same (`main.yml` → `lib-tests.yml package: autocti`); 70 test files, 0 skips |
| Hands python matrix (3.12/3.13/3.14) | yes | absent |
| Workspace per-PR smoke | 86 scripts | 3 scripts (`dataset_1d/modeling/start_here.py`, `dataset_1d/modeling/features/species_x3.py`, `imaging_ci/modeling/start_here.py`) of 118 |
| workspace_test per-PR smoke | 49 scripts | 3 scripts (`scripts/{dataset_1d,imaging_ci}/model_fit.py`, `scripts/plot/subplots.py`); `legacy/` 139 files; `imaging_ci/{cosmics,temporal}` scripts outside the smoke list |
| Heart weekly workspace-validation (notebook generate leg) | yes | absent |
| Heart Release Integrate | yes | absent |
| Docs build in CI | `docs.yml` → Heart `docs-build.yml` | no `docs.yml`; `docs-build.yml` map lacks autocti; RTD `latest` serves (HTTP 200) |
| Heart local `smoke:` runner | yes | yes (`autocti`, `autocti_test` with `arcticpy: true`) |
| Navigator Check | yes | yes |

Open bug member: `draft/bug/autocti_workspace/dataset_1d_results_database_examples_drift.md`
(large, formalised, unattended-ready).

## 5. Profiling

- No `autocti_profiling` repo. Pulse `registry.yaml` instances: `lens`
  (autolens_profiling), `fit` (autofit_profiling, `profiling-summary@2`),
  `lens-walltime`. Insight: `lens`, `fit`. Cortex has no CTI project.
- Birth precedent: `PyAutoPulse/tasks/autofit_profiling_bootstrap.md` —
  repo created by hand 2026-10-07 (human gate), skeleton + registration via
  search-extensibility B1 (PyAutoMind#492, Heart#292, .github#34), exporter +
  Pulse row via B4a. Memory `project_no_org_repo_creation_path`: nothing in
  the organism creates org repos.
- PyAutoCTI root has an empty `profiling/` directory, a `to_do_list`, an
  `eden.ini`, `files/` (citations) and `paper/` (JOSS).
- Compute shape: clocking is C++ (arcticpy), not JAX; `autocti` imports jax
  only in `__init__.py` (dispatch shim) and uses numba in
  `extract/two_d/parallel/fpr.py`. So the profiling harness is a CPU numba/C++
  breakdown, not a JAX jit study; no GPU leg.

## 6. Figures, assistant, memory

- PyAutoEyes `registry.yaml` has the `cti` instance (dispatch event
  `pyautocti-release`, never fired because Hands does not release CTI). Two
  open bug drafts carry `Epic: pyautoeyes-birth` (a retired epic); re-homed to
  `cti-upkeep` phase 5.
- autocti_assistant is public, in Broca `assistants.json`, CI green; its
  wiki-currency installs from source because PyPI is stale (autocti_assistant#1).
- PyAutoMemory `wiki/cti`: one concept, two entities (arctic, euclid-vis),
  sources, log — thin.

## 7. Hygiene

- `docs/api`: 55 of 89 autosummary entries dead
  (`draft/docs/autocti/api_rst_rewrite.md`, formalised, medium).
- README badges point at `Jammy2211/PyAutoCTI` workflows (repo moved to
  PyAutoLabs 2026-07-17).
- `pyproject.toml` classifiers: 3.12, 3.13 (no 3.14); `requires-python >=3.12`;
  floors `autofit>=2026.7.29.2`, `autoarray>=2026.7.29.2`,
  `autonerves>2026.10.4.1`, `nautilus-sampler==1.0.5`.
- Brain `bin/worktree.sh` `PYAUTO_LIBS` already includes PyAutoCTI; Heart
  `lib-tests.yml` and `docs-build.yml` disagree (lib-tests knows autocti,
  docs-build does not).

## 8. Suggested first moves

1. Rule R1 and R6 (arcticpy distribution; lockstep nightly) — they shape
   phase 1's Nerves/Colab step and Heart's gate flip.
2. `/start_dev` on `draft/release/autocti/cti_release_train_wiring.md` as
   phase 1 (human-required; TestPyPI rehearsal). Everything in §2 clears with
   the first release.
3. Open the upstream `jkeger/arctic` packaging PR (phase 2a) in parallel — it
   has the longest external latency.
