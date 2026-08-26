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

## repo-settings-org-enumeration
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/291
- issued: 2026-08-26
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/292
- prompt: active/repo_settings_org_enumeration.md
- worktree: ~/Code/PyAutoLabs-wt/repo-settings-org-enumeration
- repos:
  - PyAutoBrain: feature/repo-settings-org-enumeration
- summary: |
    Switch repo_settings.yml from body-map derivation to live org enumeration, so a
    newly created repo inherits delete_branch_on_merge without being registered first.
    Adds --outside-owner to bin/branch_sweep_targets.py for the personal-account repos
    the org sweep cannot reach, and retires --include-self-sweeping (sole consumer is
    the line being replaced). Splits the failure policy so an out-of-org PATCH refusal
    warns instead of turning the weekly schedule red. Follows PyAutoBrain#290, which
    already shipped the sweep and removed /prm's remote-delete step.
