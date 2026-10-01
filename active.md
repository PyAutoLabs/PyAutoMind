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

## dashboard-portable-prompts
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/257
- issued: 2026-10-01
- prompt: active/dashboard_portable_skill_prompts.md
- session: Codex
- status: workspace-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dashboard-portable-prompts
- repos:
  - PyAutoBrain: feature/dashboard-portable-prompts
  - PyAutoHeart: feature/dashboard-portable-prompts
  - PyAutoHands: feature/dashboard-portable-prompts
  - PyAutoMemory: feature/dashboard-portable-prompts
  - PyAutoEyes: feature/dashboard-portable-prompts
  - PyAutoGut: feature/dashboard-portable-prompts
  - PyAutoScientist: feature/dashboard-portable-prompts
  - PyAutoCortex: feature/dashboard-portable-prompts
- heart-red-override:
  - authorization: "yes you may commit push open prs and merge once CI is green"
  - scope: Task PyAutoHeart#257, development shipping and merge on all-green CI during this turn; no release.
  - reasons: release validation FAILED (stage integrate); workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py)
  - gates: 896 relevant tests passed; independent review CLEAN; generated dashboard checks passed.
- resume: User authorized RED override and merge on green CI. Commit/push eight reviewed branches, open linked PRs, inspect every run/job, merge Brain first then consumers. Preserve canonical Cortex ledger edits.
- workspace-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/436
- workspace-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/259
- workspace-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/293
- workspace-pr: https://github.com/PyAutoLabs/PyAutoMemory/pull/113
- workspace-pr: https://github.com/PyAutoLabs/PyAutoEyes/pull/10
- workspace-pr: https://github.com/PyAutoLabs/PyAutoGut/pull/17
- workspace-pr: https://github.com/PyAutoLabs/PyAutoScientist/pull/38
- workspace-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/53
