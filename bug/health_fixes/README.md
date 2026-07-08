# Release-fidelity health fixes

This folder tracks the script regressions exposed by the first real release-profile
validation in [PyAutoHeart issue #27](https://github.com/PyAutoLabs/PyAutoHeart/issues/27),
GitHub Actions run `28784914443`.

The run installed and verified all five TestPyPI wheels successfully, then reported
37 script failures and 5 timeouts across 42 scripts. Local reproduction used the
shared PyAuto development environment, current `main` library checkouts, each
workspace's `config/build/env_vars_release.yaml`, and the same 300-second cap.

Each failing script is assigned to exactly one prompt:

| Prompt | Scripts | Primary concern |
|---|---:|---|
| [samples_parameter_paths.md](samples_parameter_paths.md) — ⚠️ parked, does not reproduce on current `main` ([PyAutoFit#1327](https://github.com/PyAutoLabs/PyAutoFit/issues/1327), blocked on clean-CI re-validation) | 9 | PyAutoFit result/sample path resolution |
| [autofit_sampler_database.md](autofit_sampler_database.md) | 9 | Emcee NaNs and database output discovery |
| [aggregator_output_contracts.md](aggregator_output_contracts.md) | 7 | Result/aggregator prerequisites and generated paths |
| [jax_runtime_and_parity.md](jax_runtime_and_parity.md) | 6 | JAX/TFP compatibility and likelihood parity |
| [jit_visualization_outputs.md](jit_visualization_outputs.md) | 4 | Quick-update visualizations not producing images |
| [numerical_inversion_failures.md](numerical_inversion_failures.md) | 2 | Non-positive-definite inversion matrices |
| [release_timeout_policy.md](release_timeout_policy.md) | 5 | 300-second release-surface decisions |

Total: **42 scripts**. Scripts that pass on current `main` remain listed because they
still require a clean-worktree, directory-order reproduction before being declared
fixed. Do not rebaseline assertions or edit tutorials to conceal a library regression.
