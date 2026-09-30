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

## ep-moment-projection
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1654
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1656
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1656
- issued: 2026-09-30
- prompt: active/ep_hierarchical_scatter_moment_matching.md
- session: Claude Code CLI (Fable 5.1 main session + Opus subagents), 2026-09-30; session ID a45b0125
- status: workspace-dev (phase 2: autofit_workspace_test; library PyAutoFit#1656 merged 2026-09-30; supervised)
- autonomy: supervised (header); plan approved in-session 2026-09-30 (Plan Mode); default projection stays "mode"
- heart-red-override: authorised by the live human in the Claude Code session 2026-09-30 ~10:55 BST ("Override for all three (Recommended)", offered for PyAutoCortex#50 and "for opening the two PyAutoFit tasks (issue + worktree + plan; no merge, no release)"); RED reasons at the 10:51 BST tick: "PyAutoArray: 2 commit(s) behind origin"; "PyAutoLens: 2 commit(s) behind origin"; "release validation FAILED (stage integrate)"; scope: issue + worktree + plan; PR-open permitted; no merge/release; plan approved in-session ~11:20 BST via Plan Mode; PR-open authorised in-session 2026-09-30 ~11:50 BST ('Yes, both #1653 and #1654')
- parallel-claim: "ep-projection-exception merged 2026-09-30 (PyAutoFit#1655); claim released"
- worktree: ~/Code/PyAutoLabs-wt/ep-moment-projection
- repos:
  - PyAutoFit: feature/ep-moment-projection
  - autofit_workspace_test: feature/ep-moment-projection
- repo-note: PyAutoFit branch feature/ep-moment-projection is merged (PyAutoFit#1656, b13169e, 2026-09-30); the worktree is kept for phase 2, and the next phase claims autofit_workspace_test via /start_workspace
- summary: LaplaceOptimiser(projection="mode"|"moments"): nested quadrature (outer Gauss–Legendre over the scale variable on its support, inner conditional Laplace) ported from the analytic_ep_minimal referee; MeanField.from_weighted_nodes; SUCCESS/BAD_PROJECTION/FAILURE semantics; tests; phase 2 = autofit_workspace_test un-park via start_workspace after merge.

## streaming-p1-array-free-dataset
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/592
- issued: 2026-09-30
- prompt: active/streaming_p1_array_free_dataset.md
- epic: streaming-visibilities (phase 1 of 5; ledger draft/feature/autoarray/interferometer_from_stream_array_free_dataset.md)
- source: https://github.com/orgs/PyAutoLabs/discussions/13
- session: Claude Code CLI (Fable 5.1 main session + Opus subagents), 2026-09-30
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/streaming-p1-array-free-dataset
- autonomy: supervised (header); phase plan + design decisions (a)-(e) approved in-session 2026-09-30
- repos:
  - PyAutoArray: feature/streaming-p1-array-free-dataset
