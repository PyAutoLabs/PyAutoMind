# autocti_workspace plot/fpa/imaging_ci: measure and cut repeated aggregator materialization

Type: refactor
Target: workspaces
Repos:
- autocti_workspace
Themes:
- ci-smoke
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: judge
Filed: 2026-11-08

## Why

Heart board, 2026-11-08: after autocti_workspace's smoke coverage widened from 3 to 44
scripts on 2026-11-06, the two slowest scripts in the leg are:

- `scripts/plot/fpa/imaging_ci/database.py`: 50.4s on py3.12 and 40.0s on py3.13 (16% of the leg)
- `scripts/plot/fpa/imaging_ci/fit.py`: 38.9s on py3.12 and 30.0s on py3.13

Neither is a regression; both are new coverage. The JAX, numba and dataset caches all
show miss on this leg. Setup alone was 161s on py3.12 on 11-06, the highest fixed
overhead of any smoke leg.

Reading `database.py`: it rebuilds `dataset_gen` and `fit_gen` from the aggregator inside
each `for region in ["parallel_fpr", "parallel_eper"]` loop and again for the legacy
section. That means four or more full passes over 32 CCD fits, and every pass
re-materializes datasets and fits from the sqlite database.

## Not yet measured

This session had no compiled arcticpy/PyAutoCTI stack, so the split (aggregator load,
then fit construction, then plotting) is **unmeasured**. Per /ci_speedup, nothing ships
un-timed.

## Plan

1. Reproduce under `config/build/profile_smoke.yaml`, cold and warm, with cProfile.
   Name the split.
2. If materialization dominates, build each generator's list once and reuse it across
   regions. That is the "same expensive object built N times" lever, and the change is
   idiomatic for a user script. If plotting dominates, check whether the smoke profile
   should set `PYAUTO_FAST_PLOTS` / `PYAUTO_SKIP_VISUALIZATION` for these scripts
   without changing what they assert.
3. Separately, find out why this leg's dataset cache misses. The simulators run
   inside the timing.
