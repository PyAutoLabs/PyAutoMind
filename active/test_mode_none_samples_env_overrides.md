# Test-mode NoneType failures: scripts that need real samples/fits (env_vars overrides)

Type: bug
Target: workspaces
Repos:
- autolens_workspace_test
- autofit_workspace_test
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

From the 2026-07-21 census. These are NOT code bugs — they are the known "script needs real samples /
a real fit, but the smoke profile bypasses the sampler" env-config gap. Each fails with a NoneType
attribute error because the aggregator/samples object is empty under `PYAUTO_TEST_MODE=2`.

- autolens_workspace_test `imaging/model_fit.py` — `AttributeError: 'NoneType' object has no attribute 'parameter_lists'`
- autolens_workspace_test `latent/latent_nan_robustness.py` — `'NoneType' has no attribute 'sample_list'`
- autolens_workspace_test `latent/latent_variables_smoke.py` — `'NoneType' has no attribute 'model'`
- autofit_workspace_test `profiling/aggregator/profile_database.py` — database array HDU is None -> `'NoneType' has no attribute 'dtype'`

Fix: add per-script overrides in each repo's `config/build/env_vars.yaml` unsetting `PYAUTO_TEST_MODE`
(and `PYAUTO_SKIP_FIT_OUTPUT` where the script reads outputs), mirroring the existing
`guides/results/` and `database/scrape/` precedents. Keep them fast — prefer the minimum unset that
produces real samples. Verify each via `run_python.py <project> <scripts/dir>`; confirm no sibling
regressions and that runtimes stay within the per-script cap.
