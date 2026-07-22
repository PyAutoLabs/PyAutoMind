# point.py JAX-vmap parity assert is non-deterministic under the smoke env

Type: bug
Target: autolens
Repos:
- autolens_workspace_test
- PyAutoLens
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

`autolens_workspace_test/scripts/jax_likelihood_functions/point_source/point.py` fails its
JAX-vs-numpy parity assert under the smoke env, and **fails differently between runs**:

```
AssertionError: point: JAX vmap likelihood mismatch
  run A (parallel batch):  ACTUAL [-1.e+99]     DESIRED -83.380498
  run B/C/D (serial):      ACTUAL [16.131221]   DESIRED -83.380498
```

`-1e+99` is the failed-fit sentinel; `16.131221` is a finite but wrong value. Same script,
same env, same commit — so the assert is not measuring what it intends to.

Observed while smoke-gating PyAutoArray#398 (convolver-gaussian-small-datasets-cap, merged
2026-07-22). **Confirmed unrelated to that change**: A/B'd by checking out the pre-fix
`autoarray/operators/convolver.py` and re-running — identical failure and identical value.
The script also contains no `Convolver` / `from_gaussian` / PSF usage at all, so a
convolution change cannot reach it. It is one of the ~10 already-failing workspace scripts
Heart reported on 2026-07-20, i.e. it pre-dates that work.

Lead worth checking first: `PointSolver` has its own `PYAUTO_SMALL_DATASETS` short-circuit
at `PyAutoLens/autolens/point/solver/point_solver.py:111` that skips the triangle-tiling
solve entirely under the smoke flag. If the parity assert runs against that short-circuited
solve, the comparison may be structurally meaningless in smoke mode — in which case the fix
is either to unset the flag for this script (`config/build/env_vars.yaml` override) or to
skip the assert when the short-circuit is active, rather than to chase a numerical bug.

Second possibility to rule out: genuine non-determinism in the triangle solve (ordering /
tie-breaking) that the parity tolerance `rtol=1e-4` cannot absorb.

Repro (from `autolens_workspace_test/`):

```
PYAUTO_TEST_MODE=2 PYAUTO_SMALL_DATASETS=1 PYAUTO_SKIP_FIT_OUTPUT=1 \
PYAUTO_SKIP_VISUALIZATION=1 PYAUTO_SKIP_CHECKS=1 PYAUTO_FAST_PLOTS=1 JAX_ENABLE_X64=True \
NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib \
python scripts/jax_likelihood_functions/point_source/point.py
```

Run it several times, and once inside a parallel batch — the failure value changes. Per
`feedback_flaky_test_sample_size`, a few passing runs will not settle this; decide on the
mechanism, not on a run tally.
