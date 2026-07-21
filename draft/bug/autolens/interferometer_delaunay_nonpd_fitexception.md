# interferometer Delaunay pixelization — non-PD FitException in test-mode bypass

Type: bug
Target: autolens
Repos:
- PyAutoLens
- PyAutoArray
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Split out from `slam-adapt-inversion-cascade` (#300, autolens_workspace) during the 2026-07-21 folded-in
Delaunay verification. The imaging Delaunay/SLaM/double-ring cluster was fixed there; this interferometer
Delaunay case is a distinct, still-open failure and keeps its NEEDS_FIX marker.

## Reproduction (clean main, real CI smoke env)

```
cd autolens_workspace
NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib \
PYAUTO_DISABLE_JAX=1 PYAUTO_TEST_MODE=2 PYAUTO_SMALL_DATASETS=1 PYAUTO_SKIP_FIT_OUTPUT=1 \
PYAUTO_SKIP_VISUALIZATION=1 PYAUTO_SKIP_CHECKS=1 PYAUTO_FAST_PLOTS=1 \
python scripts/interferometer/features/pixelization/delaunay.py
```

Fails with `autofit.exc.FitException` raised at `PyAutoLens/autolens/interferometer/model/analysis.py:182`.

(Note: the old `(2,2) vs (1032,1032)` broadcast reported in the 2026-04 marker is **gone** — this is now a
different, deeper failure. Under the JAX path — `PYAUTO_DISABLE_JAX` unset — it instead dies earlier in the
JAX Delaunay `pure_callback` with `scipy qhull: Points cannot contain NaN`.)

## Mechanism

`AnalysisInterferometer.log_likelihood_function` (numpy path, `analysis.py:175-182`) wraps
`fit_from(...).figure_of_merit` in a bare `try/except Exception` and re-raises **any** underlying error as
`af.exc.FitException`. In real fitting this is correct (FitException → the sampler resamples), but in
`PYAUTO_TEST_MODE=2` bypass a single likelihood evaluation propagates the FitException as a hard script
failure. The masked underlying error is an interferometer Delaunay inversion producing a non-positive-definite
(or otherwise failing) matrix — the numpy cholesky path raises where the JAX path NaN-resamples (same lineage
as the imaging pix-NaN work: PyAutoLens#607, PyAutoArray#391/#392 opt-in `slogdet`).

## First step

Set `JAX_TRACEBACK_FILTERING=off` and/or temporarily surface the wrapped exception (comment out the re-raise)
to capture the true underlying error and confirm it is the non-PD cholesky raise. Then decide the fix tier:
- opt-in `log_det_method="slogdet"` / non-PD handling for the interferometer inversion path (mirror the imaging
  pix-NaN fix, default unchanged), and/or
- a test-mode-bypass tolerance so a single-eval non-PD instance doesn't hard-fail the smoke run.

Do NOT silently swallow the FitException — fix the producer or make bypass mode tolerate a resample-signal.

Affected (remove NEEDS_FIX once green): autolens_workspace `interferometer/features/pixelization/delaunay`.
Cross-ref: active task pix-inversion-not-positive-definite (autogalaxy_workspace#140), pix-gradient-slogdet
revalidation (#112), PyAutoLens#607.
