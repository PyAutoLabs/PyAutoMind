# Active Tasks

## transformed-message-factor-gradient-unpack
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1501 (issued 2026-08-19)
- issued: 2026-08-19
- prompt: active/16_transformed_message_factor_gradient_unpack.md
- status: HOLD — do not start dev. Fix-or-delete hangs off the PyAutoFit#1498 logpdf-contract
  decision (parked #1500 design bundle); dead code (zero production callers), crashes on first
  call if ever exercised.
- external: community PR https://github.com/PyAutoLabs/PyAutoFit/pull/1502 (@trexfr-ops) targets
  this exact unpack — review via /community before any local work; the #1498 adjudication decides
  whether the method should exist at all.
- registered: 2026-08-19 by the wake_up session — the issuing session (claude/autofit-priors-messages-audit-ylvenv)
  filed the prompt + issue but not this entry, tripping Lifecycle Drift on main.
- repos-none-claimed: this entry claims NO repos — one line deliberately, not 2-space bullets.

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

## organ-remote-block-and-uv-hook-repair
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/360 (issued 2026-08-27)
- issued: 2026-08-27
- prompt: active/session_fixes_reach_only_two_organs.md
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/organ-remote-block-and-uv-hook-repair
- repos:
  - PyAutoMind: feature/organ-remote-block-and-uv-hook-repair
  - PyAutoBrain: feature/organ-remote-block-and-uv-hook-repair
  - PyAutoHeart: feature/organ-remote-block-and-uv-hook-repair
  - PyAutoHands: feature/organ-remote-block-and-uv-hook-repair
- scope-note: PyAutoBrain is claimed though the prompt omits it — it carries a generated
  hook copy that goes stale the moment policy/session_start_hook.sh changes, and
  firewall_gate.yml checks it out. The prompt's "all four organs" was written from a
  session that could see two.
- deliberately-out-of-scope: the other 30 repos carrying a stale hook copy (no gate sees
  them; firewall_gate.yml checks out four). Filed as
  draft/maintenance/organs/session_hook_reaches_only_four_of_thirty_four_repos.md
- co-claim RELEASED 2026-08-27: pages-dashboard-publish-gap (#361) shipped and closed out
  (PR #362 merged 74c1450, record complete/2026/08/pages-dashboard-publish-gap.md), so
  PyAutoMind is now claimed by this task alone. The two ran in parallel worktrees on
  disjoint file sets — that task touched `.github/workflows/dashboard_refresh.yml` only;
  this one touches `scripts/`, `policy/`, `tests/` and the generated `.claude/hooks/`
  copies — and needed no serialisation.

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
