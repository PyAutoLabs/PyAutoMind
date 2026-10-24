
## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## likelihood-lifecycle-p0-profiling
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/442
- issued: 2026-10-23
- session: claude-code (local CLI, Opus 5.5)
- status: workspace-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p0-profiling
- prompt: active/likelihood_lifecycle_p0_profiling.md
- epic: likelihood-lifecycle
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/444 (PR 1 of 6, migration map) → aeef2756, 2026-10-23
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/447 (PR 2 of 6, move-only) → 0c6be19b, 2026-10-24
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/448 (PR 3 of 6, catalogue builder @3) → 81183fd8, 2026-10-24
- merged: https://github.com/PyAutoLabs/PyAutoPulse/pull/74 (PR 4, lens re-pin @3, receipt refetched; pulse check OK) → 5f3ec2c8, 2026-10-24
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/449 (PR 3b legacy layout; review CLEAN after fixes)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/450 (PR 5 misc grouping, stacked on #449; review CLEAN)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/451 (PR 6 coverage+parity, stacked on #450; review CLEAN; LAST 0B PR)
- next: human /prm 449 → 450 → 451 IN ORDER (stacked; base main); after 451 merges the task is complete → full close-out (record, issue close, worktrees -misc/-coverage removed); phase 0 then done
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p0-profiling-legacy (+ worktrees likelihood-lifecycle-p0-profiling-misc, -coverage for stacked -misc / -coverage)

## eclipse-catalogue-site
- issue: https://github.com/PyAutoLabs/ECLIPSE_lens_catalogue/issues/1
- issued: 2026-10-24
- session: Claude Code CLI (Fable 5.1), session de58e403
- status: pr-open
- worktree: ~/Code/PyAutoLabs/lens/ECLIPSE_lens_catalogue
- repos:
  - ECLIPSE_lens_catalogue: feature/eclipse-catalogue-site
- prs:
  - https://github.com/PyAutoLabs/ECLIPSE_lens_catalogue/pull/2
