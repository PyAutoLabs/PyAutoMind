# PointSolver profiling cells: lensed quasar → cluster runtime tier →

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- point-source
- profiling
- cluster
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: ready
Epic: cluster-strong-lensing
Phase: 2
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-08-19 (backfilled from git)

# PointSolver profiling cells: lensed quasar → cluster runtime tier → single/multi-source → multiplane

Part of the Source & Cluster arc (phase 2 of 12), gated on phase 1 (PointSolver health
verdict). User request (verbatim): "Once satisfied extend to profiling examples in
autolens_profiling but simple lensed quasar, cluster scale with single source, then
cluster with multiple source redshifts and finally cluster with multiplane ray tracing."

Survey findings (2026-08-19) — what exists vs what the four cells need:

- Cluster multi-redshift/multiplane is ALREADY covered by
  `scripts/cluster/likelihood_breakdown/{image_plane,source_plane}.py` (2 sources at
  z=1.0/2.0, multi-plane). The real gap is the **`cluster/likelihood_runtime/` tier** —
  cluster has breakdown/ and searches/ but no runtime tier, so cluster cells never appear
  in the sweep-driver runtime dashboard.
- **Lensed quasar**: no named cell; closest is `point_source/likelihood_runtime/
  image_plane.py` (generic isothermal + 1 point source). No flux (`al.FitFluxes`) or
  time-delay profiling cell exists at all — a quasar cell should include fluxes.
- **Cluster single source**: `scripts/misc/simulators/cluster.py` is hardwired to 2
  sources at 2 redshifts (source_redshifts=[1.0, 2.0] at :144-145) — needs a
  single-source preset.
- `point_source/` has no `likelihood_breakdown/` tier (imaging/interferometer/cluster
  all have one).
- `multi_dataset/` has no factor-graph/AnalysisFactor profiling cell — that is what a
  multi-source cluster fit actually costs; add one in the cluster runtime tier.

Follow the repo's taxonomy (`scripts/<dataset>/<task>/<model>.py`, canonical script shape
per `point_source/likelihood_runtime/image_plane.py`: smoke early-exit, Timer,
eager/JIT/vmap tiers, pinned-likelihood drift record). Trap on record: per-source
`plane_redshift` MUST be passed to `solve` — it defaults to the tracer's final plane
(#678 phase B); the cluster simulator's `jitted_solve_for(plane_redshift)` closure at
cluster.py:339 is the template.

Deliverable: 4 cells (quasar w/ fluxes; cluster single-source runtime; cluster
multi-source multi-z runtime incl. factor-graph; multiplane already-covered check +
runtime promotion), results in the standard results/runtime dashboard.

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/483da28c-8c96-4c83-ad87-a43448ca2164/scratchpad/source_cluster_phases/phase02_point_solver_profiling_cells.md -->
