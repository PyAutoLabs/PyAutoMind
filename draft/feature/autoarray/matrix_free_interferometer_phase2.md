# Matrix-free interferometer inversion, phase 2: sparse Matérn (SPDE) precision regularization + Powell preconditioner on it

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
Witness: tests asserting (i) the new regularization's dense matrix equals coefficient × (W⁻¹ c L² W⁻¹) built by hand on a small rectangular mesh, is symmetric positive definite, and its exact sparse log-det matches numpy slogdet to 1e-10; (ii) an InversionInterferometerSparse with the new regularization (dense path) and the phase-1 matrix-free PCG with its sparse matrix agree on the unconstrained reconstruction to 1e-8 for two coefficients; (iii) a Delaunay mesh raises a clear error
Review-minutes: 6
Unattended: ready
Filed: 2026-10-21

## Why

Phase 2 of PyAutoArray#638 (hub #39, @HRSAstro; reference section 3 `spde_matern_precision` of the attached upstream_snippets.py). The dense `MaternKernel` regularization builds and inverts an n×n covariance; the matrix-free path needs a sparse precision. For integer α = ν + 1 the Matérn precision is sparse (Lindgren, Rue & Lindström 2011): for α = 2 (ν = 1), C⁻¹ = c L², L = κ² − ∇² (5-point Laplacian, reflecting edges), κ = √(2ν)/ℓ, c chosen so the variance at the mesh centre is 1 (K(0) = 1 as for the dense kernel). Per-pixel weights enter as W⁻¹ c L² W⁻¹. Phase 1 (#645) already accepts any sparse H in `powell_preconditioner_from` / `reconstruction_via_pcg_from`.

## What to build

1. New regularization `autoarray/inversion/regularization/matern_sparse.py`, class `MaternSparse(AbstractRegularization)` with `coefficient`, `scale`, `nu=1.0` (assert integer α; only ν = 1 implemented, higher integer ν documented as c Lᵅ follow-up), optional `weights` hook mirroring the adaptive kernels' `regularization_weights_from` (phase 2 ships unweighted + a weights argument path; adaptive-brightness coupling is a follow-up). Rectangular meshes only: read the mesh shape from the mapper's rectangular mesh (`RectangularRTUAdaptDensity.shape` / `shape_native`) and its pixel scale; raise `NotImplementedError` for non-rectangular meshes. Establish and document the mesh pixel ordering (row-major from `grid_2d_slim_via_shape_native_not_mask_from`) so the 5-point adjacency indexes mesh pixels correctly.
   - `regularization_matrix_sparse_from(linear_obj) -> scipy.sparse.csr_matrix` = coefficient × RᵀR with R = √c L diag(1/w).
   - `regularization_matrix_from(linear_obj, xp)` returns the dense array of that (xp.asarray) so the class is a drop-in on today's dense path.
   - `log_det_regularization_matrix_term_from` exact: n log(coefficient) + n log c + 2 Σ log|U_ii| (sparse LU of L) − 2 Σ log w.
   - `regularization_term_from` = sᵀ H s.
   - Export via `aa.reg.MaternSparse`; numpy/scipy only in the module (xp only for the dense return).
2. Phase-1 integration: `test_matrix_free_util.py` gains a case using `MaternSparse.regularization_matrix_sparse_from` as H in `powell_preconditioner_from` / `reconstruction_via_pcg_from`, asserting parity with the dense-path `InversionInterferometerSparse` using the same `MaternSparse` instance.
3. Tests `test_autoarray/inversion/regularization/test_matern_sparse.py`: hand-built 4×3 mesh L and c; SPD; log-det vs slogdet; coefficient scaling; weights path (W⁻¹ c L² W⁻¹); non-rectangular raises; a loose documented check that C = (c L²)⁻¹ has unit variance at the centre and decays monotonically with distance.

## Acceptance

Witness passes on numpy and the nojax leg; the dense `MaternKernel` is untouched. Update #638 and the hub thread at PR-open.
