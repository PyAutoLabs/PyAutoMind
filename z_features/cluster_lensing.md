__Outstanding__ (sequenced — the "home straight" to mature cluster modeling, filed 2026-07-08)

1. [feature/cluster/5_profiling.md](../feature/cluster/5_profiling.md) — two scripts in
   `autolens_profiling/likelihood/cluster/` that time the source-plane and
   image-plane likelihood paths, following the per-model breakdown style of
   the rest of `autolens_profiling/likelihood/`.
2. [feature/cluster/6_dpie_lenstool_parameterization.md](../feature/cluster/6_dpie_lenstool_parameterization.md)
   — LensTool-native (sigma, r_core, r_cut) dPIE parameterization + numerical
   parity validation against LensTool conventions.
3. [feature/cluster/7_scaling_relation_lenstool_convention.md](../feature/cluster/7_scaling_relation_lenstool_convention.md)
   — reparameterize the scaling tier to the LensTool/referee convention:
   reference-anchored normalization, beta fixed at 0.5 by default, r_cut scaling.
4. [feature/cluster/9_cluster_visualization.md](../feature/cluster/9_cluster_visualization.md)
   — cluster-scale visualization: per-plane critical curves/caustics, large-FoV
   defaults, aplt promotion (subsumes the deferred aplt item below).
5. [feature/cluster/10_solver_over_under_prediction.md](../feature/cluster/10_solver_over_under_prediction.md)
   — deliberate over/under-prediction handling in the point-source likelihood
   + `guides/` documentation of the choices.
6. [docs/cluster/8_lenstool_users_example.md](../docs/cluster/8_lenstool_users_example.md)
   — flagship "PyAutoLens for LensTool users" example on real data
   (candidate: SMACS J0723), reproducing a published LensTool model; depends
   on (2) and (3), exercised by (4) and (5). A real prospective user is
   available for beta-testing back-and-forth once a draft exists.

   Issue one at a time as the predecessor nears shipping
   ([[feedback_no_bulk_issue_queues]]).

__Shipped__

- 0_simulator_cluster — `cluster-simulator` (autolens_workspace#77, PyAutoLens#465, 2026-04-20)
  and v2 `cluster-simulator-jax-multiplane` (autolens_workspace#91, 2026-04-27). Built the
  small multi-plane cluster simulator (2 main lens galaxies + standalone NFW host halo + 2
  sources at z=1.0/2.0) and JAX-jitted the PointSolver. Outputs `point_datasets.csv` with a
  per-source `redshift` column as the canonical hand-editable cluster input.
- 1_visualization — `cluster-viz-prototype` (autolens_workspace_test#75, 2026-05-07). Landed
  at `autolens_workspace_test/scripts/imaging/visualization_cluster.py` (not under
  `scripts/cluster/`; the move to `scripts/cluster/visualization.py` is folded into Outstanding #2).
  Produces three reference PNGs (overlaid positions, per-source grid, cluster-tuned
  critical curves) into `autolens_workspace/dataset/cluster/simple/`. Library-side `aplt`
  promotion is deferred — see __Deferred__ below.
- 2_scaling_relation — `cluster-scaling-members` (see complete.md). Scaling-relation
  tier made the cluster default: 10 members on `b0 = 0.3 * L^1.0`, `scaling_galaxies.csv`
  CSV interface, `start_here.py` rewritten and unparked (subsumed the Deferred item).
- 3_test_workspace — `cluster-test-workspace` (items 1–4 of 8 shipped; see complete.md).
  csv_api.py, simulator.py, visualization.py move, likelihood_sanity.py (precision-floor
  finding documented; follow-up queued as #106).
- 4_likelihood_function — `cluster-likelihood-function` (see complete.md).
  ~780-line step-by-step walkthrough of source-plane and image-plane chi²,
  validated against library likelihoods exactly.
- 2_modeling_cluster — `cluster-modeling-v2` (autolens_workspace#174, PR #175, 2026-05-18).
  Full rewrite of `scripts/cluster/modeling.py` against the multi-plane simulator:
  `al.list_from_csv` for per-source redshifts, JSON centres for main lenses + host halo,
  2×`dPIEMassSph` + 1×`NFWMCRLudlowSph` host halo + 2×`Point` source galaxies, factor-graph
  `search.fit` returning `result_list`. Auto-sim guard tightened to check `data.fits`.
  Smoke 7/7 green.

__Deferred (future prompts, after Outstanding chain lands)__

- ~~`cluster/start_here.py` rewrite~~ — done, subsumed into `cluster-scaling-members`.
- Lens/source CSV API — largely subsumed by `cluster-csv-api` (family CSVs are now the
  first-class cluster API); revisit only if a residual gap surfaces.
- ~~`aplt` plotter promotion~~ — subsumed into
  [feature/cluster/9_cluster_visualization.md](../feature/cluster/9_cluster_visualization.md).
- PointSolver precision floor in cluster source-plane chi² (#106 investigation) —
  interacts with over/under-prediction penalties (see 10_solver_over_under_prediction.md).
