## jax-phase3-adoption
- issue: none — direct follow-up to use-jax-for-vis-default / PyAutoFit #1278
- completed: 2026-05-16
- workspace-prs:
  - https://github.com/PyAutoLabs/autolens_workspace/pull/159 (26 scripts, 72/32)
  - https://github.com/PyAutoLabs/autogalaxy_workspace/pull/74 (3 scripts, 3/2)
  - https://github.com/PyAutoLabs/autofit_workspace/pull/61 (1 script, 6/6)
- repos: autolens_workspace, autogalaxy_workspace, autofit_workspace
- notes: |
    Phase 3 of z_features/jax_visualization.md (archived earlier today).
    Sweep adoption of use_jax=True across 30 tutorial scripts in the
    three production workspaces, filling the gaps the 2026-05-08 audit
    flagged plus consistency mismatches (slam.py had use_jax=True but
    companion modeling.py didn't, etc.) discovered in the 2026-05-16
    re-audit done at the start of this task.

    The Phase 2 default-flip (PyAutoFit #1278) made use_jax=True
    sufficient — viz auto-follows via the sentinel. User explicitly
    confirmed the API direction: a single explicit flag making JAX
    dependence fully visible. No use_jax_for_visualization=True calls
    added anywhere.

    Audit precondition: original 2026-05-08 Phase 3 framing (zero
    adoption) was stale — 66/32/4 scripts already had use_jax=True
    via incidental adoption in other tasks. Re-audit narrowed scope
    to the consistency gaps.

    Skip list (intentional opt-outs honoured): cpu_fast_modeling.py,
    autogalaxy/ellipse/modeling.py (AnalysisEllipse stability),
    expectation_propagation.py + hierarchical.py (FactorGraphModel),
    autofit/searches/mle.py (LBFGS), all simulators/fit.py/
    likelihood_function.py/aggregator scripts.

    Phase 3 of the JAX visualization roadmap is now complete. Tracker
    z_features/jax_visualization.md already archived under
    z_features/complete/. Phases 4 (subprocess viz) and 5 (live
    Colab/Jupyter cell) remain explicit stubs awaiting prompts.

    Worktree force-removed (PYAUTO_WT_FORCE=1) because smoke runs
    regenerated binary dataset files in the workspaces (the worktree
    symlinks share dataset/ with main); user-approved as part of the
    "complete the task" flow.
