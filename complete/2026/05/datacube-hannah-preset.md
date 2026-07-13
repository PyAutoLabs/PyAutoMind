## datacube-hannah-preset
- completed: 2026-05-15
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/311
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/63
- summary: |
    Added "hannah" instrument preset to the jax_profiling datacube + interferometer
    delaunay profilers, pinning Hannah Stacey's real ALMA settings (n_channels=34,
    n_visibilities=16984, pixel_scale=0.125", shape_native=(40, 40), mask_radius=2.3").
    Library side (PyAutoArray): extended `Interferometer.from_fits` to accept
    `raise_error_dft_visibilities_limit` (3-line change + regression test).
    Workspace side: promoted mask_radius into INSTRUMENTS dict; gated full-pipeline
    cube JIT (Part C) behind CUBE_FULL_JIT=1 (lower+compile alone is ~70s at
    n_channels=34); per-channel regression literal pinned at -204838.07924622478;
    cube step-by-step total at Hannah's scale is 205.92s/eval (shared-Lᵀ W̃ L
    savings est. ~34.8s once Aris's deferred optimisation lands).
