## jit-visualization-env-overrides
- issue: none — direct fix for Cluster C in `PyAutoBuild/test_results/runs/2026-04-29T14-48-47Z/triage.md`
- completed: 2026-05-01
- workspace-pr:
  - PyAutoLabs/autogalaxy_workspace_test#24
  - PyAutoLabs/autolens_workspace_test#70
- notes: 4 `modeling_visualization_jit*` integration scripts (1 in autogalaxy_workspace_test, 3 in autolens_workspace_test) failed in CI with `AssertionError: expected jax.Array, got <class 'numpy.float64'>`. Root cause was env-var-only: the CI defaults set `PYAUTO_DISABLE_JAX=1`, which `PyAutoFit/autofit/non_linear/analysis/analysis.py:42-46` intercepts and silently flips `use_jax_for_visualization` off, so `fit_for_visualization` returned a numpy `float64` and Part 1's `isinstance(..., jnp.ndarray)` failed. `PYAUTO_SMALL_DATASETS=1` would also have broken the hardcoded mask, and `PYAUTO_TEST_MODE=2` / `PYAUTO_FAST_PLOTS=1` would have broken Part 2's real-Nautilus + fit.png assertions. Fix: one new override entry per workspace's `config/build/env_vars.yaml` matching `imaging/modeling_visualization_jit`, mirroring the existing `jax_likelihood_functions/` precedent. Verified end-to-end PASS for all four scripts under the new env. Pure config change — no library or script edits.
