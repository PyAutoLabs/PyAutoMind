# Extend the singular/non-PD inversion resample guard beyond interferometer model_fit

Type: bug
Target: autolens
Repos:
- PyAutoLens
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Follow-up to the release-validation tail (PyAutoHeart#72) and the G fix
(PyAutoLens#607, "resample non-PD inversion instead of crashing the search"). #607
mirrored the imaging analysis's try/except→FitException guard into the
**interferometer** `log_likelihood_function`, which fixed `interferometer/model_fit.py`.
But the corrective re-validation (run **29341418859**, wheels `2026.7.14.1.dev65901`)
surfaced the **same singular/non-PD inversion crash in other paths that #607 did not
cover**:

```
interferometer/features/multi_gaussian_expansion/slam.py ... FAIL (59.2s) numpy.linalg.LinAlgError: Singular matrix
imaging/features/pixelization/cpu_fast_modeling.py         ... FAIL (122.3s) autoarray.exc.InversionException
```

So the guard is incomplete:
- **SLaM / multi-search pipelines** (`interferometer/.../mge/slam`) hit the singular
  matrix outside the single guarded `log_likelihood_function` (e.g. during a chained
  search's result/preload step, or a search phase that calls the inversion directly).
- **`cpu_fast_modeling`** raises `autoarray.exc.InversionException` on an *imaging*
  pixelization even though imaging's analysis already has the guard — so this path
  reaches the inversion outside the guarded likelihood too.

Why now: jax-0.10.2 numerical drift (the same drift class as cluster A of #72) lands
more samples in singular/non-PD territory, so inversions that used to just-barely
factorize now raise. This is a **conditioning robustness** issue, not a per-script
bug.

Two complementary fixes to weigh:
1. **PyAutoLens** — audit every inversion entry point in the interferometer (and
   pixelization) analysis/result/preload paths and ensure the FitException resample
   guard (`imaging/model/analysis.py:132-144` pattern) wraps all of them, not just the
   top-level `log_likelihood_function` — so a non-PD/singular inversion resamples
   instead of crashing the search.
2. **PyAutoArray** — add a conditioning floor / jitter (or a `cho_factor` fallback)
   in the inversion linear-algebra (`autoarray/.../inversion/.../abstract.py`
   Cholesky at ~line 743) so a marginally-singular curvature/regularization matrix is
   nudged PD before factorization. Validate via the JAX parity scripts in
   `*_workspace_test`, never the library unit tests.

Reproduce on jax 0.10.2 (dev venv matches the release stack): run the two scripts
above under the release profile. Cross-ref [[project_release_2026_07_13_blocked_3bugs]],
PyAutoHeart#72, and the G fix PyAutoLens#607.
