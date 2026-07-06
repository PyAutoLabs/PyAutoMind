# Fix release JAX runtime compatibility and likelihood parity

## Context

Six JAX likelihood scripts failed with the rehearsed release stack. CI included
TensorFlow Probability using removed JAX internals and NumPy/JAX likelihood mismatches.
All six passed locally with current `main` and JAX 0.9.2, so verify whether upstream
library changes already fixed them or whether environment/order sensitivity remains.

Owners: @PyAutoArray, @PyAutoFit, @PyAutoGalaxy, @PyAutoLens,
@autogalaxy_workspace_test, and @autolens_workspace_test.

## Scripts

- `autogalaxy_workspace_test/scripts/jax_likelihood_functions/imaging/delaunay_mge.py`
- `autogalaxy_workspace_test/scripts/jax_likelihood_functions/interferometer/delaunay_mge.py`
- `autogalaxy_workspace_test/scripts/jax_likelihood_functions/multi/delaunay_mge.py`
- `autolens_workspace_test/scripts/jax_likelihood_functions/interferometer/delaunay_mge.py`
- `autolens_workspace_test/scripts/jax_likelihood_functions/multi/rectangular.py`
- `autolens_workspace_test/scripts/jax_likelihood_functions/multi/rectangular_mge.py`

## Required work

1. Reproduce in a clean source environment using the release dependency constraints and
   record exact JAX, jaxlib, TFP, NumPy, nufftax, and pynufft versions.
2. Confirm whether current `main` fixes every CI traceback without cached compiled state.
3. If TFP remains incompatible, fix or replace the owning library path rather than
   disabling JAX in JAX-specific scripts.
4. Investigate parity differences from data/model construction through inversion and
   regularization; do not merely loosen tolerances without a numerical error budget.
5. Add library regression tests and rerun all six scripts in both fresh processes and
   their normal directory sequence.
