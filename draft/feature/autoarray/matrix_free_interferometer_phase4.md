# Matrix-free interferometer inversion, phase 4: positivity via primal-dual interior point with active-set polish

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: high
Parent: active/matrix_free_interferometer_inversion.md
Community: https://github.com/PyAutoLabs/.github/discussions/39
Status: formalised
Consequence: glance
Witness: tests asserting on a small rectangular-mesh interferometer case that the matrix-free positive solve (i) returns exact zeros on the same support as scipy.optimize.nnls applied to the Cholesky-whitened dense system, (ii) agrees with that NNLS solution to 1e-6 relative to its max, and (iii) agrees with InversionInterferometerSparse's positive-only reconstruction (same MaternSparse) to a documented tolerance
Review-minutes: 6
Unattended: ready
Filed: 2026-10-21
Issued: 2026-10-21

## Why

Phase 4 of PyAutoArray#638 (hub #39, @HRSAstro; reference section 6 `solve_positive` of the attached upstream_snippets.py). Positivity without an n×n factorisation: Mehrotra predictor-corrector primal-dual interior point on (F + H)x = D, x ≥ 0, each step a CG solve preconditioned by P plus the barrier diagonal; once the active set settles, the free pixels are solved exactly with CG (exact zeros) and a few primal-dual active-set corrections (Hintermüller, Ito & Kunisch 2002). The contributor found projected Newton and pure active-set stall at weak priors with ~30% of pixels at zero; this method matches scipy NNLS on small problems.

## What to build

1. In `inversion_interferometer_matrix_free_util.py`: `reconstruction_positive_via_interior_point_from(operator, regularization_sparse, coefficient, max_steps=60, tol=1e-9)` — Jacobi start, Mehrotra predictor/corrector with centring parameter σ = (μ_aff/μ)³, fraction-to-boundary 0.99, CG tolerance tied to the duality gap, barrier-diagonal-augmented P refactorised per step; then support detection (z ≤ diag·x), exact CG solve on the free set with the sub-preconditioner P[free, free], one or more active-set corrections if negatives appear; returns the solution, the support mask and iteration counts.
2. Tests `test_matrix_free_util.py`: support and values vs scipy NNLS on the whitened dense system (two coefficients, one weak so many pixels sit at zero); vs the sparse path's positive-only reconstruction; iteration counts bounded; numpy/scipy only; nojax leg.
3. Document the remaining phase-5 items (profiling note dense vs matrix-free at 50², 64², 128², 192² ingested by Pulse; workspace example; wiring as an inversion class / Settings option) in #638.

## Acceptance

Witness passes; tolerances documented; #638 and hub thread updated at PR-open.
