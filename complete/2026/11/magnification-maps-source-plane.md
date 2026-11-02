Arc phase 8b: source-plane magnification maps — how much the lens magnifies each region of the source, summed over
all of its images. `Mapper.mesh_magnification` (image-plane area mapped to each mesh pixel / its
`areas_for_magnification`; `data_pixel_area_for_pix_from` implemented, was a stub), plotted on the mesh by
`plot_magnification_source_plane`; `LensCalc.source_plane_magnification_from` + `plot_magnification_source_plane_grid`
for parametric/MGE sources on square pixels. Workspace: mesh map in all four pixelization source_science scripts
(human scope add), square-pixel map in imaging/source_science.py. Also fixed 8a's colour bar showing the config
brightness unit.

Shipped (merged 2026-11-02, human /prm "prm when green"):
- PyAutoArray#674 (`c012fa69`) — test_autoarray 2287 passed; identity-lens tests per mesh
- PyAutoGalaxy#691 (`1800a4eb`) — 1473 passed; SIS analytic 2 theta_E / beta within 1%
- PyAutoLens#816 (`70b317bd`) — 1020 passed
- autolens_workspace#615 (`238666e0`) — five scripts smoke clean; catalogue regenerated

Witness: mesh mu vs forward-traced square-pixel truth (true mass, simulated lens), averaged over each mesh pixel's
area: median per-pixel agreement 1.2% (RectangularBilinearAdaptDensity), 3.9% (Delaunay); median ratio 0.99.
Follow-up filed: draft/research/autoarray/delaunaynn_per_pixel_magnification_off_by_9.md (DelaunayNN 9% per-pixel on
the identity lens). Open for 8d: mesh maps use a log colour scale on mu, the others plot log10 mu values.

- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/674
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/691
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/816

## Original prompt

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
