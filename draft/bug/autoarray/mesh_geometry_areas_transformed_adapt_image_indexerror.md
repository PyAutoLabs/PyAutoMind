# MeshGeometryRectangular.areas_transformed raises IndexError for adapt-image meshes

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: easy
Autonomy: safe
Priority: low
Status: formalised
Filed: 2026-09-17

Found during the independent sanity check of PyAutoArray#556 (issue #552;
record `complete/2026/09/mixed-precision-inversion-gap.md`).

`MeshGeometryRectangular.areas_transformed`
(`autoarray/inversion/mesh/mesh_geometry/rectangular.py`) raises `IndexError`
for a `RectangularBilinearAdaptImage` mesh: it hands
`adaptive_rectangular_areas_from` the over-sampled data grid
(`data_grid.over_sampled`, 5056 points on the 316-pixel
`autogalaxy_workspace_test` smoke data) together with the 316-long
`mesh_weight_map`, so the weighted rank-CDF transform indexes the weight map
out of range. The sibling `edges_transformed` uses `data_grid.array` (316
points) and works; the areas it implies are what
`adaptive_rectangular_areas_from` intends. The failure is identical before and
after #556, so it is not a regression of that fix — nothing in the fit path
calls `areas_transformed` (it is a diagnostic/plotting property), which is why
no smoke script or unit test caught it.

Ask: make `areas_transformed` use the same `data_grid` as `edges_transformed`
(or the same convention the interpolator uses for the weight map), add a unit
test that calls both properties on an adapt-image rectangular mapper and
checks the areas equal the outer product of the edge spacings, and check
whether `MeshGeometryRectangular` has other properties with the same
over-sampled-vs-slim mismatch.

Reproducer: build the mapper as in
`autogalaxy_workspace_test/scripts/imaging/jax_likelihood/rectangular.py`
(NumPy backend) and read `fit.inversion.linear_obj_list[0].mesh_geometry.areas_transformed`
(the exact attribute path is the mapper's mesh geometry object; confirm at
start).
