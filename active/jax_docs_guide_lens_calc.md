# Phase 5d — `__JAX__` section in `autolens_workspace/scripts/guides/lens_calc.py`

**The canonical home for the "JIT-it-yourself" advanced path.** This is the
most detailed of the Phase 5 guides — it covers the `@jax.jit + xp=jnp`
calling convention, decorator-on-def vs `jax.jit(bound_method)`, cache-
identity footguns, closure-captured `self` vs traced-argument tracer, and
the `LensCalc.magnification_2d_via_hessian_from` etc. methods that surface
the `if xp is np:` guard.

**Authoritative design doc:** `admin_jammy/notes/jax_interface.md`,
especially §2.1 (xp judgement), §3.4.1 (canonical JIT-it-yourself
patterns), §4.8 (proposed mismatch error).
**Run in Opus** per [[feedback_tutorial_prose_opus]] — advanced guide
prose, requires precision.
**Depends on:** Phase 1, 5a, 5b, 5c shipped (cross-references).

## Scope

Single file: `autolens_workspace/scripts/guides/lens_calc.py`.

`__JAX__` section (~120-160 lines — this is the longest Phase 5 section)
covering:

1. **The audience.** This guide is for users building custom forward
   models or scientific tools using PyAutoLens primitives. Users running
   standard fits and simulations don't read this — they use the
   `Analysis` / `Simulator` paths covered in start_here and the per-dataset
   docs.
2. **The `@jax.jit + xp=jnp` pairing rule.** When you write your own
   `@jax.jit` around a library method like `tracer.image_2d_from`,
   `LensCalc.magnification_2d_via_hessian_from`, or
   `light_profile.image_2d_from`, you must pass `xp=jnp` inside the
   function body. The two go together as one unit of opt-in.
3. **The footgun: forgetting `xp=jnp` inside `@jax.jit`.** Two failure
   modes: silent host transfer (slow) or boundary error (loud). The
   library raises a clear `ValueError` on the easy mismatch (Phase 2 §4.8).
4. **Decorator-on-def vs `jax.jit(bound_method)`.** Both work. Decorator-
   on-def is the canonical example for parameter sweeps and named
   functions. `jax.jit(bound_method)` is fine for one-offs *if you
   assign-to-variable once*. The cache-identity footgun: re-creating the
   bound method on every iteration misses the JIT cache.
