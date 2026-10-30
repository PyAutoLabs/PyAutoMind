
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

## leggos-ii-literature-ingest
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/170
- issued: 2026-10-30
- session: claude-code desktop (WSL), PyAutoLabs session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/leggos-ii-literature-ingest
- repos:
  - autolens_assistant: feature/leggos-ii-literature-ingest
- prompt: active/leggos_ii_literature_ingest.md
- epic: cluster-strong-lensing (phase 6d)
- tier: judge — human said "go" (continue phase 6; prior slices merged on green)
