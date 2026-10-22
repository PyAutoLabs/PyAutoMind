# Cluster point_solver.png: readable refinement panels and many-image labels

Consequence: judge
Autonomy: human-required
Issued: 2026-10-22
builds-on: complete/2026/10/cluster-point-figures.md (PyAutoLens#794), complete/2026/10/point-solver-refinement-figure.md (PyAutoLens#788)

@PyAutoLens @autolens_visualization

## Context

This is carried over from the cluster point-figures pass. It was listed under "Known issues" there but was not part of the final approved v4 design, so it did not ship in #794.

## Known issues

- **Refinement panels.** On the cluster `point_solver.png`, refinement steps 1, 2 and final show only ▲ markers at the ~±40″ extent, and step 0 is a grey shade (369,937 triangles). Consider per-image zoom insets or a per-step adaptive extent.
- **Labelling.** The solver figure has no labelling plan for many images (>10 images → no numbers). Align it with the `k·i` labels the #794 figures now use.

## Intent

Survey the cluster `point_solver.png` with the human via /eyes, agree on the conventions, then run /start_dev.

## Human decisions (2026-10-22)

- Variants A (adaptive zoom), B (image × step grid) and per-image variant F: all REJECTED.
- APPROVED design: `round3/cluster_point_1.png` in scratch `eyes/autolens/cluster_point_solver_prototype/`. This is variant F per SOURCE: all of a source's images in one 2×2 (Step 0/1/2/final), with one span across the panels and a coarse display grid. r1/r2 labels are liked.
- Ticks should look like the other figures.
- The modelling solver grid is out of scope. More extensive PointSolver setup tests are their own thing (the robust-settings campaign).
