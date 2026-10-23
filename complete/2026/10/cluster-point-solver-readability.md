
## Outcome
Cluster-scale `point_solver.png` is now readable (PyAutoLens#795). Each panel spans its source's own images and rejected candidates, with round ticks. When the solver's step-0 triangles are too small to draw, the figure re-solves on a coarse display grid of pixel scale min(span/10, closest separation/1.6). It uses that grid only if it recovers the real solve's images, and otherwise draws the solver's own steps. Rejected candidates are labelled r1, r2, and own-plane critical curves come via `curves_for_planes` in the #794 style. The modelling solver is unchanged.

- PyAutoLens#796: merged 2026-10-22, pending release. test_autolens: 936 passed, 1 xfailed.
- autolens_visualization#15: re-render of the cluster and point_source figures. Cluster point_1 uses the approved coarse look; point_0 stays fine-grained because of its 0.39″ image pair.
- Shipped under Heart YELLOW (manifest drift, stale PyAutoArray rehearsal), acknowledged by the human.

## Follow-ups
- Unverified: a starting grid coarser than ~0.37″ appears to lose point_0 image 3, which sits 0.39″ from a member core. The workspace cluster example's 1.0″ modelling grid may therefore miss it in validation. This belongs to the cluster-PointSolver robust-settings campaign in autolens_profiling, not this task.
- Dispatch the Eyes dashboard_refresh.yml so the board shows the new figures.

## Original prompt

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
