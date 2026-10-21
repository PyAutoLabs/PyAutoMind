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
