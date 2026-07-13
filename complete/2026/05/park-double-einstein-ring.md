## park-double-einstein-ring
- completed: 2026-05-07
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/134
- repos: autolens_workspace
- notes: |
    Cluster H of the recent release-prep triage. scripts/imaging/features/
    advanced/double_einstein_ring/slam.py crashed under PYAUTO_TEST_MODE=2
    with autofit.exc.FitException at analysis.py:84. Investigation
    traced a structural cascade: Adapt regularization (used by SLaM
    pixelization phases) requires per-galaxy adapt_data that the
    synthetic samples_summary produced by bypass mode does not carry.
    Mapper.pixel_signals_from None-derefs `self.adapt_data.array` from
    multiple inversion entry points (likelihood, post-fit
    result.subtracted_signal_to_noise_map_galaxy_dict, etc.), so
    patching one site only unblocks the next. Drafted a defensive
    FitException-tolerance patch in PyAutoFit's _fit_bypass_test_mode
    (mirrors compute_latent_samples pattern) — verified the FIRST entry
    point cleared, but the SECOND failure point fired with the same
    root cause through a different call chain. Even with that fix, the
    next SLaM phase would derive adapt_images from the synthetic
    samples_summary and fail again. End-to-end fix requires either
    (a) defensively pretending Adapt works without adapt_data (silent
    semantic change — unsafe) or (b) restructuring the SLaM bypass to
    construct valid adapt_data (large refactor). User chose to park
    and handle manually. Sibling of imaging/features/pixelization/slam
    (NEEDS_FIX 2026-04-10, same root cause).
