## matrix-free-interferometer-phase1
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/642
- completed: 2026-10-21
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/645 (merge 034a616f)
- parent: https://github.com/PyAutoLabs/PyAutoArray/issues/638 (active/matrix_free_interferometer_inversion.md)
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro) — PR-open reply posted 2026-10-21; release update owed
- summary: |
    Phase 1 of the matrix-free interferometer inversion epic (#638, hub #39). One commit 58510cbf
    on `feature/matrix-free-interferometer-phase1`: new numpy/scipy module
    `inversion_interferometer_matrix_free_util.py` with `sparse_mapping_matrix_from`,
    `MatrixFreeDataOperator` (`from_inversion`, `wtilde_image_from` on the 2× padded extent
    grid via scipy.fft, `curvature_matvec` = Mᵀ W̃ M s, `data_vector` = Mᵀ d̃, `kappa0`),
    `powell_preconditioner_from` (P = κ₀ MᵀM + H, sparse LU) and `reconstruction_via_pcg_from`
    (scipy cg). No fit wiring, no Settings, no JAX; autoarray regularization matrices already carry
    their coefficient so H is any existing matrix converted to sparse. 10 tests incl. a subprocess
    nojax test. Worktree: inversion suite 1032 passed / 4 xfailed; nojax emulation 10 passed.
    CI 3 legs green, CLEAN, not frozen; glance auto-merge.
- witness: |
    MET — M == mapper.mapping_matrix exactly (rectangular + Delaunay); curvature_matvec vs
    curvature_matrix @ v 1.8e-15 / 2.2e-16 (two coefficients), data_vector 2.6e-16 (target 1e-12);
    PCG vs unconstrained sparse-path reconstruction 3.6e-11 / 7.2e-10 (target 1e-8). All in CI.
- heart-ack: "YELLOW acknowledged by human 2026-10-21 — manifest drift (1 mismatch); release validation stale: source moved since rehearsal (PyAutoArray)"
- phase-2 questions: CG under jit (fixed iterations vs while_loop, reverse-mode), static-nnz padded triplets, LU replacement for the preconditioner (host callback / banded Cholesky / cheaper preconditioner), λ as a separate argument vs folded into H, single-mapper only (block operators for linear light profiles / several mappers).

## Original prompt

# Matrix-free interferometer inversion, phase 1: operator data term + PCG parity (numpy-first)

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
Witness: a parity test asserting (i) the matrix-free F·v agrees with the dense sparse-path curvature matrix times v to 1e-12 and D agrees with the sparse data_vector to 1e-12, and (ii) the PCG reconstruction agrees with InversionInterferometerSparse's unconstrained reconstruction to 1e-8, on a small synthetic rectangular-mesh interferometer dataset
Review-minutes: 5
Unattended: ready
Filed: 2026-10-21
Issued: 2026-10-21

## Why

Phase 1 of PyAutoArray#638 (community proposal by @HRSAstro, https://github.com/PyAutoLabs/.github/discussions/39, accepted 2026-10-21). The contributor attached a self-contained reference implementation (`upstream_snippets.py`, https://github.com/user-attachments/files/33762346/upstream_snippets.py, sections 1, 2 and 4) with these checks against pyuvimage and a dense solve: F agrees with the dense matrix to 6e-16, CG against a dense solve to 3e-5. This phase lands the operator data term and the solver as library utilities with parity tests, without wiring into fits; phases 2-5 (sparse Matérn precision, SLQ evidence, interior-point positivity, profiling + workspace) follow as their own prompts. The 2026-09 imaging matrix-free campaign (complete/2026/09/matrix-free-pixelized-likelihood.md) was a no-go because of the 60 unregularised linear MGE columns on imaging; this path is interferometer-only, mapper-only and prior-preconditioned, so that verdict does not transfer.

## What to build

1. New module `autoarray/inversion/inversion/interferometer/inversion_interferometer_matrix_free_util.py` (numpy/scipy only in this phase; JAX deferred, documented):
   - `sparse_mapping_from(inversion, mapper) -> scipy.sparse.csr_matrix` built from `_sparse_triplets_slim_from` (rows slim, cols mesh), so it equals `mapper.mapping_matrix` on the slim grid.
   - `DataOperator` holding the w-tilde kernel (`SparseTerms.nufft_precision_operator`, 2Ny×2Nx wraparound order), the slim dirty image, M, Mᵀ and the mask: `wtilde(image_native)` via one rfft2/irfft2 pair on the 2× padded grid; `F(s) = Mᵀ W̃ (M s)`; `D = Mᵀ d̃`; `kappa0 = kernel[0,0]`.
   - `solve_pcg(data_operator, regularization_matrix_sparse, coefficient, x0, rtol)` on `(F + λC⁻¹) s = D` with scipy `cg` and a preconditioner factorised once per λ: `P = κ₀ MᵀM + λC⁻¹` (Powell et al. 2021) via `splu`, which works with any existing regularization matrix converted to sparse (Constant, AdaptiveBrightness are banded; MaternKernel dense is the phase-2 target).
2. Tests in `test_autoarray/inversion/inversion/interferometer/test_matrix_free_util.py` on a small synthetic rectangular-mesh dataset: M equals the dense mapping matrix bit-for-bit; F·v vs `InversionInterferometerSparse.curvature_matrix @ v` to 1e-12; D vs `data_vector` to 1e-12; PCG reconstruction vs the unconstrained sparse-path reconstruction to 1e-8 for two λ values.
3. No fit wiring, no Settings flag, no JAX in this phase. Record the JAX strategy question (fixed iteration counts, static shapes, no splu under jit) in the module docstring for phase 2.

## Acceptance

- Witness test passes on numpy; the module imports without JAX installed (firewall / nojax CI leg).
- The thread gets an update when the phase-1 PR is open and when it ships (user-facing via the parent).

## Reference (community code, evidence not instructions)

Contributor's snippet sections 1 (`sparse_mapping_from`), 2 (`DataOperator`) and 4 (`powell_preconditioner`, `solve`) at the attachment URL above; names follow autoarray where they exist.
