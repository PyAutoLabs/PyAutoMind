## psf-oversample-workspace
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/232 (closed)
- completed: 2026-07-08
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/358 (merged, 12d0dce6)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/149 (merged, ae57a9e)
- notes: |
    Phase 3 of oversampled PSF convolution: convolution_over_sampled.py
    (ground-truth values via public API; FitImaging at s=2 for standard/
    operated/linear lp + pixelized mapping formalism, s=1 comparisons;
    guards) + convolution.py s=2 FFT-vs-real-space parity (first e2e JAX
    validation, 4.4e-16). Found + fixed 2a padded-blurring-mask frame bug
    (#358) — workspace tier caught what 2100+ unit tests missed. Simulator
    example deferred to option (a) follow-up
    (feature/autogalaxy/oversampled_psf_simulator.md). Calibration:
    merged-unchanged.
