# Active Tasks

## witt-wynne-projection
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/510
- issued: 2026-08-28
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/witt-wynne-projection
- repos:
  - autolens_workspace: feature/witt-wynne-projection

## wiki-currency-ci-drift
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/317
- prompt: active/fix_wiki_currency_ci_drift_in_the.md
- issued: 2026-08-28
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/wiki-currency-ci-drift
- classification: library (two assistant repos; docs-only, no workspace follow-up)
- repos:
  - autolens_assistant: feature/wiki-currency-ci-drift
  - autogalaxy_assistant: feature/wiki-currency-ci-drift
- heart-red-at-ship: "PyAutoArray: 2 commit(s) behind origin" — verbatim from
  `pyauto-heart readiness --json` at 2026-08-29T01:56:44Z; pre-existing and unrelated
  (markdown-only changes in two other repos). Human acknowledged and authorised PR-open;
  not merged. No check was weakened to pass.
- note: the prompt's claim that autolens_assistant's `llms-chat.txt` and
  `chat_pack/01_api_surface.md` are stale on main was measured FALSE — `chat_bundle.py
  --check` is OK against the stack CI installs (2026.8.23.1). The FAIL only reproduces
  against a local source-tree PYTHONPATH, where regenerating would downgrade the version
  stamp to 2026.8.17.1 and inject unreleased autofit symbols. Left untouched.
