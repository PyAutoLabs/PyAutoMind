# Active Tasks

## delaunay-nn-numba
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/623
- issued: 2026-10-15
- prompt: active/make_delaunaynn_fast_on_the_numba_numpy.md
- session: Claude Code CLI (Opus 5.5); session 0b91c774
- status: library-shipped, awaiting-merge (phase 1); phase 2 not started
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/624
- worktree: ~/Code/PyAutoLabs-wt/delaunay-nn-numba
- phase: 1 of 2 (numba Sibson kernel) shipped as PR #624; phase 2 = routing audit (Aris measurement already shows all meshes on InversionInterferometerSparseNumba; remaining: NaN-weight guard, DelaunayNN routing tests, imaging audit + timing)
- next: human /prm on PyAutoArray#624 (CI green); phase 2 in progress stacked on it (branch feature/delaunay-nn-numba-routing)
- heart-red-override:
  - date: 2026-10-15
  - authorized-by: live human in session 0b91c774 ("I override, tests will be handled once the epic refactor elsewhere is sorted")
  - reasons: see issue #623 (verbatim reason strings recorded there)
  - permitted: commit, push, PR-open; merge separate
- repos:
  - PyAutoArray: feature/delaunay-nn-numba, feature/delaunay-nn-numba-routing

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
