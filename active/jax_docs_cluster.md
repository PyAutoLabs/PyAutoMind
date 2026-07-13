# Phase 3f — Migrate `autolens_workspace/scripts/cluster/simulator.py` to the new API

> **⚠ DEFERRED — author/issue only when cluster is out of in-development and
> Phase 2's `PointSolver(use_jax=True)` is shipped.**
>
> Per design doc (`admin_jammy/notes/jax_interface.md` §3.6 + scope anchor):
> cluster is in active development; its current `simulator.py` is the
> canonical pre-Phase-2 manual ceremony (the audit cited it as evidence,
> not as a user template). Don't refactor it for docs purposes until the
> dataset type stabilizes — refactor + ship the post-Phase-2 form once the
> cluster pipeline is mature.

**Authoritative design doc:** `admin_jammy/notes/jax_interface.md`.
**Depends on:** Phase 2 shipped (`PointSolver(use_jax=True)`), cluster
pipeline out of in-dev.
**Run in Opus** per [[feedback_tutorial_prose_opus]].

## Scope (if authored)

Migrate `autolens_workspace/scripts/cluster/simulator.py` to the post-Phase-2
`PointSolver(use_jax=True)` API. This is mostly a code edit, not a doc
addition — the existing `__JAX JIT__` section at lines 396-506 needs to be
**replaced** with the collapsed form.

**Before** (current, ~110 lines of ceremony — see audit §1.4):

```python
from autoconf import jax_wrapper
import jax
import jax.numpy as jnp
from autofit.jax import register_model as _register_model_pytrees
from autoarray.abstract_ndarray import register_instance_pytree
# ... ~60 lines building af.Collection mirror ...
_register_model_pytrees(_registration_model)
register_instance_pytree(Tracer, no_flatten=("cosmology",))
solver = al.PointSolver.for_grid(...)

@jax.jit
def jitted_solve(tracer, source_plane_coordinate):
    return solver.solve(
        tracer=tracer,
        source_plane_coordinate=source_plane_coordinate,
        xp=jnp,
        remove_infinities=False,
    ).array

# ... call site with jnp.asarray / np.asarray conversions ...
```

**After** (post-Phase-2):

```python
from autoconf import jax_wrapper
import jax
import jax.numpy as jnp

solver = al.PointSolver.for_grid(
    grid=al.Grid2D.uniform(shape_native=(800, 800), pixel_scales=0.1),
    pixel_scale_precision=0.001,
    magnification_threshold=0.1,
    use_jax=True,
)

@jax.jit
def jitted_solve(tracer, source_plane_coordinate):
    return solver.solve(tracer=tracer, source_plane_coordinate=source_plane_coordinate)

# Call site:
for i, src_centre in enumerate(source_centres):
    raw = np.asarray(jitted_solve(tracer, jnp.asarray(src_centre)).array)
    finite = ~(np.isinf(raw).any(axis=1) | np.isnan(raw).any(axis=1))
    positions_list.append(al.Grid2DIrregular(raw[finite]))
```

~60 lines of `af.Collection` mirror + `_register_model_pytrees` +
`register_instance_pytree(Tracer)` deletions. The simulator handles all of
that internally now.

Also: replace the existing `__JAX JIT__` docstring with a section
describing the (now-simple) `use_jax=True` + `@jax.jit` pattern, citing
the design doc and Phase 3d's `point_source/simulator.py` `__JAX Variant__`
as the standard form.

## Files

- `autolens_workspace/scripts/cluster/simulator.py` — the migration target.

## Validation

1. The migrated script produces a dataset numerically equivalent to the
   pre-migration version (modulo noise seed).
2. `scripts/check_sizes.sh` will flag a shrinkage — that's expected; pass
   `ALLOW_SHRINK=1` after confirming the shrinkage is intentional.
3. `/smoke_test` — cluster simulator may or may not be in the curated set;
   verify before shipping.

## References

- Phase 0 design doc: `admin_jammy/notes/jax_interface.md`, §1.4 carries
  the full pre-migration walkthrough.
- Phase 2 (library dependency): `autoarray/simulator_use_jax.md`.
- Sibling: `autolens_workspace/jax_docs_point_source.md` (3d) for the
  canonical `PointSolver(use_jax=True)` example.

## Out-of-band notes

- This is a worked migration showing the API collapse. It's the strongest
  in-the-wild validation of Phase 2's design. Author when cluster is stable
  so the migration sticks.
