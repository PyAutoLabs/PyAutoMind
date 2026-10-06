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

## standards-discovery-deferred
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/474
- issued: 2026-10-06
- prompt: active/standards_discovery_deferred_destinations.md
- session: claude (Opus 5.5 subagent, CLI; session ID unavailable)
- status: pr-open, awaiting-human-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/614
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/110
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/standards-discovery-deferred
- repos:
  - PyAutoArray: feature/standards-discovery-deferred
  - euclid_strong_lens_modeling_pipeline: feature/standards-discovery-deferred
- tier: judge
- summary: Generated shared-standards AGENTS.md block for the two deferred destinations (AGENTS.md-only PRs), proceeding alongside nnls-memo-scattered-backoff and vis-lp-inspection-bundle claims with human approval. Human /prm.
- resume: AGENTS.md-only PRs open (Array#614, pipeline#110); bounded checks OK, universal 46/46 OK with both branches. Human /prm both, then remove firewall_gate.yml standards skip + universal audit + close #474.
