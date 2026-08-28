# Numba CPU likelihood phase 3: cut the positive-only solve's active-set iterations (warm start across evaluations + block pivoting)

Type: feature
Epic: numba-cpu-likelihood
Phase: 3
Target: autoarray
Repos:
- @PyAutoArray
- @autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-08-27

> Phase 3 of the CPU-likelihood speed restoration. Phase 1 (MGE batching +
> caching, PyAutoArray#497 / PyAutoGalaxy#588) and phase 2b (fnnls in-place
> Cholesky buffer, PyAutoArray#453 / #463, backfilled record
> `complete/2026/08/numba-fnnls-inplace-cholesky-buffer.md`) are shipped.
> The "restore the deleted numba fnnls" idea is RETIRED (autolens_profiling#151
> comment 5) — the solver was never missing. Do not re-file it.

## Context (autolens_profiling#151 comments 5-6, PyAutoArray PR#453 text)

On the campaign fiducial (Delaunay + Hilbert AdaptImage + ConstantSplit,
`apply_sparse_operator_cpu()`, `use_jax=False`) the positive-only
reconstruction solve is the dominant term: euclid **3.6 s of 5.0 s (~72%)** at
1250 source pixels, hst 1.4 s (~35%) — pre-#453 numbers; #453 reports the
solve at 1.40 s -> 1.16 s on its 1310-param system, so a re-profile on current
`main` is step 0.

The instrumented probe (comment 5) decomposed a 5.06 s solve at n=1560 as: dense
warm-start solve 0.10 s (1411/1560 positives correct) + initial Cholesky 0.06 s +
**up/down-dates 3.58 s across 154 outer + 102 constraint-fix iterations** +
`cho_solve` 0.99 s + `w` matvecs 0.26 s. One from-scratch Cholesky at n=1560 is
0.08 s. Comment 6: **"the solve is iteration-bound, not resolution- or
param-bound"** — cost tracks how many entries the dense warm start gets wrong
(~150 at euclid, far fewer at hst). #453 removed the copy overhead per
iteration; the iteration COUNT is untouched.

Live solver: `autoarray/util/fnnls.py::fnnls_cholesky(ZTZ, ZTx, P_initial)`
(Bro & De Jong 1997 active set, Cholesky up/down-dating via
`autoarray/util/cholesky_funcs.py` numba kernels), called from
`inversion_util.reconstruction_positive_only_from` (numpy branch, ~line 371)
with `P_initial = np.linalg.solve(curvature_reg_matrix, data_vector) > 0`.
Tests: `test_autoarray/util/test_cholesky_inplace.py`,
`test_cholesky_degenerate.py`.

## Goal

Reduce the number of active-set iterations per solve on the numba CPU path,
keeping the solution the unique NNLS optimum (curvature_reg is PD, so the
solution is unique; pinned log-likelihoods must hold at rtol 1e-6):

1. **Step 0 — re-profile on current main** with the `delaunay_numba`
   breakdown (euclid + hst, 1250) so the baseline post-#453 is recorded; add an
   iteration counter / per-solve diagnostic (outer + inner iterations, passive
   set size, entries the warm start got wrong) to the breakdown so the win is
   measured in iterations, not just seconds.
2. **Cross-evaluation warm start**: seed `P_initial` from the previous
   evaluation's final passive set (same process; nearby parameter points share
   most of the active set) instead of the dense unconstrained solve's sign, with
   the dense solve as fallback when shapes change. Design decision in the plan:
   where the state lives (module-level like the operated-matrix memo, keyed on
   mapper shape; or a `Settings` field / preload passed through the analysis)
   and how multiprocessing workers behave (each worker keeps its own).
3. **Block pivoting** (Portugal-Judice-Vicente style) or a batched
   constraint-fix step so each outer iteration moves many indices at once
   rather than one, bounded by a fallback to the current single-index rule to
   preserve convergence guarantees.
4. Measure: iterations and solve seconds before/after at euclid + hst; pinned
   log-likelihood parity; `test_autoarray` green. Record in autolens_profiling
   (results + notes) and on the issue. Measure with
   `draft/feature/autolens_profiling/numba_breakdown_harness_memo_blind.md`
   landed or with `AUTOARRAY_NUMBA_OPERATED_MEMO=0` (the harness's fixed instance
   would otherwise hide the MGE term and, for a cross-eval warm start, would
   fake a 100%-correct warm start — perturb the instance between repeats).

Out of scope: the JAX PDIP solver (`jax_nnls.py`), the kernel-CDF phase 2a.
