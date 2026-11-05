# CTI upkeep parity — bring PyAutoCTI and its satellites to the same level of upkeep as the other libraries

Type: maintenance
Target: autocti
Repos:
- PyAutoCTI
- autocti_workspace
- autocti_workspace_test
- autocti_visualization
- autocti_assistant
- PyAutoHands
- PyAutoHeart
- PyAutoNerves
- PyAutoPulse
- PyAutoDNA
- PyAutoMind
Themes:
- cti
- release
- infrastructure
- profiling
- docs-hub
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: campaign map — phases route through /start_dev one at a time; this file is never issued itself and nothing here is bulk-issued
Consequence: judge
Witness: phase 1 — `pip install autocti` into a clean Python 3.13 venv resolves the lockstep `YYYY.M.D.n` release (not 2024.11.13.2) with `autofit>=`/`autoarray>=` floors, and `pyauto-heart readiness` lists PyAutoCTI among the release-gate libraries; phase 3 — Hands `python_matrix.yml` and Heart's board carry PyAutoCTI / autocti_workspace / autocti_workspace_test rows in every group PyAutoLens sits in, green; phase 4 — PyAutoPulse `registry.yaml` has a `cti` instance reading `profiling-summary@3` from `autocti_profiling`
Review-minutes: 30
Unattended: needs-slicing
Epic: cti-upkeep
Filed: 2026-11-04

Evidence and the per-gap survey: `cti_upkeep_epic_report.md` beside this file
(written 2026-11-04 by the Fable architect session from live checkouts, GitHub
and PyPI; no code edited).

## Why

The CTI resurrection epic (PyAutoCTI#82, phases 0–5, all merged 2026-07-17;
records `complete/2026/07/cti-resurrection-phase{0..5}.md`) made PyAutoCTI
importable, test-green and workspace-validated on the modern stack. It stopped
one step short of the ecosystem: the release-train wiring was deferred as
`draft/release/autocti/cti_release_train_wiring.md` and never issued (issued and shipped 2026-11-05 as phase 1). Four
months on, every other upkeep surface still treats CTI as a special case:

- **Not released.** PyPI `autocti` is `2024.11.13.2` (last tag 2024-11-13); the
  five release-train libraries are at `2026.11.1.1`. The PyPI wheel still
  carries the pre-fix exact pins `autofit==2024.11.13.2`, so a user's
  `pip install autocti` resolves a two-year-old stack. Hands' `LIB_PROJECTS`,
  `release.yml` checkouts, `python_matrix.yml`, `pre_build.sh`
  `WORKSPACE_SPECS` and `build_util.COLAB_PROJECTS` all omit CTI; Nerves'
  `setup_colab._PROJECTS` has no `autocti`; Heart `config/repos.yaml` marks
  PyAutoCTI `release_gate: false` ("mid-resurrection"). Downstream: 0 of 79
  workspace notebooks carry a Colab cell and 18 `Finish.` markdown cells plus 4
  syntax-broken code cells are still committed (scripts are correct — the
  generator has never run for CTI); autocti_visualization renders from library
  mains with a `rendered_with: 2024.11.13.2` stamp that PyAutoEyes shows as
  "Current"; autocti_assistant's wiki-currency check is excluded from the
  release run and its `version.txt` is `2026.7.9.1`.
- **arcticpy is stale and awkward.** The organism pins `arcticpy==2.6` (PyPI
  2023-12-19, source-only C++ sdist, no wheels, `numpy ~=1.21`, `Cython
  0.29.36`). Upstream `jkeger/arctic` main has moved on (2026-02 pixel-bounce
  update, 2026-03/04 Euclid well-filling model updated to match DR2, 2025-08
  version-history reporting) with nothing released to PyPI, and its `pyproject`
  still says `version = "2.5"`. Installing needs `libgsl-dev` plus
  `--no-build-isolation --no-deps` or numpy is downgraded below 2.0; `pip
  check` permanently reports the numpy conflict (Heart carries a special-case
  exception). PyAutoCTI's own install docs (`docs/installation/pip.rst`,
  `conda.rst`) still say a bare `pip install arcticpy`, which breaks a modern
  venv. arcticpy is in no DNA inventory or stack spec.
- **Integration testing is thin, not absent.** Per-PR `Smoke Tests` run
  through Heart's reusable workflow and are green for autocti_workspace (3 of
  118 scripts in `smoke_tests.txt`; autolens_workspace runs 86) and
  autocti_workspace_test (3 modern scripts beside 139 untriaged `legacy/` files
  of Euclid VIS heritage; autolens_workspace_test runs 49). CTI is absent from
  Hands' 3.12/3.13/3.14 unit and smoke matrices, Heart's `Release Integrate`,
  the weekly `workspace-validation.yml` notebook leg, and Heart's
  `docs-build.yml` package map (PyAutoCTI has no `docs.yml` caller, so the RTD
  build is unchecked in CI; `docs/api` has 55 of 89 dead autosummary entries).
