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

## restore-dashboard-green
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/274
- issued: 2026-10-04
- prompt: active/restore_dashboard_green.md
- session: Codex (GPT-6), session ID unavailable; resumed 2026-10-05
- status: library-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/restore-dashboard-green
- repos:
  - PyAutoHeart: feature/restore-dashboard-green
- summary: Bounded release integration recovery; report emitter dependency fix and exact-wheel execution-stall investigation. Broader dashboard scope remains deferred.
- corrective-red:
  - authorization: Live user "Yes I authroize" to corrective investigation and repairs under Heart #274 for the surfaced exact RED reason.
  - evidence: https://github.com/PyAutoLabs/PyAutoHeart/issues/274#issuecomment-5991210852
  - reason: release validation FAILED (stage integrate)
  - scope: causal investigation, tested correction, commit/push/pending-release PR; human merge separate; no production release or gate bypass.
  - validation: 119 focused and1222 full Heart tests PASS; actual empty-venv emitter replay PASS retaining22 adverse rows; independent Sol CLEAN; no scientific API/smoke impact.
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/281
- pending-release: PyAutoHeart@https://github.com/PyAutoLabs/PyAutoHeart/pull/281
- resume: PR281 head6b7bd40 fixes report dependency and adds pinned current-incident diagnostic.141 targeted/1222 preceding full tests and expanded independent Sol review PASS. Hosted bounded replay37287631900 PASS33.666s, zero provenance errors; local fresh fit40.851s no-repro. Final-head CI both Python legs green. Latest integration37217670612 remains RED. Next human mergePR281 then fresh wheels/integration (Lens main advanced to dffea805). No production release.

## profiling-setup-page
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/378
- issued: 2026-10-05
- prompt: active/profiling_setup_page.md
- session: Codex; session ID unavailable
- status: shipping
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-setup-page
- repos:
  - autolens_profiling: feature/profiling-setup-page
- summary: Phase 3a of the approved profiling refactor; dataset/model/instrument setup browser using merged catalogue #377 and shared theme. Pulse front page follows separately.
- authorization: live "$prm and continue" plus approved parent Phase 3 plan; human merge; no bulk profiling. Phase 2 shipping override does not authorize Phase 3 shipping.

- progress: Project browser implemented with shared theme, dataset/model disclosures, selectors, verified lazy shards, history, missing coverage, linear scoped charts and evidence disclosures. Pulse front page follows in its own PR.
- validation: 1061 full tests pass (5 skips); final 48 focused tests pass; final Chromium interaction/responsive/error-state suite passes; seven section smokes pass; Ruff and existing metadata/generation/Pulse checks pass; inline visual/code review complete.
- previous-shipping-blocker: Heart RED `release validation FAILED (stage integrate)`; no task-specific #378 shipping override yet. Source remains uncommitted/unpushed.
- pr-draft: .worktrees/profiling-setup-page/phase3-pr-body.md
- previews: .worktrees/profiling-setup-page/browser-artifacts/setup-1280.png and setup-390.png

- heart-red-override: Live user "I authroize, continue and do the next phase" responding to the explicit #378 development-shipping override request. Exact RED `release validation FAILED (stage integrate)`; 1061 full/48 final focused tests, Chromium interactions, seven smokes and inline review pass. Commit/push/PR only; merge separate, no release.
