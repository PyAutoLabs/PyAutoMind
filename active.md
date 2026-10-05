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

## niek-euclid-style-review
- issue: https://github.com/Jammy2211/euclid_assistant/issues/12
- issued: 2026-10-05
- prompt: active/niek_full_style_review.md
- session: Codex GPT-6
- status: awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/niek-euclid-style-review
- repos:
  - euclid_assistant: feature/niek-euclid-style-review
- summary: Approved full Style Guide/PDD coverage audit, assistant improvements, Niek manuscript corrections, independent Opus 5.5 review, and author ZIP. No merge authority.
- pr: https://github.com/Jammy2211/euclid_assistant/pull/13
- resume: Assistant commit 68c8e9c pushed; pending-release PR #13 open. 85 tests passed, 1 optional Vale skip; CLI smoke and independent Opus 5.5 review passed. Author ZIP delivered and clean-extraction build verified. Human /prm for merge.
- authorization: User replied “ok do it, I approve” to issue #12 development-shipping request. Heart recovered from RED `PyAutoGalaxy: CI failure` to GREEN (100, 2026-10-05T17:25:39Z) before commit; no RED override exercised. No merge/release authority.

## board-navigation-ears
- issue: https://github.com/PyAutoLabs/PyAutoEars/issues/11
- issued: 2026-10-05
- prompt: active/board_navigation_ears.md
- session: Codex (session ID unavailable)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/board-navigation-ears
- repos:
  - PyAutoEars: feature/board-navigation-ears
- summary: Approved all-board navigation adoption; depends on Brain PR #464. User invoked /prm for this execution turn.

## board-navigation-memory
- issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/115
- issued: 2026-10-05
- prompt: active/board_navigation_memory.md
- session: Codex (session ID unavailable)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/board-navigation-memory
- repos:
  - PyAutoMemory: feature/board-navigation-memory
- summary: Approved all-board navigation adoption; depends on Brain PR #464. User invoked /prm for this execution turn.

## board-navigation-heart
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/282
- issued: 2026-10-05
- prompt: active/board_navigation_heart.md
- session: Codex (session ID unavailable)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/board-navigation-heart
- repos:
  - PyAutoHeart: feature/board-navigation-heart
- summary: Approved all-board navigation adoption; depends on Brain PR #464. User invoked /prm for this execution turn.

## board-navigation-hands
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/298
- issued: 2026-10-05
- prompt: active/board_navigation_hands.md
- session: Codex (session ID unavailable)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/board-navigation-hands
- repos:
  - PyAutoHands: feature/board-navigation-hands
- summary: Approved all-board navigation adoption; depends on Brain PR #464. User invoked /prm for this execution turn.

## board-navigation-pulse
- issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/14
- issued: 2026-10-05
- prompt: active/board_navigation_pulse.md
- session: Codex (session ID unavailable)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/board-navigation-pulse
- repos:
  - PyAutoPulse: feature/board-navigation-pulse
- summary: Approved all-board navigation adoption; depends on Brain PR #464. User invoked /prm for this execution turn.

## board-navigation-nerves
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/185
- issued: 2026-10-05
- prompt: active/board_navigation_nerves.md
- session: Codex (session ID unavailable)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/board-navigation-nerves
- repos:
  - PyAutoNerves: feature/board-navigation-nerves
- summary: Approved all-board navigation adoption; depends on Brain PR #464. User invoked /prm for this execution turn.

## board-navigation-gut
- issue: https://github.com/PyAutoLabs/PyAutoGut/issues/21
- issued: 2026-10-05
- prompt: active/board_navigation_gut.md
- session: Codex (session ID unavailable)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/board-navigation-gut
- repos:
  - PyAutoGut: feature/board-navigation-gut
- summary: Approved all-board navigation adoption; depends on Brain PR #464. User invoked /prm for this execution turn.

## board-navigation-scientist
- issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/42
- issued: 2026-10-05
- prompt: active/board_navigation_scientist.md
- session: Codex (session ID unavailable)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/board-navigation-scientist
- repos:
  - PyAutoScientist: feature/board-navigation-scientist
- summary: Approved all-board navigation adoption; depends on Brain PR #464. User invoked /prm for this execution turn.

## board-navigation-eyes
- issue: https://github.com/PyAutoLabs/PyAutoEyes/issues/16
- issued: 2026-10-05
- prompt: active/board_navigation_eyes.md
- session: Codex (session ID unavailable)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/board-navigation-eyes
- repos:
  - PyAutoEyes: feature/board-navigation-eyes
- summary: Approved all-board navigation adoption; depends on Brain PR #464. User invoked /prm for this execution turn.

## board-navigation-insight
- issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/4
- issued: 2026-10-05
- prompt: active/board_navigation_insight.md
- session: Codex (session ID unavailable)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/board-navigation-insight
- repos:
  - PyAutoInsight: feature/board-navigation-insight
- summary: Approved all-board navigation adoption; depends on Brain PR #464. User invoked /prm for this execution turn.
