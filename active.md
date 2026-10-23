
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
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/447 (PR 2 of 6, move-only, rebuilt after #441, head 0cce1ba8; #446 closed superseded)
- next: RESUME 2026-10-24 — #447 lint was red on ruff format (newer CI ruff formats md code blocks in a moved archive note) → fixed 0cce1ba8 (archive/ added to ruff extend-exclude), lint rerun in progress at wrap-up; human /prm #447 when green; then PR 3 catalogue builder (@3; size rule Delaunay 1250 / rectangular 35²=1225; adapt remaining old-layout writers; drop results_layout.py shim)
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p0-profiling-move-v2
  - PyAutoPulse: feature/likelihood-lifecycle-p0-profiling (registry re-pin, after builder merges)
