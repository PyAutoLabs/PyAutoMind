- Issue [autolens_workspace #683](https://github.com/PyAutoLabs/autolens_workspace/issues/683) closed when [PR #684](https://github.com/PyAutoLabs/autolens_workspace/pull/684) merged at `ba7f7738` on 2026-11-22.
- The simultaneous SLaM grid search fits both waveband analyses in each cell, retaining a shared subhalo centre and per-band dataset offsets. Refinement uses the winning cell’s model for each band. The notebook was regenerated from the script.
- The script and notebook independently completed all four grid cells and final refinement from fresh output in CPU test mode with merged [PyAutoFit #1791](https://github.com/PyAutoLabs/PyAutoFit/pull/1791). Every cell kept the reference-band offsets fixed and the second band’s offsets free.
- Heart workspace smoke passed 42 scripts and two notebooks. All eight GitHub checks passed at `1bde121b`, including both Python 3.12 and 3.13 smoke jobs.

## Original prompt

# SLaM simultaneous subhalo grid search fits last band only

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: after the fix, `subhalo_grid_search` in `scripts/multi_dataset/features/slam/simultaneous.py` calls `SearchGridSearch.fit` with a `FactorGraphModel` (`model=factor_graph.global_prior_model, analysis=factor_graph`) and the resulting `model.info` lists a `dataset_model.grid_offset` entry for every band after the first; a grep for `fit(\n        model=model,\n        analysis=analysis,` in that function returns nothing.
Review-minutes: 3
Unattended: ready
Verified: 2026-11-20 fb916757 (autolens_workspace)
Lane: any

# SLaM simultaneous subhalo grid search fits last band only

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: small
Autonomy: safe
Priority: normal
Witness: after the fix, `subhalo_grid_search` in `scripts/multi_dataset/features/slam/simultaneous.py` calls `SearchGridSearch.fit` with a `FactorGraphModel` (`model=factor_graph.global_prior_model, analysis=factor_graph`) and the resulting `model.info` lists a `dataset_model.grid_offset` entry for every band after the first; a grep for `fit(\n        model=model,\n        analysis=analysis,` in that function returns nothing.

## Symptom

`autolens_workspace/scripts/multi_dataset/features/slam/simultaneous.py`, stage `subhalo_grid_search`
(lines ~480-540): the stage builds a per-band `model` and `af.AnalysisFactor` for every band in a loop,
then calls

    subhalo_grid_search.fit(model=model, analysis=analysis, grid_priors=[...])

with the loop's **last** band `model` and `analysis` only. Every other stage of the pipeline wraps its
factors in `af.FactorGraphModel(*analysis_factor_list, use_jax=True)` and fits all bands
simultaneously; this one silently fits a single band. The per-band `Collection` it builds also omits
`dataset_model`, so the per-band grid offsets modeled in every other stage are dropped here.

Found while triaging autolens_workspace#524 (the per-band `DatasetModel` rework of this pipeline),
which leaves this stage alone. `subhalo_no_subhalo` and `subhalo_refine` are fine.

## Fix

- Build `factor_graph = af.FactorGraphModel(*analysis_factor_list, use_jax=True)` as the sibling stages do.
- Call `subhalo_grid_search.fit(model=factor_graph.global_prior_model, analysis=factor_graph, grid_priors=[...])`,
  taking the `grid_priors` from the shared `subhalo` model (the same prior objects appear in every band's
  Collection, so `subhalo.mass.centre_0/1` resolve inside the global model).
- Add `dataset_model=dataset_model_list[i]` (the per-band list #524 introduces) to the per-band `Collection`.
- Confirm `af.SearchGridSearch` accepts a `FactorGraphModel` analysis (it does for the `subhalo_refine`-style
  factor graphs elsewhere in the workspace; if not, that is a PyAutoFit follow-up to file, not to fix here).
- Regenerate the notebook; smoke-run under `PYAUTO_TEST_MODE`.

<!-- formalised by the Intake (Conception) Agent on 2026-09-04 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/4caac41d-a9a3-4a30-8192-75baff5614bb/scratchpad/intake_subhalo.md -->

## Answers from the human
- Q19 (2026-11-20, shift 2026-11-20-am question on autolens_workspace#683): 1 — (a) fix PyAutoFit first (the follow-up now recorded in complete/2026/11/grid-factor-results.md), then resume branch feature/slam-simultaneous-subhalo-grid-search and open the PR https://github.com/PyAutoLabs/autolens_workspace/issues/683#issuecomment-7038127994
