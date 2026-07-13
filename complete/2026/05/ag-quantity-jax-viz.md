## ag-quantity-jax-viz
- issue: none — direct follow-up to ag-quantity-fit-from (#404)
- completed: 2026-05-14
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/405 (sibling library fix discovered during the workspace work)
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/46
- repos: PyAutoGalaxy, autogalaxy_workspace_test
- notes: |
    Phase 1C-extension. Added autogalaxy_workspace_test scripts that exercise
    use_jax_for_visualization=True on ag.AnalysisQuantity end-to-end, now
    that the dispatch (#404) is wired.

    Mid-task library gap discovered: when JIT-flattening a FitQuantity
    via the new fit_for_visualization dispatch, the `DatasetModel`
    attribute (reachable via aa.FitImaging base-class) hit
    `TypeError: not a valid JAX type`. The imaging analogue
    (autogalaxy/imaging/model/analysis.py:186) and interferometer
    analogue (interferometer/model/analysis.py:183) both register
    DatasetModel — the quantity pytree registration shipped in #401
    omitted it.

    Fix sequence:
    1. PR #405 (PyAutoGalaxy): 2-line fix — add
       register_instance_pytree(DatasetModel) to
       _register_fit_quantity_pytrees, mirroring imaging/interferometer.
       Library-first merge gate respected — merged before #46.
    2. PR #46 (autogalaxy_workspace_test): the 2 new scripts
       (visualization.py + visualization_jax.py) + env_vars override.
       Verified to pass with the library fix from #405 in place — no
       workaround in the script.

    Sonnet's initial workaround (a script-level
    register_instance_pytree(DatasetModel) call with a TODO) was
    removed before shipping the workspace PR. Cleaner end state — the
    library is correct, the script is clean.

    No modeling_visualization_jit.py for quantity (Nautilus quick-update
    visualization isn't the primary use case for quantity fits, per the
    original Phase 1C prompt scoping).

    Pre-flight diff check (per the binary-leak memory rule) was clean
    on both PRs.

    Coverage matrix after this PR:
    - imaging:        NumPy + JAX + jit-Nautilus  ✓
    - interferometer: NumPy + JAX + jit-Nautilus  ✓
    - quantity:       NumPy + JAX (no jit — one-shot fits)  ✓
    - ellipse:        NumPy only — JAX still blocked on dispatch design

    Only ellipse JAX coverage remains — blocked on autofit
    fit_for_visualization contract design for list-returning analyses
    (AnalysisEllipse.fit_list_from returns List[FitEllipse]).
