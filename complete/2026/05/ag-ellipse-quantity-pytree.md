## ag-ellipse-quantity-pytree
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/400
- completed: 2026-05-14
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/401
- repos: PyAutoGalaxy
- notes: |
    Phase 0c of jax_visualization roadmap. Completes the PyAutoGalaxy
    Fit* pytree series. Library-only PR — no workspace_test scripts
    needed at this stage; Phase 1C will exercise the registrations
    end-to-end.

    Library scope:
    - **kwargs passthrough on ag.AnalysisEllipse + ag.AnalysisQuantity
      __init__ (parity with PR #399's ag.AnalysisInterferometer fix).
    - _register_fit_ellipse_pytrees on AnalysisEllipse — registers
      Ellipse (no no_flatten), EllipseMultipole(no_flatten=("m",)), and
      FitEllipse(no_flatten=("dataset",)).
    - _register_fit_quantity_pytrees on AnalysisQuantity — registers
      FitQuantity(no_flatten=("dataset", "func_str", "use_mask_in_fit"))
      and reuses register_galaxies_pytree() for the light_mass_obj.

    Test plan: 154/154 unit tests across test_autogalaxy/{ellipse,
    quantity,imaging,interferometer}/. Interactive round-trip smoke
    verified locally (FitEllipse: 8 dynamic leaves; FitQuantity: 3
    dynamic leaves with Galaxies correctly reconstructed).

    Scope narrowing discovered mid-task: the original prompt assumed
    pytree registration would unblock use_jax_for_visualization=True
    for these analyses, but BOTH visualizers bypass
    analysis.fit_for_visualization entirely (VisualizerEllipse calls
    fit_list_from; VisualizerQuantity calls fit_quantity_for_instance).
    use_jax_for_visualization=True therefore remains a no-op for these
    two analyses despite the pytree work.

    Two deferred follow-ups (NOT in this PR):
    - **Quantity visualizer dispatch swap** (small) — add fit_from alias
      on AnalysisQuantity, switch VisualizerQuantity to use
      analysis.fit_for_visualization. Mirrors the imaging/interferometer
      pattern. Unlocks use_jax_for_visualization end-to-end on quantity.
    - **Ellipse visualizer dispatch swap** (needs design) — fit_list_from
      returns List[FitEllipse], not a single fit. Either generalize the
      autofit fit_for_visualization contract or compose the list into a
      wrapper. Separate design pass needed.

    Parallel-worktree-safe alongside in-flight nfw-jax-port (PyAutoGalaxy
    mass profiles, file-disjoint). User-cleared file-level safety.
    Worktree-conflict guard bypassed for this reason.

    PyAutoGalaxy pytree series now complete:
    - ag.FitImaging (PR #364) ✓
    - ag.FitInterferometer (PR #376) ✓
    - ag.FitEllipse + ag.FitQuantity (this PR) ✓

    Library kwargs-gap series now complete across both libs:
    - al.AnalysisImaging (always) ✓
    - al.AnalysisInterferometer (#500) ✓
    - al.AnalysisPoint (#506) ✓
    - ag.AnalysisImaging (always) ✓
    - ag.AnalysisInterferometer (#399) ✓
    - ag.AnalysisEllipse + ag.AnalysisQuantity (this PR) ✓