5. **Closure-captured `self` vs traced-argument.** The semantic difference
   between `jax.jit(tracer.image_2d_from)` (tracer is closure-captured;
   doesn't need pytree registration) and `@jax.jit def fn(tracer, grid):
   ...` (tracer is traced argument; needs pytree registration). Pick
   deliberately based on whether you want to vary the tracer across calls.
6. **`LensCalc` and the `if xp is np:` guard.** Methods like
   `magnification_2d_via_hessian_from` return wrapped `aa.Array2D` on the
   NumPy path and raw `jax.Array` on the JAX path. Document why (the guard
   pattern), and what that means for the user's downstream code.
7. **The `.array` unwrap-rewrap discipline at the JIT boundary.**

**Out of scope:**
- The `.array` host-transfer mechanics (covered in Phase 5a).
- The Galaxy/Tracer registration story at a high level (Phase 5b/5c).
- Gradients (explicitly deferred per the z_features tracker).

## Proposed structure

```python
"""
__JAX__

This guide's audience is users building **custom forward models** or
scientific tools using PyAutoLens primitives directly — not running
standard fits (which go through `Analysis(use_jax=True)` and need no
JAX-specific code from you) or standard simulations (which use
`Simulator(use_jax=True)` similarly).

If you're writing `@jax.jit` yourself around library calls like
`tracer.image_2d_from`, `LensCalc.magnification_2d_via_hessian_from`, or
your own `log_likelihood(instance)` function, this section is for you.

__The pairing rule: `@jax.jit` + `xp=jnp`__

The single rule to remember: when you decorate a function with `@jax.jit`
that calls a PyAutoLens library method internally, **pass `xp=jnp` to that
method inside the function body**.

```python
import jax
import jax.numpy as jnp

@jax.jit
def magnification_fn(lens_calc, grid):
    return lens_calc.magnification_2d_via_hessian_from(grid=grid, xp=jnp)
```

The `xp=jnp` is what tells the library "you're inside a JAX trace; route
calls through `jax.numpy` instead of `numpy` and don't wrap the return in
an autoarray type (it would fail to cross the JIT boundary)".

__The footgun: forgetting `xp=jnp`__

The default for `xp` in library method signatures is `np`. If you forget
to pass `xp=jnp` inside `@jax.jit`, one of two things happens:

- The function body does `np.sqrt(jax_array)` — NumPy routes through
  `__array__()` on the JAX tracer, which host-transfers off the GPU.
  Your fit runs, but invisibly slower than the NumPy path.
- The `if xp is np:` guard fires and wraps the result in `aa.Array2D`,
  which fails at the JIT boundary with `TypeError: ... is not a valid
  JAX type`.

The library raises a clear error on the easy case — a `ValueError` at the
function entry whenever you pass an `xp=np` declaration with a
`grid.use_jax=True` input:

```
ValueError: Called magnification_2d_via_hessian_from with xp=np but
the input grid is JAX-backed (grid.use_jax=True). Inside @jax.jit, pass
xp=jnp explicitly. See the lens_calc.py guide for the JIT-it-yourself
pattern.
```

If you see this error: add `xp=jnp` to the call site. That's the fix.

__Decorator-on-def vs `jax.jit(bound_method)`__

JAX accepts any callable — `@jax.jit` is just sugar for `fn = jax.jit(fn)`.
You can JIT a standalone function (the canonical form) or a bound method
(a one-line shortcut). Both work:

```python
# Form 1 (canonical): decorator on def
@jax.jit
def image_fn(tracer, grid):
    return tracer.image_2d_from(grid=grid, xp=jnp).array

# Form 2: jit on bound method, assign-to-variable
jitted = jax.jit(tracer.image_2d_from)
arr = jitted(grid=grid, xp=jnp).array
```

Form 2 is shorter for interactive use. **Footgun:** bound methods are
fresh objects on every attribute access, so this silently misses the JIT
cache every iteration:

```python
# DON'T DO THIS — fresh jax.jit closure every iteration
for grid in many_grids:
    arr = jax.jit(tracer.image_2d_from)(grid=grid, xp=jnp).array
```

If you're calling a JITted method in a loop, assign-to-variable once or
use the decorator-on-def form.

__Closure-captured `self` vs traced argument__

Form 1 and Form 2 differ in *semantics*, not just syntax:

- **Form 2 (`jax.jit(tracer.image_2d_from)`):** `tracer` is the bound
  method's `self`; JAX captures it as a closure constant and doesn't
  trace through it. **`Tracer` does NOT need to be pytree-registered.**
  Trade-off: if you call this with a *different* tracer later, you miss
  the cache (different bound-method object, different closure key).
- **Form 1 (`@jax.jit def image_fn(tracer, grid)`):** `tracer` is a
  traced argument. **`Tracer` DOES need pytree-registration** (which
  `Analysis(use_jax=True)` does for you, or you can trigger via
  `al.jax.enable_for_modeling()`). Trade-off: cache reuse across
  different tracers — parameter sweeps and `jax.vmap` work naturally.

Pick based on whether you want to vary the tracer across calls:

- Parameter sweep / `jax.vmap` over models? Form 1.
- Quick one-off / interactive exploration? Form 2 (assign once).

__`LensCalc` and the wrapped-vs-raw return type__

`LensCalc.magnification_2d_via_hessian_from`, `.shear_yx_2d_via_hessian_from`,
`.convergence_2d_via_hessian_from`, and the eigen-value methods all
implement the `if xp is np:` guard inside them:

```python
def magnification_2d_via_hessian_from(self, grid, xp=np):
    ...
    if xp is np:
        return aa.Array2D(values=mag, mask=grid.mask)   # numpy: wrapped
    return mag                                            # jax: raw jax.Array
```

This is intentional. Inside `@jax.jit` (where you pass `xp=jnp`), you get
back a raw `jax.Array`. On the NumPy path (where you don't pass `xp` or
pass `xp=np`), you get back an `aa.Array2D` wrapper. The library function
adapts to which path you're on.

The user-facing implication: when you JIT-wrap a `LensCalc` method, expect
a raw `jax.Array` back, and rewrap with `aa.Array2D(values=..., mask=...)`
on the host if you want the wrapper for downstream plotting:

```python
@jax.jit
def magnification_fn(lens_calc, grid):
    return lens_calc.magnification_2d_via_hessian_from(grid=grid, xp=jnp)

mag_raw = magnification_fn(lens_calc, grid)
mag_wrapped = aa.Array2D(values=mag_raw, mask=grid.mask)
aplt.plot_array(array=mag_wrapped)
```

For `Tracer` and `Galaxy` methods that don't have the guard internally
(e.g. `tracer.image_2d_from`), the `.array` unwrap inside the jit + rewrap
outside discipline applies — see `scripts/guides/data_structures.py`
`__JAX__` section.

__Summary__

The "JIT-it-yourself" path is for advanced users building custom forward
models. It's bounded by three rules:

1. `@jax.jit` and `xp=jnp` are paired. Forgetting `xp=jnp` either silently
   host-transfers or fails at the boundary.
2. `.array` unwrap inside the jit; rewrap on the host if you want the
   autoarray wrapper.
3. Tracer-as-argument needs pytree registration (`al.jax.enable_for_modeling()`
   or any `Analysis(use_jax=True)` construction); tracer-as-closure (bound-
   method form) doesn't.

For the standard `Analysis` / `Simulator` paths — where users do none of
this and JAX runs implicitly — see the top-level `autolens_workspace/start_here.py`
`__JAX__` section.
"""
```

## Validation

1. The guide runs end-to-end on NumPy.
2. The JAX code examples run (requires Phase 2 shipped for the mismatch
   error; requires `al.jax.enable_for_modeling()` if that helper has
   landed, otherwise the example uses the Analysis-as-trigger workaround).
3. `scripts/check_sizes.sh` passes.

## References

- Phase 0 design doc, especially §2.1, §3.4.1, §4.8.
- Phase 5a, 5b, 5c (cross-references throughout).
- Phase 5e (autogalaxy mirror): some of this material maps to autogalaxy
  (e.g. `Galaxy.image_2d_from(grid, xp=jnp)`); 5e cites this guide for
  the lensing-specific advanced material.
