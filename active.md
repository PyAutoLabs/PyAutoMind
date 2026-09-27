# Active Tasks

## jax-grad-nan-zero-components
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/631
- issued: 2026-09-27
- prompt: active/jax_grad_nan_at_zero_components.md
- session: Claude Code CLI (Opus 5.5 main session + Opus subagent), 2026-09-27; session ID unavailable
- status: library-dev
- autonomy: human-required (no header); plan approved in-session 2026-09-27
- worktree: ~/Code/PyAutoLabs-wt/jax-grad-nan-zero-components
- parallel-claim: "PyAutoGalaxy is also claimed by workspace-config-cleanup (PyAutoMind#441), whose Galaxy PR #630 is merged and awaiting release (no live edits); this task touches only autogalaxy/convert.py + tests. Parallel worktree human-approved 2026-09-27."
- repos:
  - PyAutoGalaxy: feature/jax-grad-nan-zero-components
- resume: implement convert.py _nudge_off_origin per issue plan, tests red-first, then /ship_library

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
- parallel-claim: "PyAutoGalaxy is also claimed by jax-grad-nan-zero-components (PyAutoGalaxy#631), convert.py + tests only; parallel worktree human-approved 2026-09-27."
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

## pointsolver-mcs-headroom
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/583
- issued: 2026-09-27
- prompt: active/pointsolver_max_containing_size_headroom.md
- epic: point-source-cpu-speed
- session: Claude Code CLI (Opus 5.5 main session + Opus subagent), 2026-09-27; session ID unavailable
- status: library-dev
- autonomy: supervised (header); plan approved in-session 2026-09-27 (measure MCS 18/20/24 first; no default change without the human's call at step 2)
- worktree: /home/jammy/Code/PyAutoLabs-wt/pointsolver-mcs-headroom
- parallel-claim: "Three disjoint claims human-approved 2026-09-27: PyAutoArray vs interferometer-sparse-cache (#582, only autoarray/inversion/inversion/interferometer*; since completed) — this task touches only autoarray/structures/triangles/; PyAutoLens vs workspace-config-cleanup (Lens#751, awaiting release) — this task touches only autolens/point/solver/shape_solver.py + its test; autolens_profiling vs point-source-source-plane-p2c (scripts/point_source_source/…, source-plane ledger) — this task touches only scripts/point_source_image/…, new hpc submits, results/breakdown/point_source_image/ and the CPU ledger."
- resume: step 1 measurement (MCS 18/20/24 vs control, laptop + RAL 8490H) in autolens_profiling; then step 2 human checkpoint picks N
- repos:
  - PyAutoArray: feature/pointsolver-mcs-headroom
  - PyAutoLens: feature/pointsolver-mcs-headroom
  - autolens_profiling: feature/pointsolver-mcs-headroom

## interferometer-mesh-numba-p2
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/332
- issued: 2026-09-27
- prompt: active/interferometer_mesh_numba_cpu_phase_2.md (phase 2 of campaign draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md; folds in the retired interferometer_sparse_cache_after_measurement.md)
- epic: interferometer-likelihood-campaign
- session: Claude Code CLI (Opus 5.5), 2026-09-27; session ID unavailable
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/interferometer-mesh-numba-p2
- autonomy: supervised (header); plan approved in-session 2026-09-27 (phase 2: in-situ numba vs FFT crossover + CPU lever arms + cached_property counter fold-in + RAL CPU rows, workspace-only)
- parallel-claim: "autolens_profiling is also claimed by point-source-source-plane-p2c (#329 / PR #331), whose files are scripts/point_source_source/**, results/breakdown/point_source_source/** and the point-source notes; this phase touches only scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py, scripts/interferometer/likelihood_breakdown/*_numba.py, scripts/misc/test/test_interferometer_pixelized_numpy.py, hpc/batch_cpu/*interferometer*numba*, results/breakdown/interferometer/**numba*, results/notes/numba_interferometer_verdict.md and results/notes/interferometer_mesh_cpu_breakdown_2026_09.md; README dashboards regenerated at ship (#177 precedent). Human-approved 2026-09-27. At worktree creation the guard named pointsolver-mcs-headroom (PyAutoArray#583; autolens_profiling files scripts/point_source_image/**, results/breakdown/point_source_image/**, point-source hpc submits, CPU ledger) instead — equally disjoint; worktree created under the same disjoint-files approval (judgement call by the executing agent, flagged for the human)."
- parallel-claim-confirmed: "human confirmed 2026-09-27 the parallel claim alongside pointsolver-mcs-headroom (PyAutoArray#583; its autolens_profiling files scripts/point_source_image/**, results/breakdown/point_source_image/**, point-source submits and the CPU ledger are disjoint)"
- repos:
  - autolens_profiling: feature/interferometer-mesh-numba-p2
- resume: "2026-09-27 local commits 5d806c4 (harness: cached_property counter, adapt guard, previous_row, --levers) + 92a2061 (RAL crossover arrays + lever submit) on feature/interferometer-mesh-numba-p2, NOT pushed. RAL worktree /mnt/ral/jnightin/autolens_profiling_wt/interferometer-mesh-numba-p2 (bundle of 4c267b7..92a2061). Jobs: 358985 (Delaunay crossover array 0-6: sma r3.5, alma r2.0/3.5/4.25/5.0/6.0, alma_high r3.5) + 358986 (rect, same) on euclid-ral-gpu-1; 359000 levers (alma r3.5 both meshes, --nodelist=euclid-ral-gpu-2 idle node; 358987 cancelled). Pull: rsync -av euclid_jump:/mnt/ral/jnightin/autolens_profiling_wt/interferometer-mesh-numba-p2/results/breakdown/interferometer/ results/breakdown/interferometer/ (+ hpc/batch_cpu/output/output.{358985_*,358986_*,359000}.out). Next: pull -> check witness (crossover bracketed per mesh; {1,1}; sma pins) -> notes (numba_interferometer_verdict.md crossover section; interferometer_mesh_cpu_breakdown_2026_09.md ranked levers + per-lever draft prompts; gate 60 confirm or general.yaml retune prompt) -> build_readme.py -> ship_workspace."

## point-source-gradient-mode
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1648
- issued: 2026-09-27
- prompt: active/point_source_source_plane_phase_2d.md (phase 2d of campaign draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md)
- epic: point-source-cpu-speed
- session: Claude Code CLI (Opus 5.5), 2026-09-27
- worktree: /home/jammy/Code/PyAutoLabs-wt/point-source-gradient-mode
- autonomy: supervised (header); plan approved in-session 2026-09-27 (library-first: PyAutoFit then PyAutoLens, then autolens_profiling follow-up)
- parallel-claim: "PyAutoLens also claimed by workspace-config-cleanup (Lens#751 merged, awaiting release) and pointsolver-mcs-headroom (point solver); this task touches only autolens/point/model/analysis.py + a new test. autolens_profiling also claimed by pointsolver-mcs-headroom and interferometer-mesh-numba-p2; follow-up touches only a new cell, its results and the source-plane note. Parallel worktree approved by the human 2026-09-27."
- repos:
  - PyAutoFit: feature/point-source-gradient-mode
  - PyAutoLens: feature/point-source-gradient-mode
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1649
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/752
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1649
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/752
- status: library-shipped, workspace-pending (PyAutoFit#1649 then PyAutoLens#752 awaiting /prm; autolens_profiling follow-up after merge)
- heart-ack: "2026-09-27 YELLOW acknowledged by the human: manifest drift x3 vs PyAutoMind/repos.yaml (hub organism blurb 7, organism-map blocks 1, workspace checkouts 1); release validation incomplete: no rehearsal for current source"
- carried: RAL scratch /mnt/ral/jnightin/p2d_check (clones, bundles, pylib, job script) + p2a/p2b/p2c RAL worktrees to remove; latent: Galaxy duplicate PyTreeDef registration (autofit.jax.register_model then autoarray register_instance_pytree) -> intake; PowerLawMultipole m=1 singular at slope 2 -> intake
