## autogalaxy-wst-jax-grad-interferometer
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/30
- completed: 2026-05-06
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/31
- repos: autogalaxy_workspace_test
- notes: Task 7/9 of the autogalaxy_workspace_test parity epic (#5). Created `scripts/jax_grad/interferometer/{lp.py, mge.py}` from scratch — autolens has no interferometer `jax_grad` reference. Both pass on CI 3.12 (`lp.py` 6.6s shape (7,), `mge.py` 11.7s shape (4,)). Used plain `ag.lp.Sersic` (not `lp_linear`) to match the validated `jax_likelihood_functions/interferometer/lp.py` setup. The `jax_grad/` env_vars override added in PR #29 already covered this PR — no env_vars.yaml change. Layout-divergence-from-autolens question now compounded by this PR (autolens has flat `jax_grad/imaging_*.py` and no interferometer scripts at all); suggested filing the autolens-retrofit follow-up after task 8 ships.
