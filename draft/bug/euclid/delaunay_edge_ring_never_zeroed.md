# vis_pix Delaunay edge ring is never zeroed: `Delaunay(pixels=<appended grid length>)` double-counts `zeroed_pixels`

Type: bug
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- PyAutoArray
Themes:
- euclid
- pixelization
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 10
Unattended: ready
Epic: euclid-dr1-prep
Filed: 2026-09-05

## The finding

`scripts/initial_lens_model.py` builds the `vis_pix` source mesh as

```python
image_plane_mesh_grid = al.image_mesh.append_with_circle_edge_points(..., n_points=edge_pixels_total)  # 500 + 30
...
mesh=al.mesh.Delaunay(pixels=image_plane_mesh_grid.shape[0], zeroed_pixels=edge_pixels_total)
```

`autoarray.inversion.mesh.mesh.delaunay.Delaunay.__init__` does `pixels = int(pixels) + zeroed_pixels`
and documents `pixels` as "the number of **active** mesh vertices". Passing the *appended* grid
length (530) therefore gives `mesh.pixels = 560` while the grid has 530 points, and the
`zeroed_pixels` property returns indices `530..559` — past the end of the mesh — so the
30-point edge ring the script says it is holding at zero is in fact solved for like any other
vertex. The docstring in the script ("`zeroed_pixels=edge_pixels_total` on the `Delaunay`
mesh below tells the inversion to hold their reconstructed values at zero") describes an
intent the code does not implement.

Measured 2026-09-05 (PyAutoLens#726 workspace leg, euclid PR #51): on the
`dataset/simulated/euclid_dr1_like` scene with a 150 + 30 point mesh, every latent is
bit-identical with `pixels=grid.shape[0]` and with `pixels=grid.shape[0] - edge_pixels_total`,
so the effect on the flux latents is nil there; whether it is nil on real tiles, where the
ring sits at the mask edge, is not established.

## What to do

1. Confirm the semantics against autoarray `main` (the `Delaunay` constructor and the mapper
   that consumes `mesh.pixels`), and whether a `pixels`/grid-length mismatch is silently
   tolerated or masked downstream.
2. Fix the script to `pixels=image_plane_mesh_grid.shape[0] - edge_pixels_total` (or whatever
   the constructor actually expects), with a unit test in `tests/` that the mesh's
   `zeroed_pixels` indices lie inside the grid and address the appended ring.
3. Check `scripts/full_model.py` and any other Delaunay stage for the same construction.
4. If the reconstruction changes on a real tile, say so on the euclid-dr1-prep epic — it
   touches Cortex phase 4's numerics witness.

## Provenance

Found by the PyAutoLens#726 workspace subagent while mirroring the `vis_pix` construction
in `tests/test_compute_latent_variable.py`; recorded on PyAutoLens#726 and euclid PR #51.
