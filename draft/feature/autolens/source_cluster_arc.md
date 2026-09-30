# Source & Cluster arc — magnification science, PointSolver trust, cluster extended sources

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
- PyAutoArray
- PyAutoGalaxy
- autolens_workspace
- autolens_workspace_test
- autolens_profiling
- HowToLens
Themes:
- cluster
- point-source
- pixelization
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: cluster-strong-lensing
Filed: 2026-08-19 (backfilled from git)

Parent tracker for a 12-phase arc (2026-08-19 intake; deep-research grounded). This
file is never routed to start_dev directly — each phase below is its own prompt,
issued ONE AT A TIME as its predecessor nears shipping (no bulk issue queues).

Science anchors: LEGGOS II (arXiv:2606.20804 — point μ = map value at pixel; area
μ_arc = A_img/A_src with A_src = Σ A_pix,i/μ_i, Eq. 6-7; errors from ~300 posterior
draws; Fig. 4 fractional-uncertainty map with constant-μ contours; critical curve as
arc-segmentation boundary), Richard+17 (HFF magnification-map deliverables), Atek+15
(magnification as source-science tool), Jullo+08 (multi-z cluster cosmography).

## Phases (order is load-bearing)

1. `draft/bug/autolens/point_solver_error_bisect_health.md` — bisect the error-behavior
   change (prime suspect: magnification-filter Hessian buffer=self.scale → hardcoded
   0.01, Mar 2026) + health-harden. Blocks everything point/cluster.
2. `draft/research/autolens_profiling/point_solver_profiling_cells.md` — quasar /
   cluster-runtime / single-source / factor-graph profiling cells. Gate: 1.
3. `draft/refactor/autogalaxy/critical_curves_dispatch_cluster.md` — context-aware
   engine dispatch, dedupe twin plot_utils, cluster plots honor the flag. Before all
   map/segmentation phases.
4. `draft/test/workspaces/mesh_magnification_correctness.md` — areas + magnification
   recovery across every mesh variant (rectangular/delaunay/delaunay_nn/knn).
5. `draft/feature/autolens/point_magnification_api.md` — μ at a point, documented in
   source_science + point package; parity decision; multi-plane.
6. `draft/feature/autolens/area_magnification_leggos.md` — LEGGOS Eq. 6-7 pixel-
   inversion area μ as primary; ShapeSolver rehabilitate-or-retire; wiki ingest.
   Gates: 3, 5.
7. `draft/feature/autolens/magnification_errors_posterior_draws.md` — standalone
   posterior-draw errors in source_science; latent decision. Gates: 5, 6.
8. `draft/feature/autolens/magnification_maps_visualization.md` — image-plane contour
   maps, source-plane mesh maps, Fig-4 uncertainty map, pretty pass. Gates: 3-7.
9. `draft/feature/workspaces/cluster_source_science.md` — new cluster/source_science.py
   (point-source tier). Gates: 1, 3, 5-8.
10. `draft/feature/workspaces/cluster_pixelized_analysisfactor.md` — per-source-mask
    pixelized refinement via AnalysisFactor; implements the extended_source plan in
    `draft/docs/workspaces/cluster_regime_narrative.md`. Gates: 4, 9.
11. → **Cortex** `PyAutoCortex/archive/tasks/inference_programme/cluster_extended_source_inference.md`
    — JAX-gradient joint-inference feasibility verdict (go/no-go only). Moved out of the
    Mind on 2026-09-01 in the Cortex phase-4 migration (was
    `draft/research/autolens/cluster_extended_source_inference.md`). **Dropped** by human
    ruling `R-20260907-05` when `inference_programme` was retired on 2026-09-07.
    History: `PyAutoCortex/projects/inference_programme.md`; ruling:
    `PyAutoCortex/archive/rulings/2026/09/R-20260907-05.md`.
    Any future science project/task needs a fresh Cortex birth; do not revive the
    retired project implicitly. Original dependency remains phase 10.

    **Known drift, not fixed here:** two different prompts both declare `Phase: 10` under
    two different parents — `draft/feature/workspaces/cluster_pixelized_analysisfactor.md`
    (this arc's phase 10) and `draft/docs/workspaces/cluster_regime_narrative.md` (a
    different parent). Different parents, so nothing is ambiguous inside this ledger, but a
    reader searching on `Phase: 10` will hit both. Recorded, deliberately left alone.
12. `draft/docs/howtolens/cluster_pixelized_source.md` — HowToLens cluster tutorial
    pixelized source + fix the already-stale cross-reference (the stale-claim fix may
    land early if a HowToLens release precedes phase 10). Gate: 10.

## Reconciliation — 2026-09-30

- Last completed numbered phase: none found. Phases 1-10 and 12 remain drafts;
  no matching active.md row or open phase issue/PR was found. No adjacent
  DECISIONS/RESULTS file was present. Phase 11 is dropped as recorded above.
- Cross-checked open issues/PRs in PyAutoLens, PyAutoArray, PyAutoGalaxy,
  PyAutoNerves, autolens_workspace, autolens_workspace_test, autolens_profiling
  and HowToLens. Related open autolens_workspace_test#106 concerns cluster
  likelihood scripts and precision-floor sensitivity; it does not complete phase 1.
- Separately shipped evidence to reuse: PyAutoLens#710 (dataset-cap guard),
  PyAutoLens#480 (source-plane selection in magnification filtering),
  PyAutoGalaxy#591 (adaptive Richardson Hessian), PyAutoArray#584 and
  PyAutoLens#753 (merged 2026-09-27; cap now 20). Point-source CPU campaign
  records are sibling work, not completion of this arc's phase 2.
- Brain classifies the existing phase-1 umbrella as too large. Next bounded step:
  `active/point_solver_error_audit.md` (phase 1a). This is
  an audit-only workspace PR before evidence-driven library hardening; phase 1
  stays incomplete until the audit and required hardening are accepted.
- Full phase-1 repo claims conflict: PyAutoArray is claimed by
  `raw-pdip-forward-polish`; autolens_profiling by that task and
  `interferometer-decision-matrix`. Phase 1a writes only autolens_workspace_test;
  the worktree conflict guard passes for that repo. Its open #106 is related but
  targets different cluster scripts. Other repositories are read-only inputs.
- start_dev: Heart STALE (no report.json); planning may continue. Phase 1a plan approved 2026-09-30; issued as autolens_workspace_test#328
  on feature/point-solver-error-audit. No issues queued for later phases.
