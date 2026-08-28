# Active Tasks

## numba-cpu-nnls-iteration-reduction
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/498
- prompt: active/numba_cpu_likelihood_nnls_iteration_reduction.md
- issued: 2026-08-27
- status: shipping (Heart RED `release validation FAILED (stage integrate)` OVERRIDDEN by user 2026-08-28 for this task — being fixed elsewhere); /prm authorized
- worktree: ~/Code/PyAutoLabs-wt/numba-cpu-nnls-iteration-reduction
- repos:
  - PyAutoArray: feature/numba-cpu-nnls-iteration-reduction
  - autolens_profiling: feature/numba-cpu-nnls-iteration-reduction
- note: epic numba-cpu-likelihood phase 3a. 2026-08-28: implementation + measurement DONE, committed
  LOCALLY only (PyAutoArray 105f6ea4+cfd7f802 guard, autolens_profiling 26cbfef+2ebf80b matrix; neither pushed, no PRs). 32-cell lens-model robustness matrix clean; relative fallback guard nnls_warm_start_error_tolerance=1.5 added. Gate met:
  random-walk median iterations 9.9x (euclid) / 4.0x (hst) fewer, parity 3e-14 → default TRUE shipped.
  Heart RED `release validation FAILED (stage integrate)` = the unfixed autolens_workspace_test MGE pin
  pair (rectangular_mge.py / rectangular_mge_rtu.py, still 99d63b3) — unrelated, but ship_library forbids
  push/PR under RED. RESUME: once Heart is GREEN or the user acks the RED reason, /ship_library
  (drafted PR body: scratchpad pr_body_array.md — re-derive from the commit if lost), then /ship_workspace
  for autolens_profiling. Phase 3b: measurement says warm path has 7-8 iterations left; only the cold /
  i.i.d. path (30-95 outer) motivates it — file from results/notes/nnls_warm_start_memo.md. Measure with AUTOARRAY_NUMBA_OPERATED_MEMO=0 (harness is memo-blind).
  Phase 3b (batched active-set moves) is NOT filed — file it from 3a's diagnostic numbers.
