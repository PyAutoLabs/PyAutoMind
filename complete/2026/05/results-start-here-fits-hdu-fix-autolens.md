## results-start-here-fits-hdu-fix-autolens
- issue: N/A (Cluster D triage follow-on for autolens; mirrors merged autogalaxy PR #61)
- completed: 2026-05-08
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/135
- repos: autolens_workspace
- notes: |
    Cluster D triage report attributed `autolens_workspace/scripts/guides/results/start_here.py`
    to a "truncated traceback ending in a 15x15 numpy pixel-coord array" — the actual
    exception was clipped from `report.md`. Reran the script with full stderr capture and
    found a `DatasetException: A value in the noise-map of the dataset is -0.0367 ... less
    than or equal to zero` at line 245 (the second `al.Imaging.from_fits(...)` block that
    re-loads the fit-output multi-HDU `image/dataset.fits` for the Simple-Loading section).
    The fit-output FITS file's HDU layout is `[0=MASK, 1=DATA, 2=NOISE_MAP, 3=PSF,
    4=OVER_SAMPLE_SIZE_LP, 5=OVER_SAMPLE_SIZE_PIXELIZATION]` (canonical reference:
    `PyAutoGalaxy/autogalaxy/aggregator/imaging/imaging.py:73-77`), but the script still
    passed `data_hdu=0, noise_map_hdu=1, psf_hdu=2`. Three-line fix bumped them to
    `1, 2, 3`. The autogalaxy_workspace half of this bug was already merged on main as
    PR #61 — `/plan_branches` caught the prior fix and narrowed the scope from "both
    workspaces" to "autolens only". The 7/7 smoke tests passed. Notebook regen
    (`/generate_and_merge`) deliberately deferred — to be batched with other notebook
    updates, mirroring how PR #61 was scripts-only too.
