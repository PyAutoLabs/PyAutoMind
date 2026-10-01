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

## point-solver-image-accuracy
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/333
- issued: 2026-10-01
- prompt: active/point_solver_image_accuracy.md
- epic: cluster-strong-lensing
- session: Codex; session ID unavailable
- status: awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/point-solver-image-accuracy
- repos:
  - autolens_workspace_test: feature/point-solver-image-accuracy
- approval: Live user “I approve” approved phase 1d plan and development-only RED override through PR creation; no merge/release.
- heart-red-override:
  - reasons: "release validation FAILED (stage integrate)"
  - additional: "workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py)"; "manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml"
  - gates: bounded cell, saved evidence/provenance/read-only summary, padding and image-plane checks, full workspace smoke, formatting/compile/JSON/diff.
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/334
- resume: PR #334 open pending-release at 4bec6a7. Final 32-row sweep/provenance and geometry PASS; evidence controls, padding 12/12, image-plane/JIT and smoke 32/32 PASS; in-session review. NO-GO: three non-converged false accepts; convergence requirement misses closest-cusp images. Wait for human /prm and green CI. No merge/release or later issue authorized.
- validation-logs: /home/jammy/Code/PyAutoLabs/.worktrees/point-solver-image-accuracy/scratch/
- ship-heart: RED reason unchanged at 2026-10-01T10:10:03.098482+00:00; approved development-only override exercised through PR-open.

## memory-digest-state
- issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/111
- issued: 2026-10-01
- prompt: active/cockpit_digest_freshness.md
- session: Codex; session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/memory-digest-state
- repos:
  - PyAutoMemory: feature/memory-digest-state
- approval: User “ok then go” approved digest freshness increment; no merge authority.
- resume: Implement structured digest observations/actions, validate and ship through Heart gate.
