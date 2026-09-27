# Active Tasks

## eyes-organ-order
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/439
- issued: 2026-09-25
- prompt: active/eyes_organ_order.md
- session: Claude Code CLI (Fable architect, Opus execution), 2026-09-25; session ID unavailable
- status: workspace-dev
- autonomy: supervised (header); plan on the issue; reorder is the next leg, merge is human
- worktree: /home/jammy/Code/PyAutoLabs-wt/eyes-organ-order
- repos:
  - PyAutoMind: feature/eyes-organ-order
  - PyAutoBrain: feature/eyes-organ-order
  - PyAutoHeart: feature/eyes-organ-order
  - PyAutoHands: feature/eyes-organ-order
  - pyautolabs.github.io: feature/eyes-organ-order
  - PyAutoScientist: feature/eyes-organ-order
  - PyAutoCortex: feature/eyes-organ-order
  - PyAutoNerves: feature/eyes-organ-order
  - PyAutoGut: feature/eyes-organ-order
- resume: bundle worktree created; implement the reorder per the issue plan (Eyes between Memory and Heart), then repos_sync --write, then ship

## workspace-config-cleanup
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/441
- issued: 2026-09-27
- prompt: active/workspace_config_cleanup.md
- epic: organ-cockpit
- session: Claude Code CLI (Opus 5.5 main session + Opus subagent), 2026-09-27; session ID unavailable
- status: library-dev
- autonomy: supervised (header); plan approved in-session 2026-09-27 (library-first: Nerves board equivalence + allow-list, PyAutoGalaxy promotion, then workspace deletes)
- worktree: ~/Code/PyAutoLabs-wt/workspace-config-cleanup
- parallel-claim: "PyAutoNerves is also claimed by eyes-organ-order (PyAutoMind#439), whose Nerves diff is only AGENTS.md; this task touches only scripts/board.py + its tests. Parallel worktree human-approved 2026-09-27; noted on #439 and #441."
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

## pointsolver-step0-gather
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/579
- issued: 2026-09-26
- prompt: active/pointsolver_step0_gather_containment.md
- epic: point-source-cpu-speed
- session: Claude Code CLI (Opus 5.5 subagent), 2026-09-26; session ID unavailable
- status: library-dev
- autonomy: supervised (header); plan approved in-session 2026-09-26 (phase 4b: step-0 containment without the (N,3,2) gather; prototype + laptop measurement first)
- worktree: /home/jammy/Code/PyAutoLabs-wt/pointsolver-step0-gather
- repos:
  - PyAutoArray: feature/pointsolver-step0-gather
  - autolens_profiling: feature/point-source-cpu-p4b
