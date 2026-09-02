# Numba CPU sparse-operator likelihood — speed restoration

## Retired from epics.md (2026-09-02)

## numba-cpu-likelihood
- title: Numba CPU sparse-operator likelihood — speed restoration
- ledger: complete/2026/08/numba-cpu-mge-batch-convolve-cache.md
- status: COMPLETE 2026-08-28. phase 1 SHIPPED 2026-08-27; phase 2a CLOSED as superseded (Bilinear rank-CDF is every default since PyAutoArray#462; the kernel-CDF/RTU path got its numba kernel in #458 and is GPU-only territory — complete/2026/08/numba-cpu-kernel-cdf-fast-path.md); phase 2b SHIPPED 2026-08-21 (backfilled); phase 3a SHIPPED 2026-08-28 (PyAutoArray#501, autolens_profiling#184); 3b NOT filed — only the cold path motivates it. Successor: HST-resolution speed-up (curvature matrix F), filed separately
- notes: Profiling shipped (autolens_profiling#151, complete/2026/08/numba-cpu-likelihood-profiling.md);
  first-call garbage bug shipped (complete/2026/08/numba-first-call-garbage-psf-weighted-data.md).
  Phase 1 = MGE batched convolution + operated-matrix caching + Convolver state reuse (PyAutoArray#497,
  PyAutoGalaxy#588). Phase 2a = kernel-CDF numba fast path
  (complete/2026/08/numba-cpu-kernel-cdf-fast-path.md — superseded by #462 + #458). Phase 2b = fnnls in-place Cholesky buffer (PyAutoArray#453/#463,
  complete/2026/08/numba-fnnls-inplace-cholesky-buffer.md — shipped untracked, backfilled). Phase 3 =
  active-set ITERATION reduction for the positive-only solve (the 72-78% Delaunay term is iteration-bound,
  not linear-algebra-bound): 3a = complete/2026/08/numba-cpu-nnls-iteration-reduction.md (PyAutoArray#498 → #501, autolens_profiling#184; random-walk iterations 9.9x/4.0x fewer; post-#497 the solve is 40%/17% of an eval — at hst the curvature matrix F now dominates);
  3b = batched active-set moves — 3a's matrix (autolens_profiling results/notes/nnls_warm_start_memo_matrix.md) shows it only pays on the cold / i.i.d. path (30-95 outer iterations); file only for that regime.
  NOTE the "restore the deleted numba fnnls" idea is RETIRED (#151 comment 5) — do not re-file it.
  Measurement prerequisite for every phase: draft/feature/autolens_profiling/numba_breakdown_harness_memo_blind.md.
  One issue at a time, never a bulk queue.
