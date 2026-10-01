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

## streaming-p4-light-profile-identity
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/598
- issued: 2026-10-01
- prompt: active/streaming_p4_light_profile_identity.md
- epic: streaming-visibilities (phase 4 of 5; ledger draft/feature/autoarray/interferometer_from_stream_array_free_dataset.md)
- source: https://github.com/orgs/PyAutoLabs/discussions/13
- session: Claude Code CLI (Fable 5.1 main session + Opus subagents), 2026-10-01
- status: library-dev
- autonomy: supervised (header); plan approved in-session 2026-10-01 (Plan Mode)
- worktree: ~/Code/PyAutoLabs-wt/streaming-p4-light-profile-identity
- repos:
  - PyAutoArray: feature/streaming-p4-light-profile-identity
  - PyAutoGalaxy: feature/streaming-p4-light-profile-identity
  - PyAutoLens: feature/streaming-p4-light-profile-identity
- summary: Ordinary (non-linear) light profiles fit array-free via data_term - 2 i_p.d~ + i_p.W~i_p (DatasetInterface data_term override; no-inversion chi_squared hook); profile_visibilities never formed.
- resume: Issue + plan on #598; next /start_library (Array -> Galaxy -> Lens), red-check parity tests on unfixed source first (fast_chi_squared would silently use the unsubtracted data_term).

## point-solver-duplicate-policy
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/331
- issued: 2026-10-01
- prompt: active/point_solver_duplicate_policy.md
- epic: cluster-strong-lensing
- session: Codex; session ID unavailable
- status: awaiting-input
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/point-solver-duplicate-policy
- repos:
  - autolens_workspace_test: feature/point-solver-duplicate-policy
- resume: Implemented locally; 54 scalar rows + 6 vmap controls complete, padding 12/12 and full smoke 32/32 passed, image-plane parity and formatting/JSON/diff checks passed, in-session review complete. NO-GO for tested grouping heuristics; close-cusp candidates exceed cap 20 (uncapped max 87), with a four-NumPy/three-JAX missing-image witness. Next: live task-specific Heart RED development override, then commit/push/open pending-release PR using tmp/duplicate-pr.md in the separate Mind planning checkout. No feature commit/push/PR yet; no merge/release authorized.
- heart-block: RED "release validation FAILED (stage integrate)" (snapshot 2026-10-01T08:11:41.393196+00:00; current readiness re-read at handoff). No override granted.
- validation-logs: /home/jammy/Code/PyAutoLabs/.worktrees/point-solver-duplicate-policy/scratch/{duplicate-policy,padding,image-plane,smoke}.log
