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
- status: workspace-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b4a-breakdown-exporter
- epic: search-extensibility
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/3
- companion-prs: https://github.com/PyAutoLabs/PyAutoPulse/pull/60 (merge after #3 + Pages live), https://github.com/PyAutoLabs/autofit_workspace_developer/pull/30 (merge after #3; pre-delete SHA 06d86ac1)
- next: human /prm in order — (1) autofit_profiling#3, wait for pages_dashboard.yml on main and the Pages site (Pages enabled via API, 404 until first deploy; org secret PAT_PYAUTOLABS reach unverified — if the pulse-refresh dispatch is skipped, run Pulse's refresh by hand); (2) on the PyAutoPulse#60 branch run `bin/pyauto-pulse board` online, commit receipts/fit.json + snapshots/fit.json + the four board files, then merge (check --offline fails `fit: no receipt yet` until then, by design); (3) autofit_workspace_developer#30 — make the Gut condemned.md entry at close-out. OPEN DECISION: `searches_minimal/nautilus_sweep.py` and `nautilus_jax_mlp.py` import the deleted module and `output/nautilus_profile_summary.txt` remains; retire them too or keep. Headline B4a finding: Nautilus checkpoint writes are 24.5 % of a full search.fit on gaussian_x1 (bare-sampler anatomy reproduced within ±10 pp, log Z -57.455). Epic 2 not opened.
- repos:
  - autofit_profiling: feature/search-ext-b4a-breakdown-exporter
  - PyAutoPulse: feature/search-ext-b4a-breakdown-exporter
  - autofit_workspace_developer: feature/search-ext-b4a-breakdown-exporter
