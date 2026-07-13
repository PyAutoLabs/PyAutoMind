## autolens-jax-simulator-release-fixes
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/140
- completed: 2026-06-09
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/141 (merged d660e64)
- repos: autolens_workspace_test
- notes: Fixed the Autolens JAX simulator release-report failures. Imaging simulator parity now honestly checks eager `use_jax=True` parity only because full imaging-simulator JIT still rebuilds `Array2D.native` via NumPy indexing on traced values. Interferometer simulator JIT roundtrip now uses `autolens.jax.register_tracer_classes`. Cluster simulator closes over the tracer in the jitted point-solver wrapper so only source-plane coordinates are dynamic JAX arguments. Verified the three targeted scripts locally and PR CI on Python 3.12/3.13 before merge.
