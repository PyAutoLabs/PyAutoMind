# interferometer-sparse-func-list

User-filed (PyAutoArray#499, @HRSAstro): `InversionInterferometerSparse` could not fit an
`AbstractLinearObjFuncList` alongside a `Mapper`; worse, the factory routed mixed lists to the
sparse class and the func-list / cross-mapper blocks were silently dropped from F.

## Shipped
- PyAutoArray#500 — `InterferometerSparseOperator.{curvature_matrix_off_diag_from,
  curvature_matrix_off_diag_func_list_from, curvature_matrix_func_list_from, operated_matrix_slim_from}`;
  `InversionInterferometerSparse.curvature_matrix` dispatch (x1 mapper bit-identical / multi-mapper /
  func-list+mapper), mirror + no-regularization diag add; `__init__` no longer overwrites `settings`
  with None. Parity vs `InversionInterferometerMapping` ~6e-16. nojax leg: `pytest.importorskip("jax")`.
- autolens_workspace_test#283 — `misc/jax_assertions/fit_interferometer_sparse_operator.py` (+ registered
  the pre-existing imaging script in smoke_tests.txt).
- autogalaxy_workspace_test#115 — `misc/jax_assertions/fit_{imaging,interferometer}_sparse_operator.py`.

## Decisions
- Func–func block via W~ (not the dense NUFFT matrix): W~ = Re(FᴴWF) is exact on the extent grid; one operator for every block.
- Func-list columns passed UN-weighted to the interferometer operator (W~ already contains N⁻¹), unlike imaging (Hᵀ N⁻¹ H split).
- Parallel worktree on PyAutoArray alongside numba-cpu-nnls-iteration-reduction (disjoint files). Heart RED acked (unrelated integrate failure).

## Follow-ups (filed via intake at close-out)
- Unequal real/imag sigma degrades the W~ sparse path (pre-existing; 5e-16 → 5e-10..3e-2).
- `delaunay_nn.py` / `delaunay_nn_caps.py` `ENV:` lines lack the `__Env__` header → declaration dead.
