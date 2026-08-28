# Active Tasks



## bundle-themes
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/311
- issued: 2026-08-27
- prompt: active/bundle_theme_grouping.md
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/bundle-themes
- repos:
  - PyAutoBrain: feature/bundle-themes
  - PyAutoMind: feature/bundle-themes

## numba-cpu-nnls-iteration-reduction
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/498
- prompt: active/numba_cpu_likelihood_nnls_iteration_reduction.md
- issued: 2026-08-27
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/numba-cpu-nnls-iteration-reduction
- repos:
- note: epic numba-cpu-likelihood phase 3a. PLAN APPROVED-PENDING on the issue (user paused for the
  night 2026-08-27 before /start_library ran — no worktree, no branch, no source edits exist yet).
  RESUME: read the issue plan, then `/start_library numba-cpu-nnls-iteration-reduction PyAutoArray`
  (PyAutoArray only — autolens_profiling is claimed by harvest-0827-gate-b-pt2 / #183, awaiting-merge,
  disjoint files; take that leg via /start_workspace after #183 merges). Fable session → delegate
  implementation to Opus. Measure with AUTOARRAY_NUMBA_OPERATED_MEMO=0 (harness is memo-blind).
  Phase 3b (batched active-set moves) is NOT filed — file it from 3a's diagnostic numbers.

## ell-comps-disk-constraint
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1537
- issued: 2026-08-27
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/ell-comps-disk-constraint
- repos:
  - PyAutoFit: feature/ell-comps-disk-constraint
  - PyAutoGalaxy: feature/ell-comps-disk-constraint
