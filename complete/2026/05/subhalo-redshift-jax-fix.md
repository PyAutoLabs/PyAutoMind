## subhalo-redshift-jax-fix
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/498
- completed: 2026-05-08
- repro-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/79 (merged d827d1c — Phase 1)
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/499 (merged b790632 — Phase 2)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/81 (merged 61b0b4f — Phase 2b)
- repos: PyAutoLens, autolens_workspace_test
- notes: |
    Slack bug report from @qiuhan96 (working with an undergraduate at
    Groningen). Free-parameter subhalo redshift (af.UniformPrior on
    Galaxy.redshift) raised jax.errors.TracerBoolConversionError under
    jax.jit. Root cause: tracer_util.plane_redshifts_from /
    planes_from / grid_2d_at_redshift_from + Tracer.galaxies_ascending_
    redshift all called Python sorted(galaxies, key=lambda g: g.redshift)
    on a list whose subhalo redshift was a traced scalar; pairwise '<'
    comparisons cannot lift to traced ops.

    Three-phase ship in a single session:

    Phase 1 — Filed the issue, then landed a clean integration-test
    reproducer (PR #79) in autolens_workspace_test as scripts/jax_
    likelihood_functions/imaging/subhalo.py. Two scenarios: fixed
    z=0.55 PASS, free UniformPrior FAIL with the expected
    TracerBoolConversionError. Used to drive the fix and as the
    eventual regression check.

    Phase 2 — Library fix (PR #499). Each of the four buggy functions
    got a JAX-aware fast-path guard: when no galaxy redshift is
    traced, behaviour is byte-for-byte identical to before; when any
    redshift is traced, the function partitions concrete vs traced,
    sorts the concrete ones with normal Python sort, and trusts input
    galaxy order for the traced ones. grid_2d_at_redshift_from
    matches the requested redshift to a galaxy by Python identity
    (its only call site, AnalysisLens.tracer_via_instance_from,
    always passes the subhalo's own redshift object). 273/273 unit
    tests pass; full smoke suite for autolens_workspace_test (11/11)
    pass with the patched library on PYTHONPATH.

    Phase 2b — Polarity-flip workspace PR (#81). The same subhalo.py
    script was converted to the regression check: both scenarios
    must now PASS, with np.testing.assert_allclose locking the vmap
    output to -1.412105e+09 (rtol=1e-4) and the JIT log_likelihood
    matching the NumPy path within rtol=1e-4.

    Notes for future:
    - The cosmology distance functions (Planck15) accepted traced
      redshifts without modification, so no JAX-friendly cosmology
      shim was needed. If a different cosmology turns out to fail,
      that's a follow-up issue.
    - The tuple(subhalo_centre.in_list[0]) round-trip in
      analysis/lens.py:116 was a suspected breakage site but turns
      out to work fine under JIT — tuple((traced_y, traced_x))
      preserves traced scalars.
    - The JAX path trusts input galaxy order; if a user puts the
      subhalo before the lens in declaration order with a redshift
      between them, the multi-plane scaling factors will be wrong.
      Documented in the PR body's Migration section but not enforced
      at runtime (would require a non-JAX validation pass).
    - The "user-helping" tone established mid-session (4 conversational
      issue updates across 5 milestones) seemed to land well — keep
      that pattern for future user-reported bug reports.
