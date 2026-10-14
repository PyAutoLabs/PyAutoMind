# Active Tasks

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

## search-ext-a4-decompose
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1684
- issued: 2026-10-14
- prompt: active/search_ext_a4_decompose_seed_family_bases.md
- session: Claude Code CLI (Fable 5.1); session 51fca711
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a4-decompose
- epic: search-extensibility
- next: Opus worker implements three stacked PRs in order (A4a decompose → A4b seed → A4c family bases + Brain/developer companions); each to PR-open, human /prm in order
- repos:
  - PyAutoFit: feature/search-ext-a4-decompose

## retire-nautilus-leftovers
- issue: https://github.com/PyAutoLabs/autofit_workspace_developer/issues/31
- issued: 2026-10-14
- prompt: active/retire_searches_minimal_nautilus_leftovers.md
- session: Claude Code CLI (Fable 5.1); session 51fca711
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/retire-nautilus-leftovers
- epic: search-extensibility
- next: committed deletion PR, glance-tier merge (human approved 2026-10-14), close-out with condemned.md entry
- repos:
  - autofit_workspace_developer: feature/retire-nautilus-leftovers
