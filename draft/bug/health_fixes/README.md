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
| ~~aggregator_output_contracts.md~~ — ✅ **SHIPPED 2026-07-07**, record `complete/2026/07/aggregator-output-contracts.md` (PyAutoFit#1324; autogalaxy_workspace#122, autolens_workspace#229, autolens_workspace_test#146 all merged) | 7 | Result/aggregator prerequisites and generated paths |
| [jax_runtime_and_parity.md](jax_runtime_and_parity.md) | 6 | JAX/TFP compatibility and likelihood parity |
| [jit_visualization_outputs.md](jit_visualization_outputs.md) | 4 | Quick-update visualizations not producing images |
| [numerical_inversion_failures.md](numerical_inversion_failures.md) | 2 | Non-positive-definite inversion matrices |
| [release_timeout_policy.md](release_timeout_policy.md) | 5 | 300-second release-surface decisions |

Total: **42 scripts**. Scripts that pass on current `main` remain listed because they
still require a clean-worktree, directory-order reproduction before being declared
fixed. Do not rebaseline assertions or edit tutorials to conceal a library regression.

## 2026-08-09 sweep — three things to know before working this folder

1. **One of the seven has shipped** (aggregator_output_contracts, struck through above);
   its file is gone from this folder and lives in `complete/2026/07/`. The table said
   nothing about that for a month.

2. **Script paths in `jit_visualization_outputs.md` and `jax_runtime_and_parity.md` are
   all stale** — every one 404s, and every one still exists under a renamed layout
   (`scripts/jax_likelihood_functions/<dataset>/` → `scripts/<dataset>/jax_likelihood/`;
   `<dataset>/modeling_visualization_jit.py` → `<dataset>/visualization/…`; `multi/` →
   `multi_dataset/`). Corrected tables are in each prompt. A 404 in this cluster means
   drift, not deletion.

3. **Many of the named scripts are now parked** in their workspace's
   `config/build/no_run.yaml`, mostly `SLOW` for cap timeouts, with dates *after* these
   prompts were filed. A parked script cannot fail release validation, so a green
   release run is not evidence of a fix — the 2026-08-07 Stage 3 integrate reports
   `657p/0f/101s/0t`, and those **101 skips** are where this cluster's scripts went. The
   parkings also cite a **different failure** (timeout) from the defects these prompts
   describe, so unparking is a precondition for reproducing any of them.

None of the five remaining prompts was graded shipped. What this sweep could establish
offline is recorded in each file; the reproduction legs all need real runs.
