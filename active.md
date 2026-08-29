# Active Tasks

## wiki-currency-ci-drift
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/317
- prompt: active/fix_wiki_currency_ci_drift_in_the.md
- issued: 2026-08-28
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/wiki-currency-ci-drift
- classification: library (two assistant repos; docs-only, no workspace follow-up)
- repos:
  - autolens_assistant: feature/wiki-currency-ci-drift (b7a6964)
  - autogalaxy_assistant: feature/wiki-currency-ci-drift (98999f3)
- library-pr: autolens_assistant#117 (OPEN), autogalaxy_assistant#21 (OPEN)
- ci: `wiki-currency` PASS on both PRs (1m11s / 1m9s), `boundary` PASS on both — the leg that
  has been red on main since 2026-08-23 is green on both branches
- next-skill: /prm on autolens_assistant#117 + autogalaxy_assistant#21
- heart-red-at-ship: "PyAutoArray: 2 commit(s) behind origin" — verbatim from
  `pyauto-heart readiness --json` at 2026-08-29T01:56:44Z; pre-existing and unrelated
  (markdown-only changes in two other repos). Human acknowledged and authorised PR-open;
  not merged. No check was weakened to pass.
- note: the prompt's claim that autolens_assistant's `llms-chat.txt` and
  `chat_pack/01_api_surface.md` are stale on main was measured FALSE — `chat_bundle.py
  --check` is OK against the stack CI installs (2026.8.23.1). The FAIL only reproduces
  against a local source-tree PYTHONPATH, where regenerating would downgrade the version
  stamp to 2026.8.17.1 and inject unreleased autofit symbols. Left untouched.
