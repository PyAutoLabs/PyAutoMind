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

## Human rulings (2026-11-26)

- Weak: "Fix #614 first" — keep `setup="auto"` for `AnalysisWeak`; make JAX weak fits visualize (PyAutoLabs/PyAutoLens#614: `autolens/weak/plot/weak_dataset_plots.py` `_positions_yx` gets a raw JAX array for `shear_yx`).
- Factor graphs: "Graph pushes backend down" — factors whose setup was DEFAULTED (not passed explicitly) inside a `FactorGraphModel` adopt one shared backend so mixed graphs run without pins; explicit setups still must agree (`check_setup_agreement`, PyAutoFit `autofit/graphical/declarative/collection.py`).

## Context

Found by the R6 phase B sweep (autolens_workspace#692, autogalaxy_workspace#285 pin `use_jax` in the affected examples). Must merge before the release that carries R6 phase A (PyAutoArray#715, PyAutoFit#1800, PyAutoGalaxy#760, PyAutoLens#894).
