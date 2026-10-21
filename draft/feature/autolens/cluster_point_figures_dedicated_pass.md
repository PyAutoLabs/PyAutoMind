# Cluster-scale point-source figures: dedicated pass

Consequence: judge
Autonomy: human-required
builds-on: complete/2026/10/point-solver-refinement-figure.md (PyAutoLens#788 / autolens_visualization#12) and complete/2026/10/point-dataset-positions-panel.md

@PyAutoLens @autolens_visualization

## Request (human, 2026-10-21)

> we will follow up with more dediciated work on cluster images next.

## Known issues to start from (2026-10-21)

- **Unreadable refinement panels.** The cluster `point_solver.png` panels for steps 1, 2 and final are only ▲ markers at the ~±40″ extent, and step 0 is a grey shade (369,937 triangles).
- **Label layout.** Image numbering and rejected-candidate labels at cluster scale needed a placement fix before #788 merged. The labelling has no plan for many images (>10 images → no numbers).
- **Multi-plane critical curves.** The curves ignore each point's source redshift: see `draft/bug/autolens/point_fit_critical_curves_ignore_source_redshift.md`.
- **Render cost.** The cluster producer takes about 4.5 min since the curves are computed (#786).

## Intent

Survey every cluster point-source figure (`dataset.png`, `fit.png`, `point_solver.png`, and the cluster-wide figures) with the human via /eyes. Decide the cluster-specific conventions: per-image zoom insets, labelling of many images, per-plane curves, and extent. Then run /start_dev for the agreed changes.

## Also fold in (2026-10-21)

The Fit Positions legend auto-placement for FitPositionsImagePairAll lands mid-panel over the mass centre, because of the longer "Residual (nearest, soft pairing)" label. Place it in the emptiest corner, like the source-plane panel. See `complete/2026/10/point-fit-source-plane-panel.md`.
