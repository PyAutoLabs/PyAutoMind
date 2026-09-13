# HowToFit tutorial 5 (EP) never shares the centre it says it shares

Type: bug
Target: HowToFit
Repos:
- HowToFit
Themes:
- graphical-ep
- tutorials
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 10
Unattended: ready
Filed: 2026-09-13

Found 2026-09-13 while rolling the model figure into
`HowToFit/scripts/chapter_3_graphical_models/tutorial_5_expectation_propagation.py`
(model-figures phase 6a, task `model-figures-rollout-autofit`, PyAutoFit#1620).

## Symptom

The tutorial's prose says "We will assume all Gaussians share the same centre"
and creates `centre_shared_prior = af.GaussianPrior(...)`, but never assigns it:
each per-dataset model gets a fresh `af.GaussianPrior` for `centre`, so nothing
is shared across the datasets. The new model figure makes this visible: no
`shared` badge appears anywhere on the map (only the orange `relation` pills
into `linear_regression`), and the EP run prints
`STALE FACTORS: dataset_0 never completed a single update`.

Related: the tutorial is listed in `config/build/no_run.yaml` as `NEEDS_FIX
2026-08-05` (PyAutoFit#1454, `LinearRegressionAnalysis.log_likelihood_function`
returns a constant `-1`), so CI never runs it and neither defect is caught.

## Fix

- Assign `centre_shared_prior` to every per-dataset model's `centre` (mirror how
  tutorial 2 / tutorial 3 share the centre), so the map shows the blue `shared`
  badge and the EP fit actually passes messages about one centre.
- Re-check the `__Seeing the EP run__` prose added in phase 6a against a fresh
  render once the centre is shared (it was written to describe only what the
  unshared map showed).
- If PyAutoFit#1454 is fixed alongside, drop the `no_run.yaml` entry so smoke CI
  runs the tutorial again; otherwise leave it and say so in the PR.

## Acceptance

- `af.ModelPlotter(factor_graph.global_prior_model).figure()` shows one shared
  `centre`; the EP state figure shows every dataset factor updating.
- Headless run exits 0; notebook regenerated.

<!-- formalised by the Intake (Conception) Agent on 2026-09-13 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b5c57673-b465-4a62-8c98-59aa5c95bac3/scratchpad/howtofit_t5_shared_centre_raw.md -->
