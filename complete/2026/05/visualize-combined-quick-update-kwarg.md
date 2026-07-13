## visualize-combined-quick-update-kwarg
- issue: none — followup to priors-jax-native (#1262); deferred Bug B at #1266
- completed: 2026-05-15
- library-prs:
  - PyAutoFit: https://github.com/PyAutoLabs/PyAutoFit/pull/1267
  - PyAutoGalaxy: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/414
- notes: Followup audit work for priors-jax-native (#1262). Pure additive one-line `quick_update: bool = False` kwarg on `VisualizerExample.visualize_combined` (PyAutoFit) and `VisualizerImaging.visualize_combined` (PyAutoGalaxy), mirroring the plumbing added by commit `a1e360567` ("Fix `AnalysisFactor.visualize_combined` dispatch in FactorGraph") which updated the base class + AnalysisFactor + PyAutoLens visualizers but missed these two. Fixed the four previously-broken graphical/EP integration scripts: `autofit_workspace_test/scripts/graphical/{simultaneous,hierarchical}.py` and `autofit_workspace/scripts/{features/graphical_models,cookbooks/multiple_datasets}.py`. PyAutoFit 1242/1242 + PyAutoGalaxy 870/870 unit tests pass. The deeper sign-convention finding surfaced during this audit (Gaussian-family `log_prior_from_value` returning cost form, biasing MCMC posteriors) was deferred to dedicated issue #1266.
