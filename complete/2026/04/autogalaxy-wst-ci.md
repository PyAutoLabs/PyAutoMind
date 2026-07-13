## autogalaxy-wst-ci
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/6
- completed: 2026-04-22
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/7
- umbrella: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/5 (task 1/9)
- notes: Added `.github/workflows/smoke_tests.yml`, `.github/scripts/run_smoke.py`, and `config/build/env_vars.yaml` — mirrors autolens_workspace_test's smoke-test setup with PyAutoLens stripped. CI green on Python 3.12 and 3.13. `pending-release` label was created on the repo for the first time during this PR. env_vars.yaml ships only the `jax_likelihood_functions/` override; sibling tasks 2–9 will add per-path overrides alongside their scripts.
