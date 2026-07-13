## ag-interferometer-jax-viz
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/43
- completed: 2026-05-14
- workspace-pr:
  - https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/44 (3 new scripts + env_vars)
  - https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/45 (cleanup — .gitignore + leaked binaries)
- repos: autogalaxy_workspace_test
- notes: |
    Phase 1C of jax_visualization roadmap. Scope narrowed mid-task to
    interferometer only — ellipse + quantity JAX coverage deferred to a
    follow-up after the Phase 0c-discovered visualizer-dispatch fixes
    ship. Workspace-only PR — all library prereqs (PRs #390, #399, #376,
    #401) already merged.

    Workspace scope shipped in #44:
    - scripts/interferometer/visualization.py (NEW) — NumPy baseline
    - scripts/interferometer/visualization_jax.py (NEW) — JAX viz with
      enable_pytrees() + register_model(model) + no try/except
    - scripts/interferometer/modeling_visualization_jit.py (NEW) —
      caching probe + live Nautilus with linear MGE basis, includes
      explicit rmtree(output/<path>/<name>/) before Nautilus (PR #87
      lesson)
    - config/build/env_vars.yaml — interferometer/visualization_jax +
      interferometer/modeling_visualization_jit overrides

    Cleanup shipped in #45 (same-session immediate follow-up):
    - .gitignore upgraded from per-type entries
      (scripts/imaging/images/, scripts/ellipse/images/) to the
      autolens_workspace_test-style **/images/ glob — covers all
      current and future dataset types
    - git rm'd 6 binary artifacts (3 PNG + 3 FITS, ~10 MB) that #44
      had leaked because the per-type gitignore didn't cover the new
      scripts/interferometer/images/ directory

    Lesson saved to memory (feedback_ship_workspace_binary_leak.md):
    when /ship_workspace introduces a NEW scripts/<type>/ subdirectory,
    pre-flight check `.gitignore` covers it or upgrade to **/images/
    before commit.

    Deferred follow-ups (unchanged from Phase 0c notes):
    - Quantity visualizer dispatch swap (small) — adds fit_from alias
      on AnalysisQuantity. Once shipped, a small follow-up workspace_test
      PR can add the quantity script triplet.
    - Ellipse visualizer dispatch swap (needs design) — fit_list_from
      returns List[FitEllipse], needs autofit fit_for_visualization
      contract generalization or list-to-single wrapper.
