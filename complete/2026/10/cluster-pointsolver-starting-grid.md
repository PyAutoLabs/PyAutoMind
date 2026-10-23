## cluster-pointsolver-starting-grid
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/439
- completed: 2026-10-23
- library-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/440

- Merged as `03d36c81` (2026-10-23) by human `/prm`; research only (autolens_profiling), Consequence judge. Epic `cluster-pointsolver-speed`, Pulse campaign `cluster-pointsolver` follow-up to phase 1 (#436/#438). Heart YELLOW at ship (manifest drift 1 mismatch; PyAutoLens rehearsal stale — unrelated), acknowledged by the human's `/prm`.
- Deliverables: `viz_cluster` ClusterCase (`_datasets.py`, constants copied from `autolens_visualization/true_models/cluster.py` with SHA + digest); `robust_settings_sweep.py` gains `--dataset viz_cluster`, `--scales`, `--draw-ids`, `--release-executables` (`_sweep_options.py`; defaults unchanged); new `separation_rule.py` (+ `separation_rule.{json,md,png}`); laptop row sets `robust_settings_sweep_{viz_cluster,simple_draws53_73_81}_laptop_cpu_fp64.{json,png}` (host laptop (diagnostic), never quotable — any config name containing "laptop" is forced non-quotable); 11 tests in `scripts/misc/test/test_cluster_starting_grid.py`; ledger + wiki + full catalogue/dashboard re-render.
- A2744 pilot (RAL job 412573) landed: FAILED after 16 diagnostic rows (LLVM "Cannot allocate memory" → `Failed to materialize symbols`); RSS 8.3 → 39.4 GB with live arrays ~0 = retained compiled executables + compile transients; log tracked as `results/logs/cluster_pointsolver/cluster_pointsolver_2026_10_18_ral_job_412573_a2744_pilot.out`. On the A2744-geometry model (3 draws, 69 roots) the production 1.0″ grid misses fewest (2), vs 0.5″ 3, 0.7″ 5, 2.0″ 8, bbox 9–11 — the opposite ordering to `simple`. No resubmission; any A2744 full sweep needs a reference tracer, `--release-executables` and explicit human authorization.
- Starting-grid result: the workspace grid (100×100 @ 1.0″) loses `point_0` image 3 of the viz model (μ −0.89, 0.39″ from `main_1`'s core) — but so do 0.7, 0.5, 0.4, 0.37 and 0.3″; only 0.2″ finds it (567 843 step-0 triangles, ~8× solve cost, laptop diagnostic) and 0.2″ still misses 3/108 viz roots near `r_core = 0` member cores. The "~0.37″ threshold" claim is refuted. Finer is not monotonically safer (6 draw-sources found coarse, lost fine; `simple` draw 81 found at 0.4″, lost at 0.37″). No separation rule holds (`scale ≲ sep/1.06` contradicted; single-separation rules need c ≈ 11–14). The solver returns spurious candidates exactly on `r_core = 0` dPIE member cores (residual 0.04″ vs ~0.002″ tolerance). Laptop `simple` 53/73/81 re-run reproduces the RAL misses exactly (6/5/2/2 at 2.0/1.0/0.7/0.5″; all found at ≤ 0.4″).
- Recommendation (ledger, no default changed): keep 1.0″; no fixed finer grid, no separation-based default; add a validation check (every observed image needs a solved counterpart, else re-solve finely around it). Human re-decision of the deferred default still open, both inputs now measured.
- Follow-ups filed: `draft/feature/autolens_workspace/cluster_point_solver_validation_check.md`; `draft/feature/autolens/point_solver_spurious_core_candidates.md`. Owed: Pulse PR pasting the refreshed Knowledge appendix from the ledger into `tasks/cluster_pointsolver_speed.md` (after Pulse#72 merges).
- Traps: `results/logs/README.md` convention is one folder per campaign + `.out` (not `results/logs/cluster/`); `script_routes.json` takes no row; full catalogue re-render touches ~550 shards (expected); the viz-case test runs the oracle cold (~10–25 s).

## Original prompt

# `@autolens_profiling` cluster PointSolver: does the workspace's 1.0″ starting grid lose an image beside a member galaxy?

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: medium
Status: issued
Consequence: judge
Epic: cluster-pointsolver-speed
Related: `complete/2026/10/cluster-pointsolver-robust-settings.md` (autolens_profiling#436, merged #438 2026-10-22; decision deferred pending this question). Phase 1 is closed, so run this as a follow-up row set on its `robust_settings_sweep.py` harness. A2744 pilot pulled 2026-10-23: job 412573 FAILED after 16 diagnostic rows; on A2744 the 1.0″ grid misses 2/69 roots vs 0.5″ 3 and 0.7″ 5 — the opposite ordering to `simple`.
Origin: complete/2026/10/cluster-point-solver-readability.md (PyAutoLens#795/#796)
Filed: 2026-10-22
Issued: 2026-10-23
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/439

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
