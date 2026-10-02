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

## benchmark-forward-model-consistency
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/142
- issued: 2026-10-02
- prompt: active/benchmark_forward_model_consistency.md
- session: Codex; session ID unavailable
- status: workspace-dev
- bundle: assistant
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/assistant
- repos:
  - autolens_assistant: feature/benchmark-forward-model-consistency
- resume: Plan approved 2026-10-02. Sequential execution in shared worktree; one issue and PR per member. Merge remains human.

## benchmark-positions-inference
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/143
- issued: 2026-10-02
- prompt: active/benchmark_positions_initialised_inference.md
- session: Codex; session ID unavailable
- status: workspace-dev
- bundle: assistant
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/assistant
- repos:
  - autolens_assistant: feature/benchmark-positions-inference
- resume: Plan approved 2026-10-02. Sequential execution in shared worktree; one issue and PR per member. Merge remains human.

## bootstrap-smoke-codex
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/144
- issued: 2026-10-02
- prompt: active/bootstrap_smoke_codex_and_bench_pr.md
- session: Codex; session ID unavailable
- status: workspace-dev
- bundle: assistant
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/assistant
- repos:
  - autolens_assistant: feature/bootstrap-smoke-codex
- resume: Plan approved 2026-10-02. Sequential execution in shared worktree; one issue and PR per member. Merge remains human.

## colab-refinement-throughout
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/145
- issued: 2026-10-02
- prompt: active/colab_refinement_throughout.md
- session: Codex; session ID unavailable
- status: workspace-dev
- bundle: assistant
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/assistant
- repos:
  - autolens_assistant: feature/colab-refinement-throughout
- resume: Plan approved 2026-10-02. Sequential execution in shared worktree; one issue and PR per member. Merge remains human.

## critical-curves-dispatch-audit
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/337
- issued: 2026-10-02
- prompt: active/critical_curves_dispatch_audit.md
- epic: cluster-strong-lensing
- session: Codex, 2026-10-02
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/critical-curves-dispatch-audit
- repos:
  - autolens_workspace_test: feature/critical-curves-dispatch-audit
  - autolens_profiling: feature/critical-curves-dispatch-audit
- coordination: Human authorized concurrent separate scope alongside point-source-search-nautilus-leaf / profiling#361 on 2026-10-02.
- resume: Plan approved with “go”; standalone CPU research, phase 3a. Implement bounded current-dispatch and geometry/timing audit, validate, ship_workspace. Concurrent unissued cluster_curves_engine_dispatch draft remains a candidate pending these results. No later issue queue.

## over-sample-snr-helper
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/602
- issued: 2026-10-02
- prompt: active/over_sample_size_via_snr_from.md
- session: Codex GPT-6; session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/autoarray-bundle-1
- repos:
  - PyAutoArray: feature/over-sample-snr-helper
  - PyAutoGalaxy: feature/over-sample-snr-helper
- resume: Bundle autoarray — bundle 1; plan and branch approved 2026-10-02. One execution delegate per member; sequential shared worktrees; linked companion PRs authorized. Preserve unregistered sparse-operator-oversampling-cache worktree. Parent owns lifecycle and shipping. No merge authorization.

## mesh-interpolator-numerics-audit
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/603
- issued: 2026-10-02
- prompt: active/final_numerics_audit_of_every_mesh_interpolator.md
- session: Codex GPT-6; session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/autoarray-bundle-1
- repos:
  - PyAutoArray: feature/mesh-interpolator-numerics-audit
  - autolens_workspace_test: feature/mesh-interpolator-numerics-audit
- resume: Bundle autoarray — bundle 1; approved plan 2026-10-02. Sequential shared worktrees; branch selected only when prior member is shipped. Linked companion PRs and coordination with critical-curves-dispatch-audit explicitly authorized by user. Preserve all other worktrees. No merge authorization.

## fit-util-masked-division
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/604
- issued: 2026-10-02
- prompt: active/fit_util_masked_division_grad_nan.md
- session: Codex GPT-6; session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/autoarray-bundle-1
- repos:
  - PyAutoArray: feature/fit-util-masked-division
  - autolens_workspace_test: feature/fit-util-masked-division
- resume: Bundle autoarray — bundle 1; approved plan 2026-10-02. Sequential shared worktrees; branch selected only when prior member is shipped. Linked companion PRs and coordination with critical-curves-dispatch-audit explicitly authorized by user. Preserve all other worktrees. No merge authorization.

## mesh-geometry-transformed-areas
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/605
- issued: 2026-10-02
- prompt: active/mesh_geometry_areas_transformed_adapt_image_indexerror.md
- session: Codex GPT-6; session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/autoarray-bundle-1
- repos:
  - PyAutoArray: feature/mesh-geometry-transformed-areas
  - autolens_workspace_test: feature/mesh-geometry-transformed-areas
- resume: Bundle autoarray — bundle 1; approved plan 2026-10-02. Sequential shared worktrees; branch selected only when prior member is shipped. Linked companion PRs and coordination with critical-curves-dispatch-audit explicitly authorized by user. Preserve all other worktrees. No merge authorization.
