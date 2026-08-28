# Active Tasks



## bundle-themes
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/311
- issued: 2026-08-27
- prompt: active/bundle_theme_grouping.md
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/312
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/366
- heart-ack: RED acknowledged 2026-08-27 (release integrate failure, shared_preloads.py timeout, hook-manifest drift, stale PyAutoFit PR — all unrelated)
- worktree: ~/Code/PyAutoLabs-wt/bundle-themes
- repos:
  - PyAutoBrain: feature/bundle-themes
  - PyAutoMind: feature/bundle-themes

## numba-cpu-nnls-iteration-reduction
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/498
- prompt: active/numba_cpu_likelihood_nnls_iteration_reduction.md
- issued: 2026-08-27
- status: library-dev, ready-to-ship (BLOCKED on Heart RED)
- worktree: ~/Code/PyAutoLabs-wt/numba-cpu-nnls-iteration-reduction
- repos:
  - PyAutoArray: feature/numba-cpu-nnls-iteration-reduction
  - autolens_profiling: feature/numba-cpu-nnls-iteration-reduction
- note: epic numba-cpu-likelihood phase 3a. 2026-08-28: implementation + measurement DONE, committed
  LOCALLY only (PyAutoArray 105f6ea4, autolens_profiling 26cbfef; neither pushed, no PRs). Gate met:
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
- status: workspace-dev (library-shipped PR #500 awaiting-merge)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/500
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
  sparse routing, parity tests vs InversionInterferometerMapping. Commit 539d9ffd, PR #500 open (workspace impact: none — option iii). Workspace follow-up (user request 2026-08-28): sparse-vs-mapping FitInterferometer parity scripts in autolens_workspace_test + autogalaxy_workspace_test (+ imaging for autogalaxy), registered in smoke_tests.txt with `ENV: jax`. Next: /ship_workspace behind library-first gate, /prm #500 then workspace PRs; milestone #4 comment at merge.

## ell-comps-disk-constraint
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1537
- prompt: active/ell_comps_joint_disk_constraint.md
- issued: 2026-08-27
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1538
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/589
- heart-ack: RED acknowledged 2026-08-28 (release validation FAILED (stage integrate) — the known human-authorised override for this task; unrelated to these branches)
- note: merge PyAutoFit#1538 FIRST — PyAutoGalaxy#589 declares geometry the PyAutoFit PR introduces the machinery to read
- worktree: ~/Code/PyAutoLabs-wt/ell-comps-disk-constraint
- repos:
  - PyAutoFit: feature/ell-comps-disk-constraint
  - PyAutoGalaxy: feature/ell-comps-disk-constraint
