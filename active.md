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

## autolens-visualization-rebirth
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/446
- issued: 2026-09-28
- prompt: active/eyes_p1a_autolens_visualization_rebirth.md
- epic: pyautoeyes-birth
- session: Claude Code CLI (Fable architect, Opus execution), 2026-09-28; session ID unavailable
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/447
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/426
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/240
- library-pr: https://github.com/PyAutoLabs/autolens_visualization/pull/1
- pending-release: PyAutoMind@https://github.com/PyAutoLabs/PyAutoMind/pull/447
- pending-release: PyAutoBrain@https://github.com/PyAutoLabs/PyAutoBrain/pull/426
- pending-release: PyAutoHeart@https://github.com/PyAutoLabs/PyAutoHeart/pull/240
- pending-release: autolens_visualization@https://github.com/PyAutoLabs/autolens_visualization/pull/1
- worktree: ~/Code/PyAutoLabs-wt/autolens-visualization-rebirth
- autonomy: supervised (header); plan approved in-session 2026-09-28; merge is human
- heart-ack: "YELLOW 2026-09-28 acknowledged by human: PyAutoMemory: open PR 8d old; manifest drift: workspace checkouts (autolens_visualization unregistered — cleared by this task's Mind PR); workspace validation timeout autolens_test multi_dataset/rectangular.py (cloud#36404726969)"
- repos:
  - autolens_visualization: feature/autolens-visualization-rebirth
  - PyAutoMind: feature/autolens-visualization-rebirth
  - PyAutoBrain: feature/autolens-visualization-rebirth
  - PyAutoHeart: feature/autolens-visualization-rebirth
- parallel-claim: "PyAutoMind, PyAutoBrain and PyAutoHeart are also claimed by eyes-organ-order (PyAutoMind#439). The only overlap is Mind repos.yaml: #439 reorders the organ rows; this task adds a project row after autolens_inference and rewrites the PyAutoEyes role string. Parallel worktree human-approved 2026-09-28; noted on #439 and #446."
- resume: "4 PRs open (merge is human, order Mind#447 → Brain#426 → Heart#240 → autolens_visualization#1). Mind#447 firewall leg is red-by-construction until Brain#426 merges (CI checks out Brain main, whose organism-map block #426 regenerates) — merge Brain first or re-run after. Then /prm; after merge ship the tmp/handover/map-block-*.patch one-line PRs (Cortex, Nerves, Gut, Scientist, .github)."

## interferometer-mesh-breakdown-jax
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/348
- issued: 2026-09-28
- prompt: active/interferometer_mesh_breakdown_jax_phase_3.md (phase 3 of campaign draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md)
- epic: interferometer-likelihood-campaign
- session: Claude Code CLI (Opus 5.5), 2026-09-28; session ID unavailable
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/interferometer-mesh-breakdown-jax
- autonomy: supervised (header); plan approved in-session 2026-09-28 (phase 3: 12 RAL A100 fp64 jobs, Delaunay-1500 + rect 39² at sma/alma/alma_high × r2.0/r5.0, ledger + wiki write-up, workspace-only)
- repos:
  - autolens_profiling: feature/interferometer-mesh-breakdown-jax
