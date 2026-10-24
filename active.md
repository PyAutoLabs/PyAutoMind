
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
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p0-profiling
- prompt: active/likelihood_lifecycle_p0_profiling.md
- epic: likelihood-lifecycle
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/444 (PR 1 of 6, migration map) → aeef2756, 2026-10-23
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/447 (PR 2 of 6, move-only) → 0c6be19b, 2026-10-24
- next: PR 3 catalogue builder IN PROGRESS 2026-10-24 on feature/likelihood-lifecycle-p0-profiling-builder (@3; size rule Delaunay 1250 / rectangular 35²=1225; old-layout writers → new tree; drop results_layout.py shim; mirror test) → /ship_workspace → human /prm; then Pulse lens re-pin @3
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p0-profiling-builder
  - PyAutoPulse: feature/likelihood-lifecycle-p0-profiling (registry re-pin, after builder merges)
