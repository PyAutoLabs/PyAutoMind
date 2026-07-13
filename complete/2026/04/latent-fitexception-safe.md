## latent-fitexception-safe
- issue: none — follow-up to autofit_workspace_test smoke-test cleanup
- completed: 2026-04-26
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1233
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/13
- notes: `Analysis.compute_latent_samples` now catches per-sample `FitException` in the non-JAX branch and substitutes a NaN row, then a row-mask filter drops those samples before the existing per-latent column mask. Motivated by stochastic CI flake on `features/assertion.py` under `PYAUTO_TEST_MODE=1` (reduced iterations + real sampler): Dynesty's `sample_list` occasionally contains parameter vectors that violate the model's inequality assertions, and the post-fit latent loop calling `model.instance_from_vector` would raise `FitException` and kill the entire fit. JAX path untouched (jit/vmap can't raise Python exceptions anyway). Workspace side flips `features/assertion` env_vars override from `unset: [PYAUTO_TEST_MODE]` (which fell back to `0`, ~67–107s) back to `set: PYAUTO_TEST_MODE: "1"` (~6s). 5/5 stable smoke runs locally; 2 CI runs × 2 Python versions all pass.
