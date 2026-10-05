# Active Tasks

## nnls-memo-scattered-backoff
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/613
- issued: 2026-10-04
- prompt: active/nnls_memo_scattered_backoff.md
- session: claude (Opus 5.5 subagent, https://claude.ai/code/session_01S11WE9oj7Mvkfhc4EPBnyN)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/nnls-memo-scattered-backoff
- repos:
  - PyAutoArray: feature/nnls-memo-scattered-backoff
- summary: Per-key exponential back-off for the fnnls warm-start memo after consecutive fallbacks, so scattered (iid) streams stop paying for a bad seed every other solve; local-walk behaviour unchanged. Pulse task organs/PyAutoPulse/tasks/interferometer_nnls_memo_scattered_stream_guard.md.
- resume: implemented locally, ship pending human (Heart RED). Local commit 0d9bbecd on feature/nnls-memo-scattered-backoff (not pushed, no PR); 1975 tests green; witness iid on/off 1.49x->1.17x, walk 0.18x kept. Follow-up: autolens_profiling harnesses should call nnls_memo.memo_clear(); real Nautilus-replay witness still open. Status on issue #613.

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

## profiling-setup-contract
- issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/10
- issued: 2026-10-05
- prompt: active/profiling_setup_contract.md
- session: Codex; session ID unavailable
- status: awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-setup-contract
- repos:
  - PyAutoPulse: feature/profiling-setup-contract
- summary: Phase 1 of the approved full setup-first profiling refactor; v2 contract reader with v1 compatibility. Parent draft/feature/pyautopulse/profiling_setup_browser.md.
- authorization: human approved full plan and coordination on 2026-10-05; merges remain human /prm.
- validation: 184 tests passed; Ruff lint/format and offline snapshot/dashboard/Brain-state checks passed. No separate independent review required or claimed on this human-approved path.
- heart-red-override:
  - authorization: user "I authorize" (2026-10-05), responding to the explicit development-only shipping request for Pulse #10.
  - reasons: "release validation FAILED (stage integrate)"
  - scope: commit, push, pending-release PR only; merge separate, no release/rehearsal/CI bypass.
  - passed-gates: 184 tests; Ruff lint/format; pyauto-pulse check --offline.
- workspace-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/11
- head: d9d2377
- resume: phase 1 shipped to PR #11, awaiting human /prm and green CI. Next is project setup catalogue/exporter (parent plan phase 2), then browser and script/wiki/assistant migration. No merge authorized.

## community-board-readability
- issue: https://github.com/PyAutoLabs/PyAutoEars/issues/9
- issued: 2026-10-05
- session: Codex; session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/community-board-readability
- repos:
  - PyAutoEars: feature/community-board-readability
