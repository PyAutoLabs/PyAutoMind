# Phase 5a — `__JAX__` section in `autolens_workspace/scripts/guides/data_structures.py`

The first of the guide-level docs. Covers the `.array` story, how autoarray
wrappers behave under each backend, when host transfer happens, and the
"not pytree" rule with the user-facing workaround. This is where the
principle 2 (no pytree registration) and principle 5 (jnp.asarray at
boundary) explanations from `admin_jammy/notes/jax_interface.md` §3.1 land.

**Authoritative design doc:** `admin_jammy/notes/jax_interface.md`,
especially §1.1 (xp pattern), §2.4 (autoarray-not-pytree judgement), §3.5
(pytree story per audience).
**Run in Opus** per [[feedback_tutorial_prose_opus]] — guide prose,
science-teaching narrative.
**Depends on:** Phase 1 shipped (top-level start_here `__JAX__` is the
conceptual home this guide expands).

## Scope

Single file edit: `autolens_workspace/scripts/guides/data_structures.py`.

Add a substantial `__JAX__` section (~80-120 lines of prose with 2-3 short
code snippets) covering five sub-topics:

1. **What `.array` is.** Every autoarray wrapper (`Array2D`,
   `Grid2DIrregular`, `VectorYX2D`, etc.) has a `.array` property that
   returns the raw backing array. On the NumPy path it's `numpy.ndarray`;
   on the JAX path it's `jax.Array`.
2. **When the backing flips to `jax.Array`.** Three situations:
   constructed with `xp=jnp` (e.g. `aa.Grid2D.uniform(..., use_jax=True)`),
   returned from an `Analysis(use_jax=True)` fit, or returned from a
   `Simulator(use_jax=True)` simulation. The user-facing constructors stay
   the same; only the backing type changes.
3. **When host transfer happens.** Plotting (`aplt.plot_array`),
   `.fits` writing (`aplt.fits_imaging`), `.copy()`, `.tolist()`, and
   direct `np.*` arithmetic all call `np.asarray()` internally and transfer
   the array off the GPU. This is transparent for one-off analysis; matters
   for hot loops.
4. **The not-pytree rule and the workaround.** Wrapper types (`Array2D`,
   `Grid2DIrregular`) are not reliably JAX pytrees for return-from-JIT
   purposes. When the user wraps a library function in their own `@jax.jit`
   and returns one of these types, the boundary may fail. The workaround:
   `.array` unwrap inside the jit, rewrap outside.
5. **The bound-method form of `jax.jit`.** Cross-reference Phase 5d's
   `lens_calc.py` for the full "JIT-it-yourself" treatment. This guide
   gives one short example; lens_calc.py is the canonical deep-dive.

**Out of scope:**
- The advanced `xp` story (`if xp is np:` guards, etc.) — that's Phase 5d.
- Anything specific to lens modeling (tracers, deflections, magnifications)
  — that's Phase 5c (tracer.py).
- The Analysis/Simulator API contract — that's Phase 1, 3, 4.

## Proposed structure of the `__JAX__` section

Placement: after the existing autoarray-wrapper introduction in
`data_structures.py` (early in the file — the section should appear
before the more advanced sub-topics that already mention `.array`).

