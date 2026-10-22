# Cluster point_solver.png: readable refinement panels and many-image labels

Consequence: judge
Autonomy: human-required
builds-on: complete/2026/10/cluster-point-figures.md (PyAutoLens#794), complete/2026/10/point-solver-refinement-figure.md (PyAutoLens#788)

@PyAutoLens @autolens_visualization

## Context

This is carried over from the cluster point-figures pass. It was listed under "Known issues" there but was not part of the final approved v4 design, so it did not ship in #794.

## Known issues

- **Refinement panels.** On the cluster `point_solver.png`, refinement steps 1, 2 and final show only ▲ markers at the ~±40″ extent, and step 0 is a grey shade (369,937 triangles). Consider per-image zoom insets or a per-step adaptive extent.
- **Labelling.** The solver figure has no labelling plan for many images (>10 images → no numbers). Align it with the `k·i` labels the #794 figures now use.

## Intent

Survey the cluster `point_solver.png` with the human via /eyes, agree on the conventions, then run /start_dev.
