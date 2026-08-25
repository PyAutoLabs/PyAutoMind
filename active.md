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

## weekly-smoke-timings-naming
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/181 (issued 2026-08-25)
- issued: 2026-08-25
- prompt: active/weekly_smoke_timings_artifact_naming.md
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/weekly-smoke-timings-naming
- repos:
  - PyAutoHeart (branch claude/weekly-smoke-timings-naming-012fuj)
- note: web-github session — no local worktree created; work done in the session clone
  and pushed to the branch above. Decision recorded on the issue: option (a), the named
  `smoke-timings-*` upload added to workspace-validation.yml's script and notebook legs.

