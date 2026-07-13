## ag-quantity-fit-from
- issue: none — direct follow-up to ag-ellipse-quantity-pytree (#401)
- completed: 2026-05-14
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/404
- repos: PyAutoGalaxy
- notes: |
    Small library fix that completes one half of the deferred follow-up
    from Phase 0c. Added fit_from(instance) as a thin alias for
    fit_quantity_for_instance on AnalysisQuantity, and swapped the
    VisualizerQuantity dispatch line from
    analysis.fit_quantity_for_instance to analysis.fit_for_visualization.

    With this PR, use_jax_for_visualization=True on ag.AnalysisQuantity
    actually fires the JIT-cached path (it was a silent no-op despite
    #401 shipping the FitQuantity pytree registration + **kwargs
    passthrough, because the visualizer bypassed fit_for_visualization
    entirely).

    18/18 test_autogalaxy/quantity/ tests pass. Alias smoke-verified
    interactively: fit_from and fit_quantity_for_instance return the
    same FitQuantity (same dataset reference).

    Pre-flight diff check (per the binary-leak memory rule from earlier
    this session) caught nothing — only 2 .py files modified.
    Parallel-worktree-safe alongside interferometer-nufftax-updates
    (which is in autolens_workspace + autogalaxy_workspace — different
    repos).

    The matching ellipse follow-up (VisualizerEllipse dispatch swap)
    is NOT in this PR. ag.AnalysisEllipse.fit_list_from returns
    List[FitEllipse], not a single fit — needs autofit-side
    fit_for_visualization contract design before it can be wired
    similarly. Tracked as a separate (still-deferred) follow-up.

    Remaining follow-up: a small Phase 1C-extension workspace_test PR
    can now add autogalaxy_workspace_test/scripts/quantity/{visualization.py,
    visualization_jax.py} to exercise the dispatch end-to-end.
