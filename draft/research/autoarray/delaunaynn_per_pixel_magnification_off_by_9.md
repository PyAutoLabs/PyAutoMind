# DelaunayNN: per-pixel magnification off by ~9% on an identity lens — areas vs Sibson weights

Type: research
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: medium
Autonomy: safe
Priority: medium
Status: formalised
Consequence: judge
Witness: A results note with DelaunayNN's per-pixel and total identity-lens magnification errors before and after candidate natural-neighbour areas, direct checks of the Sibson weights, and a recommendation the human decides.
Review-minutes: 20
Unattended: ready
Epic: cluster-strong-lensing
Filed: 2026-11-02

## Original request (human, 2026-11-02)

> intake an issue to investigate the DelaunayNN

## What was found (arc phase 8b, PyAutoArray#673 / PR #674)

`Mapper.mesh_magnification` = (image-plane area mapped to each mesh pixel, from the mapping-matrix column sums) /
`mesh_geometry.areas_for_magnification`. On the identity lens of
`test_autoarray/inversion/pixelization/mesh_geometry/test_areas_for_magnification.py` (24x24 grid, 0.2" pixels,
2x2 sub-grid, jittered 12x12-equivalent mesh) the true magnification of every pixel is 1. Median |mu - 1| over
interior pixels:

| mesh | median | max |
|---|---|---|
| Delaunay | 2.9e-3 | 1.3e-2 |
| KNearestNeighbor | 1.3e-3 | 4.5e-3 |
| KNNBarycentric | 2.5e-2 | 1.1e-1 |
| **DelaunayNN** | **9.2e-2** | **2.5e-1** |

Totals are exact for every mesh (`sum(mu * area)` = mask area). Phase 4 measured the DelaunayNN *total*
magnification error as 4.3e-3 and documented it: DelaunayNN inherits the Delaunay barycentric dual areas, exact only
for the linear interpolant, an approximation for its Sibson (natural-neighbour) weights. Per pixel the mismatch is
~20x larger than the total suggests. The 8b tests pin DelaunayNN at a loose 0.2 tolerance
(`test_mesh_magnification.py`).

## Questions

1. Is it the area definition? The fix would be natural-neighbour quadrature areas: integrate each vertex's Sibson
   basis over the hull, as `MeshGeometryKNearestNeighbor` does for KNN by midpoint quadrature of the interpolator's
   own weights (PyAutoArray#665). Measure the per-pixel and total identity-lens errors with such areas.
2. Or a weight bug in the DelaunayNN interpolator (weights not summing to 1, wrong neighbours, edge handling)?
   Check partition of unity and linear precision of the weights directly.
3. Impact: source-plane magnification maps (8b), total magnification (latent `magnification`, source_science),
   and anything else that uses `areas_for_magnification` with DelaunayNN; any effect on reconstructions / evidence
   (areas do not enter the likelihood unless a regularization uses them — confirm).
4. Recommend: new areas for DelaunayNN, a weight fix, or document and leave.

<!-- formalised by the Intake (Conception) Agent on 2026-11-02 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/5fea3a9f-ac89-4fbe-8b0e-079d4785d2d8/scratchpad/delaunaynn_intake.md -->
