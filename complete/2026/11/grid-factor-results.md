## grid-factor-results
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1789
- completed: 2026-11-22
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1791
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1791

Factor results use the fitted grid-cell submodels for full samples and summaries. Two shared priors across four grid cells reproduced the old KeyError and now yield both child results. The full PyAutoFit suite passed 4,311 tests. The existing SLaM task can resume at its workspace witness.

GitHub CI at the approved heads: PyAutoLabs/PyAutoFit#1791: 5 successful checks, 1 skipped. Any skipped checks were non-test Heart-feed refreshes.

## Original prompt

# SearchGridSearch over a FactorGraphModel crashes in make_result

Type: bug
Issued: 2026-11-22
Target: autofit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: normal
Consequence: judge
Witness: `af.SearchGridSearch(...).fit(model=factor_graph.global_prior_model, analysis=factor_graph, grid_priors=[shared_prior_a, shared_prior_b])` over a two-factor graph sharing those priors completes under `PYAUTO_TEST_MODE=1`, and its best result indexes per factor (`result.model[0]`, `result.model[1]`); a unit test in `test_autofit/non_linear/grid/` covers it.

## Symptom

Found by the shift worker on autolens_workspace#683 (SLaM simultaneous subhalo grid search), 2026-11-20.
Running a grid search over a factor graph crashes in the first cell:

```
autofit/non_linear/grid/grid_search/job.py:55 perform → search_instance.fit
autofit/graphical/declarative/collection.py:284 make_result → samples_summary.subsamples(model_factor.prior_model)
autofit/non_linear/samples/sample.py:138 subsample
KeyError: 'No path from () in sample'
```

reproduce before fixing: run autolens_workspace branch `feature/slam-simultaneous-subhalo-grid-search`
`scripts/multi_dataset/features/slam/simultaneous.py` under `PYAUTO_TEST_MODE=1`, or a minimal two-factor
Gaussian graph with a shared prior in a `SearchGridSearch`.

## Cause

`GridSearch.job_for_analysis_grid_priors_and_values` maps the global model with
`mapper_from_partial_prior_arguments`, which replaces the grid priors with new per-cell priors.
`FactorGraphModel.make_result` then splits the samples by each **original** `model_factor.prior_model`.
That model still holds the replaced priors, so `path_map_for_model` → `all_paths_for_prior` returns `()`.

## Fix (to plan)

- Split by the per-factor sub-models of the model the search actually fitted (`samples_summary.model[i]`
  for a `GlobalPriorModel`-shaped collection) instead of the factor's original `prior_model`, or have the
  job rebuild the factor graph from the mapped model.
- Unit test on a toy two-factor graph.
- Then resume autolens_workspace#683.
