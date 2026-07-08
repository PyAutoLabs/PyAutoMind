# Oversampled PSF convolution — phase 2b: inversion wiring

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft

Phase 2b of the oversampled-PSF feature — issue this only when phase 2a
(`oversampling_phase_2a_convolver_dataset.md`) nears shipping; it builds on
the 2a Convolver API. Implements design note §4
(`feature/autoarray/oversampling_design.md`, approved on
PyAutoLabs/PyAutoArray#353) verbatim.

## Scope (design note §4)

1. `Mapper.mapping_matrix_over_sampled` — sub-resolution mapping matrix
   (one row per sub-pixel, no `sub_fraction` fold), reusing
   `slim_for_sub_slim` / existing index maps.
2. `AbstractInversionImaging.operated_mapping_matrix_list`
   (`inversion/inversion/imaging/abstract.py:104-116`): route through the
   oversampled Convolver path when
   `psf.convolve_over_sample_size > 1` (mapping formalism only — mapping.py
   itself needs no logic change).
3. Loud guards on the paths that consume `psf.kernel.native` directly:
   `InversionImagingSparse.psf_weighted_data` and the preloaded linear-func
   operated matrices (`abstract.py:215-230`) raise when handed an s>1
   Convolver (deferred formalism, per the approved design).
4. Memory profile of the ×s² FFT cube on a realistic pixelization before
   anything defaults on (design §4 risk; chunking noted as mitigation).

## Tests (numpy-only)

- `mapping_matrix_over_sampled` binned by mean reproduces `mapping_matrix`
  exactly (delta-kernel identity).
- End-to-end mapping-formalism inversion at s=2 against a brute-force
  reference built from the ground-truth machinery.
- Guard tests for sparse + linear-func paths.
- Full PyAutoArray pytest suite passes.

Parent: `oversampling_phase_2_core_api.md` (split record).
Previous: `oversampling_phase_2a_convolver_dataset.md`.
Next: `oversampling_phase_2c_autogalaxy_consumer.md`.
