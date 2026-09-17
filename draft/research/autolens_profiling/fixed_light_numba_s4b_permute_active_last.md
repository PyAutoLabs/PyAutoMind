# Fixed-light numba CPU round 4, wave B — A-prime: permute the active columns last, one potrf (lever 4b)

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
Autonomy: human-required
Priority: high
Status: split out of `fixed-light-numba-s4` at close-out 2026-09-17 — wave A (lever 4a, the curvature-kernel A/B) shipped in `complete/2026/09/fixed-light-numba-s4.md` (autolens_profiling#275, PyAutoArray#557); this is what remains.
Epic: fixed-lens-light-numba-cpu
Phase: 4
Consequence: judge
Witness: On HST Delaunay N=1500 numba CPU (RAL gpu partition CPUs-only, 1 thread), lever 4b carries a before/after whole-call table with thread and backend recorded per leg, keeps the active set on every seeded draw within the witness's declared tolerance with the PDIP fallback count unchanged, returns the library's log evidence to <= 1e-9 relative, and the note chains the cumulative from 413.3 ms.
Review-minutes: 30
Unattended: never
Filed: 2026-09-17

## Context

Wave A measured lever 4a and found no lever: two-stage is the right curvature kernel on Delaunay too
(`results/notes/fixed_lens_light_s4_2026_09.md`; control `b` 230.149 ms reproduces lever 3's 230.031 ms).
The remaining dominant site after `sparse_numba.curvature_matrix` (87.7 ms) is `solver.fnnls_cholesky` at
61.5 ms (27 %). Lever 3's design measured the permuted factorisation at 41 ms against it, reading ~15–20 ms
more by folding both fancy-index copies (`ZTZ[P_inorder][:, P_inorder]`, `fnnls.py:127-137`) and the
per-iteration row gather (`:199-201`) into one symmetric permutation of `ZTZ` to passive-first order and one
`potrf` on the leading block. The cost: the passive factor is perturbed at 5e-13, which reaches the active
set's knife-edge inclusion decisions, so the solve is no longer byte-identical and lever 3's cleanest property
is given up. That is why the witness comes before the kernel.

## Plan (issue #274 steps 9–12, unchanged)

9. **Witness design first, as a note section + test, no kernel yet** — define "same active set at 5e-13" on
   the cell's seeded draw set (`--instances iid`, the phase-2 graded draws): per draw, active-set Jaccard vs
   the library `fnnls_cholesky` (expect 1.0; report every draw < 1.0 with the KKT residual of both solutions),
   Δ log evidence in nats (gate ≤ 1e-9 relative like W3), PDIP fallback count unchanged, `solver_stats`
   iteration counts. Written into the s4 note's "4b witness" section and reviewed by the human before step 10.
10. **Kernel** — `fnnls_cholesky_permuted` in `scripts/misc/likelihood_breakdown/fixed_light_numpy_solvers.py`
    next to `nnls_factor_reuse`; outer loop otherwise unchanged; `stats`/`factor` published in the same shape
    so lever 3's `log_det_from_passive_cholesky_from` still reads it. Injected as route `d_perm` through
    `numpy_solver_injected` (signature `solver(ZTZ, ZTx, *, stats)`).
11. **A/B + witness on RAL** — same submit family as s4 (new submit, own WALL-BASIS pinned from job 343394's
    measured 162 s, not from 343356), rows `b` vs `d_perm`, `--n-repeats 64`; witness script
    `fixed_light_numba_s4b_witness.py` implementing step 9's metrics. Verdict rule, written before the run:
    lever iff ≥ 5 % on the whole call AND the witness passes on every draw. Promote to PyAutoArray
    `fnnls_cholesky` only then, as its own PR.
12. Close: the note's "Phase 4 — the whole campaign" table chaining from 413.3 ms; `/prm`.

## Carried follow-ups from wave A

- Re-pin the s4 submit's `# WALL-BASIS:` block (7200 s → measured 162 s × 1.5 ≈ 250 s, `ref: RAL-job-343394`)
  in the same PR that adds the s4b submit, so the family's contract is honest.
- The `hpc/batch_gpu` array-submit dataset guard still checks `data.fits` (tracked) rather than the gitignored
  `lensed_source.fits` adapt cache (#273 finding) — unrelated to this lever, listed so it is not lost.

## Out of scope

Everything wave A closed (the curvature kernel choice, the touched variant), `fnnls` changes beyond A′, the
JAX path, route a, Euclid, rectangular meshes, the source-pixel sweep.
