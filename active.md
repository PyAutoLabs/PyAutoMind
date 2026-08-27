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
- status: workspace-dev — phase 1 (instrumentation + the ABAB dispatch) is on the branch
  below; research follow-up to the shipped jax-compile-stall epic
  (record complete/2026/08/jax-vmap-materialisation-hang.md, PyAutoFit#1528)
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
- the recoverable-cost question: if XLA's pool is merely mis-sized against the runner's
  cgroup quota rather than genuinely deadlocked, the fix is sizing it and the 15% comes back.
