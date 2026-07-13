## strip-non-jit-noise-add-alma-high-res
- issue: (none — recovered by repo_cleanup sweep)
- completed: 2026-06-07
- workspace-pr:
  - https://github.com/PyAutoLabs/autolens_profiling/pull/45
  - https://github.com/PyAutoLabs/autolens_workspace_developer/pull/85
- repos: autolens_profiling, autolens_workspace_developer
- notes: Stranded worktree with uncommitted work in two repos. Landed the conflict-free half — the new `alma_high_res` interferometer dataset (profiling #45) + its `jax_profiling/dataset_setup/interferometer.py` wiring (developer #85). DROPPED the `strip-non-jit-noise` refactor of `likelihood/*.py`: it conflicted with main and was superseded by `898fe12` ("split into likelihood_breakdown + likelihood_runtime packages"), which realizes the same eager-vs-runtime separation more thoroughly. The refactor remains recoverable as a parked stash (`strip-noise wip`) in the autolens_profiling stash list — not landed.
