# Active Tasks

## image-dropdown-contrast
- issue: https://github.com/PyAutoLabs/PyAutoEyes/issues/29
- issued: 2026-10-14
- prompt: active/image-dropdown-contrast.md
- session: Codex; session ID unavailable; launched --auto
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/image-dropdown-contrast
- repos:
  - PyAutoEyes: feature/image-dropdown-contrast

## hst-mge-pilot-qualification
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/417
- issued: 2026-10-13
- session: Codex; session ID unavailable
- status: workspace-shipped, awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/418
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/hst-mge-pilot-qualification
- next: Review and merge #418; independently validated witness implementation, coefficient tolerances and production collection remain separate pending work.
- repos:
  - autolens_profiling: feature/hst-mge-pilot-qualification

## search-ext-a4-companions
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/520
- issued: 2026-10-14
- prompt: active/search_ext_a4_companions.md
- session: Claude Code CLI (Fable 5.1); session 51fca711; launched --auto
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a4-companions
- epic: search-extensibility
- next: Opus worker ships one PR per repo (Brain reference, developer ultranest/pyswarms, workspace_test seeded Dynesty); tier glance — in-turn tiered merge on green if the Witness passes
- repos:
  - PyAutoBrain: feature/search-ext-a4-companions
  - autofit_workspace_developer: feature/search-ext-a4-companions
  - autofit_workspace_test: feature/search-ext-a4-companions

## search-ext-a5-library
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1688
- issued: 2026-10-14
- prompt: active/search_ext_a5_library_run_ctx_migrations.md
- session: Claude Code CLI (Fable 5.1); session 51fca711; launched --auto
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a5-library
- epic: search-extensibility
- next: Opus worker builds four stacked PRs (simple searches → Dynesty/NUTS/SMC → MultiStart → framework close + template) to PR-open under the ship gate; human /prm in order
- repos:
  - PyAutoFit: feature/search-ext-a5-library

## search-ext-b4b-ep-baseline
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/4
- issued: 2026-10-14
- prompt: active/search_ext_b4b_ep_graphical_baseline_port.md
- session: Claude Code CLI (Fable 5.1); session 51fca711; launched --auto
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b4b-ep-baseline
- epic: search-extensibility
- next: Opus worker ports ep/graphical + analytic cell into autofit_profiling (PR 1), reproduces baselines on the B4a host, then Pulse PR 2 after Pages is live; human /prm
- repos:
  - autofit_profiling: feature/search-ext-b4b-ep-baseline
  - PyAutoPulse: feature/search-ext-b4b-ep-baseline

## search-ext-b5a-wave2
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/8
- issued: 2026-10-14
- prompt: active/search_ext_b5a_freeze_and_scored_wave2.md
- session: Claude Code CLI (Fable 5.1); session 51fca711; launched --auto
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b5a-wave2
- epic: search-extensibility
- next: Opus worker freezes @2, builds the scored-wave infra (PR 1), submits references + wave 2 on RAL `--partition=ral` against a private pinned PyAutoFit, then Cortex (PR 2) and Insight (PR 3); human /prm; row stays open as compute-running until B5b
- repos:
  - autofit_inference: feature/search-ext-b5a-wave2
  - PyAutoInsight: feature/search-ext-b5a-wave2
  - PyAutoCortex: feature/search-ext-b5a-wave2
