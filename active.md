# Active Tasks

## nnls-memo-scattered-backoff
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/613
- issued: 2026-10-04
- prompt: active/nnls_memo_scattered_backoff.md
- session: claude (Opus 5.5 subagent, https://claude.ai/code/session_01S11WE9oj7Mvkfhc4EPBnyN)
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/nnls-memo-scattered-backoff
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/615
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/615
- repos:
  - PyAutoArray: feature/nnls-memo-scattered-backoff
- summary: Per-key exponential back-off for the fnnls warm-start memo after consecutive fallbacks, so scattered (iid) streams stop paying for a bad seed every other solve; local-walk behaviour unchanged. Pulse task organs/PyAutoPulse/tasks/interferometer_nnls_memo_scattered_stream_guard.md.
- resume: shipped 2026-10-07 as PyAutoArray#615 (rebased e54123b4, pending-release, Heart YELLOW acknowledged; 1975 passed, 4 xfailed). No workspace impact. Next: CI green then human /prm. Follow-ups on #613 (not merge gates): real Nautilus-replay witness; autolens_profiling harnesses should call nnls_memo.memo_clear().

## vis-lp-inspection-bundle
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/102
- issued: 2026-09-22
- session: claude (Fable CLI, 2026-09-23; resumed from Codex 2026-09-22)
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/vis-lp-inspection-bundle
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/vis-lp-inspection-bundle
- summary: Add an explicit vis_lp-only inspection mode that combines the main normal-model output tree with the 100-lens SED/Sersic tree, without requiring vis_pix or selecting the other 200 main-tree lenses.
- resume: Implemented + committed locally as c6b514d on feature/vis-lp-inspection-bundle (133 tests green, not pushed). Human reviews diff (scratchpad part1_diff.txt) before ship_workspace; then sync tooling to the euclid_dr1 science clone/RAL and submit the 4,922-tile vis_lp-only bundle (OUTPUT_DIR=dr1_full, INITIAL_SEARCH_NAME=vis_lp, DATASET_NAMES_PATH=all, TAR_TO set) as a Cortex run.

## dashboard-checkin-prompts
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/484
- issued: 2026-10-07
- prompt: active/dashboard_checkin_prompts.md
- session: Codex local
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dashboard-checkin-prompts
- repos:
  - PyAutoBrain: feature/dashboard-checkin-prompts
  - PyAutoEars: feature/dashboard-checkin-prompts
  - PyAutoHeart: feature/dashboard-checkin-prompts
  - PyAutoHands: feature/dashboard-checkin-prompts
  - PyAutoMemory: feature/dashboard-checkin-prompts
  - PyAutoPulse: feature/dashboard-checkin-prompts
  - PyAutoInsight: feature/dashboard-checkin-prompts
  - PyAutoNerves: feature/dashboard-checkin-prompts
  - PyAutoGut: feature/dashboard-checkin-prompts
  - PyAutoEyes: feature/dashboard-checkin-prompts
  - PyAutoScientist: feature/dashboard-checkin-prompts
- summary: Implement the thirteen individually approved check-in prompts; no dashboard restructuring, merge or publication.
- resume: Approved wording is in the prompt. Isolated owner worktrees; preserve Heart dynamic evidence and Cortex timestamp. Tests and ship gate pending.
