# Oversampled PSF convolution — phase 2: core library API

> **RETIRED 2026-07-09 (reconcile pass).** Superseded by phases 2a/2b/2c, all merged: core PyAutoArray#355, inversion #357, autogalaxy consumer PyAutoGalaxy#481 (complete.md: psf-oversample-core/inversion/galaxy). This umbrella phase-2 prompt is fully covered.

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
Difficulty: large
Autonomy: supervised
Priority: normal
Status: split-into-phases
Phases:
- oversampling_phase_2a_convolver_dataset.md
- oversampling_phase_2b_inversion_wiring.md
- oversampling_phase_2c_autogalaxy_consumer.md

<!-- Split by the Feature Agent on 2026-07-08 (score 10, too-large for one
     PR) after the phase-1 design was approved (PyAutoArray#353). The cut
     follows the design note's execution sketch: 2a = Convolver + dataset
     (design steps 1-4 autoarray side), 2b = inversion wiring (step 5),
     2c = PyAutoGalaxy consumer (step 4 galaxy side; also blocked by the
     kaplinghat-sidm-cored-nfw PyAutoGalaxy claim). This file is the split
     record, not an executable task. -->

Phase 2 of 4 of `feature/autoarray/oversampling.md`. Requires the phase-1
design note and numerical ground truth (`oversampling_phase_1_design.md`) —
do not start until phase 1 has shipped; implement what the design note
decided, not a fresh design.

## Scope

1. **`Convolver`** (`@PyAutoArray/autoarray/operators/convolver.py`): add a
   `convolve_over_sample_size` integer specifying the over sample size of the
   PSF, so convolution runs at higher-than-image resolution (size 2 = PSF at
   2× the image resolution) and bins down to the observed resolution.
2. **`Imaging`** (`@PyAutoArray/autoarray/dataset/imaging/dataset.py`): extend
   the constructor with `convolve_over_sample_size_lp` and
   `convolve_over_sample_size_pixelization` attributes, following the pattern
   of the existing `over_sample_size_lp` / `over_sample_size_pixelization`
   parameters, and plumb them into the Convolver(s).
3. **Inversion path**: wire oversampled convolution into
   `@PyAutoArray/autoarray/inversion/inversion/imaging/mapping.py` per the
   phase-1 design. `sparse.py` stays untouched — future work.
4. **Model images**: update PSF blurring in
   `@PyAutoGalaxy/autogalaxy/operate/image.py` so modeling evaluates images on
   the oversampled grid, blurs at high resolution, and downsamples.
5. **Adaptive guard**: adaptive (per-pixel) over-sample sizes are incompatible
   with oversampled 2D convolution — raise a clear error, never silently
   degrade (no None-guards; bad input crashes loudly).

## Tests

- Unit tests in both libraries, numpy-only (no JAX in library unit tests),
  asserting against the phase-1 numerical ground truth.
- `convolve_over_sample_size=1` must reproduce existing behaviour exactly
  (regression parity).

## Acceptance

- Full pytest suites pass in PyAutoArray and PyAutoGalaxy worktrees, plus
  downstream library suites if the public API surface changes.
- Library PR carries an `## API Changes` summary for the phase-3 workspace
  follow-up.

Parent: `feature/autoarray/oversampling.md`.
Previous: `oversampling_phase_1_design.md`. Next: `oversampling_phase_3_workspace_examples.md`.
