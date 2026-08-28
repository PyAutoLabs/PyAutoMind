# Active Tasks

## sparse-interferometer-unequal-sigma-guard
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/502
- issued: 2026-08-28
- prompt: active/sparse_interferometer_unequal_sigma_guard.md
- session: claude --resume b766a19b-260c-4b56-8d19-072fa9a34b28
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/sparse-interferometer-unequal-sigma-guard
- repos:
  - PyAutoArray: feature/sparse-interferometer-unequal-sigma-guard
- parallel-claim: PyAutoArray also claimed by numba-cpu-nnls-iteration-reduction (util/ NNLS files); this task touches dataset/interferometer/dataset.py + its test only — disjoint, own worktree approved 2026-08-28.
- note: follow-up from #499 close-out; guard-first, two-operator generalisation assessed in the PR only.

## delaunay-nn-env-header
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/284
- issued: 2026-08-28
- prompt: active/delaunay_nn_env_header.md
- session: claude --resume b766a19b-260c-4b56-8d19-072fa9a34b28
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/delaunay-nn-env-header
- repos:
  - autolens_workspace_test: feature/delaunay-nn-env-header
- note: follow-up from #499 close-out. If smoke runtime with jax+full_datasets exceeds budget, stop and report before touching tokens.

## phase8b-f2-ruling-scorer-verdict
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/185
- issued: 2026-08-28
- prompt: active/phase8b_f2_ruling_scorer_verdict.md
- session: claude --resume 3ebe0d5d-2ca4-45f2-9d81-8521e3266e29
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/phase8b-f2-ruling-scorer-verdict
- repos:
  - autolens_profiling: feature/phase8b-f2-ruling-scorer-verdict
- note: architect ruling recorded in DECISIONS.md BEFORE scoring. Verdict is PRELIMINARY (24/39); re-run when RAL job 341978's 15 arms land.
