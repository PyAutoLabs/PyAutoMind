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

## point-solver-duplicate-policy
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/331
- issued: 2026-10-01
- prompt: active/point_solver_duplicate_policy.md
- epic: cluster-strong-lensing
- session: Codex; independent Claude Fable review session 2eb5a6d4-323e-4a3f-bd9b-6506a6de2b0f
- status: awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/point-solver-duplicate-policy
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/332
- repos:
  - autolens_workspace_test: feature/point-solver-duplicate-policy
- resume: PR #332 open, pending-release, head 2941721. Independent Fable CLEAN after all six findings resolved; final exact-script sweep 54 scalar + 6 vmap, provenance/read-only summarize PASS, padding 12/12, image-plane/JIT PASS, smoke 32/32. NO-GO for tested grouping rules: uncapped NumPy image-position failures and JAX truncation are separate problems (18 rows exceed cap; 12 actually truncate). Future zero-candidate coverage handling is advisory only. Wait for human /prm and green CI; no merge/release authorized, no later phase queued.
- heart-red-override:
  - authorization: Live user "ok review with fable" to the #331 task-specific development-only override request; review first, commit/push/PR only.
  - reasons: "release validation FAILED (stage integrate)" (2026-10-01T08:46:35.028848+00:00; re-read before ship)
  - gates: final-revision 54 scalar + 6 vmap and provenance PASS; padding 12/12; image-plane/JIT PASS; smoke 32/32; formatting/JSON/diff PASS; independent Fable CLEAN.
- validation-logs: /home/jammy/Code/PyAutoLabs/.worktrees/point-solver-duplicate-policy/scratch/ (duplicate-policy-final-stable.log, padding.log, image-plane.log, smoke.log, fable-review.md, fable-rereview.md)

## cockpit-actionable-state
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/434
- issued: 2026-10-01
- prompt: active/cockpit_actionable_state.md
- session: Codex; session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/cockpit-actionable-state
- repos:
  - PyAutoBrain: feature/cockpit-actionable-state
  - pyautolabs.github.io: feature/cockpit-actionable-state
- summary: Additive structured action/state metadata with overnight reference producer and cockpit freshness/next-action improvements.
- approval: User approved the scoped plan in-session, “I approve”; no merge authorization.
- resume: Implement Brain producer/contract first, then website consumer; tests and ship skills to open PRs.

## streaming-p5-cubes-phase-centre
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/600
- issued: 2026-10-01
- prompt: active/streaming_p5_cubes_phase_centre.md
- epic: streaming-visibilities (phase 5 of 5; ledger draft/feature/autoarray/interferometer_from_stream_array_free_dataset.md)
- source: https://github.com/orgs/PyAutoLabs/discussions/13
- session: Claude Code CLI (Fable 5.1 main session + Opus subagents), 2026-10-01
- status: library-dev
- autonomy: supervised (header); plan approved in-session 2026-10-01 (Plan Mode); combined library + workspace, library first
- worktree: ~/Code/PyAutoLabs-wt/streaming-p5-cubes-phase-centre
- repos:
  - PyAutoArray: feature/streaming-p5-cubes-phase-centre
  - autolens_workspace: feature/streaming-p5-cubes-phase-centre
- summary: MFS SparseTerms = sum of per-channel terms (__radd__, 1e-12 parity vs in-memory MFS); phase_centre=(y, x) arcsec in sparse_terms_from_chunks / from_stream (data * exp(+2πi(u l0 + v m0)), provenance-checked in __add__); array-free datacube example modeling_array_free.py in autolens_workspace under the smoke profile.
- resume: Issue + plan on #600; next /start_library (PyAutoArray) then /start_workspace (autolens_workspace); DFT point-source test pins the shift sign.

