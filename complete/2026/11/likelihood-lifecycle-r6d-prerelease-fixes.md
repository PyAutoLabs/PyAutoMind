## likelihood-lifecycle-r6d-prerelease-fixes
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/895
- completed: 2026-11-26
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1801
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/761
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/896
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1801
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/761
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/896
- epic: likelihood-lifecycle (R6 pre-release fixes)
- follow-up: draft/feature/autolens_workspace/remove_r6_sweep_pins_after_release.md

Two release blockers found by the R6 phase B sweep, fixed before the release that carries R6 phase A (human rulings 2026-11-26):

- **PyAutoLens#614 (JAX weak visualization):** `AnalysisWeak.fit_for_visualization` builds `FitWeak(..., xp=np)`; `ResultWeak.max_log_likelihood_fit` uses it too (a second crash site). `AnalysisWeak` keeps the `setup="auto"` default (JAX).
- **Mixed factor graphs under the default:** PyAutoFit hooks `af.Analysis.setup_is_default` / `adopt_backend(use_jax)` (forwarded by AnalysisFactor, ModelAnalysis, nested graphs); `FactorGraphModel.adopt_shared_backend()` in `modify_before_fit`: factors the user configured (`setup=` or `use_jax=`) never change and must agree; defaulted factors adopt the graph's `use_jax`, else the configured factors' backend, else JAX. PyAutoGalaxy `AnalysisSetupMixin.adopt_backend` drops to the no-setup path and `AnalysisDataset._undo_resolved_setup` restores the dataset as given (operator undone, grids re-preloaded). EP unaffected.

Checks: every new test failed on a control run; suites with JAX (Fit 4399, Galaxy 1685, Lens 1182) and the CI-faithful no-JAX venv (4072/1601/1114) green; Heart smoke 8/8; end-to-end weak/modeling.py and both mixed multi_dataset scripts (pins removed) exit 0.

Trap: PyAutoFit#1801's first CI run failed 9 Zeus conformance tests ("Number of contractions exceeded maximum limit!") — not reproducible locally on the branch or main with 1 or 4 CPUs; the human-authorized re-run was green. Zeus's slice sampler on a 4-core CI runner can flake now that searches default to `number_of_cores="auto"`; if it recurs, pin `number_of_cores=1` in the conformance fixture.

## Original prompt

# Likelihood lifecycle R6 pre-release fixes: JAX weak plotting (#614) and mixed factor graphs under setup="auto"

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- PyAutoGalaxy
- PyAutoLens
Themes:
- hpc-gpu
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: (1) `al.AnalysisWeak(dataset)` with the default setup fits and visualizes on the JAX path without the `shear_yx.grid` AttributeError; (2) a `FactorGraphModel` of a default-constructed `al.AnalysisImaging` and `al.AnalysisInterferometer` (or imaging + point) passes `modify_before_fit` / `check_setup_agreement` with no `use_jax=` pins.
Epic: likelihood-lifecycle
Phase: 6 (R6 rollout, pre-release fixes)
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-26
Issued: 2026-11-26

## Human rulings (2026-11-26)

- Weak: "Fix #614 first" — keep `setup="auto"` for `AnalysisWeak`; make JAX weak fits visualize (PyAutoLabs/PyAutoLens#614: `autolens/weak/plot/weak_dataset_plots.py` `_positions_yx` gets a raw JAX array for `shear_yx`).
- Factor graphs: "Graph pushes backend down" — factors whose setup was DEFAULTED (not passed explicitly) inside a `FactorGraphModel` adopt one shared backend so mixed graphs run without pins; explicit setups still must agree (`check_setup_agreement`, PyAutoFit `autofit/graphical/declarative/collection.py`).

## Context

Found by the R6 phase B sweep (autolens_workspace#692, autogalaxy_workspace#285 pin `use_jax` in the affected examples). Must merge before the release that carries R6 phase A (PyAutoArray#715, PyAutoFit#1800, PyAutoGalaxy#760, PyAutoLens#894).
