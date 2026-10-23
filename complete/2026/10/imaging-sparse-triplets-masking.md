## imaging-sparse-triplets-masking
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/643
- completed: 2026-10-21
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/649 (merge 33435592)
- summary: |
    Side finding of #639/#641. Three commits 9b52fac5, 3e53e0aa, dd268224 on
    `feature/imaging-sparse-triplets-masking`: `mapper_util.sparse_triplets_from(pix_sizes_for_sub=)`
    masks invalid stencil entries (slot >= pix_sizes or cols < 0) on numpy and JAX; `Mapper.sparse_triplets_data`
    / `sparse_triplets_curvature` pass it; interferometer `_sparse_triplets_slim_from` uses the shared masking
    (local block removed; 24 arrays identical before/after); the two imaging scatter-add helpers dispatch on xp
    (numpy bincount, JAX segment_sum, JAX imported only on that branch); four imaging call sites pass xp.
    Defect confirmed LATENT: Delaunay/DelaunayNN unused slots hold -1 with weight exactly 0; rectangular/KNN
    emit none. Masking is a prerequisite for the numpy bincount branch (raises on -1). Worktree: inversion
    1037 passed / 4 xfailed; dataset/imaging 36 passed; nojax emulation 23 passed / 10 skipped. CI 3 legs green.
- witness: |
    MET — mapper_util test zeroes a -1 index and an unused non-zero-weight slot on numpy and JAX; imaging sparse
    data_vector / curvature / mapped reconstruction match the dense mapping inversion on such a mapper (numpy +
    JAX backends); subprocess no-JAX test covers the triplets and both helpers. Narrower than filed: the full
    InversionImagingSparse still needs JAX (operator + curvature methods import it unconditionally) — follow-up.
- heart-ack: "YELLOW acknowledged by human 2026-10-21 — manifest drift (1 mismatch); release validation stale: source moved since rehearsal (PyAutoArray)"
- follow-ups: RESOLVED 2026-10-21 as no-change — `ImagingSparseOperator` is the JAX implementation by design (lax.fori_loop / dynamic_update_slice FFT batches; `Imaging.apply_sparse_operator` docstring says so) and the NumPy/CPU alternative is the separately named `apply_sparse_operator_cpu` → `SparseLinAlgImagingNumba` / `InversionImagingSparseNumba`; the #649 numpy branches in the two helpers are the only numpy-reachable code. No prompt filed. interferometer _sparse_triplets_curvature_from left unmasked (util drops out-of-range columns).

## Original prompt

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
