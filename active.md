# Active Tasks

## multistart-per-lane-best
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1514 (issued 2026-08-23)
- issued: 2026-08-23
- prompt: active/multistart_per_lane_best.md
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/multistart-per-lane-best/
- epic: jax-inference-profiling (Phase 3 pre-req, CP-3 — PROGRAMME.md §7)
  - Repos: PyAutoFit (branch feature/multistart-per-lane-best)

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
