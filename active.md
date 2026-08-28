# Active Tasks

## xla-cpu-eigen-pool-deadlock
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1530 (issued 2026-08-27)
- issued: 2026-08-27
- prompt: active/xla_cpu_eigen_pool_deadlock.md
- status: workspace-dev — root cause FOUND and mechanism CONFIRMED. Q1 + Q3 answered
  (run 33099502356, comment 5443451389); confirmation run 33103725546 (comment 5444085654):
  pool of 4 = 1 pass/5 hang, pool of 1 = 6 pass/0 hang, Fisher p=0.015 (p=0.0002 pooled).
  Q2 CLOSED (80d7bc5): standalone reproducer, jax+numpy only, deadlocks 8/8 against 0/8
  with the workaround flag, Fisher p=0.000155. Needed a scatter feeding each FFT (else XLA
  fuses to a YnnFusionThunk and ducc0 runs inline) plus transforms above ducc0's fan-out
  threshold. Q4 DECIDED: report written, human-reviewed and committed
  (51512af, .github/scripts/xla_fft_pool_reentrancy_upstream.md) and deliberately NOT
  filed — posting to jax-ml/jax is outward-facing and outside this session's scope, so it
  needs a person; the hold is about who posts, not whether the finding stands. ALL FOUR
  acceptance criteria now met (comment 5445381638). Ready for close-out; flag removal
  stays a deliberate non-action until an upstream fix lands. Research follow-up to the shipped jax-compile-stall epic
  (record complete/2026/08/jax-vmap-materialisation-hang.md, PyAutoFit#1528)
- FOUND: re-entrant thread-pool deadlock — xla::cpu::FftThunk::Execute runs ON an Eigen
  pool worker and hands ducc0 that same pool, which fans the FFT back into it and blocks
  on a latch. 4 workers, 4 concurrent FFT thunks, every worker waiting for a worker.
  11/11 dumps identical. NOT oversubscription: no CFS quota on ubuntu-latest, every CPU
  reading agrees at 4, so the pool is correctly sized and the ~15% is NOT recoverable by
  sizing it. The flag stays.
- branch: claude/xla-cpu-eigen-deadlock-wndbfb
- repos:
  - autolens_workspace_test (claude/xla-cpu-eigen-deadlock-wndbfb) — retime harness gains
    A/B arms + native stack capture; no profile change, nothing un-quarantined
- no-worktree: web-github session, direct clones as in phase 3; PyAutoFit and
  autogalaxy_workspace_test are deliberately untouched until a result earns a change
- phase 1 dispatch: retime.yml on the branch, imaging/jax_likelihood/mge_group.py,
  6 repeats x 2 python legs, 300s cap, --dump-after 150,
  arms control:XLA_FLAGS= vs quota:XLA_FLAGS=,affinity=auto
- why: #1528 shipped a WORKAROUND. Every JAX script in both test workspaces now runs
  single-threaded Eigen (~15% slower on the heaviest), and that flag is load-bearing —
  removing it silently brings back seven quarantines.
- the recoverable-cost question: ANSWERED NO, twice over — no cgroup quota exists to
  match, and a pool of 1 costs 56-62s against control's 48.1s, i.e. what the flag already
  costs. Pool sizing recovers nothing; the 15% comes back only upstream.

## result-instance-fallback
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1535
- issued: 2026-08-27
- prompt: active/result_instance_fallback_samples_persist.md
- status: library-shipped, awaiting-merge (Heart RED override: release validation FAILED (stage integrate))
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1536
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/713
- worktree: ~/Code/PyAutoLabs-wt/result-instance-fallback
- repos:
  - PyAutoFit: feature/result-instance-fallback
  - PyAutoLens: feature/result-instance-fallback

## harvest-0827-gate-b-pt2
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/182
- issued: 2026-08-27
- prompt: active/harvest_2026_08_27_gate_b_pt2.md
- status: workspace-shipped, awaiting-merge (Heart RED override: release validation FAILED (stage integrate))
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/183
- worktree: ~/Code/PyAutoLabs-wt/harvest-0827-gate-b-pt2
- repos:
  - autolens_profiling: feature/harvest-0827-gate-b-pt2
