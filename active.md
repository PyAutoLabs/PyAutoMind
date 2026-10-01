# Active Tasks

## heart-score-resusitate
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/255
- issued: 2026-10-01
- prompt: active/heart-score-resusitate.md
- session: Codex; session ID unavailable
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/256
- pending-release: PyAutoHeart@https://github.com/PyAutoLabs/PyAutoHeart/pull/256
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/heart-score-resusitate
- repos:
  - PyAutoHeart: feature/heart-score-resusitate
- summary: Approved Score and Resusitate headers, compact readiness text and repair rows with icon copy controls.
- heart-red-override:
  - authorization: Live user "I approve" on 2026-10-01 in response to the task plan and development-only RED override. No merge/release authority.
  - reasons: release validation FAILED (stage integrate)
  - gates: 1105 Heart tests passed; tenant-firewall OK; HTML render and in-session diff review passed. Browser verification blocked by sandbox sockets. No downstream scientific smoke applies.
  - records: Issue #255, PR #256, active.md and autonomy_log.md record the override.
- resume: PR #256 opened with pending-release label at 4e87903. Both Python CI jobs in progress at the single post-push check. Preview and full-tests.log in task root. Await human /prm; no merge or deployment authorized for this task.

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
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/599
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/642
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/762
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/599
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/642
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/762
- issued: 2026-10-01
- prompt: active/streaming_p4_light_profile_identity.md
- epic: streaming-visibilities (phase 4 of 5; ledger draft/feature/autoarray/interferometer_from_stream_array_free_dataset.md)
- source: https://github.com/orgs/PyAutoLabs/discussions/13
- session: Claude Code CLI (Fable 5.1 main session + Opus subagents), 2026-10-01
- status: library-shipped, awaiting-merge
- autonomy: supervised (header); plan approved in-session 2026-10-01 (Plan Mode)
- worktree: ~/Code/PyAutoLabs-wt/streaming-p4-light-profile-identity
- repos:
  - PyAutoArray: feature/streaming-p4-light-profile-identity
  - PyAutoGalaxy: feature/streaming-p4-light-profile-identity
  - PyAutoLens: feature/streaming-p4-light-profile-identity
- heart-red-override:
  - authorization: Live user "Yes, ship (push + PR-open)" on 2026-10-01 in the Fable CLI session, in answer to the override question naming streaming-p4-light-profile-identity (PyAutoArray#598). Push + PR-open only; merge is a separate human /prm on green checks; no release.
  - reasons: release validation FAILED (stage integrate); workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py); manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - gates: tests 1903 / 1305 / 793+1xfail (autoarray / autogalaxy / autolens); Codex astra review 4 findings, 3 fixed in-branch + red-checked, 1 pre-existing filed (draft/bug/autogalaxy/galaxy_image_dict_mixed_galaxy_overwrites_ordinary_light.md); smoke n/a (library-only, no workspace consumer of from_stream yet).
- summary: Ordinary (non-linear) light profiles fit array-free via data_term - 2 i.d~ + i.W~i on the total model image (DatasetInterface data_term override; FitInterferometer.sparse_chi_squared hook; typed raises for model_data and for data/noise-map overrides); profile_visibilities never formed; in-memory sparse path bit-for-bit unchanged.
- resume: PRs open (#599 / #642 / #762), CI pending. Next: human /prm, merge Array -> Galaxy -> Lens; then Discussion #13 follow-up post (draft in session scratchpad reply_discussion13_followup.md, needs text approval; update its "Not yet" paragraph since P4 is now in) and phase 5 (draft/feature/autoarray/streaming_p5_cubes_phase_centre.md).

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
