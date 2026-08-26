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

## repo-settings-bash-e-abort
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/293
- issued: 2026-08-26
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/294
- prompt: active/repo_settings_bash_e_abort.md
- worktree: ~/Code/PyAutoLabs-wt/repo-settings-bash-e-abort
- repos:
  - PyAutoBrain: feature/repo-settings-bash-e-abort
- summary: |
    Regression in PyAutoBrain#292: repo_settings.yml runs under GitHub's default
    `bash -e`, so the per-repo `before=$(gh api ... 2>/dev/null)` read aborts the
    script silently on the first unreadable repo, making the unreadable handler and
    the in-org/out-of-org failure split dead code. Fix: explicit `set +e`, replace
    two trailing `[ ] && failed=1` compounds with `if` blocks, and add the missing
    regression leg that exercises the run: block under `bash -e`.
