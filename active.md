
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
- concurrency: ruling F11 — shares PyAutoFit with hpc-campaign-p2-campaign-core; owns autofit/results/, aggregator/, status/identity.py, ResultState in states.py, identity hook
- tier: judge — merge mode: human /prm
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1743
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1744 (stacked on #1743)
- heart-ack: STALE (release validation stale: source moved since rehearsal) — human 2026-10-30

## hpc-campaign-p2-campaign-core
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1740
- issued: 2026-10-30
- session: claude-code desktop (WSL), PyAutoLabs session (background fork)
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/hpc-campaign-p2-campaign-core
- repos:
  - PyAutoFit: feature/hpc-campaign-p2-campaign-core
  - PyAutoFit: feature/hpc-campaign-p2b-collector-retro
- prompt: active/hpc_campaign_p2_campaign_core.md
- epic: hpc-campaign (phase 2)
- concurrency: ruling F11 — shares PyAutoFit with results-library-p1-index; owns autofit/campaign/ only
- tier: judge — merge mode: human /prm
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1741
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1742 (stacked on #1741)
- heart-ack: STALE (release validation stale: source moved since rehearsal) — human 2026-10-30

## area-magnification-validation
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/351
- issued: 2026-10-30
- session: claude-code desktop (WSL), PyAutoLabs session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/area-magnification-validation
- repos:
  - autolens_workspace_test: feature/area-magnification-validation
- prompt: active/area_magnification_validation.md
- epic: cluster-strong-lensing (phase 6b)
- tier: judge — human authorized merge on green 2026-10-30

## area-magnification-subpixel-area
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/686
- issued: 2026-10-30
- session: claude-code desktop (WSL), PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/area-magnification-subpixel-area
- repos:
  - PyAutoGalaxy: feature/area-magnification-subpixel-area
- epic: cluster-strong-lensing (phase 6a follow-up, blocks 6b smoke)
- tier: judge — human authorized merge on green 2026-10-30
