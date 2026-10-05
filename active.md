# Active Tasks

## worktree-sh-root-activate-clobber
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/469
- issued: 2026-10-05
- prompt: active/worktree_sh_clobbers_root_activate.md
- session: claude (Opus 5.5, bundle pyautobrain-worktree-guards)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/pyautobrain-worktree-guards
- repos:
  - PyAutoBrain: feature/worktree-sh-root-activate-clobber
- summary: worktree_create never writes through a symlinked activate.sh (skip own names in sibling loops, rm -f before write) + opt-in worktree_repair_activate for bundle paths; hermetic test.
- bundle: pyautobrain-worktree-guards

## unregistered-worktree-guard
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/470
- issued: 2026-10-05
- prompt: active/unregistered_worktrees_invisible_to_conflict_guard.md
- session: claude (Opus 5.5, bundle pyautobrain-worktree-guards)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/pyautobrain-worktree-guards
- repos:
  - PyAutoBrain: feature/unregistered-worktree-guard
- summary: Conflict guard warns (exit unchanged) on unregistered on-disk worktrees of the requested repo; report-only worktree_audit_orphans lists orphans and zero-work STALE? claims.
- bundle: pyautobrain-worktree-guards

## cortex-find-script-symlink
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/471
- issued: 2026-10-05
- prompt: active/cortex_test_worktree_symlink.md
- session: claude (Opus 5.5, bundle pyautobrain-worktree-guards)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/pyautobrain-worktree-guards
- repos:
  - PyAutoBrain: feature/cortex-find-script-symlink
- summary: Cortex find_script walks ancestors without resolving symlinks (absolute() not resolve()); restore deleted witness test + tmp_path symlink regression test.
- bundle: pyautobrain-worktree-guards

## intake-declared-header-fields
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/472
- issued: 2026-10-05
- prompt: active/intake_agent_silently_drops_unknown_type_values.md
- session: claude (Opus 5.5, bundle pyautobrain-worktree-guards)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/pyautobrain-worktree-guards
- repos:
  - PyAutoBrain: feature/intake-declared-header-fields
- summary: Intake honours declared Target and Repos, flags unknown Type visibly (alias map hygiene->maintenance, else triage), splits leading header block from title/body.
- bundle: pyautobrain-worktree-guards

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
