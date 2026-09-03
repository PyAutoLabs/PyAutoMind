# Gaussian precompute phase 2: JAX trace-time constant — fold the fixed-geometry deflection field out of the jaxpr

Type: feature
Epic: gaussian-deflections-precompute
Phase: 2
Target: autogalaxy
Repos:
- @PyAutoGalaxy
- @autolens_profiling
- @autolens_workspace_test
Themes:
- numba-cpu
- mass-profiles
- jax
- profiling
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-09-03
Parent: draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md

> Phase 2 of the `gaussian-deflections-precompute` epic — ledger
> `draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md`. Successor work to the
> completed `numpy-deflections-cpu` epic (`complete/archive/epics/numpy_deflections_cpu_speedup.md`).
> **Phase 1 is a hard predecessor and is SHIPPED** (2026-09-03, record
> `complete/2026/09/gaussian-precompute-p1.md`; PyAutoGalaxy#602 + autolens_profiling#214): it landed
> `deflections_memo.py`, the content-keyed grid fingerprint with its weakref cache, the L1/L2 levels
> and the `Galaxy` / `Basis` summation-site hooks that this phase extends. This is the "JAX doesn't use this so would help there" half of the user's idea.

## Goal

Under JAX the fixed Gaussian geometry is **concrete** and only `mass_to_light_ratio` is a tracer, so the
whole Faddeeva subgraph is a constant that JAX nonetheless re-traces and re-executes. Compute the
unit-ratio field **at trace time with numpy** (scipy `wofz`, exact) and embed it as a constant: the
Faddeeva subgraph leaves the jaxpr entirely and the JAX path inherits scipy accuracy for fixed geometry.

## Steps

1. **Concrete-value test** in `deflections_memo.py`: a value is concrete when
   `type(value).__module__.startswith(("numpy", "jax", "jaxlib"))` — the same tracer-detection precedent
   used, without importing jax, by `autogalaxy/jax/registration.py:93-108` (`_is_builtin`). Fixed
   parameters reach the instance as plain Python floats/tuples and free ones as tracers
   (`PyAutoFit/autofit/mapper/prior_model/prior_model.py:495-530`; `Constant` subclasses `float`;
   `fitness.py:727-731` closes over the model and `vmap`s only the parameter vector). The instance carries
   no free/fixed record — the **values** do.
2. **JAX branch of the memo**: when `xp` is JAX, the grid is concrete and every geometry value is concrete
   while `m2l` is a tracer, evaluate the unit field with numpy/scipy and return `m2l * jnp.asarray(field)`.
   If **anything** in the key is a tracer, fall through unchanged — no data-dependent branching on a traced
   value anywhere.
3. Recompilation happens only when the embedded constant changes (a new model is a new fit anyway); state
   this in the module docstring beside the numpy contract.
4. **autolens_profiling**: JAX before/after in the phase-1 profiling cell (`--xp jax` if `_driver.py` has
   it, else a sibling script under `scripts/lens/deflections/`), recorded in
   `results/notes/numpy_deflections_cpu.md`.

## Verification

- Validation is `jax.vmap` over the free ratio — **never jit-on-concrete**, which would fake the win by
  constant-folding a fixed-value trace.
- A jaxpr check that **no `wofz` ops remain** in the traced graph for a fixed-geometry Gaussian / MGE stack.
- `test_autogalaxy` green under both backends; `ruff check` + `ruff format --check` clean.
- `autolens_workspace_test` JAX likelihood pins for a fixed-MGE lens must hold. They are exact-arithmetic
  identical except for the scipy-vs-rational Faddeeva difference (≤ 4e-6) — **report any shift, do not edit
  the pins** in this phase.
- Deflection pins in `scripts/lens/deflections/` unchanged at rtol 1e-6, numpy and JAX.

## Ship

Library-first: PyAutoGalaxy PR → autolens_profiling PR. `autolens_workspace_test` is read/reported only —
no edit expected; if a pin genuinely must move, that is a separate filed finding.

## Out of scope

The numpy memo itself (phase 1); the downstream sweep (phase 3); editing JAX likelihood pins; the JAX
20-term omega default or any other JAX numerics decision; `convergence_2d_from` / `potential_2d_from`.
