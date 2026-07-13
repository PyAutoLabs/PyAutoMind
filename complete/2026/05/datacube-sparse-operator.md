## datacube-sparse-operator
- completed: 2026-05-15
- status: partially-shipped (guard only, math fix deferred)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/315
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/314
- follow-up: PyAutoPrompt/planned.md ##fix-interferometer-sparse-operator-irregular-meshes
- summary: |
    Attempted to wire `dataset.apply_sparse_operator(use_jax=True)` into the
    just-shipped hannah profilers; the path explodes at Cholesky with
    "Matrix is not positive definite". Diagnosed: the interferometer
    sparse-operator curvature math
    (`InterferometerSparseOperator.curvature_matrix_via_sparse_operator_from`)
    is wrong by ~34% Frobenius on Delaunay (Pmax=3 barycentric weights) — only
    validated against Rectangular Pmax=1. Independent of zeroed_pixels,
    independent of use_jax. CPU and JAX paths match each other to 5.5e-14,
    both wrong vs the mapping path.

    Shipped: PR #315 added a defensive NotImplementedError guard at
    `InversionInterferometerSparse.curvature_matrix_diag` for Delaunay-mesh
    mappers, with a regression test. Future users get a clear early failure
    pointing at issue #314 instead of confusing downstream LinAlgError.

    Deferred (to planned.md): the actual math rewrite of the interferometer
    sparse-operator curvature path to handle Pmax > 1 correctly, plus audit
    of the existing ~0.4 % rectangular_sparse discrepancy that may share the
    same root cause. Filed for an inversion-math maintainer to pick up.

    Workspace impact: none. The previously-shipped Delaunay profilers
    (datacube-hannah-preset) stay on plain DFT path and continue to work.
