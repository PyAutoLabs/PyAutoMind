# Fixed-light numba CPU round 4 — the curvature-matrix kernel A/B on Delaunay, then permute-active-last

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoArray
Themes:
- profiling
- pixelization
- cpu
- numba
- inversion
Difficulty: large
Sizing-note: the intake sizing faculty derived too-large (score 12); large is kept — the two levers are
ordered and 4a is a measurement of two kernels that already exist; if it must be split, split between
lever 4a and lever 4b, never between a lever and its witness.
Autonomy: human-required
Priority: high
Status: formalised
Epic: fixed-lens-light-numba-cpu
Phase: 4
Consequence: judge
Witness: On HST Delaunay N=1500 numba CPU (RAL gpu partition CPUs-only, 1 thread), each lever carries a
before/after whole-call table with thread and backend recorded per leg; lever 4a returns the library's log
evidence to <= 1e-9 relative; lever 4b keeps the active set on every seeded draw within the witness's declared
tolerance with the PDIP fallback count unchanged; the note chains the cumulative from 413.3 ms.
Review-minutes: 30
Unattended: never
Filed: 2026-09-16
Issued: 2026-09-17
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/274

## Original request (verbatim)

> and you think theres nowhere else tp gp wotj numba? without digging through deeper stuff is level 4 not low hanging
> [...] i think 1 and 2 are worth doing

## Context

Phase 3 (#267, `complete/2026/09/fixed-light-numba-levers.md`) took the production numba CPU
fixed-light call from 413.3 to 230.0 ms. Its residue, from the lever-3 decomposition
(`results/notes/fixed_lens_light_levers_2026_09.md`, "Next"): `sparse_numba.curvature_matrix`
87.8 ms (38 %), `solver.fnnls_cholesky` 61.1 ms (27 %), `delaunay.triangulation` 18.9 ms (8 %),
everything else under 9 ms a site. This phase inserts ahead of the renumbered memo / scaling /
verdict phases of `fixed-lens-light-numba-cpu`, which become 5, 6 and 7. Two levers, measurement
first, in order.

## Lever 4a — A/B the two existing curvature kernels on Delaunay (low-hanging)

`curvature_matrix_via_sparse_operator_from` (PyAutoArray
`inversion/inversion/imaging_numba/inversion_imaging_numba_util.py`) dispatches on a pixel-count cap
(`two_stage_max_pix_pixels` = `CURVATURE_TWO_STAGE_MAX_PIX_PIXELS`) between the two-stage kernel and
the direct quadruple loop. The two-stage docstring itself says it wins for bilinear rectangular
(u0 = 4, 2.9x at the HST rectangular fiducial) and can lose for barycentric Delaunay (u0 ~ 1.55),
because stage 2 does a dense `pix_pixels`-long AXPY per mapping of every data pixel and then
re-zeroes the full accumulator, regardless of how few indices stage 1 touched. The choice was
never measured on the Delaunay fixed-light cell.

1. A/B the two existing kernels on the HST Delaunay N=1500 fixed-light cell (route b, memo ON):
   RAL `gpu` partition CPUs-only, 1 thread across numba and BLAS, the #267 two-arm harness with a
   private merge-base PyAutoArray on PYTHONPATH as control, `--n-repeats 64`. The direct kernel is
   already reachable by passing `two_stage_max_pix_pixels=0`; no library change is needed for the
   measurement.
2. If neither pure form wins, a touched-index variant of stage 2: record the indices stage 1
   touched, scatter only over them, zero only them. Same inputs, same outputs, same
   halved-diagonal / `A + A.T` contract.
3. Fix the stale dispatcher docstring regardless: it names
   `CURVATURE_TWO_STAGE_COST_RATIO_THRESHOLD`, the code branches on `pix_pixels`.

Pins: the kernels agree to floating-point reassociation (~4e-13 measured), log evidence <= 1e-9
relative, `log_likelihood` not comparable across arms.

## Lever 4b — A-prime: permute the active columns last, one potrf

Lever 3's design measured the permuted factorisation at 41 ms against `fnnls_cholesky`'s 61.1 ms,
reading ~15-20 ms more by folding both fancy-index copies and the second pass away. The cost: the
passive factor is perturbed at 5e-13, which reaches the active set's knife-edge inclusion
decisions, so the solve is no longer byte-identical and lever 3's cleanest property is given up.

1. Witness design FIRST: what "the same active set" means at 5e-13 — active-set Jaccard across the
   seeded graded draw set, evidence delta in nats, PDIP fallback count unchanged. Written down and
   agreed before a kernel exists.
2. The kernel, on the numpy/numba path only (`fnnls_cholesky`), behind the same seam lever 3 used.
3. The A/B on the same cell and host, control = lever 4a's merged state.

## Cell prerequisite (before either lever)

The harness's `max_instrumentation_overhead_ratio = 1.03` was calibrated on a ~400 ms call; its
fixed cost does not shrink with the call (1.0147 at 413 ms, 1.0366 at 224 ms) and it killed RAL
job 343355. Fix it in the cell before measuring: scale the cap with call length, or require a
minimum block count, or state it as a per-call millisecond budget (note "Next" item 6).

## Out of scope

`fnnls` algorithm changes beyond A-prime (phase 2 closed the solver round); the edge-zeroed
generalisation and the covariance third factorisation (zero gain on the production cell); the
`delaunay.triangulation` / `find_simplex` site (a separate candidate); the JAX path (both log-det
levers proven CPU-only, the A100 has no fnnls factor to read); route a, Euclid, rectangular meshes,
the source-pixel sweep, the sparse-operator/profile-subtracted-image bug.

## Witness

On HST Delaunay N=1500 numba CPU, each lever carries a before/after whole-call table with thread
and backend settings recorded per leg; 4a returns the library's log evidence to <= 1e-9 relative;
4b keeps the active set on every seeded draw within the witness's declared tolerance and the PDIP
fallback count unchanged; the note carries both tables and the cumulative chain from 413.3 ms.

<!-- formalised by the Intake (Conception) Agent on 2026-09-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/3f1053cc-606f-4477-bef4-abe3a68cd02b/scratchpad/intake_raw.md -->
