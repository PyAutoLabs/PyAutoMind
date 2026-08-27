# Active Tasks

## xla-cpu-eigen-pool-deadlock
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1530 (issued 2026-08-27)
- issued: 2026-08-27
- prompt: active/xla_cpu_eigen_pool_deadlock.md
- status: not started — research follow-up to the shipped jax-compile-stall epic
  (record complete/2026/08/jax-vmap-materialisation-hang.md, PyAutoFit#1528)
- repos-none-claimed: no worktree claimed; investigation is CI-driven via retime.yml
- why: #1528 shipped a WORKAROUND. Every JAX script in both test workspaces now runs
  single-threaded Eigen (~15% slower on the heaviest), and that flag is load-bearing —
  removing it silently brings back seven quarantines.
- the recoverable-cost question: if XLA's pool is merely mis-sized against the runner's
  cgroup quota rather than genuinely deadlocked, the fix is sizing it and the 15% comes back.

## numba-cpu-mge-batch-convolve-cache
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/496
- issued: 2026-08-27
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/497
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/588
- heart-ack: user authorised ship over RED `release validation FAILED (stage integrate)` (unrelated autolens_workspace_test rectangular_mge pin drift), 2026-08-27
- worktree: ~/Code/PyAutoLabs-wt/numba-cpu-mge-batch-convolve-cache
- repos:
  - PyAutoArray: feature/numba-cpu-mge-batch-convolve-cache
  - PyAutoGalaxy: feature/numba-cpu-mge-batch-convolve-cache
- note: epic numba-cpu-likelihood phase 1. Plan on the issue. Item 4 (pair-loop hoist + mirror) approved
  by user 2026-08-27 after the per-pixel-noise-map check; strict bit-identity NOT required (ulp-level BLAS
  ordering in the mirrored half accepted, pins at rtol 1e-6 are the guard).

## result-instance-fallback
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1535
- issued: 2026-08-27
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/result-instance-fallback
- repos:
  - PyAutoFit: feature/result-instance-fallback
  - PyAutoLens: feature/result-instance-fallback

## harvest-0827-gate-b-pt2
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/182
- issued: 2026-08-27
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/harvest-0827-gate-b-pt2
- repos:
  - autolens_profiling: feature/harvest-0827-gate-b-pt2

## dashboard-bundles
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/309
- issued: 2026-08-27
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/dashboard-bundles
- repos:
  - PyAutoBrain: feature/dashboard-bundles
  - PyAutoMind: feature/dashboard-bundles
