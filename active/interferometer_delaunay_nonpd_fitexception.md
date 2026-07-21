# interferometer Delaunay pixelization — stale NEEDS_FIX marker (already fixed on main)

Type: bug
Target: autolens
Repos:
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Split out from `slam-adapt-inversion-cascade` (autolens_workspace#300). On 2026-07-21 the script raised
`autofit.exc.FitException` at `interferometer/model/analysis.py:182` (the numpy path's bare
`except Exception: raise FitException` masking a non-PD inversion). **Re-diagnosis a few hours later, on
freshly-synced `main`, found it deterministically GREEN** (3 clean runs, fresh dataset, CI smoke env) —
recent concurrent work fixed it, so this collapses to a stale-marker cleanup, not a code fix.

## Verification (clean main, real CI smoke env)

```
cd autolens_workspace
NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib \
PYAUTO_DISABLE_JAX=1 PYAUTO_TEST_MODE=2 PYAUTO_SMALL_DATASETS=1 PYAUTO_SKIP_FIT_OUTPUT=1 \
PYAUTO_SKIP_VISUALIZATION=1 PYAUTO_SKIP_CHECKS=1 PYAUTO_FAST_PLOTS=1 \
python scripts/interferometer/features/pixelization/delaunay.py     # EXIT 0
```

## What fixed it (not this task)

Not the `f1817af0` GaussianKernel PD-guard — this script uses `ConstantSplit`/`AdaptSplit` regularization
(correct for a Delaunay mesh), not GaussianKernel. The prime suspect is
`PyAutoArray#396` (`SMALL_DATASETS` fast-mode cap 15×15 → 16×16, even): the original failure was
grid-size-sensitive (the odd 15×15 cap produced the degenerate non-PD inversion the numpy path raised on).
The pix-not-PD cluster work (autogalaxy_workspace#140) and gradient-safe-logdet (`PyAutoArray#392`) also
landed in the same window.

## Task (marker-only)

- autolens_workspace `config/build/no_run.yaml` — remove the
  `interferometer/features/pixelization/delaunay` NEEDS_FIX entry (verified green).

## Noted latent issue (NOT in scope — separate if pursued)

`AnalysisInterferometer.log_likelihood_function` (numpy path, `analysis.py:175-182`) wraps **any**
underlying error in a bare `except Exception: raise af.exc.FitException`, which masked the real error and
made this hard to diagnose. Correct for real fitting (resample), but it hides genuine bugs. A targeted
improvement (narrow the except, or log the original) could be filed separately.
