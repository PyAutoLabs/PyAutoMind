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
