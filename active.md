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

## log-det-multistart-tag
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/175
- issued: 2026-08-26
- session: claude --resume session_01MdmS2jfUPi8BNjtDVBjBYX
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/log-det-multistart-tag
- repos:
  - autolens_profiling: feature/log-det-multistart-tag
- summary: |
    Reproduced on clean main: multi_start_unique_tag returns an identical tag for
    cholesky and slogdet arms, so the second resumes the first's .completed fit
    (RAL job 340576: 20 delaunay arms -> 10 output dirs). Fix is a PATH SUFFIX in
    autolens_profiling only -- tag on the SEARCHES_LOG_DET_METHOD env override
    only, never on the W8-resolved default, so an unset env keeps today's exact
    tag. No PyAutoFit change, no PyAutoFit worktree. Next: /start_workspace.
