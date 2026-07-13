## ludlow16-jax-native
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/403
- completed: 2026-05-14
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/406
- repos: PyAutoGalaxy
- notes: |
    Phase 2 of the Ludlow16 JAX-native work (Phase 1 was #397 / PR #402).
    The colossus jax.pure_callback in mcr_util.py is GONE from production.

    What landed:
    - New autogalaxy/profiles/mass/dark/ludlow16.py — JAX-native port of
      colossus.halo.concentration.modelLudlow16 (~400 lines, xp-aware).
      EH98 transfer + Heath '77 growth factor + Einasto gammainc +
      200-point Ludlow c-solver.
    - mcr_util.py rewritten: replaced _ludlow16_cosmology_callback and
      ludlow16_cosmology_jax with a single xp-aware ludlow16_cosmology(...).
      The if-xp-is-np branching in kappa_s_and_scale_radius_for_ludlow and
      kappa_s_scale_radius_and_core_radius_for_ludlow collapsed to single
      xp-aware calls.
    - colossus moved from required runtime dep to test/dev extras in
      pyproject.toml. Production no longer imports colossus.
    - 10 new tests in test_autogalaxy/profiles/mass/dark/test_ludlow16.py
      (numpy-path cross-check vs colossus, skipped if colossus unavailable).
    - Test tolerances loosened from 1e-4 → 1e-3 (still 0.1%) in 4 NFW-MCR
      test files. Justified: the old 1e-4 implicitly claimed colossus-level
      precision; JAX impl differs from colossus by ~2e-4 (sub-Ludlow-scatter).
    - Bug fix during CI debug: replaced xp.trapezoid with a manual
      _trapezoid_last_axis helper for numpy<1.26 compat (CI's Python 3.12
      runs older numpy than the local dev venv).

    Cross-implementation verification: autolens_workspace_test/subhalo.py
    (Scenarios C and D, regression literals locked in via workspace_test
    PR #92 from the colossus path) produces vmap = -1.349200e+09 — exact
    match to rtol=1e-4. The JAX-native code reproduces the colossus
    pure_callback's downstream log-likelihood at the precision we care
    about.

    Production grep confirms: no import colossus, no jax.pure_callback
    anywhere in autogalaxy/. The only remaining "colossus" references are
    in docstrings explaining what the new code replaced.
