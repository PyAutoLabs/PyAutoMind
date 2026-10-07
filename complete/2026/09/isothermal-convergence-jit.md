## isothermal-convergence-jit
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/632
- completed: 2026-09-27
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/633
- merged: 152695e0 (single commit 3ac1ec1f); CI green on all 4 legs; Heart freeze not frozen
- summary: `PowerLawCore.convergence_2d_from` (power_law_core.py) called `convergence_func(grid_radius=...)` without `xp`, so the default `np` hit `Isothermal.axis_ratio` with a JAX tracer (`TracerArrayConversionError` under `jax.jit`). It was the only `convergence_func(...)` call site omitting `xp`; the fix passes `xp=xp`, repairing PowerLaw, PowerLawIntermediate, IsothermalCore and other subclasses too.
- test: jax-free spy-`xp` regression in `test_autogalaxy/profiles/mass/total/test_isothermal.py` asserting `convergence_func` receives the caller's `xp`; red on unfixed main, green after. Scratch jit witness: jit output equals NumPy output.
- workspace impact: none (API Changes: None).
- origin: carried from point-source-source-plane-p2c `carried:` intake list (the phase 2b bug).

## Original prompt

# Isothermal.convergence_2d_from not jit-traceable (PowerLawCore drops xp)

Type: bug
Target: @PyAutoGalaxy
Issued: 2026-09-27

## Original request (verbatim)

fix this - Isothermal.convergence_2d_from still can't be traced under jax.jit (the phase 2b bug).

Carried from the active.md row point-source-source-plane-p2c `carried:` intake list.

## Witness (reproduced 2026-09-27 on PyAutoGalaxy main)

With `ell_comps` as JAX tracers, `ag.mp.Isothermal(...).convergence_2d_from(grid, xp=jnp)`
under `jax.jit` raises `TracerArrayConversionError`.

## Root cause

`PowerLawCore.convergence_2d_from` (`autogalaxy/profiles/mass/total/power_law_core.py:111`)
calls `self.convergence_func(grid_radius=grid_eta)` without `xp`, so the default `np` is
used and `Isothermal.axis_ratio(np)` calls `np.minimum` on a tracer. The shared method means
PowerLaw, PowerLawIntermediate, IsothermalCore and other subclasses are affected too. It is
the only `convergence_func(...)` call site that omits `xp`.

## Plan

1. `power_law_core.py:111` -> `return self.convergence_func(grid_radius=grid_eta, xp=xp)`.
2. jax-free regression test in `test_autogalaxy/profiles/mass/total/test_isothermal.py`:
   call `convergence_2d_from` with a numpy-delegating spy `xp` module and assert
   `convergence_func` receives that same `xp`. Red on unfixed main, then green.
3. Scratch jit witness: jit output equals NumPy output.
