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
- session: Claude Code CLI (Opus 5.5 main session + Opus subagent), 2026-09-28; session ID unavailable
- status: workspace-dev
- autonomy: supervised (header); plan approved in-session 2026-09-28 (workspace-only, no library edits)
- worktree: ~/Code/PyAutoLabs-wt/point-source-search-nautilus-leaf
- repos:
  - autolens_inference: feature/point-source-search-nautilus-leaf
- resume: "Branch pushed (2307eea), NO PR yet. Probe RAL job 366937 COMPLETED (seed 0: wall_s 56.6 s, 4,850 evals, per_call 4.72 us batched, likelihood_share 0.041% [single-basis 1.8%], all truth |dsigma|<0.74; row committed). Seeds 1-4 = RAL array 367140 (%1, euclid-ral-gpu-2). Next: sacct -j 367140; scp euclid_jump:/mnt/ral/jnightin/autolens_inference-wt-psleaf/results/searches/point_source/nautilus/simple/source_plane_solved/hpc_a100_jax_cpu_dense_fp64/search_seed{1..4}.{json,png} into the same path in the local worktree (+ hpc/batch_cpu/{output,error}/*367140* logs by hand); check each seed recovers truth; build_readme.py; wiki admission-bar entry (wiki/project/state.md); scripts/point_source/searches/README.md leaf note; ruff/pytest/check_submits; /ship_workspace to PR (Heart YELLOW ack: PyAutoMemory open PR 7d old; other YELLOW -> DRAFT); then remove RAL worktree: cd /mnt/ral/jnightin/autolens_inference && git worktree remove /mnt/ral/jnightin/autolens_inference-wt-psleaf"

## ecosystem-layers
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/440
- workspace-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/441
- issued: 2026-10-01
- prompt: active/explore_source_project_workspace_and_organ_level.md
- session: Codex (GPT-6), local, 2026-10-01
- status: awaiting-merge
- autonomy: supervised; research plan and feature/ecosystem-layers explicitly approved in-session
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/ecosystem-layers
- repos:
  - PyAutoBrain: feature/ecosystem-layers
- summary: Research library/project/organ roles and agent routing; one non-normative design note; evidence repos read-only.
- resume: Research note committed/pushed as 9ae0db9; pending-release PR https://github.com/PyAutoLabs/PyAutoBrain/pull/441 open. Independent Claude Fable 5.1 final draft review CLEAN; committed content matches reviewed SHA256 3345cd00f3354c428426ef87d9092ef7683ca570e5c3bb8941d1abc860ef9d0b. Sphinx zero warnings; 32 citations/17 pinned sources verified. Development-only Heart RED override recorded below and on issue/PR/autonomy log. Next: human /prm when every required CI leg is green; no merge authorization or background waiter. Task-bundle fable-final-review.md and research-validation.txt retain evidence.
- heart-red-override:
  - authorization: 'Live user "yes do it", then "I authorize", to the task-specific Brain #440 request for development-only commit, push and PR creation.'
  - scope: 'ecosystem-layers; feature/ecosystem-layers; no merge, release, rehearsal or CI bypass.'
  - snapshot: "2026-10-01T17:10:05.266085+00:00"
  - red-reason: "release validation FAILED (stage integrate)"
  - other-reason: "workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py)"
  - other-reason: "manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml"
  - other-reason: "manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml"
  - passed-gates: "Sphinx zero warnings; 32 citations/17 pinned source files; whitespace; independent Claude Fable 5.1 draft review CLEAN; scientific smoke N/A (research Markdown only). Reviewed SHA256 3345cd00f3354c428426ef87d9092ef7683ca570e5c3bb8941d1abc860ef9d0b."
