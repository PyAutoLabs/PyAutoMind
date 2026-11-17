## convolver-fft-frame-from-mask
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/698 (closed 2026-11-17)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/699 (MERGED 2026-11-17T15:18:52Z, merge e81c6e16; CI verdict GREEN, Heart freeze not active)
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/699
- completed: 2026-11-17
- merged-by: human-typed /prm
- tier: judge (declared Consequence) — no shadow row
- user-facing: true — hub #43 (@samlange04, co-author)
- summary:
  - `ConvolverState` sizes its FFT frame from the mask instead of the native array: `fft_shape = next_fast_len(max(full_shape, min(trimmed_shape, padded_shape)))`, never larger than before. Internal `mask` / `blurring_mask` are cropped (centred, parity-preserving) to that frame, with a fallback to the old frame if a crop would lose a pixel. Outputs stay on the caller's mask, so dataset shapes, fit images, image meshes and saved results are unchanged; no config key.
  - New `mask_2d_util.trimmed_shape_for_kernel` taken with its tests from @samlange04's PyAutoArray#675 (co-authored). Only that utility came over; #675's `Imaging.apply_mask` / `dataset:trim_to_mask` changes did not.
  - Final commit 88b391d0 is test-only: the JAX modes of the frame-equality tests skip when JAX is absent.
- evidence:
  - PyAutoArray unit suite 2458 passed; PyAutoGalaxy 1486 and PyAutoLens 1021 (1 xfailed) passed against the branch.
  - Smoke 140 passed / 0 failed (autolens_workspace, autogalaxy_workspace, autolens_workspace_test, HowToLens) — the suites where #675 broke 6 scripts.
  - Likelihood parity, `autolens_workspace_test/scripts/imaging/jax_likelihood/delaunay.py`: −532.29584351 on main == branch.
  - CPU benchmark on Sam's geometry (400² stamp, 0.03"/px, 1.5" mask, 37×37 PSF, JAX FFT, fp64): `fft_shape` 400² → 180²; `convolved_mapping_matrix_from` 2309 → 531 ms median per call (4.3×); max |new − old| 5e-13.
- follow-ups:
  - Supersedes PyAutoArray#675 (closed by the parent /community session, not this close-out).
  - @samlange04 asked on hub #43 (https://github.com/PyAutoLabs/.github/discussions/43) to re-run his GPU benchmark; a contributor "it's released" update is owed on #43 after the next release.
  - Release: the `active.md` row held no `pending-release:` line; the `pending-release:` key above was added by hand after close-out so the dashboard tracks the release (the PR carries the label).

## Original prompt

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
