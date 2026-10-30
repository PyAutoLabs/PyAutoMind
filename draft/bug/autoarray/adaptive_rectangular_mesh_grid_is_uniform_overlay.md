# Adaptive rectangular meshes report a uniform overlay as their source-plane node positions

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Epic: cluster-strong-lensing
Phase: 4e (blocker)
Arc: draft/feature/autolens/source_cluster_arc.md
Difficulty: medium
Autonomy: supervised
Priority: high
Consequence: judge
Filed: 2026-10-30
Witness: for every adaptive rectangular mesh, `mapper.source_plane_mesh_grid` equals the source-plane positions at which the mapper's interpolant takes each reconstruction value (node i's basis function peaks there); `griddata` of the reconstruction on those positions integrates to `sum(reconstruction * areas_for_magnification)` within a few percent; the reconstruction CSV writes those positions; RectangularUniform and Delaunay-family output is unchanged.

## Original request (human, 2026-10-30)

> Library fix first (Recommended) — Park this PR. File and fix a PyAutoArray bug so source_plane_mesh_grid (or a
> new attribute) gives the adapted node centres, then come back and finish this workspace PR on top of it,
> library-first. The whole script then gives right answers.

## Finding (autolens_workspace#605 comment, 2026-10-30)

Every adaptive rectangular mesh (`RectangularBilinearAdaptDensity`, `RectangularBilinearAdaptImage`,
`RectangularRTUAdaptDensity`, `RectangularRTUAdaptImage`) builds its interpolator with
`mesh_grid=overlay_grid_from(shape, relocated_grid.over_sampled)`
(`autoarray/inversion/mesh/mesh/rectangular_rtu_adapt_density.py` ~L273): a **uniform** grid over the traced
data's bounding box. The mapper's interpolant instead places reconstruction value `(row r, col c)` at unit-CDF
node `U_y = (n_y - r - 1)/(n_y - 3)`, `U_x = (c - 1)/(n_x - 3)` (guard ring at the border), mapped back to the
source plane through the inverse adaptive CDF (`adaptive_rectangular_transformed_grid_from`). So
`mapper.source_plane_mesh_grid` (= `interpolator.mesh_grid`) is not where the values live.

Measured on autolens_workspace `imaging/simple__no_lens_light` (true tracer, 28×28 BilinearAdaptDensity,
coefficient 1.0, extra galaxy noise-scaled): reported node spacing is uniformly 0.11″ (data span / 28); the
library's own `areas_for_magnification` at the brightest nodes is 0.0013 arcsec² against 0.0097 implied by the
reported positions; correlation between the areas and the Delaunay dual of the reported positions is 0.13.
`griddata` of the reconstruction on the reported positions integrates ~4.6× too high, so the workspace
interpolation-route magnification is 6.9 against a mesh-route 31.6 and a truth of 34.9, at any interpolation
resolution.

## Blast radius

- `autoarray/inversion/plot/inversion_plots.py` ~L510: `source_plane_reconstruction_{i}.csv` (a documented science
  product) writes `y, x` from `mapper.source_plane_mesh_grid`, so its coordinates are wrong for adaptive meshes.
- Every workspace `source_science.py` / CSV-loading example that interpolates with `griddata` on those positions
  (interpolated source, zoom, errors, S/N masking, interpolation-route magnification), plus anything downstream
  that reads the CSV.
- Plots are fine: `autoarray/plot/inversion.py` uses `mesh_geometry.edges_transformed`.
- Check before changing `interpolator.mesh_grid` itself: the rectangular interpolator passes it to its mesh geometry
  (`interpolator/rectangular.py` ~L759), and preloads / `to_inversion` code paths touch `source_plane_mesh_grid`.
  A separate attribute that the mapper and the CSV writer use may be the safer shape — decide in the plan.

## Work

1. Decide the API: make `mapper.source_plane_mesh_grid` return the adapted node centres for adaptive rectangular
   meshes, or add a node-centre attribute on the rectangular mesh geometry and route the mapper property and the
   CSV writer through it. Guard-ring nodes: state where they sit (clamped to the data span) and say so in the
   docstring.
2. Unit tests: node centres equal the positions where each node's basis weight is 1 (map a grid at the centres
   through the mapper and check the weight matrix is ~identity on interior nodes); the griddata integral check in
   the Witness; RectangularUniform unchanged.
3. Fix the CSV writer if it does not pick the change up automatically; note the coordinate change in the PR body
   (CSV contents change for adaptive meshes).
4. Re-run autolens_workspace_test `scripts/imaging/mesh_magnification.py` (areas untouched; it must stay green).
5. Then resume `pixelization-mesh-mag-docs` (autolens_workspace#605, branch `feature/pixelization-mesh-mag-docs`,
   WIP commit 7c30f74f): scale out the extra galaxy, interferometer coefficient, print the truth beside both routes,
   honest accuracy wording.
