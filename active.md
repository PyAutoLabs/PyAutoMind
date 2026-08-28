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

## interferometer-sparse-func-list
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/499
- issued: 2026-08-28
- user-facing: true
- session: claude --resume b766a19b-260c-4b56-8d19-072fa9a34b28
- status: workspace-shipped, awaiting-merge (library-first: #500 then workspace PRs)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/500
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/283
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/115
- heart-ack: RED acknowledged 2026-08-28 (release integrate failure = MGE pin pair; shared_preloads.py timeout; hook-manifest drift — all unrelated)
- worktree: ~/Code/PyAutoLabs-wt/interferometer-sparse-func-list
- repos:
  - PyAutoArray: feature/interferometer-sparse-func-list
  - autolens_workspace_test: feature/interferometer-sparse-func-list
  - autogalaxy_workspace_test: feature/interferometer-sparse-func-list
- parallel-claim: PyAutoArray also claimed by numba-cpu-nnls-iteration-reduction (util/ NNLS + Cholesky files);
  this task touches inversion/inversion/interferometer/{sparse.py,inversion_interferometer_util.py} + factory.py +
  its tests only — disjoint file sets, own worktree approved by the human 2026-08-28.
- note: external reporter @HRSAstro. Receipt + plan comments posted 2026-08-28 (milestones 1-2 of ~4).
  Plan: off-diag operator methods on InterferometerSparseOperator, func-list dispatch in
  InversionInterferometerSparse.curvature_matrix/data_vector, loud factory failure for unrepresentable
  sparse routing, parity tests vs InversionInterferometerMapping. Commit 539d9ffd, PR #500 open (workspace impact: none — option iii). Workspace follow-up (user request 2026-08-28): sparse-vs-mapping FitInterferometer parity scripts in autolens_workspace_test + autogalaxy_workspace_test (+ imaging for autogalaxy), registered in smoke_tests.txt with `ENV: jax`. Workspace PRs open (al#283 ae977686, ag#115 a358186a); they FAIL smoke CI against PyAutoArray main until #500 merges. Next: /prm #500 (CI green ffafa86a), then /prm al#283 + ag#115; milestone #4 comment at merge. Follow-up candidates (not filed): unequal real/imag sigma degrades W~ sparse path (pre-existing); delaunay_nn*.py ENV lines lack __Env__ header so are dead.
