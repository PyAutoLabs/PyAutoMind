# Phase 5c — `__JAX__` section in `autolens_workspace/scripts/guides/tracer.py`

Covers ray-tracing performance on JAX vs NumPy, multi-plane traces under
JIT, and the `Tracer` pytree contract (registered by `Analysis(use_jax=True)`
and `Simulator(use_jax=True)`, walked once on first call).

**Authoritative design doc:** `admin_jammy/notes/jax_interface.md`.
**Run in Opus** per [[feedback_tutorial_prose_opus]].
**Depends on:** Phase 1 + Phase 5a + Phase 5b shipped (cross-references).

## Scope

Single file: `autolens_workspace/scripts/guides/tracer.py`.

`__JAX__` section (~60-90 lines) covering:

1. **`Tracer.image_2d_from`, `Tracer.deflections_yx_2d_from`,
   `Tracer.traced_grid_2d_list_from` all run on JAX** when called with
   `xp=jnp` inside a user-written `@jax.jit`. The library functions are
   xp-aware — same code path, different backend.
2. **Multi-plane traces under JIT** — the recursive lens equation walks
   are JIT-friendly (no data-dependent control flow). For multi-plane
   point-source simulations specifically, see `PointSolver(use_jax=True)`
   in the point_source/simulator.py `__JAX Variant__`.
3. **The `Tracer` pytree contract** — registered automatically by
   `AnalysisImaging._register_fit_imaging_pytrees()` and
   `SimulatorImaging.via_tracer_from` (when `use_jax=True`). User passes
   a `Tracer` as a `@jax.jit` argument; library handles flattening.
4. **Performance framing** — typical speedups for tracer-level operations
   are 10-100× on GPU for large grids. Reference autolens_profiling for
   measured numbers if available.

**Out of scope:**
- The `.array` and host-transfer mechanics (Phase 5a).
- The Galaxy registration story (Phase 5b).
- The `@jax.jit + xp=jnp` calling convention (Phase 5d).
- Cluster-scale point-source solving — covered in the cluster docs
  (Phase 3f, deferred).

## Proposed structure

```python
"""
__JAX__

The ray-tracing operations on `Tracer` are the most JAX-friendly part of
PyAutoLens — they're pure numerical kernels with no data-dependent
control flow. Typical speedups for `tracer.image_2d_from(grid)` and
related on a large image grid are 10-100× on GPU vs CPU NumPy.

You access this speed in two ways:

__1. The implicit path: `Analysis` and `Simulator`__

If you're going through `AnalysisImaging(use_jax=True)` (the default for
`autolens[jax]` installs) or `SimulatorImaging(use_jax=True)`, the
`Tracer` is JAX-accelerated automatically. The library handles pytree
registration of `Tracer` and the JIT compilation internally; you write
nothing JAX-specific.

__2. The explicit path: your own `@jax.jit`__

If you want to JIT a `Tracer` operation directly — for parameter sweeps,
custom forward models, or batch figure generation — the canonical pattern
is:

```python
import jax
import jax.numpy as jnp

al.jax.enable_for_modeling()   # one-time registration of Tracer / Galaxy / profile classes

@jax.jit
def image_fn(tracer, grid):
    return tracer.image_2d_from(grid=grid, xp=jnp).array

image = image_fn(tracer, grid)
```

Two pairing rules to remember:

- **`@jax.jit` + `xp=jnp` go together.** If you wrap a tracer method in
  `@jax.jit`, pass `xp=jnp` to the method call inside the body. Forgetting
  this either host-transfers silently or errors loudly at the JIT
  boundary; the library can also raise a clear error on the mismatch (see
  design doc §4.8).
- **`.array` unwrap inside, rewrap outside.** The `aa.Array2D` wrapper
  isn't reliably JAX-pytree for return-from-JIT purposes; return the raw
  `.array` and rewrap on the host side.

__Multi-plane traces under JIT__

The recursive multi-plane lens equation in
`tracer.traced_grid_2d_list_from(grid)` is pure numerical with no
data-dependent control flow, so it JITs cleanly. For multi-plane
**point-source** simulations (forward-solving multiple-image positions
through several planes), use the higher-level `al.PointSolver(use_jax=True)`
— see `scripts/point_source/simulator.py` `__JAX Variant__`.

__Performance expectations__

Tracer image generation on JAX-GPU typically beats NumPy-CPU by:

- 10-30× for galaxy-scale models (single lens galaxy, single source).
- 30-100× for cluster-scale models (many galaxies, multi-plane).

The actual speedup depends on grid size, profile complexity, and GPU
hardware. The `autolens_workspace_developer/jax_profiling/` directory has
measured numbers for representative configurations.

For the full advanced JIT-it-yourself treatment (bound method form,
cache-identity considerations, the closure-captured `self` vs
traced-argument distinction), see `scripts/guides/lens_calc.py` — that's
the canonical advanced guide. `scripts/guides/galaxies.py` covers the
pytree registration mechanics in more detail.
"""
```

## Validation

Standard. Verify the cross-references to Phases 5a/5b/5d resolve once
those ship.

## References

- Phase 0 design doc, especially §3.4.1 (JIT-it-yourself), §4.1 (open
  question on the enable helper).
- Phase 5a, 5b, 5d (cross-references).
