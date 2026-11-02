# Magnification maps 8b: source-plane magnification per mesh pixel

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace
Themes:
- visualization
- cluster
Epic: cluster-strong-lensing
Phase: 8b
Parent: draft/feature/autolens/magnification_maps_visualization.md
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: no
Filed: 2026-11-02

## Context

Slice of phase 8. Per mesh pixel j: mu_j = (image-plane area mapped into pixel j: sum_i M_ij * pixel area) /
`mesh_geometry.areas_for_magnification[j]` (phase 4, all meshes). Plot via `plot_mapper(mapper, solution_vector=mu)`.
Square-pixel variant for parametric / MGE sources: ray-trace a fine image-plane grid, histogram image area per
source-plane pixel over its area. Uses the 8a colour/contour conventions. Workspace: pixelization source_science.
Witness: mesh mu map vs the forward-traced truth on a simulated lens (median per-pixel agreement stated).
