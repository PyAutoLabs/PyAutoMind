## ep-profiling-breakdown
- issue: https://github.com/Jammy2211/ic50_workspace/issues/6
- completed: 2026-05-18
- workspace-pr: https://github.com/Jammy2211/ic50_workspace/pull/7
- notes: Added `scripts/profile_ep_sim.py` to `z_projects/ic50_workspace`, an instrumented EP run that monkey-patches `HillAnalysis` / `GlobalLinearAnalysis` / `FixedHillCoefEPFactor` / `DynestyStatic.fit` to split wall time into Hill-LL evals (per dataset), global-LL evals, set_model_approx, Dynesty-wrapper overhead (search.fit minus LL evals), and EP-loop orchestration (optimise minus search.fit minus set_model_approx). Production scripts untouched. Writes `scripts/results/ep_sim_profile.{md,json}` with a scaling projection to 100/1000/10000 datasets. Headline: **~86% of `factor_graph.optimise` time is Dynesty wrapper overhead** (sampler init, paths, per-fit plot attempts, internal-folder cleanup) — only ~10% of `search.fit(...)` wall time is actual likelihood evaluation. Per-Dynesty-fit overhead ~5 s/fit dominates at every N. Projection (using observed M≈2 EP iterations under `kl_tol=1.0`): 5→1min, 100→20min, 1000→3h, 10000→1.4 days. Three independent runs validated bucket proportions stable across ~25% run-to-run variance. The profile script clears `output/ep_sim/` at startup to avoid the AutoFit cache-resume short-circuit ([[feedback_autofit_cache_resume_pyauto_test_mode]]). Out of scope: actual optimisation, cProfile pass, N=100 validation measurement. Same z_projects/ caveats as previous ic50 PRs ([[reference_ic50_workspace_nonstandard]]) — no worktree, no pending-release label, ship ran in Opus.

## Original prompt

The project @z_projects/ic50_workspace is our IC50  use case which we are now aiming to scale up the EP framework
to the IC50 use case.

Can you perform a run of ep_sim.py, and perform a timing break down of all the different steps that go into
the overall EP run time, which would include things like:

1) Time spent doing each IC50 Hill curve fit in a FactorAnalysis using Dynesty, total time and time per EP iteration.
2) Time spent fitting the global model.
3) Time spent doing all non fitting boiler plate (e.g. PyAutoFit over heads seting up graph, iterations around the EP loop, and so forth).

Can you attempt to break 3) down into sub categories.

Given the time taken for 5 datasets in this example, present a proejction for how long 100, 1000, 10000 would take.

This will then form the basis of us optimizing and improving all EP functioanlity so it runs fast enough to scale up
to lsrger samples.