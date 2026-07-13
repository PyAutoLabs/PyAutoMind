## nfw-jax-port
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/397
- completed: 2026-05-14
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/402
- repos: PyAutoGalaxy
- notes: |
    Phase 1 feasibility study for replacing the jax.pure_callback wrapping
    colossus.halo.concentration in autogalaxy/profiles/mass/dark/mcr_util.py.

    Verdict: Approach A (full JAX port of modelLudlow16 including the
    Eisenstein-Hu '98 transfer + Heath '77 growth factor + Einasto
    gammainc mass ratio + 200-point c-solver) is viable. ~330 lines of
    straight-line JAX. Max c200c rel error vs colossus = 7.5e-4 across the
    lensing parameter grid (log M ∈ [10, 14] Msun/h, z ∈ [0.1, 2.5]).
    Single-call post-JIT 0.69 ms (vs colossus 0.83 ms). vmap × 32 is
    1.29× faster than colossus serial. jax.grad agrees with finite-diff
    to 7e-4.

    Science-impact validation (science_check.py): end-to-end propagation
    through NFWMCRScatterLudlow and cNFWMCRScatterLudlow gives
    kappa_s max rel error 1.07e-3, NFW κ/α per-pixel max 8.21e-4, cNFW
    α per-pixel max 7.60e-4. Intrinsic Ludlow16 scatter is ~350× larger
    than the JAX-vs-colossus offset — scientifically invisible.

    All deliverables under docs/research/nfw_ludlow16_jax/:
      - nfw_ludlow16_jax_assessment.md (the report)
      - ludlow16_jax.py (the prototype)
      - validate.py, bench.py, tune.py, science_check.py

    No production code changed in this issue/PR. Phase 2 follow-up issue
    (to be filed) will swap the prototype into mcr_util.py, collapse the
    xp-branching in the two callers, and make colossus an optional dep.

    Known issue surfaced in cNFW science check (not blocking): the
    Penarrubia mcr formula goes negative for f_c=0.20, producing a
    negative kappa_s (pre-existing, unrelated to this work). Also
    cNFWSph.convergence_2d_from returns zeros — "not yet implemented"
    in PyAutoGalaxy.
