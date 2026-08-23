# Active Tasks

## transformed-message-factor-gradient-unpack
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1501 (issued 2026-08-19)
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

## bump-autonerves-floor
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/482 (issued 2026-08-23)
- prompt: active/bump_autoarray_autonerves_floor_after_stamp_release.md
- status: library-dev
- worktree: cloud session (no local worktree — PyAutoArray cloned at /home/user/pyautoarray)
- repos:
  - PyAutoArray (branch claude/small-datasets-regime-stamp-tlvobd)
- note: unblocked 2026-08-23 — autonerves 2026.8.23.1 is the first release carrying
  the SMALLDAT stamp (verified by unpacking both wheels from PyPI).