- parallel-claim: "autolens_profiling is also claimed by point-source-cpu-p4 (PR #321 open), interferometer-mesh-breakdown-a100 and point-source-source-plane-p2a. p4b is the human-approved sequential follow-on of p4: its branch feature/point-source-cpu-p4b is based on feature/point-source-cpu-p4 until #321 merges, then rebases onto main. It touches scripts/point_source_image/likelihood_breakdown/solver_config_sweep.py and later results/breakdown/point_source_image/ + point_source_cpu_campaign.md (Phase 4b section); disjoint from the interferometer and source-plane tasks. Human-approved 2026-09-26."
- checkpoint: 2026-09-26 WIP commit 8755072f on PyAutoArray feature/pointsolver-step0-gather (LOCAL only, not pushed): 4 step-0 routes behind array._STEP0_CONTAINMENT, scratch bit-identity OK; resume = tests (fuzz, refinement, HLO guard red-on-main) -> PyAutoArray+PyAutoLens suites -> --step0-route laptop A/B in the p4b profiling worktree (no changes there yet) -> pick default (see issue #579 checkpoint comment)

## point-source-cpu-p4
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/314
- issued: 2026-09-26
- prompt: active/pointsolver_cpu_speed_phase_4.md
- epic: point-source-cpu-speed
- session: Claude Code CLI (Opus 5.5), 2026-09-26; session ID unavailable
- status: awaiting-merge (phase 4a PR #321 open; human runs /prm)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/321
- autonomy: supervised (header); plan approved in-session 2026-09-26 (phase 4a: re-baseline + solver-config sweep, single-source, workspace-only)
- worktree: /home/jammy/Code/PyAutoLabs-wt/point-source-cpu-p4
- repos:
  - autolens_profiling: feature/point-source-cpu-p4
- parallel-claim: |
    autolens_profiling also claimed by interferometer-transform-real-scatter (1 file: hpc/batch_gpu interferometer A100 submit); file sets disjoint; human-approved own worktree 2026-09-26

## point-source-source-plane-p2b
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/325
- issued: 2026-09-27
- prompt: active/point_source_source_plane_phase_2b.md (phase 2b of campaign draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md)
- epic: point-source-cpu-speed
- session: Claude Code CLI (Opus 5.5), 2026-09-27
- worktree: /home/jammy/Code/PyAutoLabs-wt/point-source-source-plane-p2b
- autonomy: supervised (header); plan approved in-session 2026-09-27 (backward-pass A/B, workspace-only)
- parallel-claim: autolens_profiling also claimed by point-source-cpu-p4 (#321), pointsolver-step0-gather (p4b) and interferometer-mesh-breakdown-a100; phase 2b touches only scripts/point_source_source/likelihood_breakdown/backward_pass_ab.py, results/breakdown/point_source_source/backward_pass_ab_*, hpc/batch_{cpu,gpu}/submit_backward_pass_ab_point_source_source_*, point_source_source_plane_campaign.md (Phase 2b section), README rows. Own worktree approved by the human 2026-09-27.
- repos:
  - autolens_profiling: feature/point-source-source-plane-p2b
- status: workspace-dev

## interferometer-mesh-numba-p1
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/326
- issued: 2026-09-27
- prompt: active/interferometer_mesh_numba_cpu_phase_1.md (phase 1 of campaign draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md)
- epic: interferometer-likelihood-campaign
- session: Claude Code CLI (Opus 5.5), 2026-09-27; session ID unavailable
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/interferometer-mesh-numba-p1
- autonomy: supervised (header); plan approved in-session 2026-09-27 (phase 1: library-dispatch numba CPU cells + --mask-radius + RAL CPU rows, workspace-only)
- parallel-claim: "autolens_profiling is also claimed by point-source-cpu-p4 (#321), point-source-cpu-p4b (pointsolver-step0-gather) and point-source-source-plane-p2b; this phase touches only scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py (+ --mask-radius in interferometer_pixelized.py), scripts/interferometer/likelihood_breakdown/*_numba.py, hpc/batch_cpu/*interferometer*, results/breakdown/interferometer/**numba*, and instruments/interferometer.py only if needed for the mask radius; README dashboards regenerated at ship (#177 precedent). Human-approved 2026-09-27."
- repos:
  - autolens_profiling: feature/interferometer-mesh-numba-p1
- resume: 2026-09-27 phase-1 code + laptop sma rows committed LOCALLY on feature/interferometer-mesh-numba-p1 (defb5a8, 7cc976f, a40ffb7, 9721d39; not pushed). RAL CPU jobs submitted 2026-09-27 from RAL worktree /mnt/ral/jnightin/autolens_profiling_wt/interferometer-mesh-numba-p1 (branch via git bundle): 357554 del alma, 357555 del alma N-sweep, 357556 del alma_high, 357557 del sma, 357558 pix alma, 357559 pix alma N-sweep, 357560 pix alma_high, 357561 pix sma (gpu partition CPUs-only). Next: squeue/sacct + grep Traceback in hpc/batch_cpu/{output,error}/*.3575{54..61}.*; pull results/breakdown/interferometer/{,sma/,alma_high/,n_sweep/}*hpc_ral_cpu_fp64* back (rsync from the RAL worktree, or hpc/sync pull), check source_revisions vs mains, commit + build_readme, then /ship_workspace.
