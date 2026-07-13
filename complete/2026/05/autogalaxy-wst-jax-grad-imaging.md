## autogalaxy-wst-jax-grad-imaging
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/28
- completed: 2026-05-05
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/29
- repos: autogalaxy_workspace_test
- notes: Task 6/9 of the autogalaxy_workspace_test parity epic (#5). Ported autolens `jax_grad/imaging_{lp,mge}.py` to autogalaxy under a new `scripts/jax_grad/imaging/` subfolder; both scripts pass on CI 3.12 (`lp.py` 11.3s, `mge.py` 16.8s). Established subfolder layout convention even though autolens is currently flat — surfaced the retrofit question to the maintainer via PR body. Added `jax_grad/` env_vars override mirroring `jax_likelihood_functions/` (unsets `PYAUTO_SMALL_DATASETS` + `PYAUTO_DISABLE_JAX`). Pytree registration on `autogalaxy/imaging/model/analysis.py` was already in place from task 3.
