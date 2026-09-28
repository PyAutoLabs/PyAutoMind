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

## interferometer-mesh-breakdown-jax
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/348
- issued: 2026-09-28
- prompt: active/interferometer_mesh_breakdown_jax_phase_3.md (phase 3 of campaign draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md)
- epic: interferometer-likelihood-campaign
- session: Claude Code CLI (Opus 5.5), 2026-09-28; session ID unavailable
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/352
- worktree: /home/jammy/Code/PyAutoLabs-wt/interferometer-mesh-breakdown-jax
- autonomy: supervised (header); plan approved in-session 2026-09-28 (phase 3: 12 RAL A100 fp64 jobs, Delaunay-1500 + rect 39² at sma/alma/alma_high × r2.0/r5.0, ledger + wiki write-up, workspace-only)
- ral-worktree: /mnt/ral/jnightin/autolens_profiling_wt/interferometer-mesh-breakdown-jax (fe0d4b5; mirror /mnt/ral/jnightin/PyAuto refreshed by HPCPullPyAuto 2026-09-28 to Nerves bf104102 / Fit 404b3e5f / Array 9428eca2 / Galaxy c9609825 / Lens 21b520be; nufftax 0.6.1)
- ral-jobs: delaunay 366895 (tasks 2-5) + 366907 (sma tasks 0-1), pixelization 366896 (tasks 2-5) + 366908 (sma tasks 0-1); 366895_0-1 / 366896_0-1 cancelled (sma dataset missing in the RAL worktree; seeded from the canonical RAL checkout, md5 = the #324 A100 worktree copy). All 12 legs COMPLETED 2026-09-28 in 1-3 min each; rows + ledger + wiki committed 04187dd, lint green locally
- heart-ack: "human acknowledged YELLOW at ship 2026-09-28: workspace validation timeout (autolens_test multi_dataset/rectangular.py), manifest drift x1, PyAutoMemory PR 8d old, release validation incomplete; none touch autolens_profiling"
- repos:
  - autolens_profiling: feature/interferometer-mesh-breakdown-jax

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

## eyes-board-conductor-registry
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/451
- issued: 2026-09-28
- prompt: active/eyes_p2_board_and_conductor_registry.md
- epic: pyautoeyes-birth
- session: Claude Code CLI (Fable architect, Opus execution), 2026-09-28; session ID unavailable
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/eyes-board-conductor-registry
- autonomy: supervised (header); epic phasing human-approved ("do next phase") 2026-09-28; merge is human
- heart-ack: "2026-09-28 YELLOW acknowledged by human: PyAutoMemory open PR 8d old; manifest drift workspace checkouts (autolens_visualization unregistered, stale Heart snapshot); workspace validation timeout autolens_test multi_dataset/rectangular.py (cloud#36404726969)"
- repos:
  - PyAutoEyes: feature/eyes-board-conductor-registry
  - PyAutoBrain: feature/eyes-board-conductor-registry
- parallel-claim: "PyAutoEyes and PyAutoBrain are also claimed by eyes-organ-skeleton (PyAutoMind#448), which is MERGED (PyAutoEyes#2, PyAutoBrain#428) and whose close-out is running concurrently; no open branch overlap. Noted on #451."

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
