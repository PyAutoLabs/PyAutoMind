## mesh-geometry-picklable
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/320
- completed: 2026-05-16
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/321
- parent-issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1279 (Phase 4 feasibility — Q2 carve-out)
- repos: PyAutoArray
- notes: |
    Q2 of the Phase 4 subprocess-visualization feasibility (#1279).
    AbstractMeshGeometry stored `self._xp = xp` (a module reference),
    making FitImaging unpicklable. Replaced with `self._use_jax: bool`
    + `_xp` as a property — same pattern as Analysis._xp (PyAutoFit)
    and AbstractMaker._xp (PyAutoArray decorators). One class change,
    one new test file (5 new tests covering numpy + JAX backends across
    Rectangular + Delaunay geometries). 171 inversion tests still pass.

    End-to-end verified: a populated FitImaging round-trips through
    pickle.dumps/loads with log_likelihood Δ=0.00e+00 on both backends.
    Pickle size ~4.6 MB for a Rectangular-adaptive-density pixelization
    fit. Strong positive signal for Q1 (IPC choice) — mp.Process+Queue
    and ProcessPoolExecutor are both viable; no need to fall back to
    "send raw arrays + reconstruct in worker".

    Spike scripts (picklability_spike.py, picklability_spike_jax.py)
    and q2_findings.md remain in ~/Code/PyAutoLabs-wt/viz-subprocess-
    feasibility/ as in-progress notes for Q1/Q3/Q4 work. The parent
    viz-subprocess-feasibility task stays in active.md.

    File-disjoint coexistence with knn-barycentric (#317) on PyAutoArray
    worked cleanly (different files under inversion/mesh/).
