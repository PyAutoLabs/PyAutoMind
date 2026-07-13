## unify-jax-visualization
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1296
- completed: 2026-05-27
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1297
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/130, https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/62
- repos: PyAutoFit, autolens_workspace_test, autogalaxy_workspace_test
- notes: Removed use_jax_for_visualization flag; visualization follows use_jax automatically. Added _warmup_visualization to Fitness.__init__ — pre-compiles ~200 per-function JAX JIT caches before sampling starts, moving the ~16s first-call cost from the first quick update to search setup. Profiling revealed the 20s was 234 individual XLA compilations through the decorator chain, not numba. The jax.jit(fit_from) single-graph approach didn't help steady-state (~2-6s) because FitImaging properties evaluate lazily outside the JIT. Also removed enable_pytrees()/register_model() from 57 jax_likelihood_functions scripts — confirmed unnecessary for _vmap (flat vector input). Smoke 33/34 (1 pre-existing latent magzero failure).
