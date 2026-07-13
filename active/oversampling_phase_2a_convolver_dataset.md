# Oversampled PSF convolution — phase 2a: Convolver + dataset core API

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 2a of the oversampled-PSF feature. Implements steps 1–4 (PyAutoArray
side) of the approved design `feature/autoarray/oversampling_design.md`
(approved unchanged on PyAutoLabs/PyAutoArray#353) — implement the design
verbatim, do not re-design. Split from `oversampling_phase_2_core_api.md`
(scored too-large): 2a = Convolver + dataset; 2b = inversion wiring;
2c = PyAutoGalaxy consumer switch (blocked on an unrelated PyAutoGalaxy claim).

## Scope (design note §§1–3, 5 autoarray half, 6)

1. `mask_2d_upscaled_from(mask, s)` util (+ `derive_mask` hook if idiomatic)
   and the cached sub-block ↔ fine-row-major slim permutation builder.
2. `Convolver(convolve_over_sample_size: int = 1)`: fine-kernel semantics,
   `state_from` builds the fine `ConvolverState` (+ permutation + bin
   indices), oversampled scatter/convolve/bin/slim in `convolved_image_from`
   and `convolved_mapping_matrix_from` (all four variants), shape check that
   raises on binned input when s > 1, kernel pixel-scale validation.
3. `Imaging` / `GridsDataset`: `convolve_over_sample_size_lp` /
   `convolve_over_sample_size_pixelization` (int, default 1), equality rule
   vs `over_sample_size_*` (uniform int, equal, else raise), blurring grid
   `over_sample_size = s`, `psf_setup_state` fine state, `from_fits` /
   `apply_mask` / `apply_over_sampling` pass-through, sparse_operator guard.
4. `over_sample` decorator: `binned: bool = True` pass-through kwarg
   (autoarray side only — the PyAutoGalaxy caller switch is phase 2c).
5. Adaptive guards per design §6 (TypeError / DatasetException, loud).

## Tests (numpy-only)

- Unit tests assert the ground-truth numbers in design §7
  (`oversampling_ground_truth.py`): s=1 strict parity with existing
  behaviour, s=2 reference values through `Convolver.convolved_image_from`.
- Guard tests: adaptive + s>1 raises; binned input to s>1 Convolver raises;
  kernel pixel-scale mismatch raises.
- Full PyAutoArray pytest suite passes.

## Acceptance

- `convolve_over_sample_size=1` leaves every existing test untouched.
- PR carries `## API Changes` for phases 2b/2c/3.

Parent: `oversampling_phase_2_core_api.md` (split record) /
`oversampling.md`. Next: `oversampling_phase_2b_inversion_wiring.md`.
