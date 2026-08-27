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

## result-instance-fallback
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1535
- issued: 2026-08-27
- prompt: active/result_instance_fallback_samples_persist.md
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/result-instance-fallback
- repos:
  - PyAutoFit: feature/result-instance-fallback
  - PyAutoLens: feature/result-instance-fallback

## harvest-0827-gate-b-pt2
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/182
- issued: 2026-08-27
- prompt: active/harvest_2026_08_27_gate_b_pt2.md
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/harvest-0827-gate-b-pt2
- repos:
  - autolens_profiling: feature/harvest-0827-gate-b-pt2

## dashboard-bundles
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/309
- issued: 2026-08-27
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/310
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/365
- heart-ack: RED acknowledged 2026-08-27 (release integrate failure, shared_preloads.py timeout, hook-manifest drift, stale PyAutoFit PR — all unrelated)
- worktree: ~/Code/PyAutoLabs-wt/dashboard-bundles
- repos:
  - PyAutoBrain: feature/dashboard-bundles
  - PyAutoMind: feature/dashboard-bundles
