## analysis-shared-state
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1307
- completed: 2026-06-07
- epic: z_features/analysis_shared_state.md (sub-task A — autofit deliverable)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1308
- workspace-pr:
  - https://github.com/PyAutoLabs/autofit_workspace/pull/69
  - https://github.com/PyAutoLabs/autofit_workspace_test/pull/31
- notes: Generic cross-`Analysis` shared-state mechanism for `FactorGraphModel` (opt-in `shared_state_from` + `shared=` kwarg, lead-factor compute-once forwarding), the `af.ex` 1D Gaussian toy, the `shared_analysis_state` workspace tutorial, and fast + JAX assertion suites. Sub-task B (lensing datacube consumer, `autolens/datacube_shared_state_consumer.md`) now unblocked, still un-issued.
