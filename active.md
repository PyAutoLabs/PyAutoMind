# Active Tasks

## point-solver-magnification-plane-redshift
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/480 (filed 2026-04-28, pre-existing)
- issued: 2026-08-27
- prompt: active/point_solver_magnification_filter_ignores_plane_redshift.md
- status: library-dev
- branch: claude/point-source-json-regime-tmk7la (@PyAutoLens)
- repos:
  - PyAutoLens
- worktree-none: remote web session — no task worktree; the container checkout at
  /home/user/pyautolens is the working tree and is discarded with the session.
- note: no new issue was opened — PyAutoLens#480 already describes this bug, so /create_issue
  was deliberately skipped. Unblocks the two multiple_sources scripts in @autolens_workspace
  config/build/no_run.yaml and the parked
  draft/bug/pyautolens/point_source_json_datasets_record_no_regime.md.

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
