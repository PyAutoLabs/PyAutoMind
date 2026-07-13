## use-jax-for-vis-default
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1275
- completed: 2026-05-16
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1278
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/28
- repos: PyAutoFit, autofit_workspace_test
- notes: |
    Phase 2 of z_features/jax_visualization.md. Default of
    Analysis(use_jax_for_visualization) flipped from bool=False to
    Optional[bool]=None — sentinel that resolves to use_jax. Analysis(use_jax=True)
    now turns on the JIT visualization path automatically. Explicit True/False,
    PYAUTO_DISABLE_JAX=1, and the JAX-not-installed fallback all preserve
    their existing behaviour.

    Test split per long-standing rule (numpy-only unit tests; JAX-needing
    assertions in workspace_test): 1 numpy-only env-var-override test in
    test_autofit/analysis/test_use_jax_for_visualization.py; 4 JAX-conditional
    assertions in autofit_workspace_test/scripts/jax_assertions/fitness_dispatch.py.

    Workspace audit at ship time: zero production workspace scripts set
    use_jax_for_visualization= explicitly. autolens_workspace_test has ~12
    redundant =True call sites (harmless; optional cleanup follow-up).

    Tracker z_features/jax_visualization.md is now archivable — Phases 3-5
    are explicit stubs. Re-run /start_dev z_features/jax_visualization.md
    to verify shipped state and move to z_features/complete/.
