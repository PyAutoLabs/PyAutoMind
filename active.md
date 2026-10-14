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

## search-ext-a3-postmerge-fixes
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1682
- issued: 2026-10-14
- session: Claude Code CLI (Fable 5.1); session 51fca711
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a3-postmerge-fixes
- epic: search-extensibility
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1683
- next: human /prm on PyAutoFit#1683 (pending-release; all 7 review-05 findings reproduced and fixed test-first; full leg 3579 pass, nojax emulation 3274 pass, Sphinx 30/30 warnings; item-7 witness on the PR). Decisions on the PR: ExecutionSettings in preflight.py via NonLinearSearch.execution_settings(analysis); ctx.update saves resume state only; _pools(analysis) fix extended to Dynesty cores, initializer n_cores, make_sneaky_pool. Note: `pytest -n auto` is broken on the suite (address-based parametrize ids) — pre-existing.
- repos:
  - PyAutoFit: feature/search-ext-a3-postmerge-fixes

## search-ext-b3-postmerge-fixes
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/6
- issued: 2026-10-14
- session: Claude Code CLI (Fable 5.1); session 51fca711
- status: workspace-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b3-postmerge-fixes
- epic: search-extensibility
- workspace-pr: https://github.com/PyAutoLabs/autofit_inference/pull/7
- companion-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/28
- next: human /prm — merge autofit_inference#7 first, then PyAutoInsight#28; both green 2026-10-14. After #7 merges the Insight `fit` snapshot needs one refresh (ingest reads producer main); the new acceptance test already accepts revision 162644e. Contract stayed inference-summary@1 (additive fields). `@2` freeze proceeds on 17 calibration rows (decision on the PR); the freeze commit itself is B5's first step.
- repos:
  - autofit_inference: feature/search-ext-b3-postmerge-fixes
  - PyAutoInsight: feature/search-ext-b3-postmerge-fixes

## search-ext-b4a-breakdown-exporter
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/2
- issued: 2026-10-14
- session: Claude Code CLI (Fable 5.1); session 51fca711
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b4a-breakdown-exporter
- epic: search-extensibility
- next: implement B4a (Opus worker): autofit_profiling PR first, then PyAutoPulse PR (merges after Pages deploy), then autofit_workspace_developer deletion PR; human /prm
- repos:
  - autofit_profiling: feature/search-ext-b4a-breakdown-exporter
  - PyAutoPulse: feature/search-ext-b4a-breakdown-exporter
  - autofit_workspace_developer: feature/search-ext-b4a-breakdown-exporter
