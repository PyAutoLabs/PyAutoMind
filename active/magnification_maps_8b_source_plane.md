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
Issued: 2026-11-02
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/673

## Context

Slice of phase 8. Per mesh pixel j: mu_j = (image-plane area mapped into pixel j: sum_i M_ij * pixel area) /
`mesh_geometry.areas_for_magnification[j]` (phase 4, all meshes). Plot via `plot_mapper(mapper, solution_vector=mu)`.
Square-pixel variant for parametric / MGE sources: ray-trace a fine image-plane grid, histogram image area per
source-plane pixel over its area. Uses the 8a colour/contour conventions. Workspace: pixelization source_science.
Witness: mesh mu map vs the forward-traced truth on a simulated lens (median per-pixel agreement stated).

## Original request (human, 2026-11-02)

> start 8b
> rtu frame should be done so autoarray free now?
> yes go ahead, create the issue

## Approved plan (2026-11-02)

1. PyAutoArray: `Mapper.mesh_magnification` — mu_j = (sum_i M_ij * image pixel area) /
   `mesh_geometry.areas_for_magnification[j]`; tests: sum(mu_j * area_j) = masked image area, no-lens identity
   mapping gives mu ~ 1 in the mesh interior, rectangular / Delaunay / KNN.
2. PyAutoGalaxy: `plot_magnification_source_plane(mapper, ...)` (log10 mu on the mesh via
   `plot_inversion_reconstruction`, 8a conventions, optional caustics) and
   `plot_magnification_source_plane_grid(mass_obj, grid, ...)` (square-pixel: ray-trace a fine image grid,
   histogram traced image area per source pixel / pixel area; constant-mu contours).
3. Witness: mesh mu map vs forward-traced square-pixel truth on a simulated lens; median per-pixel agreement stated.
4. PyAutoLens: aplt exports + Tracer tests.
5. autolens_workspace: source-plane map sections in imaging/features/pixelization/source_science.py (mesh) and
   imaging/source_science.py (square-pixel); catalogue regen; smoke.

Scope update (human, 2026-11-02: "I guess other source_science fiels which are on mesh in other packages throughout
the workspace makes sense"): mesh map in all four pixelization source_science scripts (imaging, interferometer,
multi_galaxy, group); square-pixel map in imaging/source_science.py.
