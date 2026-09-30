# Active Tasks

## interferometer-decision-matrix
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/356
- issued: 2026-09-30
- prompt: active/interferometer_decision_matrix.md
- epic: interferometer-likelihood-campaign
- session: Claude Code CLI (Opus 5.5 main session + Opus subagent), 2026-09-30
- status: workspace-dev
- autonomy: supervised (header); plan approved in-session 2026-09-30 via Plan Mode (workspace-only, no library edits)
- parallel-claim: "autolens_profiling is also claimed by raw-pdip-forward-polish (workspace-pending). File sets disjoint (this task: instruments/interferometer.py, new hpc/batch_{cpu,gpu}/submit_breakdown_interferometer_*_{radius_gaps,sdp81}_*, new results/breakdown/interferometer/** JSONs, results/notes/interferometer_likelihood_decision_matrix_2026_09.md, wiki/campaigns/interferometer_likelihood.md, wiki/index.md row, results/README.md Campaign findings paragraph; raw-pdip: results/notes/linear_solver_accuracy_2026_09.md, wiki/campaigns/linear_solver_accuracy.md, euclid_latent.py). Whichever ships second merges results/README.md. Parallel claim human-approved 2026-09-30 with the plan."
- worktree: ~/Code/PyAutoLabs-wt/interferometer-decision-matrix
- repos:
  - autolens_profiling: feature/interferometer-decision-matrix
- resume: "Issued; next start_workspace (worktree), then delegated execution: sdp81 preset, RAL CPU gap array + sdp81 CPU/A100 jobs, note."

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
- session: Claude Code CLI (Opus 5.5 main session + Opus subagent), 2026-09-28; session ID unavailable
- status: workspace-dev
- autonomy: supervised (header); plan approved in-session 2026-09-28 (workspace-only, no library edits)
- worktree: ~/Code/PyAutoLabs-wt/point-source-search-nautilus-leaf
- repos:
  - autolens_inference: feature/point-source-search-nautilus-leaf
- resume: "Branch pushed (2307eea), NO PR yet. Probe RAL job 366937 COMPLETED (seed 0: wall_s 56.6 s, 4,850 evals, per_call 4.72 us batched, likelihood_share 0.041% [single-basis 1.8%], all truth |dsigma|<0.74; row committed). Seeds 1-4 = RAL array 367140 (%1, euclid-ral-gpu-2). Next: sacct -j 367140; scp euclid_jump:/mnt/ral/jnightin/autolens_inference-wt-psleaf/results/searches/point_source/nautilus/simple/source_plane_solved/hpc_a100_jax_cpu_dense_fp64/search_seed{1..4}.{json,png} into the same path in the local worktree (+ hpc/batch_cpu/{output,error}/*367140* logs by hand); check each seed recovers truth; build_readme.py; wiki admission-bar entry (wiki/project/state.md); scripts/point_source/searches/README.md leaf note; ruff/pytest/check_submits; /ship_workspace to PR (Heart YELLOW ack: PyAutoMemory open PR 7d old; other YELLOW -> DRAFT); then remove RAL worktree: cd /mnt/ral/jnightin/autolens_inference && git worktree remove /mnt/ral/jnightin/autolens_inference-wt-psleaf"

## point-solver-padding-backend
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/759
- issued: 2026-09-30
- prompt: active/point_solver_padding_backend.md
- epic: cluster-strong-lensing
- session: Codex; session ID unavailable
- status: library-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/point-solver-padding-backend
- repos:
  - PyAutoLens: feature/point-solver-padding-backend
  - autolens_workspace_test: feature/point-solver-padding-backend
- heart-red-override: Live user “I authorize” in response to phase-1b task-specific development-only override request. Exact RED “release validation FAILED (stage integrate)”. Plan approved with “go”. Commit/push/open PRs only; no merge/release authority. Gates passed: 776 library tests (1 xfailed), 12 focused cases, 32 smoke scripts, in-session review. Fresh main-checkout Heart at 18:35:14Z confirmed the same exact RED reason.
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/760
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/330
- release-gate: PyAutoLens
- validation: PyAutoLens 776 passed, 1 xfailed; focused regression 12/12 passed; full workspace smoke 32/32 passed; Black/diff checks and in-session review passed. No independent review claimed on supervised path.
- resume: Human review and explicit merge command required. Library #760 before workspace #330; workspace release gate applies. Phase 1 remains incomplete; no next-phase issue queued.
