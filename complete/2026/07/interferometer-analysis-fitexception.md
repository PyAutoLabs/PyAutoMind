## interferometer-analysis-fitexception
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/606 (closed)
- completed: 2026-07-14
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/607 (merged 5250d80a5, squash)
- repos: PyAutoLens
- summary: interferometer (+point_source) log_likelihood_function lacked imaging's NumPy-path try/except→FitException guard → non-PD np.linalg.cholesky crashed the search instead of resampling (JAX path masks via NaN). Mirror imaging/model/analysis.py guard. Release-tail item G. Corrective validation GREEN on mode=release v2026.7.14.1.dev66001 (integrate:pass 542p/0f/0t); Heart YELLOW. See project_interferometer_nonpd_numpy_path_fitexception.

## Original prompt

# interferometer/model_fit crashes: LinAlgError "Matrix is not positive definite" on release wheels

Type: bug
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_workspace_test
Difficulty: easy
Autonomy: supervised
Priority: normal
Status: diagnosed

Surfaced burning down the 2026-07-13 release-validation tail (PyAutoHeart#72). On the
release wheels under the release profile:

```
scripts/interferometer/model_fit.py ... FAIL (38.3s) numpy.linalg.LinAlgError: Matrix is not positive definite
```

## Confirmed diagnosis (2026-07-14) — the jax-0.10.2-drift hypothesis is FALSIFIED

Reproduced locally on jax **0.10.2**. The cause is not jax numerical drift; it is a
**NumPy/JAX backend divergence** in the interferometer analysis, selected by
`PYAUTO_DISABLE_JAX`:

| Run | Backend | Result |
|-----|---------|--------|
| no env (jax path, `use_jax=True`) | `jnp.linalg.cholesky` | completes clean, full prior exploration, exit 0 |
| `PYAUTO_DISABLE_JAX=1` (release profile, `use_jax=False`) | `np.linalg.cholesky` | crashes on the FIRST sampled point |

The release workspace-validation profile
(`autolens_workspace_test/config/build/env_vars_release.yaml`) sets
`PYAUTO_DISABLE_JAX: "1"` as the default, and `interferometer/model_fit.py` matches
none of the JAX re-enable patterns → it runs the pure **NumPy** path. (The smoke
profile is green because it runs `PYAUTO_TEST_MODE=2` — no sampler, no search, so the
pathological point is never sampled.)

**Mechanism.** A Nautilus-sampled model yields a non-positive-definite regularization
matrix. At `PyAutoArray/autoarray/inversion/inversion/abstract.py:743`
(`log_det_regularization_matrix_term`, reached via `FitInterferometer.log_evidence` →
`figure_of_merit` → `log_likelihood_function`):
- **NumPy** `np.linalg.cholesky` **raises** `LinAlgError` → propagates uncaught through
  Nautilus's multiprocessing pool → kills the whole search (~38 s).
- **JAX** `jnp.linalg.cholesky` **returns NaN** → `figure_of_merit` = NaN →
  `autofit/non_linear/fitness.py:239` maps NaN → `resample_figure_of_merit` → the
  sample is silently rejected and the search continues.

So a pathological model that JAX rejects gracefully, NumPy crashes on.

## Fix (locus: PyAutoLens, not PyAutoArray)

The imaging analysis already handles exactly this — `autolens/imaging/model/analysis.py:132-144`
splits on `self._use_jax`: the jax path returns unwrapped (must stay exception-free for
tracing), the numpy path wraps the fit in `try/except Exception → raise af.exc.FitException`,
which `fitness.py:235` catches and resamples.

The interferometer analysis `log_likelihood_function`
(`autolens/interferometer/model/analysis.py:170-173`) is **missing this wrapper entirely** —
no `_use_jax` split, no try/except. Mirror the imaging analysis exactly so the numpy
backend rejects (resamples) a bad point instead of crashing. This is backend path-parity,
not a symptom mask — a pathological sampled model is meant to be rejected, and the jax path
already rejects it.

Follow-ups to check during the fix:
- **point_source analysis** — verify whether `autolens/point/model/analysis.py`
  (and any other dataset analysis) has the same missing wrapper, and align it.
- **Root question (non-blocking):** why is the `ConstantSplit` `regularization_matrix_reduced`
  non-PD on the first sampled point (Delaunay mesh degeneracy vs. a genuine ConstantSplit
  conditioning issue)? Both the imaging-mirror fix and a PyAutoArray jitter make it a rejected
  sample either way; log if it looks systematic rather than a rare extreme.

## Reproduce

```
cd autolens_workspace_test
# crashes (numpy path, release profile):
PYAUTO_TEST_MODE=0 PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1 PYAUTO_DISABLE_JAX=1 JAX_ENABLE_X64=True \
  python scripts/interferometer/model_fit.py
# completes clean (jax path, no env):
PYAUTO_TEST_MODE=0 PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1 \
  python scripts/interferometer/model_fit.py
```
(Wipe `output/build/model_fit/interferometer` first so Nautilus explores from scratch
rather than resuming cached samples.)

Related: cluster A jax-drift fix (multi/rectangular goldens) and the NNLS-solver history
[[project_nnls_solver_ledger_closed.md]] — those ARE jax-drift; this one is not. Release run:
PyAutoHeart workspace-validation `29279095224`, TestPyPI `2026.7.13.1.dev65601`. See
[[project_release_2026_07_13_blocked_3bugs]] and PyAutoHeart#72.
