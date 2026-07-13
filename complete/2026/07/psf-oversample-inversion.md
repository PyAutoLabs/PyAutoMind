## psf-oversample-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/356 (closed)
- completed: 2026-07-08
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/357 (merged, squash ea75b948)
- notes: |
    Phase 2b of oversampled PSF convolution. Mapper.mapping_matrix_over_sampled
    (sub-res rows via existing util, identity parents), inversion wiring in
    AbstractInversionImaging._mapping_matrix_for_convolution_from, guards on
    linear-func/preload/sparse kernel-native paths. End-to-end s=2 vs
    independent brute force 2.2e-16; suites 860+940+334. CRLF normalization
    slip caught pre-ship (diff +191/-3). Calibration: merged-unchanged.
