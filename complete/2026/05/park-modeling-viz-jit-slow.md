## park-modeling-viz-jit-slow
- completed: 2026-05-07
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/76
- followup-issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/77
- repos: autolens_workspace_test
- notes: |
    Cluster D of the recent release-prep triage. Three autolens
    workspace_test imaging scripts (modeling_visualization_jit,
    modeling_visualization_jit_delaunay, modeling_visualization_jit_rectangular)
    timed out at the 300s per-script cap. NOT a regression — PR #70
    (fix(env): unblock modeling_visualization_jit tests in CI defaults)
    cleared the prior `AssertionError: expected jax.Array, got numpy.float64`
    that had masked this perf issue. Autogalaxy sibling passes in ~88.6s;
    autolens variants are ~3.5x slower (>300s) — JIT compile + full
    visualization. Parked via standard `# SLOW <YYYY-MM-DD>` convention
    in autolens_workspace_test/config/build/no_run.yaml. Mega-runs
    surface SLOW entries with a loud warning banner so they don't
    silently rot. Follow-up perf issue #77 filed against
    autolens_workspace_test capturing the 3.5x disparity, investigation
    pointers (Tracer vs Galaxy, pixelization variants, JAX visualization
    pipeline) and acceptance criteria for removing the SLOW markers.
