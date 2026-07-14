# interferometer/model_fit crashes: LinAlgError "Matrix is not positive definite" on release wheels

Type: bug
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Surfaced burning down the 2026-07-13 release-validation tail (PyAutoHeart#72). On the
release wheels under the release profile:

```
scripts/interferometer/model_fit.py ... FAIL (38.3s) numpy.linalg.LinAlgError: Matrix is not positive definite
```

A Cholesky factorization (`numpy.linalg.cholesky` / `scipy` `cho_factor`) hit a matrix that
isn't positive-definite — in an interferometer fit this is the inversion / regularization
linear-algebra path (curvature matrix `F`, or a regularization Cholesky). It fails fast
(38.3 s), so it is a hard numerical error, not a timeout. Runs in `autolens_workspace_test`
(`PYAUTO_TEST_MODE=0`).

**Leading hypothesis:** jax-0.10.2 numerical drift. Cluster A of this same tail showed the
pixelized-inversion log-likelihood drifts ~1e-3 between jax 0.9.2 and 0.10.2 (NNLS/linalg
reduction-order change); here the same class of drift may push a **marginally** positive-
definite interferometer matrix over the edge to indefinite, so a Cholesky that succeeded on
jax 0.9.2 now raises. Confirm by reproducing on jax 0.9.2 vs 0.10.2 (dev venv is now 0.10.2 —
[[reference_laptop_gpu_jax_setup]]). If it's a conditioning issue, the fix may be a jitter /
`cho_factor` fallback / regularization-floor in the inversion (PyAutoArray), NOT loosening a
test. If it reproduces on jax 0.9.2 too, it's a pre-existing interferometer conditioning bug.

Reproduce from the `autolens_workspace_test` checkout on current main:

```
cd autolens_workspace_test
PYAUTO_TEST_MODE=0 PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1 \
  python scripts/interferometer/model_fit.py
```

Get the full traceback (which matrix / which solve) and classify (jax-0.10.2 conditioning vs
real bug). Related: cluster A jax-drift fix (multi/rectangular goldens) and the NNLS-solver
history [[project_nnls_solver_ledger_closed.md]]. Release run: PyAutoHeart workspace-validation
`29279095224`, TestPyPI `2026.7.13.1.dev65601`. See [[project_release_2026_07_13_blocked_3bugs]]
and PyAutoHeart#72.
