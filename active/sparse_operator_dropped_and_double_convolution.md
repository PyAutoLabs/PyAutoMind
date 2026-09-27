# apply_over_sampling drops the sparse operator; dense route convolves the mapping matrix twice

Type: bug
Target: @PyAutoArray
Autonomy: human-required
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/585
Issued: 2026-09-27

## Request (verbatim)
"file both and then do them now" — the two PyAutoArray fixes found during the Euclid DR1 campaign (2026-09-27).

## 1. `Imaging.apply_over_sampling` silently drops `sparse_operator`
`autoarray/dataset/imaging/dataset.py` `apply_over_sampling` (~l.539-577) rebuilds `Imaging` without
`sparse_operator=`. Calling `apply_sparse_operator_cpu()` before `apply_over_sampling()` therefore
falls back to dense `InversionImagingMapping` with no warning. euclid_dr1 `vis_pix` ran dense the whole
campaign: 987 -> 180 ms and 799 -> 152 ms per eval once fixed (science-script reorder, euclid_dr1 32fbf62),
logL identical (<=2.7e-10 nats), identifier unchanged. The operator depends only on noise_map, PSF kernel and
mask, so carrying it through over-sampling is valid. Adjacent: `apply_sparse_operator_cpu` lacks the
`convolve_over_sample_size > 1` guard `apply_sparse_operator` has, and neither sparse method nor
`apply_noise_scaling` carries `convolve_over_sample_size_*`; `apply_mask` / `apply_noise_scaling` change
inputs the operator depends on, so they must not carry it but should not drop it silently either.

## 2. `operated_mapping_matrix_list` is an uncached `@property`
`autoarray/inversion/inversion/imaging/abstract.py:119`. On the dense route it is evaluated twice per
likelihood call (curvature/data-vector path and `mapped_reconstructed_operated_data_dict`), each a full PSF
`fftconvolve` of the mapping matrix: ~425 ms each, ~800 of 1005 ms per eval on a DR1 tile. Caching per
inversion instance saves ~40% on the dense route. Check the interferometer analogue for the same pattern.

## Witness
- A dataset with `apply_sparse_operator_cpu()` then `apply_over_sampling(...)` keeps a non-None
  `sparse_operator` and the inversion factory selects the sparse Numba class (red on current main).
- One likelihood evaluation on the dense route calls `psf.convolved_mapping_matrix_from` once per linear
  object, not twice (red on current main).

Evidence: session scratchpad lever_probe.log, sparse_ab.py, ab_*.json.

## Scope addition (user, 2026-09-27)
"check theres no other parts of source code which lose the sparse operator thing" — sweep every Imaging/Interferometer rebuild in PyAutoArray (fix) and PyAutoGalaxy/PyAutoLens (audit; fixes there are a scope decision).
