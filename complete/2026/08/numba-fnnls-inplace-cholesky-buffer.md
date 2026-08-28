## numba-fnnls-inplace-cholesky-buffer
- issue: none — PR-only (2026-08-20 session off autolens_profiling#151 comments 5-6); backfilled 2026-08-27 while scoping epic numba-cpu-likelihood phase 3.
- completed: 2026-08-21
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/453 (MERGED 2026-08-20, commits 2c9a22bb + 89be276c)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/463 (MERGED 2026-08-21, fc00636a)
- epic: numba-cpu-likelihood — phase 2b (solver, first lever)
- shipped: `fnnls_cholesky` (autoarray/util/fnnls.py, Bro & De Jong active-set NNLS with Cholesky
  up/down-dating — the LIVE numpy/numba positive-only solver, never deleted for good: dropped as dead
  code in 8bb449a1, restored verbatim in 47d81d28) now keeps its factor in a preallocated buffer with
  copy-free numba kernels `_solve_upper_transposed_buffer`, `_cho_solve_buffer`,
  `cholinsertlast_inplace`, `choldeleteindexes_inplace`, `_choldelete_shift_buffer`
  (autoarray/util/cholesky_funcs.py). #463: coerce JAX `ZTx` inputs to numpy for the buffer kernels.
- measured (PR text): euclid Delaunay-1310 solve 1.40 s → 1.16 s in-place, 2.83× vs the 3.29 s
  pre-buffer baseline; euclid eval 2.34 s/call.
- verdict carried: the "restore the deleted numba fnnls" hypothesis from #151 comment 4 is RETIRED
  (comment 5): the solver was present all along; the cost was the np.insert/np.delete factor rebuilds
  around the up/down-dates (3.58 s of a 5.06 s solve at 1560), and the solve is ITERATION-bound
  (153 active-set iterations; warm start gets 1411/1560 right), not resolution-bound.
- lifecycle note: shipped with no Mind prompt or record; the phase-1 record and epics.md briefly
  advertised "phase 3 = restore fnnls" on the strength of the stale comment-4 suspicion (corrected
  2026-08-27). Tests: test_autoarray/util/test_cholesky_inplace.py, test_cholesky_degenerate.py.
- affected-repos:
  - PyAutoArray
