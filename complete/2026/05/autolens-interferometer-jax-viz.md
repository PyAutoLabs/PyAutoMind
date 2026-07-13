## autolens-interferometer-jax-viz
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/86
- completed: 2026-05-08
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/500
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/87
- repos: PyAutoLens, autolens_workspace_test
- notes: |
    Phase 1A of z_features/jax_visualization.md shipped end-to-end as a
    "Both" task (started workspace-only, reclassified mid-session when a
    missing **kwargs passthrough in al.AnalysisInterferometer.__init__
    was discovered).

    Library PR #500 (PyAutoLens): added **kwargs to
    AnalysisInterferometer.__init__ and forwarded to super(). 2-line
    change. ag.AnalysisImaging had the passthrough all along; the
    AnalysisDataset parent already accepts **kwargs. PyAutoLens 116/116
    tests pass.

    Workspace PR #87 (autolens_workspace_test): added
    scripts/interferometer/visualization_jax.py and
    scripts/interferometer/modeling_visualization_jit.py mirroring the
    imaging analogues. Split env_vars.yaml `imaging/visualization`
    pattern into NumPy-only + JAX-only entries; added
    `interferometer/modeling_visualization_jit` override.

    Discovered + fixed: modeling_visualization_jit.py Part 2 has a brittle
    assertion `_jitted_fit_from is not None` that only fires if Nautilus
    actually does live sampling. If output/<path>/ already has cached
    samples.csv from a prior run, Nautilus resumes and skips, so the JIT
    wrapper is never installed and the assertion AttributeErrors. Fix:
    explicit rmtree of the autofit search output directory before the
    Nautilus call. The imaging analogue
    (autolens_workspace_test/scripts/imaging/modeling_visualization_jit.py)
    has the same brittleness — worth a tiny follow-up backport.

    Follow-ups deferred:
    - al.AnalysisPoint.__init__ has the same **kwargs gap. Phase 1B of
      the roadmap will need it.
    - ag.AnalysisInterferometer.__init__ has the same gap. Phase 1C
      will need it.
    - Backport the rmtree fix to imaging/modeling_visualization_jit.py.
    - sma.fits is gitignored — CI runs depending on it stay red on main.
