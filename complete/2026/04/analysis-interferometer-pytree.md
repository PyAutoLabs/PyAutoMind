## analysis-interferometer-pytree
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/375
- completed: 2026-04-28
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/376
- repos: PyAutoGalaxy
- notes: Adds JAX pytree registration for `AnalysisInterferometer` (mirrors imaging scaffold from #364). Galaxies flatten/unflatten lifted into `autogalaxy/analysis/jax_pytrees.py::register_galaxies_pytree()`; imaging body collapsed from 41 → 11 lines as a side benefit. Quantity and Ellipse deferred to follow-ups. End-to-end JIT verification will land in the queued `autogalaxy_workspace_test_jax_likelihood_interferometer` task. Smoke tests: 42/42 passed.
