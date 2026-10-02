# Active Tasks

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
- status: awaiting-merge, workspace-release-gated
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/evaluation-grid-cap-field
- repos:
  - PyAutoGalaxy: feature/evaluation-grid-cap-field
  - autolens_workspace_test: feature/evaluation-grid-cap-field
  - autolens_profiling: feature/evaluation-grid-cap-field
- coordination: Human approved plan and separate-scope concurrency on 2026-10-02 alongside Galaxy docs, workspace numerical-audit and point-solver ledger tasks. Restrict edits to evaluation_grid, new operate tests, critical_curves CI and critical_curves campaign ledger/wiki. Prior phase-3a claim is released in its completion record; retained evidence worktree is not an active claim.
- resume: Phase 3b shipped: Galaxy#646 f19a3377; profiling#365 d8a46c3; workspace#343 fcd6bd5 is DRAFT until library fix is available to CI dependencies. Library-first gate; no release performed or phase-3b merge authorized. All local checks pass. Resume /prm for library/research when green, release-dependent workspace afterward. No further phase issued.

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

## lint-lychee-exclude-blob
- issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/3
- issued: 2026-10-02
- prompt: active/lint_lychee_exclude_github_blob_pages.md
- epic: profiling-organ-birth
- session: Claude Code CLI (Fable 5.1); session ID unavailable
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/lint-lychee-exclude-blob
- repos:
  - PyAutoPulse: feature/lint-lychee-exclude-blob
  - PyAutoEyes: feature/lint-lychee-exclude-blob
- library-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/4
- library-pr: https://github.com/PyAutoLabs/PyAutoEyes/pull/13
- pending-release: PyAutoPulse@https://github.com/PyAutoLabs/PyAutoPulse/pull/4
- pending-release: PyAutoEyes@https://github.com/PyAutoLabs/PyAutoEyes/pull/13
- resume: Corrective: PyAutoPulse main lint red on lychee 503s for github.com blob pages (token did not help). Exclude `^https://github\.com/.*/blob/` in both organs' lint.yml. Two PRs, end at PR-open, merge /prm (Pulse first).
