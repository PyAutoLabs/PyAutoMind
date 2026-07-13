## autogalaxy-wst-jax-grad-multi
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/32
- completed: 2026-05-06
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/33
- repos: autogalaxy_workspace_test
- notes: **Final task (8/9) of the autogalaxy_workspace_test parity epic (#5) — epic is now closed.** Created `scripts/jax_grad/multi/{lp.py, mge.py}` from scratch. Each script joins per-band `AnalysisImaging` factors via `af.FactorGraphModel(use_jax=True)` and wraps the global log-likelihood in `jax.value_and_grad`. Both pass on CI 3.12 (`lp.py` 10.6s shape (9,), `mge.py` 21.0s shape (6,)). Used `ag.lp.Sersic` and option B per-band `ell_comps` matching `jax_likelihood_functions/multi/{lp,mge}.py` patterns. The `jax_grad/` env_vars override added in PR #29 covered all three jax_grad subfolders. Suggested follow-up: file an autolens-retrofit issue covering `imaging_lp.py → imaging/lp.py`, `imaging_mge.py → imaging/mge.py`, plus net-new interferometer/multi ports for autolens.
