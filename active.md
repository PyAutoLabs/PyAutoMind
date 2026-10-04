# Active Tasks

## point-image-pair-all-forward-grad-nan
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/767
- issued: 2026-10-04
- prompt: active/point_image_pair_all_forward_grad_nan.md
- status: issued
- repos:
  - PyAutoLens: feature/pair-all-forward-grad-nan (not claimed)
- summary: Forward-mode (default gradient_mode) gradient is NaN for FitPositionsImagePairAll(Solved) because inf-sentinel padded model positions give inf*0 tangents in square_distance; fix with double-where in pair_all.py. Witness reproduced on 2026.10.4.1+3 CPU.

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

## interferometer-streaming-scaling
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/368
- issued: 2026-10-04
- session: claude-code subagent (Opus 5.5), https://claude.ai/code/session_01S11WE9oj7Mvkfhc4EPBnyN
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/interferometer-streaming-scaling
- prompt: active/interferometer_streaming_scaling.md
- repos:
  - autolens_profiling: feature/interferometer-streaming-scaling
- coordination: adds scripts/interferometer/streaming_scaling/, results/streaming_scaling/, wiki/campaigns/interferometer_streaming.md + one wiki/index.md row only; parallel autolens_profiling worktrees touch other paths.

## interferometer-decision-matrix-last-cell
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/369
- issued: 2026-10-04
- session: claude-code subagent (Opus 5.5), https://claude.ai/code/session_01S11WE9oj7Mvkfhc4EPBnyN
- status: library-dev, ship-blocked (Heart RED)
- worktree: ~/Code/PyAutoLabs-wt/interferometer-decision-matrix-last-cell
- prompt: active/interferometer_decision_matrix_last_cell.md
- repos:
  - autolens_profiling: feature/interferometer-decision-matrix-last-cell
- coordination: same session as interferometer-streaming-scaling (#368) and the human-approved priority order (2026-10-04). Touches only the decision-matrix note, results/breakdown/interferometer/alma_high/, wiki/campaigns/interferometer_likelihood.md and the existing interferometer wiki/index.md row; disjoint from #368's paths.
- resume: local commit 93a002a on feature/interferometer-decision-matrix-last-cell, lint + pytest green locally. Heart RED at ship gate: "release validation FAILED (stage integrate)" (pyauto-heart readiness 2026-10-04). Committed locally, NOT pushed, no PR. Ship needs a live human RED override (AUTONOMY.md "Human override for Heart RED (development only)") or a GREEN/YELLOW Heart; PR body drafted at scratchpad checkin/prA.md (session-local).

## point-source-wiki-reconcile
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/370
- issued: 2026-10-04
- session: claude-code subagent (Opus 5.5), https://claude.ai/code/session_01S11WE9oj7Mvkfhc4EPBnyN
- status: library-dev, ship-blocked (Heart RED)
- worktree: ~/Code/PyAutoLabs-wt/point-source-wiki-reconcile
- prompt: active/point_source_wiki_reconcile_cpu_completion.md
- repos:
  - autolens_profiling: feature/point-source-wiki-reconcile
- coordination: same session as interferometer-streaming-scaling (#368) and interferometer-decision-matrix-last-cell (#369), human-approved priority order 2026-10-04. Touches only the three point-source campaign pages, their wiki/index.md rows and results/notes/point_source_cpu_campaign.md.
- resume: local commit 0560284 on feature/point-source-wiki-reconcile, lint + pytest green locally. Heart RED at ship gate: "release validation FAILED (stage integrate)" (pyauto-heart readiness 2026-10-04). Committed locally, NOT pushed, no PR. Ship needs a live human RED override (AUTONOMY.md "Human override for Heart RED (development only)") or a GREEN/YELLOW Heart; PR body drafted at scratchpad checkin/prB.md (session-local).

## runtime-single-jit-median
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/371
- issued: 2026-10-04
- session: claude-code subagent (Opus 5.5), https://claude.ai/code/session_01S11WE9oj7Mvkfhc4EPBnyN
- status: library-dev, ship-blocked (Heart RED)
- worktree: ~/Code/PyAutoLabs-wt/runtime-single-jit-median
- prompt: active/runtime_cell_single_jit_gpu_warmup_option_a.md
- repos:
  - autolens_profiling: feature/runtime-single-jit-median
- coordination: same session as #368/#369/#370, human-approved priority order 2026-10-04 (option (a) decided). Touches scripts/misc/likelihood_breakdown/timing.py, the source-plane runtime cell, build_dashboard.py, dashboard/, tests and the source-plane ledger caveat.
- resume: local commit 87a7fcc on feature/runtime-single-jit-median, lint + pytest green locally. Heart RED at ship gate: "release validation FAILED (stage integrate)" (pyauto-heart readiness 2026-10-04). Committed locally, NOT pushed, no PR. Ship needs a live human RED override (AUTONOMY.md "Human override for Heart RED (development only)") or a GREEN/YELLOW Heart; PR body drafted at scratchpad checkin/prC.md (session-local).
