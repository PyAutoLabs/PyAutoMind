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

## point-source-search-nautilus-leaf
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/15
- issued: 2026-09-28
- prompt: active/point_source_search_nautilus_leaf.md
- epic: point-source-cpu-speed
- session: Codex, resumed 2026-10-02; approved 2026-09-28 plan retained
- status: awaiting-merge
- autonomy: supervised (header); plan approved in-session 2026-09-28 (workspace-only, no library edits)
- worktree: ~/Code/PyAutoLabs-wt/point-source-search-nautilus-leaf
- repos:
  - autolens_inference: feature/point-source-search-nautilus-leaf
  - autolens_profiling: feature/point-source-search-nautilus-leaf
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/17
- ledger-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/361
- ledger-worktree: /home/jammy/Code/PyAutoLabs/.worktrees/point-source-resume/autolens_profiling
- resume: "All five RAL seeds recovered and imported (366937 + 367140), identical recorded library revisions, max truth offset 0.74 sigma; estimated warmed batched likelihood share 0.0405–0.0447%, wall 50.38–58.51 s. Inference results/docs and profiling campaign reconciliation prepared. 78 tests, ruff, dashboard, wall-submit checks pass; Heart GREEN 2026-10-02. Approved CI repair 2026-10-02: test-local one-sided 95% Student-t bounds, deterministic cases and unconditional gross guard; broad audit #362 planned. PRs open: autolens_inference#17 (e76566b) and autolens_profiling#361. Leaf import smoke passed. CI pending when checked. Next: human /prm when checks are green; no new phase issued. Keep RAL worktree/output until bulk outputs are preserved; do not force-remove it."
