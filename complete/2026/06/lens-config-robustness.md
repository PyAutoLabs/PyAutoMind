## lens-config-robustness
- issue: (none — recovered by repo_cleanup sweep)
- completed: 2026-06-07
- workspace-pr:
  - https://github.com/PyAutoLabs/autolens_workspace_developer/pull/84
- repos: autolens_workspace_developer
- notes: Stranded worktree surfaced by the repo_cleanup sweep — 9 untracked files (no committed work) on `feature/lens-config-robustness`, branch 0 ahead of main. Landed the 5 `source_science/` helper modules (`lens_configs`, `sim_helpers`, `fit_helpers`, `extract_mge_lens_truth`, `run_all_tests`) and four imaging "truth" config datasets (`config_0_{1..4}`: sérsic/MGE truth × sérsic-lens/no-lens). Per user decision, committed inputs only (`data`/`noise_map`/`psf.fits`, `source_science.json`, truth `tracer.json`); regenerable fit outputs (`fit_comparison.*`, `fits/`) excluded and cleaned on teardown. FF'd the stale branch onto main before committing.
