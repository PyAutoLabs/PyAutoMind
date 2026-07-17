- issue: https://github.com/PyAutoLabs/PyAutoCTI/issues/86 (closed)
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/87 (merged 12a3eca97)
- summary: CTI resurrection Phase 2 — autofit sync. The 5 multi-analysis aggregator tests quarantined in Phase 0 (analysis summing removed from PyAutoFit) are ported to af.AnalysisFactor + af.FactorGraphModel and pass; the suite is now 271 passed / 0 skipped / 0 failed with no quarantines anywhere. Loaders: new _cti_list_from helper in aggregator/{fit_dataset_1d,fit_imaging_ci}.py extracts per-dataset CTI models from single-analysis OR factor-graph instances. Conftest: aggregator_from accepts a list of analyses, builds the graph with the model shared across factors, and rebuilds the mock samples against global_prior_model. Drift sweep clean; visualize_*_combined multi-dataset path exercised end-to-end by the graph fits.
- traps: a factor-graph global_prior_model instance carries the per-factor child instances PLUS the FactorGraphModel itself as a trailing child — filter children by hasattr(child, "<component>") when unpacking. Samples built against the single shared model DON'T resolve against global_prior_model (paths gain per-factor prefixes like ('0','cti',...)) — rebuild Sample.from_lists against the global model. The database scraper error surfaces as a misleading sqlalchemy NoResultFound (the real KeyError is swallowed into the except branch's item.instance evaluation).
- heart: shipped + merged through the same pre-existing CTI-unrelated organism-scope RED reasons on human ack 2026-07-17 ("Ship + merge + Phase 3").
- epic-next: Phase 3 CI + ecosystem plumbing (GitHub Actions rework, worktree.sh/labels/Build/Heart registration, RTD/docs hub) starts immediately per the same human authorization.

## Original prompt

# CTI resurrection — Phase 2: autofit sync (factor-graph aggregator port)

Type: feature
Target: PyAutoCTI
Repos:
- @PyAutoCTI
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Phase 2 of the CTI resurrection epic (Phase 0: #82/#83; Phase 1: #84/#85, both
merged 2026-07-17). Sync PyAutoCTI's model-fit layer with current PyAutoFit,
principally the multi-analysis path: autofit removed analysis summing
(`analysis + analysis`) in favour of `af.AnalysisFactor` +
`af.FactorGraphModel`, and 5 aggregator tests were skipped in Phase 0 pending
this port.

## Scope

1. **Port the multi-analysis aggregator tests**: update
   `test_autocti/aggregator/conftest.py` (`aggregator_from`) so multi-dataset
   cases build `af.AnalysisFactor(prior_model=model, analysis=...)` per
   dataset and fit `af.FactorGraphModel(*factors)` (the pattern of
   `autolens_workspace/scripts/multi/start_here.py`); un-skip the 5
   `pytest.mark.skip` tests in `test_autocti/aggregator/` and fix whatever
   falls out of the loaders (they read `fit.children`).
2. **Autofit drift sweep**: grep autocti source for other removed autofit
   idioms (analysis summing references, stale Result/Samples attribute use,
   search-plotting hooks) and fix or file what surfaces. Verify the
   `visualize_combined` / `in_ascending_fpr_order_from` multi-dataset
   visualizer path is exercised by the factor-graph fit.

## Out of scope

CI workflows / ecosystem plumbing (Phase 3), workspace scripts (Phase 4),
workspace_test rebuild + release (Phase 5).

## Context

- Phase records: `PyAutoMind/complete/2026/07/cti-resurrection-phase{0,1}.md`.
- PyAutoGalaxy deleted its aggregator tests entirely; CTI keeps and ports its
  own because CTI calibration is inherently multi-dataset (many injection
  levels fitted simultaneously).
- Worktree trap: activate.sh lacks PyAutoCTI on PYTHONPATH — prepend manually.
