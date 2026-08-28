## numba-cpu-nnls-iteration-reduction
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/498 (closed, completed)
- completed: 2026-08-28
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/501 (MERGED 1f5c636e)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/184 (MERGED 9a04e5ff)
- epic: numba-cpu-likelihood — phase 3a
- shipped: PyAutoArray — `fnnls_cholesky(…, stats=None)` diagnostics (outer/inner iterations, final
  passive set, warm-start errors), mask-or-index `P_initial`, warm start factorised ONCE and extended in
  place (was dense `solve` + from-scratch `cholesky` on the first outer iteration), infeasible warm
  passive set repaired BEFORE the outer loop (an all-True seed used to skip the loop and return the
  clipped vector — unreachable from the dense-sign start, reachable from a memo seed; the repair is an
  explicit drop-and-refactor because `fix_constraint_cholesky` has no prior feasible iterate there and its
  `alpha` is 0/0). Cross-evaluation memo `autoarray/inversion/inversion/nnls_memo.py` (FIFO 8, keyed on
  `n` + mesh/data shapes + `ids_to_keep` hash, `AUTOARRAY_NNLS_WARM_START=0` kill-switch), wired through
  `reconstruction_positive_only_from(…, fingerprint=)` / `AbstractInversion._nnls_warm_start_fingerprint`,
  with a once-only dense-sign retry on a failed seeded solve. `Settings.nnls_warm_start_memo` default
  TRUE (yaml AND the `KeyError` fallback — workspace `general.yaml`s shadow autoarray's and lack the key;
  the test suite's own config does too). Relative fallback guard `Settings.nnls_warm_start_error_tolerance`
  = 1.5: each entry keeps the dense-sign start's error fraction; a seed worse than 1.5× it is dropped and
  the next solve restarts dense.
  autolens_profiling — `delaunay_numba_nnls_iterations.py` (`--model`, `--n-instances`, fallback counts),
  `nnls_iterations_matrix.py`, notes `nnls_warm_start_memo.md` + `nnls_warm_start_memo_matrix.md`.
- measured: Delaunay-1250 + MGE-60 fiducial, random walk: median active-set iterations 70→7 (euclid,
  9.9×), 32→8 (hst, 4.0×); solve 0.54→0.05 s / 0.25→0.07 s; whole evaluation 1.51→0.56 s (euclid).
  32-cell lens-model matrix (PowerLaw, NFW subhalo, no/Sersic lens light, rectangular mesh, AdaptSplit,
  no edge-zeroing, complex source, Hilbert 600/2000; euclid + hst): parity ≤ 4e-14 everywhere, 0 seeded
  failures, median solve time never worse than memo-off by >2%; every random-walk cell gains
  (3.2×–118×, rectangular most — its dense-sign start is 44–70% wrong); only i.i.d. sequences lose
  iterations (worst 0.52×), never time. Guard fired 3/240 evaluations, all in the one cell at seed/dense
  ratio 1.42. test_autoarray 1279 passed.
- finding: post-#453/#497 the solve is 40% (euclid) / 17% (hst) of an evaluation, not the ~72% the
  phase-3 prompt cited; at hst the curvature matrix F (1.77 s) dominates. Re-profile before filing more
  solve-side phases.
- finding: seed quality is only separable RELATIVE to the dense-sign start — absolute seed error fraction
  overlaps between helpful and harmful cells (0.048–0.138); the seed/dense ratio separates (≤0.89 vs 1.42).
- trap: `fix_constraint_cholesky` cannot repair a warm start — with `d = clip(s_chol)` every violator has
  `d[q] − s_chol[q] == 0`, so `alpha` is 0/0 (nan) or x/0 (inf).
- trap: the fingerprint is shape-based on purpose (the memo must hit across nearby parameter points); a
  key only churns when the index space changes (`ids_to_keep`), which no mesh in the matrix does.
- gate: shipped over Heart RED `release validation FAILED (stage integrate)` (unrelated
  autolens_workspace_test `rectangular_mge{,_rtu}.py` pin drift, being fixed separately) on explicit
  human authorisation 2026-08-28.
- epic next: phase 3b (batched active-set moves) is NOT a warm-path win — the warm path is at 7–8
  iterations; its only remaining case is the cold / uncorrelated path (30–95 outer iterations: first
  evaluation, i.i.d.-like proposals). File it, if at all, from `nnls_warm_start_memo_matrix.md`. Phase 2a
  kernel-CDF still deferred. At hst the next target is the curvature matrix F, not the solve.
- affected-repos:
  - PyAutoArray
  - autolens_profiling

## Original prompt

# Numba CPU likelihood phase 3: cut the positive-only solve's active-set iterations (warm start across evaluations + block pivoting)

Type: feature
Epic: numba-cpu-likelihood
Phase: 3a
Target: autoarray
Repos:
- @PyAutoArray
- @autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-08-27
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
