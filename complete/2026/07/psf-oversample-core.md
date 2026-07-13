## psf-oversample-core
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/354 (closed)
- completed: 2026-07-08
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/355 (merged, squash 279a5a00)
- notes: |
    Phase 2a of oversampled PSF convolution (design #353). Convolver
    convolve_over_sample_size + fine ConvolverState (upscaled-mask reuse of
    existing machinery + sub-block<->fine-slim permutation + mean bin-down),
    Imaging/GridsDataset plumbing with adaptive/equality/sparse guards,
    decorator binned=False. Tests pinned to phase-1 ground truth (<=1e-12);
    857+933+331 suites green. Supervised --auto: parked at ship sign-off,
    human approved unchanged (calibration: merged-unchanged). Follow-ups:
    2b #356 (inversion wiring), 2c (PyAutoGalaxy consumer, unblocked),
    phases 3-4 (workspace, docs).
