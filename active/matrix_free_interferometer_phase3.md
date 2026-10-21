# Matrix-free interferometer inversion, phase 3: log-evidence via exact sparse log-det + stochastic Lanczos quadrature

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
Witness: tests asserting (i) ln det P from the sparse LU equals numpy slogdet of the dense P to 1e-10; (ii) the SLQ estimate of ln det(F + H) on a small rectangular-mesh interferometer case lies within 0.5% of the dense slogdet for 10 probes / 40 steps with a fixed seed, and the estimate is deterministic for a fixed seed; (iii) the matrix-free log_evidence equals InversionInterferometerSparse.log_evidence (unconstrained, same MaternSparse) within the same tolerance on the ln det term and exactly on the other four terms
Review-minutes: 6
Unattended: ready
Filed: 2026-10-21
Issued: 2026-10-21

## Why

Phase 3 of PyAutoArray#638 (hub #39, @HRSAstro; reference section 5 `log_det_A` / `log_evidence` of the attached upstream_snippets.py). The evidence needs ln det(F + H) and ln det H without forming n×n matrices. ln det H is exact from the sparse factor (phase 2 `MaternSparse`). ln det(F + H) = ln det P + ln det(P⁻¹(F + H)) with P the Powell preconditioner (phase 1): the first term is exact from P's sparse LU, the second from stochastic Lanczos quadrature (Ubaru, Chen & Saad 2017) in the P inner product with probes v ~ N(0, P⁻¹) drawn via P = BᵀB, B = [√κ₀ M; √λ R], full reorthogonalisation, fixed seed so the estimate is smooth in λ. The contributor reports ~0.2% of ln Z agreement; Powell et al. stop at ln det P (1-20% off).

## What to build

1. In `inversion_interferometer_matrix_free_util.py`: `log_det_preconditioner_from(lu)`; `log_det_curvature_reg_via_slq_from(operator, regularization_sparse, R_sparse, coefficient, n_probes=10, n_steps=40, seed=...)` (Lanczos on P⁻¹A, P-orthonormal, full reorthogonalisation, Gauss quadrature on the tridiagonal eigenpairs; returns mean estimate and the per-probe spread); `log_evidence_matrix_free_from(operator, regularization, coefficient, reconstruction, data_term, noise_normalization)` assembling the five terms (chi² = dᵀN⁻¹d − 2 sᵀD + sᵀFs, regularization term, ln det(F+H), −ln det H, noise normalisation) with the same sign/0.5 conventions as `AbstractInversion.log_evidence`.
2. `MaternSparse` exposes its factor R (phase 2) for the probe draw.
3. Tests `test_matrix_free_util.py`: ln det P exact; SLQ within 0.5% of dense; deterministic seed; probe-count convergence (error shrinks from 2 → 10 probes); evidence parity with the dense path term by term. numpy/scipy only; nojax leg.

## Acceptance

Witness passes; tolerance documented in the module docstring; #638 and hub thread updated at PR-open.
