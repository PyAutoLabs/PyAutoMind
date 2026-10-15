# Active Tasks

## delaunay-nn-numba
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/623
- issued: 2026-10-15
- prompt: active/make_delaunaynn_fast_on_the_numba_numpy.md
- session: Claude Code CLI (Opus 5.5); session 0b91c774
- status: library-shipped, awaiting-merge (phase 1 #624, phase 2 #625 stacked)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/624
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/625
- worktree: ~/Code/PyAutoLabs-wt/delaunay-nn-numba
- phase: 2 of 2 shipped — #624 numba Sibson kernel; #625 routing tests (no routing change needed); follow-up draft/feature/autoarray/delaunaynn_wide_row_imaging_overhead.md
- next: human /prm #624 then #625 (stacked, base feature/delaunay-nn-numba — retarget/merge in order)
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
