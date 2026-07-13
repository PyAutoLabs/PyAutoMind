## latent-jax-release-failures
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1316
- completed: 2026-06-09
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1317 (merged 3ae0ccc)
- workspace-prs:
  - https://github.com/PyAutoLabs/autofit_workspace_test/pull/33 (merged 13e6f17)
  - https://github.com/PyAutoLabs/autogalaxy_workspace/pull/112 (merged de9a355)
  - https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/65 (merged 627a8fa)
- repos: PyAutoFit, autofit_workspace_test, autogalaxy_workspace, autogalaxy_workspace_test
- notes: Fixed the first grouped release failures after the latent refactor. PyAutoFit now skips latent sample computation when an analysis has no enabled latent keys; workspace scripts were updated to match the current `use_jax` / `supports_jax_visualization` contract; the Autogalaxy results guide reloads its saved combined FITS with unchecked noise-map validation; and Autogalaxy ellipse JAX release-build env overrides were added. Verified targeted release reruns, PyAutoFit full suite, PyAutoBuild section checks, and PR CI before merge. Kaplinghat branches were not touched.

## Original prompt

# Fix latent/JAX release failures after latent refactor

Original user request:

> ok fix the first group

Context:

The adjusted PyAutoBuild report at
`PyAutoBuild/test_results/runs/2026-06-08T20-19-35Z/report_adjusted_after_latent_refactor.md`
groups the active release failures after rerunning the latent-refactor-suspect
scripts. Group A still fails after the latent class refactor and should be fixed
first.

Target failures:

- `autofit_workspace_test/scripts/jax_assertions/fitness_dispatch.py`
  - `Analysis has no attribute _jitted_fit_from`
- `autogalaxy_workspace/scripts/guides/results/start_here.py`
  - invalid/zero noise-map values
- `autogalaxy_workspace_test/scripts/ellipse/modeling_visualization_jit.py`
  - expected `jax.Array`, got `numpy.float64`
- `autogalaxy_workspace_test/scripts/ellipse/visualization_jax.py`
  - `fit_ellipse.png` not produced
- `autogalaxy_workspace_test/scripts/interferometer/modeling_visualization_jit.py`
  - `compute_latent_samples` empty stack

Start with the smallest PyAutoFit-level failure,
`autofit_workspace_test/scripts/jax_assertions/fitness_dispatch.py`, because it
asserts the JAX visualization dispatch state directly and may clarify the
downstream JAX visualization failures.

Likely affected repositories:

- `@PyAutoFit`
- `@autofit_workspace_test`
- `@autogalaxy_workspace`
- `@autogalaxy_workspace_test`
- possibly `@PyAutoGalaxy`
