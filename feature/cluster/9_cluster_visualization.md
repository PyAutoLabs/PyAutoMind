# Cluster-scale visualization: multi-plane critical curves/caustics, large-FoV plots, aplt promotion

Type: feature
Target: cluster
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Dedicated cluster-scale visualization: large-field plots, all critical curves and caustics, promoted into the library aplt interfaces.

Cluster-scale lenses need visualization that is qualitatively different from the galaxy-scale plots
in place: fields of view are arcminutes not arcseconds, there are tens of mass components, multiple
source planes each with their own critical curves and caustics, and multiple-image families that need
per-source identification at a glance.

A prototype already exists — `autolens_workspace_test/scripts/cluster/visualization.py` (moved from
scripts/imaging/visualization_cluster.py) produces overlaid positions, per-source grids and
cluster-tuned critical curves — and z_features/cluster_lensing.md has a deferred "aplt plotter
promotion" item this prompt subsumes. Promote and extend into first-class library support:

- **All critical curves / caustics**: for a multi-plane tracer, compute and plot the tangential and
  radial critical curves for every source-plane redshift (they differ per plane), and the
  corresponding caustics in each source plane, with per-plane colouring and a legend. Current
  galaxy-scale defaults assume one source plane.
- **Large-image handling**: sensible defaults for arcminute-scale FoVs — critical-curve resolution
  (the marching grid must be fine enough to resolve member-galaxy-scale features without an
  intractable grid), position markers sized for the FoV, and zoom-grid subplots per multiple-image
  family.
- **Per-source colouring** of observed vs model-predicted positions, matched by pairing, so
  over/under-prediction is visible immediately.
- Promote via the standard `aplt` / `Visuals2D` / `Include2D` interfaces (e.g. Include2D flags for
  per-plane critical curves; a `TracerPlotter`/point-fit subplot tuned for clusters), so the cluster
  workspace scripts and the flagship LensTool example get these plots without bespoke matplotlib.
- Watch JAX interplay: critical-curve computation on big grids has known pitfalls
  (ZeroSolver vmap incompatibility; use the jit-friendly path where relevant) — numpy-path-only is
  acceptable for visualization, stated explicitly.

Scope is library (PyAutoLens/PyAutoGalaxy aplt) + workspace (cluster scripts consume the new
plotters; update visualization script). The flagship LensTool example and real-user beta testing
will exercise these plots, so this should land before or alongside that example.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/fa55f70e-2cea-4887-bf12-61f81cff042f/scratchpad/p4_cluster_visualization.md -->
