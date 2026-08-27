# Active Tasks

## required-workflow-file-drift
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/188
- issued: 2026-08-27
- prompt: active/required_workflow_file_drift.md
- status: ready-to-ship
- worktree: none — remote web session; PyAutoHeart cloned flat at /home/user/pyautoheart
- repos:
  - PyAutoHeart: feature/required-workflow-file-drift
- summary: |
    Implemented and pushed in the same session that filed the prompt.
    heart/checks/required_workflow_drift.py names a required workflow that has
    no workflow file — the state ci_status.rollup() can only render as a
    permanent `in_progress`, indistinguishable from a run in flight. Wired into
    state.py, tick.sh and readiness.py (YELLOW per missing workflow; a stale
    "unverified" reason when a repo's workflow list cannot be read, so a missing
    gate cannot hide behind a 403). 15 new tests; full suite 656 passed; the
    tenant-firewall gate verified clean with a canary.
    Branch pushed, NO PR opened — awaiting the go-ahead.

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
