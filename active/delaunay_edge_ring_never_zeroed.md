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
Issued: 2026-09-05
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/526

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

## History (2026-09-05 audit)

The human remembered finding this before and fixing it. The record says the semantics were
set once, in PyAutoArray, and the workspace never uniformly followed them:

- **PyAutoArray 2119d6b (2026-02-24)** gave `Delaunay.__init__` its `pixels`/`zeroed_pixels`
  arguments with `pixels = int(pixels) + zeroed_pixels`; **446e5bc (2026-02-25)** turned the
  zeroed ids positive (`pixels - n .. pixels - 1`) with the docstring example
  `pixels = 780, zeroed_pixels = 30 -> 750..779`. That is the whole library history: the
  semantics never changed after February.
- **autolens_workspace** has carried *both* call forms since its fresh-start commit
  f1a9203b (2026-04-03). `scripts/group/slam.py` (62df6ce9, 2026-04-05) and the group SLaM
  variants (2026-04-14) use the correct `pixels=hilbert_pixels, zeroed_pixels=edge_pixels_total`
  — that is the "fix" — while `imaging/features/pixelization/delaunay.py` and
  `interferometer/features/pixelization/delaunay.py` use `pixels=image_plane_mesh_grid.shape[0]`
  from the same initial commit. Every later script was copied from the feature scripts, not
  from SLaM: `group/features/pixelization/*` (b2b70f32, 2026-05-01), `interferometer/features/datacube/delaunay.py`
  (2026-05-05, #123), `multi_galaxy/features/pixelization/delaunay.py` (7fd11daa, 2026-07-31).
  No commit in any repo ever wrote `shape[0] - edge_pixels_total`. Today: 20 sites of the
  wrong form vs 6 of the right form in `scripts/` (14 vs 6 in the notebooks).
- **euclid_strong_lens_modeling_pipeline** inherited the wrong form at every Delaunay site:
  `initial_lens_model.py` (f203f6e7, 2026-07-16), both sites in `full_model.py` (db09e3b8,
  2026-08-29 port from Science/euclid), `hpc/diagnostics/jax_fork_control.py` (5e6a16e0,
  2026-09-02). **autolens_workspace_developer** `jax_profiling/*/delaunay.py` too
  (`n_mesh_vertices = image_plane_mesh_grid.shape[0]`).
- **The library's own tests do not respect `pixels` either**: PyAutoLens
  `test_simulate_and_fit_imaging.py` builds `Delaunay(pixels=25, zeroed_pixels=5)` over an
  `Overlay(shape=(7, 7))` grid whose length is unrelated to 25.

**Why the fix was never noticed to be missing — the over-count is self-cancelling for one
mapper.** `Mapper.params` is `source_plane_mesh_grid.shape[0]` (the grid length), not
`mesh.pixels`; the *only* consumer of `mesh.pixels` is `AbstractInversion.zeroed_ids_to_keep`,
which offsets each mapper's local ids by `n_total - sum(mesh.pixels)`. With one mapper that is
`n_total - (N + 2r) + (N + r .. N + 2r - 1) = n_total - r .. n_total - 1` — the last `r`
parameters, i.e. the appended ring, whatever `pixels` was. So the ring **is** zeroed in every
single-source script above, and the bit-identical latents measured on euclid PR #51 are the
expected result, not evidence that zeroing is inert. Verified with a mock inversion against
autoarray `main` (2026-09-05, `de92d09`): 1 mapper, with and without linear light profiles
ahead of the mesh block — ring zeroed under both forms; 2 mappers with the wrong form — the
*first* mapper's ids land `r` too low, zeroing `r` interior vertices and leaving its ring
live, the last mapper is always right.

So the prompt's headline ("solved for like any other vertex") holds only for inversions
with two or more pixelized mappers, or for any future consumer that trusts `mesh.pixels`
(the shelved `jax_visualization_inversion_blowup.md` already records one: a Delaunay fit
reloaded from `tracer.json` crashes because the stored `zeroed_pixels` array is re-added to
`pixels`). Steps 2–3 above stand as hygiene across all four repos; step 4's Cortex note is
moot for `initial_lens_model.py` (one mapper). Consider a fifth step: have
`Delaunay.__init__`/the mapper assert `mesh.pixels == source_plane_mesh_grid.shape[0]` so the
mismatch cannot be silent again.

**The test workspaces are where the fix actually lives.** `autolens_workspace_test` and
`autogalaxy_workspace_test` use the correct form almost everywhere — `pixels = 750` (or 300 /
400 / 500) feeds both `Hilbert(pixels=pixels)` and `Delaunay(pixels=pixels,
zeroed_pixels=edge_pixels_total)`, and the scripts keep a separate
`total_mapper_pixels = image_plane_mesh_grid.shape[0]` for the grid length, so the distinction
was understood there: every `jax_likelihood/`, `jax_grad/`, `datacube/` and
`modeling_visualization_delaunay_jit.py` site, from the 2026-04-03 fresh start through the
2026-07-26 `jax_grad` certifications. The one wrong-form site is
`multi_dataset/dataset_model_parity_delaunay.py` (ef250b7a, 2026-05-15, #97):
`pixels=OVERLAY_SHAPE[0] * OVERLAY_SHAPE[1] + EDGE_PIXELS`. Those parity and certification runs
all went through green because they are single-mapper: the two forms give bit-identical
inversions there, so no parity, JIT-equality or FD-gradient test *could* have caught the
feature-script form — and none asserts on `mesh.pixels` or the `zeroed_pixels` indices, which
is the assertion the fifth step above would add. `autogalaxy_workspace` proper has no Delaunay
site at all.
