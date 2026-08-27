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

## jax-traceback-filtering-release-harness
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/186 (issued 2026-08-27)
- issued: 2026-08-27
- prompt: active/jax_traceback_filtering_release_harness.md
- status: library-dev (organ repo — PyAutoHeart CI workflow, not a PyAuto library or workspace)
- worktree: ~/Code/PyAutoLabs-wt/jax-traceback-filtering-release-harness
- session: web session https://claude.ai/code/session_01SFoQCsxRTGjKk2YGe4R9Rs (not `claude --resume`-able)
- origin: split out of the retired prompt `complete/archive/shelved/interferometer_release_leg_oom.md`
  by /start_dev on 2026-08-27, when that prompt's headline OOM was found already shipped
  (`complete/2026/08/interferometer-start-here-integrate-oom.md`).
- repos:
