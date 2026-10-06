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

## organ-prompt-headings
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/479
- issued: 2026-10-06
- prompt: active/organ_prompt_headings.md
- session: Codex (session ID unavailable)
- status: awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/organ-prompt-headings
- repos:
  - PyAutoBrain: feature/organ-prompt-headings
  - PyAutoEars: feature/organ-prompt-headings
  - PyAutoHeart: feature/organ-prompt-headings
  - PyAutoHands: feature/organ-prompt-headings
  - PyAutoMemory: feature/organ-prompt-headings
  - PyAutoPulse: feature/organ-prompt-headings
  - PyAutoInsight: feature/organ-prompt-headings
  - PyAutoNerves: feature/organ-prompt-headings
  - PyAutoGut: feature/organ-prompt-headings
  - PyAutoEyes: feature/organ-prompt-headings
  - PyAutoScientist: feature/organ-prompt-headings
- summary: Approved thirteen organ-named headings; preserve payloads/controls/work links; shared responsive heading and owner rollout. Human /prm.
- heart-ack:
  - autogalaxy_workspace: open PR 7d old
  - autolens_workspace: open PR 7d old
  - euclid_strong_lens_modeling_pipeline: open PR 7d old
  - release validation stale: source moved since rehearsal (PyAutoNerves)
- workspace-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/481
- workspace-pr: https://github.com/PyAutoLabs/PyAutoEars/pull/14
- workspace-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/286
- workspace-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/302
- workspace-pr: https://github.com/PyAutoLabs/PyAutoMemory/pull/117
- workspace-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/16
- workspace-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/7
- workspace-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/187
- workspace-pr: https://github.com/PyAutoLabs/PyAutoGut/pull/23
- workspace-pr: https://github.com/PyAutoLabs/PyAutoEyes/pull/19
- workspace-pr: https://github.com/PyAutoLabs/PyAutoScientist/pull/44
- resume: All eleven PRs opened; Brain, Ears, Memory, Insight and Gut confirmed merged. Remaining consumer CI pending. Human authorized ship and /prm with the recorded Heart YELLOW acknowledgement. Do not close task or remove worktree until all eleven branches merged.

## profiling-baseline-readiness
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/384
- issued: 2026-10-06
- prompt: active/profiling_baseline_readiness.md
- session: Codex (session ID unavailable)
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-baseline-readiness
- repos:
  - autolens_profiling: feature/profiling-baseline-readiness
- summary: Approved profiling redesign Phase 6; specification and pending campaign only. No jobs, pin changes, archive acceptance or charts. Human /prm.

## profiling-baseline-campaign
- issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/17
- issued: 2026-10-06
- prompt: active/profiling_baseline_campaign.md
- session: Codex (session ID unavailable)
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-baseline-campaign
- repos:
  - PyAutoPulse: feature/profiling-baseline-campaign
- summary: Approved profiling redesign Phase 6; specification and pending campaign only. No jobs, pin changes, archive acceptance or charts. Human /prm.
- coordination: Human explicitly allowed isolated Pulse work alongside organ-prompt-headings, limited to campaign/task metadata and generated board.
