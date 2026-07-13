## point-source-jax-viz
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/90
- completed: 2026-05-08
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/506
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/91
- repos: PyAutoLens, autolens_workspace_test
- notes: |
    Phase 1B of z_features/jax_visualization.md shipped end-to-end as a
    "Both" task — known up front (unlike Phase 1A which was discovered
    mid-session).

    Library PR #506 (PyAutoLens): added **kwargs to
    AnalysisPoint.__init__ + forwarded to super(). 2-line change
    mirroring PR #500's AnalysisInterferometer fix. 76/76 tests pass
    (test_autolens/point + test_autolens/analysis).

    Workspace PR #91 (autolens_workspace_test): three new scripts —
    scripts/point_source/visualization.py (NumPy baseline),
    scripts/point_source/visualization_jax.py (JAX path), and
    scripts/point_source/modeling_visualization_jit.py (caching probe +
    live Nautilus). Closes the autolens point_source gap (was the only
    autolens dataset type with zero visualization coverage). Plus two
    env_vars.yaml overrides (point_source/visualization_jax,
    point_source/modeling_visualization_jit) mirroring the imaging
    + interferometer analogues.

    Design choices forced by JIT constraints:
    - Image-plane chi-squared (FitPositionsImagePairAll) only — source-
      plane (FitPositionsSource) is still JIT-blocked per
      scripts/CLAUDE.md L132.
    - No free cosmology parameter in the model — cosmology distance
      calc caches global state and breaks JIT round-trip (per the
      existing jax_likelihood_functions/point_source/image_plane.py
      L144-147 caveat). The model is af.Collection(galaxies=...) only.
    - modeling_visualization_jit.py includes explicit rmtree of both
      scripts/point_source/images/modeling_visualization_jit/ AND
      output/scripts/point_source/images/modeling_visualization_jit/
      point_image_plane/ before Nautilus, so reruns force a fresh
      sampling pass and _jitted_fit_from gets populated (lesson from
      PR #87).

    JAX visualization roadmap **kwargs gap status:
    - al.AnalysisImaging: always had **kwargs ✓
    - al.AnalysisInterferometer: fixed in PR #500 ✓
    - al.AnalysisPoint: fixed in PR #506 ✓ (this task)
    - ag.AnalysisInterferometer: still has the gap — Phase 1C will fix.
    - ag.AnalysisImaging: always had **kwargs ✓

    Follow-ups:
    - Source-plane chi-squared visualization (FitPositionsSource) — gated
      behind the existing CLAUDE.md L132 JIT blocker. Defer until that
      lifts.
    - Backport the rmtree(output/<path>/<name>/) fix to
      scripts/imaging/modeling_visualization_jit.py and its delaunay /
      rectangular variants — they have the same brittleness on reruns.
