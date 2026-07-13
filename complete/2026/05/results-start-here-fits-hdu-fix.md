## results-start-here-fits-hdu-fix
- completed: 2026-05-08
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/61
- repos: autogalaxy_workspace
- notes: |
    Surfaced as "Cluster B" in a release-prep triage report — four
    autogalaxy results scripts (start_here.py + three under
    aggregator/) supposedly sharing a `KeyError ('galaxies', 'galaxy',
    'bulge', 'ell_comps', 'ell_comps_0')` from
    `parameter_lists_for_paths`, attributed to `_quick_fit.py`
    building a model that doesn't expose `ell_comps`. Investigation
    on current main contradicted both halves: `ag.lp_linear.Sersic`
    and `ag.lp_linear.Exponential` both expose `ell_comps`
    (`model.info` confirms 9 free parameters incl. `bulge.ell_comps`)
    and the three aggregator scripts already pass cleanly under
    `PYAUTO_TEST_MODE=1` from a fresh `output/results_folder`. The
    original `KeyError` I saw on first run came from a stale cached
    output folder — once `_quick_fit.py` regenerated, it vanished.
    Only `start_here.py` was actually broken, and for an unrelated
    reason: lines 233–235 reloaded the saved `dataset.fits` with
    `data_hdu=0, noise_map_hdu=1, psf_hdu=2`, but the visualizer
    writes the file as `MASK, DATA, NOISE_MAP, PSF,
    OVER_SAMPLE_SIZE_LP, OVER_SAMPLE_SIZE_PIXELIZATION`, so
    `psf_hdu=2` pulled the 100×100 noise map and `Convolver` rejected
    it with `KernelException: "Convolver must be odd"`. Fix: shift
    indices by one (0→1, 1→2, 2→3). Three lines, one file. Smoke
    tests 6/6, aggregator regression confirmed the three siblings
    still pass. Cluster B as originally described is therefore
    already-resolved on main and needed no aggregator-path rewrites.
    Lesson worth keeping: when a triage cluster says "N scripts share
    root cause X, mechanical fix Y", verify reproduction on current
    main before mass-applying Y — clusters age out as upstream PRs
    merge, and the surviving failures often have a different cause.
