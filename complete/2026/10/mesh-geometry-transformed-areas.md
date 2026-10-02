# mesh-geometry-transformed-areas

Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/605
Date: 2026-10-02

## Shipped
Derived transformed cell areas from geometry edges, preserving guard cells and supporting adapt-image slim weights. Full1919passed, focused34passed, smoke2passed; conflict-resolution smoke passed5.3s.

- https://github.com/PyAutoLabs/PyAutoArray/pull/608
- https://github.com/PyAutoLabs/autolens_workspace_test/pull/339

- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/608

Human authorized linked PRs, development shipping with exact Heart YELLOW acknowledgment, then merge and full close-out. Every head run and matrix leg was checked; merge receipts are recorded by GitHub. No release performed. Shared bundle worktree cleanup follows all four members; logs and data preserved under organs/PyAutoMind/tmp/autoarray-bundle-1-closeout/.

For workspace conflict updates, the human explicitly acknowledged generated organism-map and public front-door table drift (one mismatch each); stale release rehearsal evidence remained disclosed. Only smoke manifest entries were reconciled; scripts unchanged.

Final workspace head c7ac7f3747717d67c06eefb528317c4a1130624d passed every job in run37003384830, including Python3.12/3.13. Workspace merge87fd033242e4f33cfa435965d627717b86803675. Both conflicts resolved by preserving the union of smoke registrations; scripts unchanged.

Backlog reconciliation retained four resemblance-only suspects; no sibling was proven complete. Recheck `/intake reconcile draft/bug/autoarray` (non_uniform_over_sample_jax_compile_cost, rectangular_mapper_bilinear_row_weights, sparse_terms_nufft_origin_and_mask_compatibility) and `/intake reconcile draft/feature/autoarray` (source_clumps_robust_scale).

## Original prompt

# MeshGeometryRectangular.areas_transformed raises IndexError for adapt-image meshes

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: easy
Autonomy: safe
Priority: low
Status: formalised
Issued: 2026-10-02
Consequence: glance
Witness: `areas_transformed` and `edges_transformed` on a `RectangularBilinearAdaptImage` mapper both return, the areas equal the outer product of the edge spacings (unit test), and under `xp=jnp` `edges_transformed` either returns the raw array or is documented NumPy-only.
Review-minutes: 3
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
over-sampled-vs-slim mismatch. Related, found in the same check:
`edges_transformed` raises under the JAX backend because it returns a
`Grid2DIrregular`, which is not a valid JAX type — decide whether it should
return the raw array under `xp=jnp` (the `if xp is np:` guard pattern of
`docs/agents/jax_and_decorators.md`) or be documented NumPy-only.

Reproducer: build the mapper as in
`autogalaxy_workspace_test/scripts/imaging/jax_likelihood/rectangular.py`
(NumPy backend) and read `fit.inversion.linear_obj_list[0].mesh_geometry.areas_transformed`
(the exact attribute path is the mapper's mesh geometry object; confirm at
start).