```python
"""
__JAX__

PyAutoLens runs on either NumPy or JAX. The data structures you've met so
far (`aa.Array2D`, `aa.Grid2D`, `aa.Grid2DIrregular`, ...) are *backend-
polymorphic* — they're Python wrappers around an underlying numerical
array, and that array can be a `numpy.ndarray` or a `jax.Array` depending
on how it was constructed and what code path produced it.

You can always reach the raw backing array via `.array`:

```python
grid = al.Grid2D.uniform(shape_native=(100, 100), pixel_scales=0.1)
grid.array         # numpy.ndarray on the default path
print(type(grid.array))   # <class 'numpy.ndarray'>
```

__When the backing becomes `jax.Array`__

Three situations switch the backing to `jax.Array`:

1. You construct with `use_jax=True`:
   ```python
   grid_jax = al.Grid2D.uniform(shape_native=(100, 100), pixel_scales=0.1, use_jax=True)
   print(type(grid_jax.array))   # <class 'jaxlib.xla_extension.ArrayImpl'>
   ```
2. The structure comes back from a JAX-accelerated `Analysis(use_jax=True)`
   fit (which is the default — see the top-level start_here `__JAX__`
   section). The `fit.residual_map.array`, `fit.model_image.array`, etc.
   are JAX-backed.
3. The structure comes back from a `Simulator(use_jax=True)` simulation
   (see the per-dataset `simulator.py` `__JAX Variant__` sections).

In all three cases, the *Python-level wrapper* is the same `aa.Array2D` /
`aa.Grid2D` / etc. you've been using. Only the underlying array type
changes. This is the whole point — workspace code reads the same on either
backend.

__Host transfer (the JAX → NumPy boundary)__

Many things you do with these structures automatically convert back to
NumPy on the host:

- Plotting (`aplt.plot_array`, `aplt.subplot_fit`, ...) — calls
  `np.asarray(...)` internally.
- `.fits` writing (`aplt.fits_imaging`).
- `.copy()`, `.tolist()`.
- Direct NumPy arithmetic: `np.sqrt(fit.residual_map.array)` transfers the
  array off the GPU to evaluate. Use `jnp.sqrt(...)` instead if you want
  to stay on the GPU.

For one-off analysis code (notebook exploration, single-image visualization),
the transfer is invisible. For hot loops or production fits, prefer the
JAX-native call where applicable.

__The not-pytree rule__

There's one place the abstraction does leak: if you write your own JAX-jit
function and try to return an `aa.Array2D` (or `aa.Grid2DIrregular`) from
inside it, the JIT boundary may fail with `TypeError: ... is not a valid
JAX type`. The wrapper types are not reliably registered as JAX pytrees
for return-from-JIT purposes.

The workaround: return the raw `.array` from inside the jit and rewrap
outside:

```python
@jax.jit
def my_image_fn(tracer, grid):
    return tracer.image_2d_from(grid=grid, xp=jnp).array   # raw jax.Array

arr = my_image_fn(tracer, grid)
img_wrapped = al.Array2D(values=arr, mask=grid.mask)   # rewrap on the host
```

You only encounter this when *you* write the `@jax.jit` — the library
handles its own returns correctly (`AnalysisImaging(use_jax=True)` returns
proper `FitImaging` objects; `SimulatorImaging(use_jax=True)` returns
proper `Imaging` objects).

For the full deep-dive on writing your own JAX-jit functions that compose
PyAutoLens library calls — including `jax.jit(method)` vs decorator-on-def,
cache-identity considerations, and the closure-captured `self` vs
traced-argument distinction — see `scripts/guides/lens_calc.py`'s `__JAX__`
section. That's the canonical home for the "JIT-it-yourself" advanced path.

__Summary__

| You construct / receive | Backing type |
|---|---|
| `aa.Grid2D.uniform(shape_native, pixel_scales)` | `numpy.ndarray` |
| `aa.Grid2D.uniform(shape_native, pixel_scales, use_jax=True)` | `jax.Array` |
| `fit = analysis.fit_from(instance)` from `AnalysisImaging(use_jax=True)` | `jax.Array` |
| `dataset = simulator.via_tracer_from(...)` from `SimulatorImaging(use_jax=True)` | `jax.Array` |

In all cases, `.array` is the safe accessor for the raw backing. Plotting
and `.fits` writers handle the conversion to NumPy transparently.
"""
```

## Validation

1. The guide runs end-to-end on NumPy.
2. The one JAX code example in the section runs (requires Phase 2 shipped
   for `use_jax=True` constructor flag on Grid2D, OR adjust the example
   to use `aa.Grid2D.uniform(...)` and then explicitly construct
   `aa.Grid2D(values=jnp.array(grid.array), ...)` if Phase 2 hasn't
   landed Grid2D.use_jax — though Grid2D auto-self-registers on jnp
   construction so should work).
3. `scripts/check_sizes.sh` passes (grew, not shrunk).
4. Cross-reference to Phase 5d's `lens_calc.py` resolves correctly once
   Phase 5d ships.

## References

- Phase 0 design doc: `admin_jammy/notes/jax_interface.md` §1.1, §2.4, §3.5.
- Phase 1: `PyAutoPrompt/workspaces/jax_start_here_intros.md` —
  conceptual home; this guide expands the "what JAX changes for users"
  story.
- Phase 5d (cross-reference target): `autolens_workspace/jax_docs_guide_lens_calc.md`.
- Phase 5e (mirror for autogalaxy): `autogalaxy_workspace/jax_docs_guides.md`.

## Out-of-band notes

- The `.array` accessor is the canonical pattern per
  `PyAutoArray/CLAUDE.md` "Decorator System" section. Cite that idiom
  consistently — `grid.array[:, 0]` over `grid[:, 0]`.
