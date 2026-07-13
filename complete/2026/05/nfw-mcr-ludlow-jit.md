## nfw-mcr-ludlow-jit
- issue: none — extension of the subhalo JAX regression script
- completed: 2026-05-14
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/92
- repos: autolens_workspace_test
- notes: |
    Extended scripts/jax_likelihood_functions/imaging/subhalo.py from
    two scenarios to four: kept the existing IsothermalSph + fixed/free
    subhalo-redshift pair (Scenarios A/B, regression check for PyAutoLens
    #498/PR #499) and added NFWMCRLudlowSph + fixed/free subhalo-redshift
    (Scenarios C/D, regression check for the colossus jax.pure_callback
    path in PyAutoGalaxy/autogalaxy/profiles/mass/dark/mcr_util.py).

    Refactored build_model + run_scenario to take a subhalo-mass-factory
    callable and an expected-vmap literal so each scenario is one call.

    Regression literals (vmap log-likelihood at prior medians):
      A/B (IsothermalSph)   : -1.412105e+09 (unchanged)
      C/D (NFWMCRLudlowSph) : -1.349200e+09 (new)
    Single-instance jit log-likelihood = -3.523166e+05 in all four
    scenarios and matches the numpy path to rtol=1e-4.

    Only the fitness._vmap path actually exercises the pure_callback
    inside the JAX trace — the single-instance jit(fit_from)(instance)
    path receives a pre-built ModelInstance whose kappa_s was computed
    at construction time outside the trace. C/D's vmap literal is the
    load-bearing assert and will catch any drift when the JAX-native
    Ludlow concentration of PyAutoGalaxy #403 (Phase 2) lands.

    Sundry fix during shipping: switched the canonical
    autolens_workspace_test remote from SSH (git@github.com:...) to
    HTTPS to match the convention used by every other PyAuto repo
    (only PyAutoConf still uses SSH). Was blocking gh pr create.
