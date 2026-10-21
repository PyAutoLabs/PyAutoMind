# Imaging sparse inversion: unmasked mapper triplets in the reconstructed-image path and an unconditional JAX import

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: glance
Witness: a test asserting the imaging sparse `mapped_reconstructed_data_dict` equals `mapping_matrix @ reconstruction` for a mapper whose `pix_indexes_for_sub_slim_index` contains unused stencil slots (slot >= pix_sizes) and a negative index, on numpy without JAX importable (nojax leg) and under JAX
Review-minutes: 3
Unattended: ready
Filed: 2026-10-21
Issued: 2026-10-21

## Why

Side finding from PyAutoArray#639 (merged as #641, 2026-10-21). The interferometer sparse path zeroes invalid triplet slots in `_sparse_triplets_slim_from` (slot >= `pix_sizes_for_sub_slim_index`, or `cols < 0` → weight 0, column 0). The imaging sparse path does not.

## Where

- `autoarray/inversion/inversion/imaging/sparse.py` around line 526, `_mapped_reconstructed_data_dict_from`, uses `linear_obj.sparse_triplets_curvature`, built in `inversion/mappers/abstract.py:460-470` via `mapper_util.sparse_triplets_from(..., return_rows_slim=False)` with no masking. A `-1` source index silently wraps to the last source pixel and unused slots contribute if their weights are non-zero.
- The same helper, `inversion_imaging_util.mapped_reconstructed_operated_data_via_sparse_operator_from` (~line 280), imports JAX unconditionally even on the numpy path (nojax leg risk).
- The imaging data-vector and curvature paths that consume the same unmasked `Mapper.sparse_triplets_*` likely share the gap; audit them in the same PR.

## Fix

Apply the slot/negative-index masking once at the `Mapper.sparse_triplets_*` builders (or in `sparse_triplets_from` behind a flag) so every consumer is covered; make the JAX import lazy (`xp`-dispatched) in the imaging util. First establish whether any current mesh (Rectangular, Delaunay, DelaunayNN, Voronoi) actually emits negative indices or non-zero weights in unused slots; if none does, the fix is a guard plus the regression test, and the prompt notes the latent nature.
