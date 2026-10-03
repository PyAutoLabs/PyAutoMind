# Active Tasks

## assistant-feedback-distribution
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/148
- issued: 2026-10-03
- prompt: active/assistant_feedback_distribution.md
- epic: community-organ-birth
- session: Codex Work; session ID unavailable
- location: /tmp/feedback-distribution (standalone clones)
- status: awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/458
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/149
- workspace-pr: https://github.com/PyAutoLabs/autofit_assistant/pull/53
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/32
- workspace-pr: https://github.com/PyAutoLabs/autocti_assistant/pull/34
- validation: 1168 Brain tests; 67 focused after boundary correction; four discovery/generation checks; two synthetic feedback checks passed.
- resume: Human /prm across all five PRs, Brain first; do not close phase 4 until all companions merge.
- repos:
  - PyAutoBrain: feature/assistant-feedback-distribution
  - autolens_assistant: feature/assistant-feedback-distribution
  - autofit_assistant: feature/assistant-feedback-distribution
  - autogalaxy_assistant: feature/assistant-feedback-distribution
  - autocti_assistant: feature/assistant-feedback-distribution
- summary: Distribute the canonical portable feedback workflow through assistant clone sync and actual discovery adapters.
- authorization: Existing whole-programme development authorization continued by "OK do thr next stuff"; judge-tier human /prm required, no release or merge.
- heart-red-override: Same previously reported published RED reasons; development only.
  - "release validation FAILED (stage integrate)"
  - "PyAutoHeart/workflows/Release Integrate: failure"
  - "PyAutoArray/Tests: red"
  - "PyAutoArray/Tests: red"
  - "PyAutoFit/Tests: red"
  - "autofit_workspace_test/Smoke Tests: red"
  - "autogalaxy_workspace_test/Smoke Tests: red"
  - "autolens_workspace_test/Smoke Tests: red"
  - "CI wall-clock: 26 gates \u00b7 slowest PyAutoBrain Nightly Release 83m \u00b7 1 slowed \u00b7 6 hang events"
  - "Release readiness: release validation FAILED (stage integrate)"
  - "PyAutoCTI/test_autocti/extract/two_d/parallel/test_parallel_fpr.py::test__estimate_capture: red"
  - "PyAutoNerves/test_autonerves/test_fitsable.py::test__output_to_fits: red"
  - "Unit-test timing: 3 test regressions (>3\u00d7 baseline), 1 slow (>1.5\u00d7)"
  - "autolens_test: red"
  - "Release validation: NOT release_ready \u2014 v2026.10.3.1.dev79901 profile=release (2026-10-03T07:43:31+00:00)"
  - "validation_report/stages/integrate: fail"
  - "autolens_assistant: red"
  - "autolens_profiling: red"
  - "autolens_workspace_test: red"
  - "Worktree drift: 0 orphan / 0 missing / 4 dirty"
  - "euclid_strong_lens_modeling_pipeline: red"

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

## evaluation-grid-cap-field
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/645
- issued: 2026-10-02
- prompt: active/evaluation_grid_cap_preserves_field.md
- epic: cluster-strong-lensing
- session: Codex; session ID unavailable
- status: library-merged, workspace-release-gated
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/evaluation-grid-cap-field
- repos:
  - PyAutoGalaxy: feature/evaluation-grid-cap-field
  - autolens_workspace_test: feature/evaluation-grid-cap-field
- coordination: Human approved plan and separate-scope concurrency on 2026-10-02 alongside Galaxy docs, workspace numerical-audit and point-solver ledger tasks. Restrict edits to evaluation_grid, new operate tests, critical_curves CI and critical_curves campaign ledger/wiki. Prior phase-3a claim is released in its completion record; retained evidence worktree is not an active claim.
- resume: 2026-10-02 /prm merged Galaxy#646 (2e36de4e) and profiling#365 (9d0b1317); autolens_profiling claim released (branch merged, Pulse tasks may proceed there). workspace#343 fcd6bd5 stays DRAFT until PyAutoGalaxy is released with the fix; then mark ready and /prm it to close the task. No release performed. No further phase issued.

- heart-ack:
  - "manifest drift: organism-map blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml"
  - "manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml"
- authorization: Human answered "Acknowledge both and ship" for phase 3b on 2026-10-02. No release authority; no additional phase queued.
- validation: Before fix six geometry failures/two compatibility passes; after fix 49 focused and 1315 full Galaxy tests pass. Real-decorator probe yields 1000x1000 at 0.06 arcsec with pixel-centre bounds ±29.97. Companion CI example passes standalone; full workspace smoke in progress.

- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/646
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/646
- library-commit: f19a3377; 1315 full and 49 focused tests pass. Linked CI witness and profiling ledger/wiki prepared; full workspace smoke in progress.
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/343
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/365
- final-validation: Galaxy 1315 passed; focused 49 passed; full companion smoke 33/33 in 501.91s (changed example 2.2s). Galaxy exact-head CI all green; new companion CI pending. Wiki/results-layout and whitespace checks pass. No raw phase-3a evidence changed.
