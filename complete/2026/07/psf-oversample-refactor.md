## psf-oversample-refactor
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/360 (closed)
- completed: 2026-07-08
- prs: PyAutoArray#361 + PyAutoGalaxy#484 (merged, mains green)
- notes: |
    Series refactor, conservative cut per Refactor Agent too-large verdict.
    Four oversampled Convolver helper bodies -> two shared engines (net -31);
    operate/image s>1 switch -> _psf_evaluation_grids_from; gitignore for
    test_autoarray/output. Invariant exact (863/946/336 unchanged, np/jax
    parity 2e-16). Deferred: convolver/ package split (recorded on #360).
    Calibration: merged-unchanged.
