# `@autolens_profiling` cluster PointSolver: does the workspace's 1.0″ starting grid lose an image beside a member galaxy?

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Epic: cluster-pointsolver-speed
Related: `complete/2026/10/cluster-pointsolver-robust-settings.md` (autolens_profiling#436, merged #438 2026-10-22; decision deferred pending this question). Phase 1 is closed, so run this as a follow-up row set on its `robust_settings_sweep.py` harness. A2744 pilot pulled 2026-10-23: job 412573 FAILED after 16 diagnostic rows; on A2744 the 1.0″ grid misses 2/69 roots vs 0.5″ 3 and 0.7″ 5 — the opposite ordering to `simple`.
Origin: complete/2026/10/cluster-point-solver-readability.md (PyAutoLens#795/#796)
Filed: 2026-10-22

## Original request (verbatim)

"well do the starting grid question in anothe prompt"

(Context, from the PyAutoLens#795 session: "we need to do more extensive point solver tests for setup but thats its own thing.")

## The question

While building the readable cluster `point_solver.png` (PyAutoLens#795), the implementation worker made a measurement that nobody has re-checked. In the autolens_visualization cluster model (`true_models/cluster.py`, 15 member galaxies), image 3 of `point_0` sits **0.39″** from a member galaxy's core. According to that measurement, **any starting grid coarser than ~0.37″ loses that image.**

The two grids in play:
- autolens_workspace `scripts/cluster/modeling.py` (around lines 241-247, then 582) builds one `PointSolver` on a **100×100, 1.0″** grid (±50″), shared by every `AnalysisPoint`. The search uses `FitPositionsSourceSolved`, so the solver runs only for visualization and best-fit validation, not in each likelihood evaluation.
- The viz producer solves on **400×400 at 0.2″** (369,937 triangles tested at step 0). That is the viz repo's own choice.

If the measurement holds, the workspace's 1.0″ grid would silently miss image 3 when validating or visualizing a model like this one.

## Deliverables

0. **Land the A2744 pilot after-measurement.** Record job 412573's 16 diagnostic rows, the failure (LLVM `Cannot allocate memory` → `Failed to materialize symbols` at row 17, `tight_s1_p0.001`) and the RSS attribution (RSS 8.3 → 39.4 GB with live arrays ~0: retained compiled executables plus compile transients) in `results/notes/cluster_pointsolver_campaign.md`: replace the "A2744 pilot leg (not pulled)" section, close follow-up 1, and update the wiki phase-1 row and journal. Commit the log as a tracked `.out` under `results/logs/cluster/` (the repo ignores `*.log`; the `.out` convention is tracked). State the required harness change (release executables between rows, or one row per process) as a finding. No resubmission without explicit human authorization.
1. **Reproduce or refute.** Solve the `true_models/cluster.py` model for `point_0` at the workspace's grid (1.0″, ±50″). Then sweep the starting pixel scale (for example 1.0, 0.7, 0.5, 0.4, 0.37, 0.3, 0.2″) at production `pixel_scale_precision` and magnification threshold. Report each image as found or missing against an independent numerical reference (reuse phase 1's oracle). Report the coarsest scale that finds all images, and its step-0 triangle count and solve time.
2. **Generalise the rule.** Test whether the coarsest safe scale tracks the smallest image-to-member-core separation (and the smallest image-to-image separation), for example scale ≲ separation/1.06, on a few placements or members. State the rule only if the data support it. Test the rule on the A2744-geometry member galaxies too, since the scale ranking differs between `simple` and A2744.
3. **Recommend, don't edit.** Put a results-note row set and a recommendation for the workspace cluster example's starting grid (fixed finer grid, a separation-based default, or a validation check) in the phase-1 supported-settings table. Any library or workspace change becomes its own bounded Mind prompt.

## Out of scope

Editing PyAutoLens, the workspace cluster scripts, or the viz producer's figure-only display grid (already shipped in #796). The figure is settled.

## Constraints

CPU fp64. Bulk arrays go on RAL `ral` only, never `gpu` (AGENTS.md HPC rule). A laptop run is fine if the sweep is small. Failing configurations stay in the table, labelled diagnostic.
