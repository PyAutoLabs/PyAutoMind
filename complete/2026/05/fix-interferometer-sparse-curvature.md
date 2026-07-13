## fix-interferometer-sparse-curvature
- completed: 2026-05-16
- issue: https://github.com/Jammy2211/PyAutoArray/issues/314
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/316
- workspace-pr: https://github.com/Jammy2211/autolens_workspace_test/pull/98
- summary: |
    Replaced the NotImplementedError guard from PR #315 with a real math fix.
    InterferometerSparseOperator.curvature_matrix_via_sparse_operator_from →
    curvature_matrix_diag_from(rows, cols, vals, *, S), mirroring
    ImagingSparseOperator. New Mask2D.extent_index_for_masked_pixel property
    plumbed through so triplets land in the operator's extent-flat scatter
    buffer (the old code used native-flat fft_index_for_masked_pixel which
    silently fell out-of-bounds and was dropped by JAX for any mask with
    extent < native — both the Delaunay 34% Frobenius gap and the previously-
    documented Pmax=1 ~0.4% "numerical reformulation" gap were the same bug).
    Converted the raise-test to a sparse-vs-mapping parity assertion at
    rtol=1e-4. Updated the one Pmax=1 workspace call-site and the
    rectangular_sparse.py likelihood literal (-3152.03 → -3164.29 to match
    DFT-no-sparse and NUFFT-no-sparse to ~1e-13).
