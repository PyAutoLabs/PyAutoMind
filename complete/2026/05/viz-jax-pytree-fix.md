## viz-jax-pytree-fix
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/84
- completed: 2026-05-08
- workspace-pr:
  - https://github.com/PyAutoLabs/autolens_workspace_test/pull/85 (lead, closes #84)
  - https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/37 (autogalaxy sibling)
- repos: autolens_workspace_test, autogalaxy_workspace_test
- notes: |
    Direct follow-up to autogalaxy-viz-dispatch-swap (PyAutoGalaxy #390).
    Both visualization_jax.py scripts (autolens + autogalaxy versions) had
    been silently broken under JAX since their respective dispatch swaps
    landed: PyAutoLens #443 (2026-04-19) for the autolens version,
    PyAutoGalaxy #390 (2026-05-08) for the autogalaxy version. Each
    script's try/except wrapper caught the JAX trace failure
    (TypeError: ModelInstance not a valid abstract array), printed
    "PILOT FAILED", and exited 0 — invisible to test runners.

    Root cause: missing enable_pytrees() + register_model(model) so that
    jax.jit(fit_from) could trace the ModelInstance arg across the JIT
    boundary. Working sibling modeling_visualization_jit.py had these
    calls all along (lines 43-45) — visualization_jax.py just lacked them.

    Fix in both repos:
      1. Add enable_pytrees() + register_model(model) before constructing
         the analysis.
      2. Drop the try/except wrapper so future regressions fail loud.
      3. Split each workspace's config/build/env_vars.yaml imaging/visualization
         override into a NumPy-only pattern (visualization.py — substring
         match) and a JAX-only pattern (visualization_jax) that also unsets
         PYAUTO_DISABLE_JAX. Mirrors the existing
         imaging/modeling_visualization_jit override.

    Verified: both scripts now print PILOT SUCCEEDED with JAX enabled.

    Future work: neither visualization_jax.py is in smoke_tests.txt, so a
    future regression of the same shape would still be invisible to CI
    smoke. Promoting them to smoke is a separate decision per the user's
    "small curated subset" smoke policy and was not in scope here.
