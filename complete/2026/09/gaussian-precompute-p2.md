## gaussian-precompute-p2
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/604 (closed, completed)
- completed: 2026-09-03
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/520 (MERGED e36a5af4c)
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/605 (MERGED 65af11227)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/216 (MERGED 991b4da26)
- epic: gaussian-deflections-precompute — phase 2 of 3, **epic stays open** (ledger
  draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md)
- shipped: the **JAX branch** of the fixed-geometry deflection memo — the memoised field becomes a
  **trace-time constant** instead of a staged computation. Two halves:
  **PyAutoArray** — `Grid2D.subtracted_and_rotated_from` now runs under `jax.ensure_compile_time_eval()`
  when the offset and rotation angle are concrete, so the grid arrives at the profiles as a concrete
  array rather than a tracer.
  **PyAutoGalaxy** — the memo grew a JAX branch: `_is_concrete_array` (a `jax.Array` that is not a
  `Tracer`, resolved through `sys.modules` so nothing imports jax eagerly), a **numpy twin grid**,
  numpy/scipy evaluation **at trace time**, `ratio * xp.asarray(field)` for the L2 rescale, and a
  `jax_folds` counter. Anything traced falls straight through to the direct call.
- measured: SLaM-shaped hst fit, `jit(vmap)`, batch 3 —
  `_wofz` compile-call counts **numpy 180 / jnp 0** with the memo on, against **0 / 240** with it off;
  steady state **0 / 0** either way. `jax_folds` **90**. jaxpr **53,369 → 13,289 equations (−75%)**.
  Log-likelihood agreement **8.6e-15** relative. `vmap_first_call` **10.8 → 5.4 s (2.0x**; 1.64x on the
  second run). `vmap_steady_x10` **UNCHANGED at 2.5–2.6 s**.
- honest-negative: the steady-state `vmap` leg does **not** move. It is inversion-dominated, so folding
  the deflections out of the trace buys compile time and nothing else there. Recorded as measured rather
  than framed as a win — phase 3's downstream sweep is where the remaining cost lives.
- controls: kill switch = memo-off; a **free `grid_offset`** traces the grid, takes the direct path, and
  reports `jax_folds` **0**. autolens_workspace_test imaging/jax_likelihood **15/15 before and after**,
  vmap pins **bit-identical**. `mge.py` and `delaunay.py` `jit(fit_from)` legs became **more** accurate
  against their numpy references (**4.5e-5 → 1e-16**) — the trace-time numpy evaluation *is* the reference.
  test_autoarray **1412**, test_autogalaxy **1181**; deflection pins held.
- finding: the plan's premise — "the grid is already concrete under `jit`" — was **false**, and that is
  why this phase grew a PyAutoArray half it was not scoped for. `jit` stages every `jnp` op, and
  `autonerves/jax_wrapper.py` disables XLA constant folding, so concrete offset/angle still produced a
  traced grid. A phase plan that asserts a runtime property should measure it before scoping around it.
- finding: `worktree_check_conflict` raised a **false positive** on this task — it matched the `heart-ack`
  sub-bullets in `active.md`. The rows have since been reformatted; the guard itself was not changed.
- finding: a `DatasetModel` carrying a **free `grid_offset`** cannot round-trip
  `autofit.jax.register_model` — `Prior.tree_unflatten` raises `TypeError`. Filed as
  draft/bug/autofit/dataset_model_free_grid_offset_pytree_roundtrip.md.
- heart: RED at PR-open, human-acknowledged for PR-open only — three reasons: "release validation FAILED
  (stage integrate)", "PyAutoArray: open PR 11d old", "PyAutoLens: CI failure". The third was repaired by
  the sibling task `positions-threshold-repin` (PyAutoLens#722) earlier the same day; none touches this diff.
- session: local CLI; merged and closed out via /prm 2026-09-03, in the order
  PyAutoArray#520 → PyAutoGalaxy#605 → autolens_profiling#216. PyAutoArray and PyAutoGalaxy are
  pending-release.
- epic next: phase 3 — the downstream sweep,
  draft/feature/autogalaxy/gaussian_precompute_p3_downstream_sweep.md.
- affected-repos:
  - PyAutoArray
  - PyAutoGalaxy
  - autolens_profiling

## Original prompt

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
Status: active
Filed: 2026-09-03
Issued: 2026-09-03
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
