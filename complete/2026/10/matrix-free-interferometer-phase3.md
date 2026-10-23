## matrix-free-interferometer-phase3
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/647
- completed: 2026-10-21
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/651 (merge 625e1196)
- parent: https://github.com/PyAutoLabs/PyAutoArray/issues/638 (active/matrix_free_interferometer_inversion.md)
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- summary: |
    Phase 3 of #638. Commits 9feb4f3e, 5d6bbb9d on `feature/matrix-free-interferometer-phase3` (2 files,
    +591/-9): `log_det_preconditioner_from` (exact, sparse LU), `log_det_curvature_reg_via_slq_from`
    (ln det P + SLQ of ln det P⁻¹(F+H), probes ~ N(0, P⁻¹), full reorthogonalisation, fixed seed 20221,
    steps capped at n), `log_evidence_matrix_free_from` (fit_util conventions, optional exact log-det
    substitution; R passed as √coefficient·R₀, verified against H). FINDING: SLQ accuracy depends on how
    well the Powell preconditioner matches F+H — 0.10–0.14% (mean 0.21%, worst 0.56% over 30 seeds) on a
    data-dominated case (500 long-baseline vis, eigenvalues ~[0.6, 1.6]), but 14–40% on the prior-dominated
    tiny fixture (eigenvalues ~[0.01, 63]); tests use the data-dominated case (new uv_scale on the test
    helper); human confirmed the merge in chat knowing this. Regime dependence → phase-5 profiling question.
    Worktree: inversion 1061 passed / 4 xfailed. CI 3 legs green; glance auto-merge.
- witness: |
    MET on the data-dominated small rectangular case — ln det P vs slogdet 2.8e-14; SLQ within 0.5% at 10
    probes / 40 steps, deterministic for the fixed seed, 2-probe error larger; evidence with the dense ln det
    substituted equals fit_util.log_evidence_from exactly (0.0), total within SLQ tolerance (ln Z bias
    −0.11 to −0.16 nats on ln Z ≈ −1500). NOT met on the prior-dominated 40-visibility fixture (14–40%).
- heart-ack: "YELLOW acknowledged by human 2026-10-21 — manifest drift (1 mismatch); release validation stale: source moved since rehearsal (PyAutoArray)"
- phase-5 questions: SLQ error vs preconditioner quality on real data; FFT preconditioner from the gridded uv weight density (contributor's alternative for unweighted priors) as a fallback for prior-dominated regimes; seed/probe-count policy.

## Original prompt

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
