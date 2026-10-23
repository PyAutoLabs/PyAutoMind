## sparse-mapped-reconstructed-image
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/639
- completed: 2026-10-21
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/641 (merge 7ecc6ef3)
- community: https://github.com/PyAutoLabs/.github/discussions/40 (@HRSAstro) — contributor update owed at merge (draft approved in chat) and again at release
- summary: |
    Community proposal (hub #40, @HRSAstro): after 2026.10.18.1 made the sparse interferometer
    `data_vector` sparse, the inherited `mapped_reconstructed_data_dict` still built the dense
    image-pixels × mesh-pixels mapping matrix L for fit outputs (2.7 GB on a 384² unmasked grid
    with a 48² mesh). One commit 422f60a9 on `feature/sparse-mapped-reconstructed-image`:
    `InversionInterferometerSparse.mapped_reconstructed_data_dict` override + helper
    `_mapped_reconstructed_data_mapper_from` (scatter-add of `vals * s[cols]` over the slim
    triplets from `_sparse_triplets_slim_from`; numpy `bincount`, JAX `.at[rows].add`);
    linear-function objects keep the dense product; the numba subclass inherits it;
    `mapped_reconstructed_operated_data_dict` unchanged. Tests: sparse-vs-dense parity on
    numpy (1e-10) and under `jax.jit` (1e-12) for Rectangular, Delaunay, sub_size 2, two
    mappers, mapper + linear funcs in both orders. Worktree runs: inversion + dataset
    interferometer suites 1052 passed / 4 xfailed; PyAutoGalaxy interferometer 77 passed.
    CI: unittest 3.12, 3.13, nojax all green; mergeStateStatus CLEAN; not frozen.
- witness: |
    MET — the parity tests asserting the sparse `mapped_reconstructed_data_dict` equals the
    dense `mapping_matrix @ reconstruction` on numpy and under jit, Rectangular and Delaunay,
    sub-size > 1, two mappers and mapper-plus-linear-functions, ran green in all three CI legs.
- heart-ack: "YELLOW acknowledged by human 2026-10-21 — manifest drift (1 mismatch); test run status unknown; release validation incomplete (no rehearsal)"
- side-finding: imaging `inversion/imaging/sparse.py` `_mapped_reconstructed_data_dict_from` uses unmasked `Mapper.sparse_triplets_curvature` (no slot/negative-index zeroing) and `inversion_imaging_util.mapped_reconstructed_operated_data_via_sparse_operator_from` imports JAX unconditionally — follow-up issue to file.
- follow-ups: interferometer-primary-beam (#640, planned.md, now unblocked) → matrix-free phase 1 (draft, #638 parent); contributor replies on hub #40 at release.

## Original prompt

# Sparse mapped reconstructed image on the interferometer sparse inversion path…

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
- autolens_profiling
Difficulty: medium
Autonomy: safe
Priority: high
Issued: 2026-10-21
Memory: reading-queue.md; wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/cosmos-survey.md
Status: formalised
Consequence: glance
Witness: a test asserting the sparse `mapped_reconstructed_data_dict` equals the dense `mapping_matrix @ reconstruction` result to 1e-10 on numpy and under JAX jit, for Rectangular and Delaunay meshes, sub-size > 1, two mappers and mapper-plus-linear-functions
Review-minutes: 3
Unattended: ready

# Sparse mapped reconstructed image on the interferometer sparse inversion path (never build the dense mapping matrix L)

Community proposal accepted 2026-10-21: https://github.com/PyAutoLabs/.github/discussions/40 (@HRSAstro, Ideas & Proposals, 2026-10-20). user-facing: send the contributor an update when the fix merges and when it is released. Note the discussion body is truncated at its code block, so the proposer's own replacement is unknown; we are implementing our own.

## Problem

After 2026.10.18.1 made `InversionInterferometerSparse.data_vector` sparse (`_data_vector_mapper_from`, segment-sum), the inherited `AbstractInversionInterferometer.mapped_reconstructed_data_dict` (`autoarray/inversion/inversion/interferometer/abstract.py:179-180`) still calls `mapped_reconstructed_data_via_mapping_matrix_from(mapping_matrix=linear_obj.mapping_matrix, ...)`, which builds the dense (image pixels × mesh pixels) matrix L via the cached `Mapper.mapping_matrix`. Sampling does not hit it (log_evidence uses `fast_chi_squared`), but it is built for model visibilities (`sparse.py:555` `mapped_reconstructed_operated_data_dict`), galaxy image dicts (`autogalaxy/abstract_fit.py:186`), `model_image_natural` (`autogalaxy/interferometer/fit_interferometer.py:626`) and the array-free `sparse_chi_squared_from` (`fit_interferometer.py:298`), so fit outputs, visualization and array-free log_likelihood pay the n_image × n_mesh memory.

## Fix

Override `mapped_reconstructed_data_dict` in `InversionInterferometerSparse` (and check the numba sibling) as the mirror of `_data_vector_mapper_from` (`sparse.py:174-196`): rows, cols, vals from `_sparse_triplets_slim_from(mapper)` (which already zeroes invalid slots); contrib = vals * reconstruction[cols]; image = bincount(rows, contrib, minlength=n_pixels) on numpy, `.at[rows].add` / `jax.ops.segment_sum(num_segments=n)` under JAX. Non-mapper linear objects keep `mapping_matrix @ reconstruction`. Do not reuse the imaging helper (`imaging/inversion_imaging_util.py:280`): it imports JAX unconditionally and takes raw triplets without the negative-index masking (check `imaging/sparse.py:526` for the same latent bug as a side finding).

## Scope notes

- Mixed precision: dense L is fp32 under JAX while this path runs fp64 (same note as #630); expect ~1e-12 agreement, not bit-identity.
- `mapper.mapping_matrix` remains lazily available for plotting; `mapped_to_source_from` and image regions are numpy-only follow-ups.
- Record memory before/after on one large real_space_mask in autolens_profiling if cheap.

<!-- formalised by the Intake (Conception) Agent on 2026-10-21 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/16b1291e-5d7e-43ae-8250-0eea830cc6ed/scratchpad/intake40.md -->
