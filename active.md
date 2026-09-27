# Active Tasks

## jax-grad-nan-zero-components
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/631
- issued: 2026-09-27
- prompt: active/jax_grad_nan_at_zero_components.md
- session: Claude Code CLI (Opus 5.5 main session + Opus subagent), 2026-09-27; session ID unavailable
- status: library-dev
- autonomy: human-required (no header); plan approved in-session 2026-09-27
- worktree: ~/Code/PyAutoLabs-wt/jax-grad-nan-zero-components
- parallel-claim: "PyAutoGalaxy and PyAutoLens are also claimed by workspace-config-cleanup (PyAutoMind#441), whose Galaxy #630 / Lens #751 PRs are merged and awaiting release (no live edits); this task touches convert.py, isothermal.py + tests, and 6 Lens test pins. Parallel worktree human-approved 2026-09-27."
- repos:
  - PyAutoGalaxy: feature/jax-grad-nan-zero-components
  - PyAutoLens: feature/jax-grad-nan-zero-components
- scope: "2026-09-27 human-approved extension: remove Isothermal q<=0.99999 clamp (series near q->1) so ell_comps grad at 0 is correct; companion PyAutoLens PR repins 6 tests pinned to the clamp artefact."
- resume: galaxy fix done (convert.py tracer-only lax.select nudge + isothermal series); lens repin in progress; then /ship_library (Galaxy first, Lens with it)

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
- parallel-claim: "PyAutoGalaxy and PyAutoLens are also claimed by jax-grad-nan-zero-components (PyAutoGalaxy#631), convert.py/isothermal.py + tests and 6 Lens test pins; parallel worktree human-approved 2026-09-27."
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

## point-source-source-plane-p2e
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/334
- issued: 2026-09-27
- prompt: active/point_source_source_plane_phase_2e.md (phase 2e of campaign draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md)
- epic: point-source-cpu-speed
- session: Claude Code CLI (Opus 5.5), 2026-09-27
- worktree: /home/jammy/Code/PyAutoLabs-wt/point-source-source-plane-p2e
- autonomy: supervised (header); approved in-session 2026-09-27 as the phase-2d plan's workspace follow-up
- parallel-claim: "autolens_profiling also claimed by pointsolver-mcs-headroom and interferometer-mesh-numba-p2; phase 2e touches only scripts/point_source_source/likelihood_breakdown/gradient_mode_library_ab.py, its results/submits, point_source_source_plane_campaign.md (Phase 2e section), README rows. Approved with the phase-2d plan 2026-09-27."
- repos:
  - autolens_profiling: feature/point-source-source-plane-p2e
- status: workspace-dev
