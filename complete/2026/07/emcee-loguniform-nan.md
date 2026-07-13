## emcee-loguniform-nan
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1328 (closed)
- completed: 2026-07-08
- repos: PyAutoFit (PR #1329, merged 0f26ff2d8)
- branch: feature/emcee-loguniform-nan (deleted local + remote)
- prompt: bug/health_fixes/autofit_sampler_database.md (scoped — Emcee-NaN slice; database/minimal_output scripts remain live in the prompt for a parked clean-output follow-up)
- validation:
  - Root cause reproduced A/B on clean main: emcee stretch move proposes value<=0
    for a LogUniform param → NumPy log_prior_from_value returned -log(value)=NaN →
    propagated to fom=log_likelihood+Σlog_prior (fitness.py; NaN-guard covers only
    the likelihood) → emcee ValueError: Probability function returned NaN. OLD main
    crashes; NEW completes (same seed).
  - Fix (minimal scope, user-chosen): NumPy LogUniform path returns -inf for
    value<=0 via double-where (no RuntimeWarning); positive values keep -log(value)
    (documented unnormalised/unbounded contract preserved, its test kept); UniformPrior
    and JAX path untouched.
  - Tests: test_autofit/{mapper,non_linear,messages} 918 passed / 13 skipped + 250
    prior tests; new regression test__log_prior_from_value__non_positive_returns_neg_inf;
    autofit_workspace_test parity gates (priors_xp_dispatch, emcee_gaussian_bias_check)
    pass unchanged (only exercise positive/in-bounds values).
- notes: |
    Second bug shipped off PyAutoHeart #27 (after samples_parameter_paths parked
    non-reproducing). Confirms #27 is only PARTLY stale — the Emcee-NaN leg was a
    live LogUniform producer bug. Routed via /bug → Bug Agent (not Feature: its own
    4-phase split was the feature-phasing heuristic misfiring on the 9-script bundle;
    scoped to the single reproducing library defect). PR body edited via gh api PATCH
    (gh pr edit hits the Projects-classic GraphQL bug); merged via gh api PUT.
