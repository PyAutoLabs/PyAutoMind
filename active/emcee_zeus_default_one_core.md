# Emcee and Zeus default to one core until their pooled path is fixed

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: easy
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Epic: likelihood-lifecycle
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1802
Filed: 2026-11-26

## Finding

This prompt replaces `draft/bug/autofit/ensemble_searches_number_of_cores_auto_hang.md`. That draft's claim of an R6-only hang was wrong: it rested on runs that reloaded an already completed fit.

With a fresh output folder and `number_of_cores=2`, Emcee returns `log_likelihood = inf` and then hangs at interpreter exit, because its SneakyPool workers are never sent a stop signal (`multiprocessing.util._exit_function` joins children that are blocked in `queue.get`). This happens on the released 2026.11.25.1 (339640e3a) and on main alike. `number_of_cores=1` is correct on both. Pooled Zeus gets wrong log probabilities (`Number of contractions exceeded maximum limit`).

R6 (PyAutoFit#1800) made `"auto"` the default, so the broken pool is now used by default:
- PyAutoFit main Tests (3.13) has 9 Zeus conformance tests failing intermittently.
- The release-integrate validation times out on `autofit_workspace/scripts/plot/emcee_plotter.py`.

## Ask

Set Emcee and Zeus back to a default of `number_of_cores=1` (as GridSearch already is), keeping `"auto"` as an opt-in, and explain why in the docstrings. Fixing the pooled path is `draft/bug/autofit/pooled_emcee_zeus_wrong_likelihoods.md`.
