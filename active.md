
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
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/448 (PR 3 of 6, catalogue builder @3)
- workspace-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/74 (PR 4, lens re-pin @3; merge AFTER #448, refetch lens receipt on branch first)
- next: human /prm 448 then /prm PyAutoPulse#74 back to back (lens receipt invalid between); then PR 3b (draft likelihood_lifecycle_p0_profiling_3b_legacy_layout.md) → PR 5 misc → PR 6 coverage+parity
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p0-profiling-builder
  - PyAutoPulse: feature/likelihood-lifecycle-p0-profiling (registry re-pin #74)
