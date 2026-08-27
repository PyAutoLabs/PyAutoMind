# Active Tasks

## board-github-data-seam
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/303 (issued 2026-08-27)
- issued: 2026-08-27
- prompt: active/board_without_gh_phase1_seam.md
- status: library-dev — not started; routed by /start_dev, no worktree claimed yet
  (this session is remote: no ~/Code/PyAutoLabs-wt, so /start_library runs on the
  machine that picks the task up).
- worktree: ~/Code/PyAutoLabs-wt/board-github-data-seam/ (to be created by /start_library)
- repos: PyAutoBrain
- phase: 1 of 2 — phase 2 is draft/feature/pyautobrain/board_without_gh_phase2_legs.md,
  blocked-by this one; parent design + probe evidence in
  draft/feature/pyautobrain/board_without_gh.md
- why: the board is the morning door and eleven legs are dark on the surface it is
  read from. The 2026-08-27 probe closed the two cheaper options — $GH_TOKEN 403s
  every repo path — so the injection seam is the design.

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