- **No profiling.** There is no `autocti_profiling` repo; Pulse's registry has
  `lens`, `fit`, `lens-walltime` and Insight has `lens`, `fit`. The library
  root still carries an empty `profiling/` directory, a `to_do_list` file and
  an `eden.ini` from the pre-resurrection era.

The ask (human, 2026-11-04): "take us through all the steps to get PyAutoCTI
to the same level of upkeep as all other repos".

## Phases

Library first; one issue per repo per phase; each phase routes through
`/start_dev` from its own prompt. Phases 1 and 2 are the critical path; 3a and
5c do not depend on a release and may run alongside 1–2.

0. **Census + rulings (research, small, this session's report is the draft).**
   Re-verify the report against live state on the day the epic opens, then
   collect the rulings in §Decisions below. Output: rulings recorded in this
   ledger; phase 1 prompt un-blocked. **0b (code, first to ship): numerical
   log-likelihood pins in autocti_workspace_test** (DONE 2026-11-04,
   autocti_workspace_test#25; record `complete/2026/11/cti-likelihood-pins.md`) — the lens and
   galaxy test workspaces pin absolute `log_likelihood` literals per likelihood
   function; CTI has none, so nothing would notice a value change from a
   library PR or the phase 2 arcticpy bump. Lands before any library or
   arcticpy change (human, 2026-11-04).
1. **Release-train wiring + first modern release** (member:
   `complete/2026/11/cti-release-train-wiring.md`, PyAutoHands#332, human-required; DONE 2026-11-05). Hands
   `LIB_PROJECTS` += PyAutoCTI; `release.yml` library checkouts, release notes,
   Slack and aggregate maps; `python_matrix.yml` unit + smoke legs;
   `pre_build.sh` `WORKSPACE_SPECS` rows for autocti_workspace (generate) and
   autocti_workspace_test (no generate); `build_util.COLAB_PROJECTS` += autocti;
   Nerves `setup_colab._PROJECTS["autocti"]` with an arcticpy pre-install step
   (`apt-get install libgsl-dev`, `pip install numpy cython`, then the
   `--no-build-isolation --no-deps` build — Colab permits apt); Hands
   `wiki_currency_check_autocti` on the release run; the `pyautocti-release`
   visualization dispatch; Heart `release_gate: true`, `Release Integrate` and
   `workspace-validation.yml` rows, `docs-build.yml` `autocti` mapping;
   FIREWALL_ALLOWLIST tokens in Mind for every organ file gaining CTI names.
   TestPyPI rehearsal through `/release rehearse` before the first real
   release; never hand-dispatch the nightly. Regenerated notebooks (Colab cells,
   `Finish.` and `# %%` defects gone) ride the release. Then close the
   `autocti_visualization` PyPI-mode bug (phase 5a) becomes possible.
2. **arcticpy modernisation (library + Heart + DNA + docs; human-required at
   the upstream boundary).** 2a upstream: a PR to `jkeger/arctic` that makes
   the package installable on a modern stack — `numpy>=1.21,<3` (not `~=`),
   Cython 3, unpinned `setuptools_scm`, declared build requires, `version`
   bumped — and a request for a `2.7` PyPI release carrying the 2026 Euclid
   DR2 well-filling and pixel-bounce changes, ideally with `cibuildwheel` wheels
   (GSL vendored or statically linked). Richard Massey owns the PyPI name; the
   human decides whether to wait for upstream or publish PyAutoLabs-built wheels
   under a distinct name (R1). 2b organism: bump `ARCTICPY_VERSION` in Heart's
   `install_arcticpy.sh` (the single pin), drop the `--no-deps` workaround and
   the `pip check` exception if upstream fixes its metadata, add arcticpy to DNA
   `PUBLIC_PACKAGES` with a stack spec and support rationale, re-run
   `arcticpy_smoke.py`. Trap: the DR2 well-filling model changes clocked values,
   so `test_autocti` fixtures and the workspace_test recover scripts are
   expected to move — regenerate deliberately, record the before/after in the
   PR, never loosen tolerances silently. 2c PyAutoCTI: rewrite
   `docs/installation/{pip,conda,arctic,troubleshooting}.rst` to the recipe
   (and `arcticpy_no_gsl` only as the documented fallback); decide R2 (lazy
   import of arcticpy so `import autocti` works for docs, Eyes and the
   assistant without a C++ build; clocking raises a clear error instead).
3. **Integration-test parity.** 3a autocti_workspace `smoke_tests.txt` from 3
   scripts to a representative set across `dataset_1d/`, `imaging_ci/`,
   `plot/`, `advanced/database` within Heart's smoke time budget, and the
   results/database drift bug (member:
   `draft/bug/autocti_workspace/dataset_1d_results_database_examples_drift.md`, DONE 2026-11-05 → `complete/2026/11/cti-database-examples-drift.md`).
   3b autocti_workspace_test rebuilt to the autolens_workspace_test shape
   (`run_all_scripts.sh`, `no_run.yaml`, recover-the-input-traps scripts for 1D
   and 2D fits, aggregator round trip, `remove_cti`, cosmic-ray flagging);
   `legacy/` triaged per R3 (archive in place with a README, or retire via
   PyAutoGut). 3c PyAutoCTI `docs.yml` caller on Heart's `docs-build.yml` with a
   Sphinx warning baseline; Python 3.14 classifier once the Hands matrix leg is
   green (R4); `ci_timing` rows for the CTI workflows on Heart's board.
4. **Profiling + Pulse day zero.** Birth `autocti_profiling` (org repo is a
   human gate — nothing in the organism creates org repos; precedent
   `PyAutoPulse/tasks/autofit_profiling_bootstrap.md` and search-extensibility
   B1/B4a): register in Mind `repos.yaml` (`cti/autocti_profiling`), Heart
   `excluded:`, the org profile; harness + producers for the CTI likelihood —
   `add_cti`/`remove_cti` clocking cost against `express`, image size, trap
   count and ROE, Dataset1D vs ImagingCI fit per-stage breakdown (clock, FPR/EPER
   extraction, chi-squared), numba leg (`extract/two_d/parallel/fpr.py`) — at
   `profiling-summary@3` with a Pages dashboard; Pulse `registry.yaml` row
   `cti`; retire the library's empty `profiling/` directory. Insight (sampler
   benchmark on trap recovery) is a stretch item, not in scope.
5. **Figures, assistant, docs currency.** 5a autocti_visualization: `render.yml`
   back to PyPI mode after phase 1 and the two bug members
   (`draft/bug/autocti_visualization/render_yml_blocked_until_pyautocti_release.md`,
   `draft/bug/autocti_visualization/manifest_rendered_with_stale_in_mains_mode.md`);
   `/eyes` sign-off of the 135 figures. 5b autocti_assistant: `version.txt` to
   the released stack, `PENDING.md` (390 lines) triaged, wiki-currency on the
   release run (phase 1 wires it), Broca receipts current. 5c PyAutoCTI docs:
   `docs/api` rewrite (member: `draft/docs/autocti/api_rst_rewrite.md`), README
   badges off `Jammy2211/`, RTD on the released version; `/audit_docs`,
   `/dep_audit`, `/hygiene` and `/cli_noise_clean` enumerate the CTI repos.
6. **Hygiene + close.** Repo debris (`to_do_list`, `profiling/`, `eden.ini`,
   `files/`, `paper/` — keep JOSS material, retire the rest via Gut),
   `__version__`/`check_version` parity with autolens, dependency-cap audit,
   PyAutoMemory `wiki/cti` enrichment from the resurrection and this epic, DNA
   stack spec committed, Heart README/REFERENCE say "six libraries" where they
   say five; completion record and this ledger's `status:` → COMPLETE.

## Decisions (human, ruled 2026-11-04)

- R1 **arcticpy distribution — RULED: fix upstream.** Phase 2a prepares the
  packaging fix as a PR to `jkeger/arctic` (modern `numpy` range, Cython 3,
  declared build requires, version bump, wheels if feasible); the human
  contacts Richard Massey to cut and publish the new PyPI release. No
  PyAutoLabs-published wheels or renamed fork.
- R2 **lazy arcticpy import — RULED: do it if it works.** Phase 2c makes
  `import autocti` succeed without arcticpy, with clocking raising a clear
  error naming the install recipe; drop it only if the test suite or the
  factor-graph path cannot be kept clean that way, and record why.
- R3 **workspace_test `legacy/` — RULED: retire via Gut** (phase 3b; the 139
  Euclid VIS heritage files leave the tree as a recoverable Gut ref through
  the transit window, never a plain delete).
- R4 **Python 3.14 — RULED: defer.** CTI stays on the 3.12/3.13 legs until
  arcticpy builds on 3.14; no 3.14 classifier or matrix leg in this epic.
- R5 **autocti_profiling — RULED: public repo**, created by the human or by the
  session under `PyAutoLabs/` (explicit authorisation for this one repo; the
  no-org-repo-creation default otherwise stands). Name `autocti_profiling`.
- R6 **lockstep nightly — RULED: recommendation adopted.** CTI joins the
  nightly release driver as the sixth lockstep library from phase 1, with
  Heart `release_gate: true` in the same phase.

## Boundaries

- Science use of CTI (Euclid VIS calibration runs) is out of scope; this epic
  is upkeep parity only. No new CTI physics beyond what the arcticpy bump
  carries.
- No bulk issue queue: one phase at a time, each phase its own prompt(s).
- Never hand-dispatch `release.yml`; rehearsal first; merge/close stay human.
- The arcticpy pin lives in exactly one place (Heart `install_arcticpy.sh`,
  PyAutoHeart#170); no phase adds a second copy.
- Workspace_test heritage content is not deleted without R3.

## Members

- Phase 0: 0b DONE 2026-11-04 — `complete/2026/11/cti-likelihood-pins.md` (autocti_workspace_test#25)
- Phase 1: DONE 2026-11-05 — `complete/2026/11/cti-release-train-wiring.md` (PyAutoHands#332; Nerves#210, Hands#333, Brain#585, Heart#323, Mind#535, autocti_workspace#40; TestPyPI rehearsal run 42011123173 passed, 6 wheels). Scope deferred to p3/5: Heart workspace-validation/release-integrate rows, run_all, docs-build mapping. New phase-3 member: fits_fit FAST_PLOTS bug (DONE 2026-11-05, `complete/2026/11/cti-fits-fit-output-dir.md`). First modern autocti PyPI release rides the next lockstep release.
- Phase 2 (filed 2026-11-05): 2a `draft/release/arcticpy/upstream_packaging_pr.md` (PR jkeger/arctic#73 OPEN 2026-11-05; human asks Massey for 2.7);
  2b `draft/maintenance/pyautoheart/arcticpy_pin_bump_after_upstream_release.md` (blocked by the upstream release);
  2c DONE 2026-11-05 `complete/2026/11/arcticpy-lazy-import.md` (PyAutoCTI#118 merged) and
  `draft/docs/autocti/installation_docs_arcticpy_recipe.md` (blocked by 2b)
- Phase 3 (started 2026-11-05 while 2b waits on upstream): 3a `active/autocti_workspace_smoke_breadth.md` (autocti_workspace#43, IN DEV); DONE 2026-11-05 `complete/2026/11/cti-fits-fit-output-dir.md` (PyAutoCTI#120 + autocti_workspace#41; FAST_PLOTS back to 1); dataset_1d results/database drift DONE 2026-11-05 `complete/2026/11/cti-database-examples-drift.md` (PyAutoCTI#122 + autocti_workspace#42; new follow-up `draft/bug/autofit/samples_with_paths_shared_prior_factor_graph.md`)
- Phase 5: `draft/bug/autocti_visualization/render_yml_blocked_until_pyautocti_release.md`,
  `draft/bug/autocti_visualization/manifest_rendered_with_stale_in_mains_mode.md`,
  `draft/docs/autocti/api_rst_rewrite.md`
- Other phases: prompts filed when the preceding phase closes.

## Log

- 2026-11-04 — filed from the human's request; survey in the report; rulings
  R1–R6 open. First step: `/start_dev` on the phase 1 member after R1/R6.
- 2026-11-04 — human: add numerical likelihood test values to the test
  workspace early, as the other projects have; filed as phase 0b member
  (no dependency on rulings — can `/start_dev` now).
- 2026-11-04 — human ruled R1–R6 (fix arcticpy upstream + Massey release;
  lazy import if it works; legacy/ via Gut; 3.14 deferred; public
  autocti_profiling; lockstep from phase 1). Phase 1 un-blocked.
- 2026-11-05 — phase 1 CLOSED (complete/2026/11/cti-release-train-wiring.md); nightly is armed, so the first autocti release rides the 2026-11-06 02:00 UTC nightly with no manual release. Phase 2 filed as 4 members; 2c lazy import starts first because 2a needs the human's go-ahead for a third-party PR and 2b waits on upstream.
- 2026-11-05 — 2c lazy import MERGED (PyAutoCTI#118, complete/2026/11/arcticpy-lazy-import.md). 2a upstream PR jkeger/arctic#73 open; the human asks Massey for 2.7. 2b and the install docs wait on that release.
- 2026-11-05 — phase 3 started while 2b waits on upstream: fits_fit FAST_PLOTS fix MERGED (PyAutoCTI#120 + autocti_workspace#41, glance auto-merge, complete/2026/11/cti-fits-fit-output-dir.md). Release profile is back to FAST_PLOTS=1.
- 2026-11-05 — dataset_1d results/database drift MERGED (PyAutoCTI#122 + autocti_workspace#42, glance auto-merge, complete/2026/11/cti-database-examples-drift.md). CTIAgg returns a per-dataset list for factor-graph fits (human ruling); the ignored-instance bug is fixed; smoke list is now 6. Follow-up: draft/bug/autofit/samples_with_paths_shared_prior_factor_graph.md. Phase 3 remaining: 3a smoke breadth (imaging_ci/plot), 3b workspace_test rebuild + legacy/ via Gut (R3), 3c docs.yml + ci_timing; deferred from p1: Heart workspace-validation/release-integrate rows, run_all.
