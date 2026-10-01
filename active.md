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

## cloud-board-validation-evidence
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/263
- issued: 2026-10-01
- session: Codex, local health remediation
- status: awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/cloud-board-validation-evidence
- repos:
  - PyAutoHeart: feature/cloud-board-validation-evidence
- notes: Infrastructure task. Plan approved in chat; no release or publication included.
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/264
- validation: 1139 full-suite tests plus 40 focused tests pass; tenant firewall passes; real-artifact isolated readiness GREEN/100; live Heart GREEN/100.
- resume: Judge every exact-head CI leg through prm; merge and publish are separate actions.

## ecosystem-routing-trial
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/444
- issued: 2026-10-01
- prompt: active/trial_ecosystem_role_routing.md
- session: Codex (GPT-6), local, 2026-10-01
- status: awaiting-input
- autonomy: supervised; human "ok do it" authorized the recommended next routing trial
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/ecosystem-routing-trial
- repos:
  - PyAutoBrain: feature/ecosystem-routing-trial
- summary: Routing trial plus authorized profiling/inference organ specification; proposal only, no implementation or new organ.
- workspace-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/445
- review: original routing trial independently reviewed CLEAN; organ-specification continuation self-checked only. User explicitly instructed no further Fable reviews.
- validation: Sphinx HTML 0 warnings; frozen input/response hashes and JSON verified; 36 source paragraphs checked against pinned commits; Heart GREEN score 100 at 2026-10-01T19:53:08.542623+00:00
- ship-blocker: Heart RED score 80 at 2026-10-01T20:02:44.036627+00:00 — autofit_workspace: Smoke Tests failure on main
- resume: Organ specification complete locally at docs/research/profiling_inference_organs.md, with a link from the trial report; uncommitted/unpushed behind current Heart RED. Sphinx HTML zero warnings; seven pinned source objects verified; frozen trial files unchanged. PR #445 still contains only the earlier trial commit 6ea1571 (all three CI jobs passed). Need fresh GREEN or an explicit development-only override for the exact current RED reasons before committing/pushing this extension. Rewrite PR title/body around combined final scope after push. Do not call Fable for reviews; do not describe the extension as independently reviewed. No organ repositories or follow-up implementation tasks created.
