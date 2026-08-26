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

## organ-repo-spelling-splits
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/287
- issued: 2026-08-26
- prompt: active/organ_repo_spellings_split_across_keys.md
- status: library-dev
- worktree: n/a — web-github session; the session's own PyAutoBrain + PyAutoMind
  clones are the checkout, on the designated branch below (no
  ~/Code/PyAutoLabs-wt/ worktree exists in this environment).
- repos:
  - PyAutoBrain: claude/organ-repo-spelling-splits-hbbms0
  - PyAutoMind: claude/organ-repo-spelling-splits-hbbms0
- summary: |
    Infrastructure task (organism repos only). Fourth instance of the
    hand-maintained-aliases vs derived-target-set defect class (#267, #269);
    this one closes the class. Keying decision taken up front per the prompt:
    organs key PREFIXED (`pyautobrain`), extending #271's rule — canonical key
    is the bare package name where the repo ships one, the repo name where it
    does not. Fix derives the bare/prefixed/package alias join from the body
    map (new `package:` identity key in repos.yaml) and adds three coverage
    guards to test_policy_seams.py. Sweep also covers PyAutoScientist and
    pyautolabs.github.io, both split/unresolvable and not named in the prompt.
    Heart unreachable from this environment — ship gate leg 4 will record NOT
    EVALUATED.
