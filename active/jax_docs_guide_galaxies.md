# Phase 5b — `__JAX__` section in `autolens_workspace/scripts/guides/galaxies.py`

Covers how `Galaxy` and `Galaxies` objects traverse JAX boundaries — the
implicit pytree registration done by `Analysis(use_jax=True)` and
`Simulator(use_jax=True)`, what it means to pass a `Galaxy` as a JIT
argument vs as a closure variable.

**Authoritative design doc:** `admin_jammy/notes/jax_interface.md`,
especially §1.2 (auto-registration), §3.4.1 (closure vs argument
distinction).
**Run in Opus** per [[feedback_tutorial_prose_opus]].
**Depends on:** Phase 1 shipped, Phase 5a strongly recommended (cross-refs).

## Scope

Single file: `autolens_workspace/scripts/guides/galaxies.py`.

`__JAX__` section (~60-90 lines) covering:

1. **`Galaxy` objects are JAX-traversable when registered.** The library
   registers `Galaxy` and its constituent profile classes as JAX pytrees
   automatically when the user goes through `Analysis(use_jax=True)` or
   `Simulator(use_jax=True)`. The user does NOT call
   `register_instance_pytree(Galaxy)` themselves.
2. **Without going through Analysis/Simulator first**, registration hasn't
   happened — and a user-written `@jax.jit def fn(galaxy, grid): ...`
   passing a `Galaxy` as a traced argument will fail. The fix is the
   one-liner `al.jax.enable_for_modeling()` helper (currently planned —
   see design doc §4.1) OR the easy workaround: instantiate an
   `Analysis(dataset=dummy_dataset, use_jax=True)` at the top of the script
   to trigger registration as a side effect.
3. **Closure-captured `self` doesn't need registration.** If you do
   `jax.jit(galaxy.image_2d_from)`, the `galaxy` is the bound-method's
   `self` and is closed over — JAX treats it as a constant, no pytree
   registration needed. Trade-off: you can't vary the galaxy across calls
   and still hit the JIT cache.
4. **Galaxies (the container)** behave the same way — registered when an
   Analysis/Simulator constructed with `use_jax=True` walks them.

**Out of scope:**
- Lens-equation specifics (deflection composition, ray tracing) — that's
  Phase 5c (tracer.py).
- The advanced `@jax.jit + xp=jnp` calling convention — that's Phase 5d
  (lens_calc.py).
- The `.array` host-transfer mechanics — that's Phase 5a (data_structures.py).

## Proposed structure

```python
"""
__JAX__

When you write your own `@jax.jit` around a function that takes a `Galaxy`
or `Galaxies` as an argument, JAX needs to know how to flatten and
unflatten that object across the JIT boundary (this is what JAX calls a
"pytree"). The library handles this for you automatically in two
situations:

1. You constructed an `Analysis` with `use_jax=True` (the default for
   modeling fits). `AnalysisImaging._register_fit_imaging_pytrees()` walks
   the dataset on first `fit_from` call and registers every reachable
   `Galaxy` / profile class.
2. You constructed a `Simulator` with `use_jax=True`. Same walk happens
   on first `via_tracer_from`.

In both cases, after the first call, every `Galaxy`, `LightProfile`,
`MassProfile`, `Point`, etc. of the same class is JIT-safe forever in the
current process. You never call `register_instance_pytree(Galaxy)`
yourself.

__The "I have no Analysis or Simulator handy" case__

If you're writing a quick exploration script (or a custom forward model
that doesn't go through `Simulator.via_tracer_from`), you may want to JIT
a function that takes a `Galaxy` as an argument:

```python
@jax.jit
def galaxy_image(galaxy, grid):
    return galaxy.image_2d_from(grid=grid, xp=jnp).array
```

Without prior pytree registration, this fails the first time `galaxy` is
traced. The workaround: trigger registration via a one-line setup at the
top of your script. Two equivalent ways:

```python
# Option (a): Reach for an Analysis instance — its first construction
# triggers the registration walk on the (possibly dummy) dataset.
_ = al.AnalysisImaging(dataset=dataset, use_jax=True)

# Option (b): Use the dedicated helper (planned — see Phase 0 design doc
# open question §4.1; this may not yet exist).
al.jax.enable_for_modeling()
```

After either, `galaxy_image` JITs cleanly.

__Closure-captured galaxy: registration not needed__

There's a way to JIT a galaxy-method call that *doesn't* need pytree
registration: pass the galaxy as the bound method's `self`, not as an
argument.

```python
jitted_image = jax.jit(galaxy.image_2d_from)   # bound method; assign ONCE
arr = jitted_image(grid=grid, xp=jnp).array
```

`galaxy` here is closed over inside the bound method object; JAX treats
it as a closure constant, doesn't trace through it, and the pytree
registration question never comes up.

Trade-off: you can't vary `galaxy` across calls and still hit the
compilation cache. If you want to evaluate the same function for many
different galaxies (parameter sweep), the argument form (with prior
registration) is the right choice.

__Galaxies (the container)__

`Galaxies` — and `Tracer`, which is built from them in PyAutoLens — go
through the same registration path. `Analysis(use_jax=True)` or
`Simulator(use_jax=True)` walks them and registers each Galaxy class once.

For the full deep-dive on the bound-method-vs-argument trade-off, cache-
identity footguns, and the `@jax.jit + xp=jnp` pairing rule, see the
`__JAX__` section of `scripts/guides/lens_calc.py`. The `.array` host-
transfer behavior is covered in `scripts/guides/data_structures.py`.
"""
```

## Validation

Standard. Verify cross-references to Phase 5a and Phase 5d resolve.

## References

- Phase 0 design doc, §1.2 (auto-registration mechanism), §3.4.1 (closure
  vs argument), §4.1 (open question on `al.jax.enable_for_modeling()`).
- Phase 5a: cross-referenced for `.array` host-transfer.
- Phase 5d: cross-referenced for the JIT-it-yourself advanced patterns.
- Phase 5e (mirror): `autogalaxy_workspace/jax_docs_guides.md`.
