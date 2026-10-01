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

## ecosystem-routing-trial
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/444
- issued: 2026-10-01
- prompt: active/trial_ecosystem_role_routing.md
- session: Codex (GPT-6), local, 2026-10-01
- status: awaiting-merge
- autonomy: supervised; human "ok do it" authorized the recommended next routing trial
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/ecosystem-routing-trial
- repos:
  - PyAutoBrain: feature/ecosystem-routing-trial
- summary: Six-case exploratory baseline/checklist comparison of ecosystem routing; retain bounded evidence and report before changing machinery.
- workspace-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/445
- review: independent Claude Fable FINDINGS corrected; focused re-review CLEAN; all 14 committed files match reviewed SHA256 snapshot
- validation: Sphinx HTML 0 warnings; frozen input/response hashes and JSON verified; 36 source paragraphs checked against pinned commits; Heart GREEN score 100 at 2026-10-01T19:53:08.542623+00:00
- resume: PR #445 open at 6ea15719854f19a3c9a8f2d0c828fbfdfbc8e3cc. Both conditions correct on 6/6 change targets; checklist conflates decision owner in three fields while action routes stay correct. Retain guidance, no mandatory checklist. Context scoring leniency is disclosed as grading-time; no retrieval-efficiency claim. Review evidence at tmp/ecosystem-routing-trial-review/. Next human /prm judges every exact-head CI run/leg and merges/closes. Candidate organ-specification work proposed only; not filed.
