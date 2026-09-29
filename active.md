# Active Tasks

## workspace-config-cleanup
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/441
- issued: 2026-09-27
- prompt: active/workspace_config_cleanup.md
- epic: organ-cockpit
- session: Claude Code CLI (Opus 5.5 main session + Opus subagent), 2026-09-27; session ID unavailable
- status: awaiting-release (6/7 merged 2026-09-27: Galaxy#630 cbd89ced, Lens#751 1e6372fd, Nerves#176 0b6e7c78, autofit_ws#164 aa7361df, autogalaxy_ws#250 7fd1953d, autocti_ws#34 7aa79ac6; autolens_workspace#578 OPEN, held for the PyAutoGalaxy release)
- autonomy: supervised (header); plan approved in-session 2026-09-27 (library-first: Nerves board equivalence + allow-list, PyAutoGalaxy promotion, then workspace deletes)
- worktree: ~/Code/PyAutoLabs-wt/workspace-config-cleanup
- parallel-claim: "PyAutoNerves is also claimed by eyes-organ-order (PyAutoMind#439), whose Nerves diff is only AGENTS.md; this task touches only scripts/board.py + its tests. Parallel worktree human-approved 2026-09-27; noted on #439 and #441."
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/630
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/751
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/176
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/630
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/751
- pending-release: PyAutoNerves@https://github.com/PyAutoLabs/PyAutoNerves/pull/176
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/164
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/250
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/578
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/34
- release-gate: PyAutoGalaxy
- resume: "6/7 merged. Once PyAutoGalaxy (with #630) is on PyPI: /prm autolens_workspace#578, then full close-out (records, issue #441 close, worktree removal). Nerves board re-dispatched after merge."
- repos:
  - PyAutoNerves: feature/workspace-config-cleanup
  - PyAutoGalaxy: feature/workspace-config-cleanup
  - PyAutoLens: feature/workspace-config-cleanup
  - autofit_workspace: feature/workspace-config-cleanup
  - autogalaxy_workspace: feature/workspace-config-cleanup
  - autolens_workspace: feature/workspace-config-cleanup
  - autocti_workspace: feature/workspace-config-cleanup

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

## sparse-operator-oversampling-cache
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/585
- issued: 2026-09-27
- status: library-shipped, awaiting-merge
- prompt: active/sparse_operator_dropped_and_double_convolution.md
- session: Claude Code CLI (Opus 5.5), 2026-09-27
- worktree: /home/jammy/Code/PyAutoLabs-wt/sparse-operator-oversampling-cache
- repos:
  - PyAutoArray: feature/sparse-operator-oversampling-cache
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/586
- heart-ack: "YELLOW 2026-09-27 acknowledged by human ('prm'): manifest drift x4 vs repos.yaml (hub organism blurb, organism-map blocks, where-to-file blocks, workspace checkouts); PyAutoMemory open PR 7d old"

## point-source-gpu-p01
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/350
- issued: 2026-09-28
- prompt: active/point_source_gpu_p01.md
- session: Claude Code CLI (Opus 5.5 main session + Opus subagent), 2026-09-28; session ID unavailable
- status: awaiting-merge (autolens_profiling#353 open; supervised, merge is human)
- autonomy: supervised (header); plan approved in-session 2026-09-28 (lean phase 0+1, no library edits; phase-2 go/no-go is human)
- worktree: ~/Code/PyAutoLabs-wt/point-source-gpu-p01
- parallel-claim: "autolens_profiling is also claimed by interferometer-mesh-breakdown-jax (#348) and source-plane-runtime-refresh (#349), both registered 2026-09-28 after this task's first survey. File sets disjoint (scripts/point_source_image/, results/breakdown/point_source_image/, new notes file, point_source_gpu_breakdown wiki page); shared only wiki/index.md rows + generated README/dashboard, regenerated by whichever merges second. Parallel claim human-approved 2026-09-28."
- repos:
  - autolens_profiling: feature/point-source-gpu-p01
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/353
- heart-ack: "YELLOW 2026-09-28 acknowledged by human at ship: autolens_test multi_dataset/rectangular.py timeout (cloud#36404726969); manifest drift 1 mismatch vs repos.yaml; PyAutoMemory open PR 8d old"
- follow-up: draft/bug/autolens/point_image_pair_all_forward_grad_nan.md (released forward-mode gradient NaN, found here)
- resume: human go/no-go on phase 2 (memo in results/notes/point_source_gpu_breakdown_2026_09.md); then /prm #353

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

## eyes-fit-cti-instances
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/455
- issued: 2026-09-29
- status: library-dev
- prompt: active/eyes_p4_fit_cti_instances.md
- epic: pyautoeyes-birth (phase 4)
- session: Claude Code CLI (Fable 5.1), 2026-09-29
- worktree: /home/jammy/Code/PyAutoLabs-wt/eyes-fit-cti-instances
- repos:
  - autofit_visualization: feature/eyes-fit-cti-instances
  - autocti_visualization: feature/eyes-fit-cti-instances
  - PyAutoEyes: feature/eyes-fit-cti-instances
  - PyAutoMind: feature/eyes-fit-cti-instances
  - PyAutoBrain: feature/eyes-fit-cti-instances
  - PyAutoHeart: feature/eyes-fit-cti-instances
