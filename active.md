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

## point-image-pair-all-forward-grad-nan
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/767
- issued: 2026-10-04
- prompt: active/point_image_pair_all_forward_grad_nan.md
- session: claude (Opus 5.5 subagent, session_01S11WE9oj7Mvkfhc4EPBnyN; resume ID unavailable)
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/point-image-pair-all-forward-grad-nan
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/768 (draft, pending-release; Heart RED override = push+PR-open only, human /prm required)
- heart-override: human granted Heart RED development override (push + PR-open only, no merge) in-session 2026-10-04
- repos:
  - PyAutoLens: feature/point-image-pair-all-forward-grad-nan
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
- resume: 2026-10-04 phase-1 runs + wiki/index/results README rows done and all lints/pytest green in the worktree (uncommitted). PARKED at ship gate: pyauto-heart readiness RED "release validation FAILED (stage integrate)" (not caused by this task). Human Heart-RED override needed to commit/push/open PR; PR body drafted. Dashboard regen was timestamp-only, not committed.

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
