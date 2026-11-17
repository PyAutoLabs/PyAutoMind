# ConvolverState: size the FFT frame from the mask, not the native array (Sam's trim, internal)

Type: feature
Target: autoarray
Repos:
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: high
Consequence: judge
Community: https://github.com/PyAutoLabs/.github/discussions/43
Filed: 2026-11-17
Issued: 2026-11-17

Agreed by the human in the /community chat on 2026-11-17, and promised to @samlange04 on
#43 (https://github.com/PyAutoLabs/.github/discussions/43#discussioncomment-19680883):
we implement it on our side, building on his PR, credit him as co-author
(`Co-authored-by: samlange04`), ask him to re-run his GPU benchmark, then close
PyAutoArray#675 in favour of ours.

## What

`ConvolverState` (`autoarray/operators/convolver.py`, ~lines 97-155) sets
`full_shape = mask_shape + kernel - 1` from the *native* mask shape and only ever pads
(`required_shape_for_kernel`). Size it instead from
`mask_2d_util.trimmed_shape_for_kernel(mask, kernel_shape_native, buffer=1)` (take that
function and its tests from PR #675 branch `samlange04:...`, commits a7f9fbc7..bbd126ce)
and crop/pad the internal `self.mask` / `self.blurring_mask` to that frame
(`resized_from` is centred and parity-preserving, so slim ordering is unchanged). Never make
the frame larger than today's. All outputs stay on the caller's mask
(`Array2D(values=..., mask=image.mask)`), so dataset shapes, fit images, image meshes and
saved results do not change: no config key, always on.

Check every path that uses `state.mask` / `fft_shape`: `convolved_image_from` (incl. the
blurring image), `convolved_mapping_matrix_from`, the real-space and numpy variants, the
over-sampled convolve paths (`convolve_over_sample_size > 1`), the sparse operator setup,
`is_for_mask` caching, and JAX jit/vmap static shapes.

## Witness

- Unit: convolved image / mapping matrix identical (to FFT rounding) between a small mask on a
  large stamp and the same mask on a tight stamp; blurring region preserved; even/odd frames.
- Smoke: autolens, autogalaxy, autolens_test, howtolens all green, and pinned likelihoods
  unchanged (the PR #675 approach broke 6 scripts; this one must break none).
- Benchmark: Sam's JWST geometry (400 px stamp, 0.03"/px, 1.5" mask, 37x37 PSF, 30x30 mesh)
  FFT frame 400x400 -> ~180x180, ~4x per call on GPU (his A6000/4090 table on #43).
