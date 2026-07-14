## inversion-testmode-singular-guard
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/388 (closed)
- completed: 2026-07-14
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/389 (merged 1ff90287, squash)
- repos: PyAutoArray
- summary: release-tail singular/non-PD inversion FAILs (slam/cpu_fast_modeling) were a flaky TEST_MODE artifact, not a conditioning bug — test-mode-gated dummy at inversion raise-sites (is_test_mode()), no conditioning floor. Corrective validation GREEN on v2026.7.14.1.dev66001 (integrate:pass 542p/0f/0t); Heart YELLOW. See project_inversion_testmode_singular_guard.

## Original prompt

# Test-mode-gate the singular/non-PD inversion crash in PyAutoArray

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Follow-up to the release-validation tail (PyAutoHeart#72) and the G fix
(PyAutoLens#607). Re-validation (run 29341418859, wheels `2026.7.14.1.dev65901`)
reported two release FAILs:

```
interferometer/features/multi_gaussian_expansion/slam.py ... FAIL (59.2s) numpy.linalg.LinAlgError: Singular matrix
imaging/features/pixelization/cpu_fast_modeling.py         ... FAIL (122.3s) autoarray.exc.InversionException
```

## Diagnosis (revised after reproduction, 2026-07-14)

The original prompt hypothesised a general conditioning bug and proposed a
PyAutoArray conditioning floor **plus** PyAutoLens result/preload guards. That
scope is wrong. Investigation + reproduction on the dev venv (jax 0.10.2,
matches release) established:

- Both `log_likelihood_function`s are **already guarded** (imaging
  `analysis.py:144`, interferometer `analysis.py:182`) — a singular inversion
  during sampling raises `FitException` and resamples. The reported errors are
  `LinAlgError` / `InversionException`, i.e. they fire **outside** the guarded
  likelihood.
- Both failing scripts are **chained pipelines** run by the release harness
  under `PYAUTO_TEST_MODE=1` (release.yml) — reduced *real* searches whose
  under-converged max-likelihood sample is fed into **unguarded** downstream
  inversions (`Result.max_log_likelihood_fit → analysis.fit_from`, preload
  construction, next-search chaining).
- The crash **does not reproduce deterministically on clean `main`**: TEST_MODE=2
  passes; TEST_MODE=1 clean passes (full chain); TEST_MODE=1 on stale output
  gives a *different* error (resume/cache contamination). The passing runs emit
  `mapper_util.py:84 divide-by-zero` / `invalid value in power` — the inversion
  produces degenerate near-singular values on some samples, which only *raises*
  under specific numeric conditions (wheel build, run ordering, jax build). This
  is a **flaky test-mode tail, not a deterministic library bug**. Real science
  is unaffected (converged models are well-conditioned; excursions resample).

Because real inference is already protected by the resample guard, and because
in test mode the fit is fabricated/meaningless anyway (cf. `skip_latents`), the
correct fix is **test-mode-gated** and lives entirely in PyAutoArray. It must
**not** perturb real-mode numerics (no conditioning floor) — that would violate
`feedback_no_silent_guards` and shift every real evidence/reconstruction.

## Plan (PyAutoArray only, test-mode-gated)

In normal mode behaviour is byte-for-byte unchanged (still raises → still
resamples in the guarded likelihood). Only when `is_test_mode()` (from
`autoconf`) do the inversion sites return a benign dummy instead of raising, so
the flaky test-mode crashes disappear wherever the inversion is invoked:

1. `inversion_util.reconstruction_positive_negative_from` (~:224) — wrap
   `xp.linalg.solve` in `try/except np.linalg.LinAlgError`; in test mode return
   `xp.ones_like(data_vector)`, else raise `exc.InversionException`.
2. `inversion_util.reconstruction_positive_only_from` (~:352-353) — the `except`
   already raises `InversionException`; in test mode return `xp.ones_like(...)`.
3. `inversion/inversion/abstract.py` `log_det_curvature_reg_matrix_term`
   (~:715-721) — wrap the Cholesky; in test mode return `0.0` on `LinAlgError`
   (else the crash just moves here once the reconstruction stops raising).
4. `abstract.py` `log_det_regularization_matrix_term` (~:740-746) — same.

Small shared helper (e.g. `_test_mode_dummy_or_raise`) to keep it DRY.

**Validation:** numpy-only unit test in `test_autoarray/` — a deliberately
singular `curvature_reg_matrix` (a) raises normally, (b) under a monkeypatched
`PYAUTO_TEST_MODE` returns finite dummies. No JAX in unit tests
(`feedback_no_jax_in_unit_tests`); the JAX path is covered by the existing
`*_workspace_test` parity scripts. The flaky end-to-end scripts are **not** used
as a gate.

Cross-ref [[project_release_2026_07_13_blocked_3bugs]], PyAutoHeart#72, the G fix
PyAutoLens#607, and the parked "mode=release advisory-tiering" follow-up.
