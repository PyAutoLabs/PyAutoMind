## psf-oversample-galaxy
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/480 (closed)
- completed: 2026-07-08
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/481 (merged, squash 6c33c76b)
- notes: |
    Phase 2c of oversampled PSF convolution + user-directed linear-lp
    addition. operate/image.py blurred-image variants evaluate on
    grid.over_sampled (Grid2DIrregular pass-through, no signature changes;
    Tracer inherits); LightProfileLinearObjFuncList override evaluates fine
    too. Support matrix at s>1: lp/linear-lp/operated/pixelized-mapping all
    supported; sparse/preload/adaptive raise. Suites 944+335. Calibration:
    amended (scope addition at human sign-off). Phase 3 queued blocked
    (autolens_workspace #232); phase 4 + refactor follow after.
