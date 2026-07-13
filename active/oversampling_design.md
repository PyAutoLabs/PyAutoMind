# Oversampled PSF convolution — design note (phase 1)

> **RETIRED 2026-07-09 (reconcile pass).** Deliverable of the shipped phase-1 design (PyAutoArray#353, complete.md: psf-oversample-design). The full oversampling series is shipped — see the oversampling.md close-out. Historical.

Deliverable of `oversampling_phase_1_design.md` (PyAutoLabs/PyAutoArray#353).
Companion ground truth: `oversampling_ground_truth.py` (same directory).
File/line references are against `feature/psf-oversample-design` worktree
branches of PyAutoArray and PyAutoGalaxy (cut from main, 2026-07-08).

## 1. The core insight: reuse the Convolver on an upscaled mask

Everything the `Convolver` does is driven by a mask and a kernel:
`ConvolverState` (`autoarray/operators/convolver.py:20-142`) derives the FFT
geometry (`fft_shape`, padded mask, `blurring_mask`, precomputed kernel FFTs)
from *any* `Mask2D` + kernel pair, and both convolution entry points —
`convolved_image_from` (`convolver.py:477`) and
`convolved_mapping_matrix_from` (`convolver.py:599`) — just scatter slim
values onto that mask's native grid, convolve, and slim again.

Oversampled convolution therefore does not need new convolution machinery.
Define a **fine mask**: the image mask upscaled by integer factor `s`
(pixel scale `ps/s`, every unmasked pixel becomes an s×s unmasked block).
Then:

1. build `ConvolverState(kernel=kernel_fine, mask=mask_fine)` — the existing
   FFT/real-space paths run verbatim at the fine resolution;
2. scatter the *over-sampled* (sub-gridded) evaluation of the scene onto the
   fine native grid;
3. convolve exactly as today;
4. bin the fine result down to image resolution by the mean of each s×s
   block (the semantics of `OverSampler.binned_array_2d_from`,
   `autoarray/operators/over_sampling/over_sampler.py:202-279`);
5. slim with the original image mask.

The one genuinely new piece is index bookkeeping: autoarray's over-sampled
arrays are ordered as **per-pixel sub-blocks** (pixel 0's s² sub-pixels
contiguous — `over_sampler.py:33-45`), while the fine mask's slim ordering is
row-major over the fine grid. Phase 2 adds a cached permutation
(`sub_slim_index -> fine_slim_index`), computed once alongside
`ConvolverState`; with it, steps 2 and 5 are single fancy-index operations
and the whole path is JAX-compatible (pure gathers/scatters, static shapes).

New utils needed (phase 2): `mask_2d_upscaled_from(mask, s)` (or a
`derive_mask.upscaled_from` method) and the permutation builder — both belong
next to the existing mask/over-sample utils.

## 2. `Convolver.convolve_over_sample_size`

`Convolver.__init__` (`convolver.py:146-233`) gains
`convolve_over_sample_size: int = 1`.

- **Kernel semantics:** for `s > 1` the supplied `kernel` is the PSF sampled
  at the *fine* pixel scale (`image ps / s`), odd-shaped in both axes (the
  existing odd-kernel check at `convolver.py:226-231` applies unchanged;
  note a fine kernel of the same physical radius r has
  `2*(r/ps_f)+1` pixels — e.g. r=2.0", ps=1", s=2 → 9×9, still odd).
  `s=2` means the PSF has 2× the image resolution, per the parent prompt.
  Normalization (`normalize=True`, `convolver.py:219-222`) sums the fine
  kernel to 1 — with mean-binning after convolution this preserves total
  flux to the same accuracy as today.
- **`state_from(mask)`** (`convolver.py:235-246`): when `s > 1`, the mask it
  receives is the *image* mask; it derives `mask_fine` and builds the state
  from `(kernel, mask_fine)`, caching the sub↔fine permutation and the bin
  indices on the state. `Imaging(psf_setup_state=True)` precomputes this once
  (`autoarray/dataset/imaging/dataset.py:126-132`).
- **Entry points:** `convolved_image_from` and
  `convolved_mapping_matrix_from` keep their signatures but, when `s > 1`,
  expect over-sampled (sub-gridded slim) inputs — `image` of length
  `n_unmasked * s²` in sub-block order, `blurring_image` likewise on the
  blurring mask — and return image-resolution slim outputs, exactly as
  callers consume them today. A shape check raises loudly if a binned
  image-resolution array is passed while `s > 1` (no silent guessing).
- **`s=1` is a strict no-op:** every existing code path is untouched;
  regression parity is `convolve_over_sample_size=1` ≡ current behaviour
  (verified by the ground truth: max |diff| vs installed Convolver 5.6e-17).
- **Validation at construction:** `s` must be a plain `int >= 1` —
  `Array2D`/adaptive input raises immediately (see §6). When a mask arrives
  in `state_from`, `kernel.pixel_scales ≈ mask.pixel_scales / s` is checked;
  mismatch raises `exc.KernelException`.

## 3. `Imaging` plumbing

`Imaging.__init__` (`dataset.py:24-143`) gains, per the parent prompt:

```
convolve_over_sample_size_lp: int = 1,
convolve_over_sample_size_pixelization: int = 1,
```

- Defaults of 1 keep every existing dataset byte-identical in behaviour.
- **Coupling to evaluation over-sampling:** the values to be convolved at
  the fine resolution must first be *evaluated* at that resolution. The
  `over_sample` decorator (`autoarray/operators/over_sampling/decorator.py:15-63`)
  currently bins immediately after evaluation, so the Convolver only ever
  sees image-resolution arrays. Phase-2 rule (minimal and explicit): when
  `convolve_over_sample_size_lp > 1`, `over_sample_size_lp` must be a
  uniform int equal to it (same for the pixelization pair); anything else
  raises at `Imaging.__init__`. Generalising to
  `over_sample_size = k * convolve_over_sample_size` (partial bin from k·s to
  s before convolving) is recorded as future work — it is a pure extension of
  the bin step, not a redesign.
- **One PSF, two sizes:** the dataset holds a single `psf`. If
  `s_lp != s_pix`, the user supplies the kernel at the *finer* of the two
  and the coarser variant is derived by sum-binning + renormalizing the fine
  kernel (binning a PSF down is exact; upsampling is not). Phase 2 may ship
  with the `s_lp == s_pix` restriction first and lift it in the same PR if
  time allows — the design supports both.
- `GridsDataset` (`autoarray/dataset/grids.py:13`) needs one change: when
  `convolve_over_sample_size_lp > 1`, the `blurring` grid (`grids.py:118`)
  must carry `over_sample_size = s` instead of 1, so the blurring image can
  be evaluated on the fine grid (the blurring region participates in the
  fine convolution exactly as it does today at image resolution).
- `from_fits`, `apply_mask`, `apply_over_sampling` and the trimming/padding
  helpers pass the two new ints through mechanically.

## 4. Inversion wiring — hypothesis corrected

The parent prompt hypothesised the wiring lands in
`inversion/inversion/imaging/mapping.py`. **Correction:** `mapping.py`
contains no convolution call. The PSF is applied in the shared parent
`AbstractInversionImaging.operated_mapping_matrix_list`
(`inversion/inversion/imaging/abstract.py:104-116`), which calls
`psf.convolved_mapping_matrix_from(...)`; `InversionImagingMapping`
(mapping.py) merely consumes the result in `data_vector` (mapping.py:53-71)
and `curvature_matrix` (mapping.py:73-99). Wiring the oversampled path into
that inherited property serves the mapping formalism — the *effect* the
prompt wanted — with no edit to mapping.py's own logic.

Two additional findings:

- **The mapper must emit a sub-resolution mapping matrix.**
  `Mapper.mapping_matrix` (`inversion/mappers/abstract.py:255-275`) already
  folds sub-pixels down to image resolution via `sub_fraction`
  (`= 1/s²` per sub-pixel, `over_sampler.py:149`). For oversampled
  convolution the convolution must happen *before* that fold: the mapper
  needs a `mapping_matrix_over_sampled` variant with one row per sub-pixel
  and no `sub_fraction` weighting; the fine convolution runs per column;
  binning rows by mean afterwards reproduces the current matrix exactly when
  the kernel is a delta. The pieces (sub→pix index maps,
  `slim_for_sub_slim`) already exist. **Main phase-2 risk:** the FFT path's
  native cube becomes `(ny·s, nx·s, n_src)` — ×s² memory; on GPU this
  compounds the known vmap fan-out pressure, so the PR must profile a
  realistic pixelization and consider chunking before enabling it by
  default.
- **`sparse.py` and the linear-func fast path bypass the Convolver.**
  `InversionImagingSparse.psf_weighted_data`
  (`inversion/inversion/imaging/sparse.py:54-61`) and the preloaded
  linear-func operated matrices (`abstract.py:215-230`) consume
  `psf.kernel.native` directly to build precomputed PSF-weighted products.
  Oversampling those requires re-deriving that formalism — deferred to
  future work, as the prompt intended. Guard: `Imaging.__init__` raises if
  `sparse_operator is not None` and
  `convolve_over_sample_size_pixelization > 1`; the linear-func kernel
  consumers raise similarly when handed an `s > 1` Convolver.

## 5. PyAutoGalaxy `operate/image.py` (survey only — phase 2 implements)

`blurred_image_2d_from` (`autogalaxy/operate/image.py:98-146`) evaluates the
image via `image_2d_from(grid)` — which returns *binned* values because of
the `over_sample` decorator — and hands it to `psf.convolved_image_from`
(`image.py:93-96`). For `s > 1` the evaluation must reach the Convolver
unbinned:

- extend the `over_sample` decorator with a pass-through `binned: bool = True`
  kwarg (static, JAX-safe); `binned=False` returns the sub-gridded values in
  sub-block order — exactly the input format §2 defines;
- `_blurred_image_2d_from` checks `psf.convolve_over_sample_size` and calls
  with `binned=False` for both the image and blurring-grid evaluations;
- the list/dict variants (`blurred_image_2d_list_from`,
  `galaxy_blurred_image_2d_dict_from`, `image.py:268-460`) route through the
  same two functions and need only the same switch;
- `padded_image_2d_from` / `unmasked_blurred_image_2d_from`
  (`image.py:148-217`, visualization-only) stay at image resolution in
  phase 2 — documented limitation, revisit in phase 4 docs.

## 6. Adaptive over-sampling guard

Adaptive (per-pixel `Array2D`) sub-sizes make the fine raster non-uniform, so
2D convolution on it is ill-defined. Behaviour (loud, producer-side, no
silent fallbacks):

- `convolve_over_sample_size_*` accept only plain `int` — an `Array2D` or
  other type raises `TypeError` in `Imaging.__init__`.
- `convolve_over_sample_size_lp > 1` with an adaptive/non-uniform
  `over_sample_size_lp` raises `exc.DatasetException` in `Imaging.__init__`
  (checked via `OverSampler.sub_is_uniform`, `over_sampler.py:170-175`);
  same for the pixelization pair.
- The Convolver's oversampled entry points re-assert uniformity on the
  structures they receive, so a hand-built call path cannot sneak an
  adaptive grid past the dataset check.

## 7. Numerical ground truth (`oversampling_ground_truth.py`)

Independent brute-force implementation (plain numpy loops): 11×11 image,
ps=1", circular mask r=3.5" (37 unmasked pixels), off-centre Gaussian source
(σ=1.2", centre (0.3,-0.4)"), Gaussian PSF σ=0.8" with fixed physical kernel
radius 2.0" (5×5 native, 9×9 fine at s=2), masked-embedding scene
(mask ∪ blurring region), direct fine-raster convolution, s×s mean binning.

| quantity | s=1 | s=2 |
|---|---|---|
| sum over mask | 2.807349652595196e+00 | 2.796562184524787e+00 |
| blurred[slim 0] | 3.655472905370449e-02 | 3.726289901353439e-02 |
| blurred[slim 17] | 2.069771979137382e-01 | 2.025075336159483e-01 |
| blurred[slim 36] | 1.042470837248629e-02 | 1.090767109119494e-02 |

- **Parity:** s=1 vs installed `Convolver.convolved_image_via_real_space_np_from`:
  max |diff| = 5.6e-17 (machine precision) — the ground truth and the current
  Convolver agree exactly on what s=1 means.
- **Effect size:** s=2 shifts pixel values by up to 4.99e-3 (≈2.4% of the
  peak) on this small test — comfortably above any noise floor phase-2 unit
  tests will care about, and physical evidence the feature matters.

Phase-2 unit tests (numpy-only, per the no-JAX-in-unit-tests rule) assert the
s=2 column above; the phase-3 workspace test re-derives the same numbers
through the public `Imaging`/fit API.

## 8. Phase-2 execution sketch

1. `mask_2d_upscaled_from` + sub↔fine permutation util (+ tests).
2. `Convolver(convolve_over_sample_size=...)` + fine `ConvolverState` +
   oversampled scatter/bin in the four convolution methods (+ tests vs §7).
3. `Imaging`/`GridsDataset` plumbing + §6 guards (+ tests).
4. Decorator `binned=False` + `operate/image.py` switch in PyAutoGalaxy
   (+ tests).
5. Mapper `mapping_matrix_over_sampled` + `operated_mapping_matrix_list`
   wiring, sparse/linear-func guards (+ tests; profile memory before
   defaulting on).
