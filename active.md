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

## pointsolver-step0-gather
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/579
- issued: 2026-09-26
- prompt: active/pointsolver_step0_gather_containment.md
- epic: point-source-cpu-speed
- session: Claude Code CLI (Opus 5.5 subagent), 2026-09-26; session ID unavailable
- status: library-merged, profiling-pending (PyAutoArray PR #580 MERGED 2026-09-27 as 4383ea81; 8490H job 357321 queued; profiling data PR not yet opened)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/580
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/580
- autonomy: supervised (header); plan approved in-session 2026-09-26 (phase 4b: step-0 containment without the (N,3,2) gather; prototype + laptop measurement first)
- worktree: /home/jammy/Code/PyAutoLabs-wt/pointsolver-step0-gather
- repos:
  - PyAutoArray: feature/pointsolver-step0-gather
  - autolens_profiling: feature/point-source-cpu-p4b
- parallel-claim: "autolens_profiling is also claimed by point-source-cpu-p4 (PR #321 open), interferometer-mesh-breakdown-a100 and point-source-source-plane-p2a. p4b is the human-approved sequential follow-on of p4: its branch feature/point-source-cpu-p4b is based on feature/point-source-cpu-p4 until #321 merges, then rebases onto main. It touches scripts/point_source_image/likelihood_breakdown/solver_config_sweep.py and later results/breakdown/point_source_image/ + point_source_cpu_campaign.md (Phase 4b section); disjoint from the interferometer and source-plane tasks. Human-approved 2026-09-26."
- checkpoint: 2026-09-27 PyAutoArray PR #580 open (default route structured; Heart YELLOW acked by human: manifest drift + stale rehearsal). autolens_profiling feature/point-source-cpu-p4b has LOCAL unpushed commits da46563 7725a6b f7edb9f 311e690 84a867b 9f3fc61 db94264 (harness --step0-route, instrument fixes, laptop/EPYC/A100 results, ledger Phase 4b). Quotable RAL 8490H job 357321 PENDING on saturated ral (10-4); on finish it writes solver_config_sweep_step0_hpc_ral_cpu_fp64.json in /mnt/ral/jnightin/autolens_profiling_wt/pointsolver-step0-gather. Resume = pull that JSON -> commit + update the ledger NOT RUN (queued) subsection -> make the A100 fiducial gate device-aware (...806) -> rebase onto main once #321 merges -> ship_workspace data PR; PyAutoLens needs no PR

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

## interferometer-mesh-numba-p1
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/326
- issued: 2026-09-27
- prompt: active/interferometer_mesh_numba_cpu_phase_1.md (phase 1 of campaign draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md)
- epic: interferometer-likelihood-campaign
- session: Claude Code CLI (Opus 5.5), 2026-09-27; session ID unavailable
- status: awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs-wt/interferometer-mesh-numba-p1
- autonomy: supervised (header); plan approved in-session 2026-09-27 (phase 1: library-dispatch numba CPU cells + --mask-radius + RAL CPU rows, workspace-only)
- parallel-claim: "autolens_profiling is also claimed by point-source-cpu-p4 (#321), point-source-cpu-p4b (pointsolver-step0-gather) and point-source-source-plane-p2b; this phase touches only scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py (+ --mask-radius in interferometer_pixelized.py), scripts/interferometer/likelihood_breakdown/*_numba.py, hpc/batch_cpu/*interferometer*, results/breakdown/interferometer/**numba*, and instruments/interferometer.py only if needed for the mask radius; README dashboards regenerated at ship (#177 precedent). Human-approved 2026-09-27."
- repos:
  - autolens_profiling: feature/interferometer-mesh-numba-p1
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/328
- heart-ack: "manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: organism-map blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml; release validation incomplete: no rehearsal for current source" (acknowledged 2026-09-27, none touch autolens_profiling)
- resume: 2026-09-27 SHIPPED — PR autolens_profiling#328 open (6 commits defb5a8..2908bb2; RAL CPU numba/FFT/JAX-CPU rows + alma N sweep; sma adapt image kept at May-18 copy, human decision). Next = human /prm 328; then phase 2 (crossover) and phase 3 (A100 mask-radius sweep) can start in parallel. Follow-up draft filed: draft/feature/autoarray/interferometer_sparse_numpy_cache_curvature_and_data_vector.md

## point-source-source-plane-p2c
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/329
- issued: 2026-09-27
- prompt: active/point_source_source_plane_phase_2c.md (phase 2c of campaign draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md)
- epic: point-source-cpu-speed
- session: Claude Code CLI (Opus 5.5), 2026-09-27
- worktree: /home/jammy/Code/PyAutoLabs-wt/point-source-source-plane-p2c
- autonomy: supervised (header); plan approved in-session 2026-09-27 (crossover study, workspace-only)
- parallel-claim: autolens_profiling also claimed by pointsolver-step0-gather, point-source-cpu-p4 (#321) and interferometer-mesh-numba-p1; phase 2c touches only scripts/point_source_source/likelihood_breakdown/gradient_mode_crossover.py, results/breakdown/point_source_source/gradient_mode_crossover_*, hpc/batch_{cpu,gpu}/submit_gradient_mode_crossover_point_source_source_*, point_source_source_plane_campaign.md (Phase 2c section), README rows. Own worktree approved by the human 2026-09-27.
- repos:
  - autolens_profiling: feature/point-source-source-plane-p2c
- status: workspace-dev

## interferometer-sparse-cache
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/581
- issued: 2026-09-27
- prompt: active/interferometer_sparse_numpy_cache_curvature_and_data_vector.md
- epic: interferometer-likelihood-campaign
- session: Claude Code CLI (Opus 5.5), 2026-09-27; session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/interferometer-sparse-cache
- autonomy: supervised (header); plan approved in-session 2026-09-27 (cache curvature_matrix / data_vector on the interferometer sparse + mapping inversions)
- parallel-claim: "PyAutoArray also claimed by point-source-cpu-p4b / PR #580 — PointSolver step-0 files; this task touches only autoarray/inversion/inversion/interferometer*/ and test_autoarray/inversion/inversion/interferometer*/; human-approved 2026-09-27"
- repos:
  - PyAutoArray: feature/interferometer-sparse-cache
