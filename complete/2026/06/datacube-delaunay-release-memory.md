## datacube-delaunay-release-memory
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/142
- completed: 2026-06-09
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/143 (merged f028dd1)
- repos: autolens_workspace_test
- notes: Fixed the heavy datacube Delaunay release failure by preserving 4-channel DFT cube vmap/JIT coverage while reducing only the high-memory TransformerNUFFT Delaunay cross-check to one identical channel. Verified the target script locally and PR CI on Python 3.12/3.13 before merge.

## Original prompt

# Datacube Delaunay release memory failure

## Original Request

ok merge and on to the next fix

## Context

After merging the Autolens JAX simulator release fixes, continue the release
failure list with the heavy datacube JAX Delaunay failure.

## Current Failure

Primary repo: @autolens_workspace_test

- `@autolens_workspace_test/scripts/jax_likelihood_functions/datacube/delaunay.py`
  - The DFT vmap and `jax.jit(factor_graph.log_likelihood_function)` checks pass
    on current `main`.
  - The process then dies during the `TransformerNUFFT` Delaunay cube
    cross-check before printing the NUFFT result, matching the release report's
    SIGKILL-style failure.

## Proposed Scope

Reduce or restructure the release script so it still validates the Delaunay
datacube JAX path without exceeding the release runner memory budget. Treat this
as workspace-only unless investigation proves the NUFFT memory spike is caused
by a library regression that should be fixed in @PyAutoArray or @PyAutoLens.
