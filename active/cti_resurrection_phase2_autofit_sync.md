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
