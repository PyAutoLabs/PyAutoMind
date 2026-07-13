## cluster-visualization
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/577 (closed)
- completed: 2026-07-09
- prs: PyAutoLens#578 + autolens_workspace_test#152 (both merged)
- notes: autolens/cluster/plot/ package (weak/plot pattern) re-exported into aplt:
  plot_positions_overlay, plot_image_group_zooms, plot_critical_curves, plot_caustics,
  subplot_cluster_dataset. Headline: per-source-plane critical curves/caustics for multi-plane
  tracers via LensCalc(use_multi_plane=True, plane_j=j) — each source redshift has its own curve
  set. Integration script (rewritten prototype) validates the physics: z=1 plane 3 tangential
  curves outermost 13.35", z=2 one at 22.53" (radius grows with source redshift). Numpy-path only
  (contour solvers not vmap-safe; grid guidance in docstrings). Subsumed the tracker's deferred
  aplt-promotion item. Follow-up candidates noted on the issue: caustic × source-position overlay,
  Include2D-level integration after the flagship example exercises the API on real data.
