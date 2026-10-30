
## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## r2-pages-function-access
- issue: https://github.com/PyAutoLabs/ECLIPSE_lens_catalogue/issues/4
- issued: 2026-10-29
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/r2-pages-function-access
- repos:
  - ECLIPSE_lens_catalogue: feature/r2-pages-function-access
- tier: judge — merge mode: human /prm

## results-library-p1-index
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1739
- issued: 2026-10-30
- session: claude-code desktop (WSL), PyAutoLabs session
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/results-library-p1-index
- repos:
  - PyAutoFit: feature/results-library-p1-index
  - PyAutoFit: feature/results-library-p1b-lazy-reads
- prompt: active/results_library_p1_index.md
- epic: results-library (phase 1)
- concurrency: ruling F11 — shared PyAutoFit with hpc-campaign-p2-campaign-core (merged 2026-10-30); owns autofit/results/, aggregator/, status/identity.py, ResultState in states.py, identity hook
- tier: judge — merge mode: human /prm
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1743
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1744 (stacked on #1743)
- heart-ack: STALE (release validation stale: source moved since rehearsal) — human 2026-10-30

## hpc-campaign-p3-plan-evidence
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1745
- issued: 2026-10-30
- session: claude-code desktop (WSL), PyAutoLabs session (background fork)
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/hpc-campaign-p3-plan-evidence
- repos:
  - PyAutoFit: feature/hpc-campaign-p3-plan-evidence
- prompt: active/hpc_campaign_p3_plan_evidence.md
- epic: hpc-campaign (phase 3)
- concurrency: ruling F11 — shares PyAutoFit with hpc-campaign-p4-carbon-report (disjoint campaign/ files; __main__.py shared, p3 merges first) and results-library-p1-index (shipped, awaiting /prm; disjoint results/ + aggregator/)
- heart-red-override: authorized live by the human 2026-10-30 ("Override, proceed") for hpc-campaign phases 3 + 4; RED reasons quoted on PyAutoFit#1745; development only, merge via /prm
- tier: judge — merge mode: human /prm
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1747

## hpc-campaign-p4-carbon-report
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1746
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/208
- issued: 2026-10-30
- session: claude-code desktop (WSL), PyAutoLabs session (background fork)
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/hpc-campaign-p4-carbon-report
- repos:
  - PyAutoFit: feature/hpc-campaign-p4-carbon-report
  - PyAutoNerves: feature/hpc-campaign-p4-carbon-report
- prompt: active/hpc_campaign_p4_carbon_report.md
- epic: hpc-campaign (phase 4)
- concurrency: ruling F11 — shares PyAutoFit with hpc-campaign-p3-plan-evidence (rebases onto p3 for __main__.py) and results-library-p1-index (shipped, awaiting /prm)
- heart-red-override: authorized live by the human 2026-10-30 ("Override, proceed") for hpc-campaign phases 3 + 4; RED reasons quoted on PyAutoFit#1746
- tier: judge — merge mode: human /prm
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1748 (stacked on #1747)
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/209

## magnification-latent-raw-flux
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/812
- issued: 2026-10-30
- session: claude-code desktop (WSL), PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/magnification-latent-raw-flux
- repos:
  - PyAutoLens: feature/magnification-latent-raw-flux
  - autolens_workspace: feature/magnification-latent-raw-flux
- prompt: active/magnification_latent_raw_flux.md
- epic: cluster-strong-lensing (phase 7a)
- tier: judge
