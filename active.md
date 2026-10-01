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

## streaming-p5-cubes-phase-centre
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/600
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/601
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/643
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/601
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/643
- issued: 2026-10-01
- prompt: active/streaming_p5_cubes_phase_centre.md
- epic: streaming-visibilities (phase 5 of 5; ledger draft/feature/autoarray/interferometer_from_stream_array_free_dataset.md)
- source: https://github.com/orgs/PyAutoLabs/discussions/13
- session: Claude Code CLI (Fable 5.1 main session + Opus subagents), 2026-10-01
- status: library-shipped, workspace-pending
- autonomy: supervised (header); plan approved in-session 2026-10-01 (Plan Mode); combined library + workspace, library first
- worktree: ~/Code/PyAutoLabs-wt/streaming-p5-cubes-phase-centre
- repos:
  - PyAutoArray: feature/streaming-p5-cubes-phase-centre
  - PyAutoGalaxy: feature/streaming-p5-cubes-phase-centre
  - autolens_workspace: feature/streaming-p5-cubes-phase-centre
- heart-red-override:
  - authorization: Live user "Yes: library now, workspace when its run passes" on 2026-10-01 in the Fable CLI session, in answer to the override question naming streaming-p5-cubes-phase-centre (PyAutoArray#600). Push + PR-open only (library PRs now; the autolens_workspace PR under the same grant once its full-profile run + smoke pass); merge is a separate human /prm on green checks; no release.
  - reasons: release validation FAILED (stage integrate); workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py); manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml
  - gates: tests 1917 (autoarray) / 1307 (autogalaxy); Codex astra review 5 findings, 3 introduced fixed + red-checked, 2 pre-existing filed (draft/bug/autoarray/sparse_terms_nufft_origin_and_mask_compatibility.md); workspace smoke exit 0 + lint OK, full run pending.
- summary: MFS SparseTerms = sum of per-channel terms (__radd__, 1e-12 parity vs in-memory MFS); phase_centre=(y, x) arcsec in sparse_terms_from_chunks / from_stream (data * exp(+2πi(u l0 + v m0)), provenance-checked in __add__); array-free datacube example modeling_array_free.py in autolens_workspace under the smoke profile.
- resume: Library PRs open (PyAutoArray#601, PyAutoGalaxy#643), CI pending. Workspace: modeling_array_free.py drafted in the task worktree (smoke exit 0, lint OK), full-profile run in progress → then /ship_workspace (notebook regen, smoke test, PR under the same override grant). Then human /prm (Array → Galaxy → workspace), Discussion #13 follow-up post.
