# Oversampled-PSF series follow-up: refactor pass (Refactor Agent)

Type: refactor
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
Difficulty: medium
Autonomy: safe
Priority: normal
Status: draft

Follow-up to the oversampled PSF convolution series (design PyAutoArray#353;
phases 2a #354/PR#355 merged, 2b #356/PR#357, 2c PyAutoGalaxy#480). Filed in
`feature/autoarray/` alongside the series per instruction; **Type is refactor —
route through the Refactor Agent** (`/refactor` → `bin/pyauto-brain refactor`),
behaviour-preserving with no API changes.

**Sequencing:** run only after PR#357 (2b) and the 2c PR have merged *and* the
phase-3 workspace numerical tests exist — the refactor's safety comes from the
test surface, and phase 3 completes it (unit ground-truth + workspace-level
parity). Do not start while any series PR is open.

## Scope — refactor everything the series touched, in particular:

1. **`@PyAutoArray/autoarray/operators/convolver.py` (priority)** — now ~1400
   lines. Structural duplication has compounded: 4 public convolution methods ×
   (numpy real-space / JAX real-space / JAX FFT) variants, plus the phase-2a
   `_convolved_*_over_sampled_{np,jax}_from` helpers which mirror the FFT body
   with permuted scatter + mean bin-down. Extract the shared machinery
   (masked scatter → convolve → gather/bin pipeline; the roll/dynamic-slice FFT
   epilogue; the blurring-image warning) and consider splitting the module
   (e.g. `convolver/` package: state, real-space, fft, over-sample). The
   even→odd fft_shape workaround noted in `ConvolverState`'s docstring is a
   known wart to evaluate while in there.
2. **`@PyAutoGalaxy/autogalaxy/operate/image.py` (priority)** — getting large
   (~580 lines). Phase 2c added three near-identical
   `convolve_over_sample_size > 1` switches (`blurred_image_2d_from`,
   `blurred_image_2d_list_from`, `galaxy_blurred_image_2d_dict_from`); extract
   the oversampled-evaluation branching into one helper, and assess splitting
   the module (blurring / padding-visualization / visibilities concerns are
   distinct).
3. **Smaller series debris:**
   - `@PyAutoArray/autoarray/dataset/imaging/dataset.py` —
     `_validate_convolve_over_sample_size` placement, and the psf
     rebuild/normalize/state block in `Imaging.__init__` which has grown
     conditional arms.
   - `@PyAutoArray/autoarray/inversion/mappers/abstract.py` —
     `mapping_matrix` / `mapping_matrix_over_sampled` share their call shape;
     parameterize rather than duplicate if it reads cleaner.
   - `@PyAutoArray/autoarray/operators/over_sampling/over_sample_util.py` —
     `mask_2d_upscaled_from` / `sub_slim_to_fine_slim_from` docstring + naming
     consistency with the module's conventions.

## Constraints (behaviour-preserving — the refactor contract)

- Zero behaviour change: the ground-truth-pinned tests (s=1 parity, s=2
  reference values to 1e-12, delta-kernel identities) and all suite counts
  must pass unmodified — never edit a test to make a refactor pass.
- Public API unchanged (no renames/removals; the series' new API is
  user-facing as of the next release).
- JAX paths stay JAX-compatible (static shapes, pure gathers/scatters); no
  new closures that cache-bust JIT.
- Full suites in PyAutoArray, PyAutoGalaxy and PyAutoLens are the gate, plus
  the phase-3 workspace tests once they exist.
