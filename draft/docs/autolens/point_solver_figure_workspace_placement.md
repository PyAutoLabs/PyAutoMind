# Point-source phase 3: place and describe the PointSolver figure across the workspace

Consequence: judge
Autonomy: human-required
blocked-by: draft/feature/autolens/point_solver_refinement_figure.md (phase 2; the figure and API must exist and be released first)

@HowToLens @autolens_workspace @autolens_workspace_test

## Request (human, 2026-10-21)

> also include a follow up which scans the workspace for places to slot it in and describe it (e.g. HowToLens's section of position solviung, which is either in chapter 1 or has a placeholder).

## Scope

Scan HowToLens and autolens_workspace (and the autolens_assistant skills, if relevant) for every place the PointSolver is explained or configured. Then insert the phase-2 figure with prose that walks through what each panel shows.

Known candidates (2026-10-21):
- **HowToLens `scripts/chapter_1_introduction/tutorial_4_point_sources.py:200`, "__Point Solver__".** The four triangle steps are described in prose only, so this is the primary slot.
- **HowToLens chapter 4:** `chapter_4_scaling_up_lensing/tutorial_5_cluster_scale.py:277` and the "Point Solver" sections in `simulator/cluster.py` and `simulator/no_lens_light.py`.
- **autolens_workspace:** `scripts/point_source/` (`modeling.py`, `fit.py`, the simulators) and `guides/point_source_pairing.py`.
- **autolens_workspace_test:** `scripts/point_source/jax_likelihood/solver_extent.py`, as a diagnostic cross-reference.

Deliver a placement list (file, section, what to show) for human approval before editing. Then edit the scripts, regenerating the notebooks via the usual generate step. Add the diagnostic framing for modellers: check that the solver grid covers every image, and check the triangle counts per step.
