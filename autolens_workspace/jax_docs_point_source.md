# Phase 3d — `__JAX__` sections in `autolens_workspace/scripts/point_source/*.py`

Per-dataset-type doc pass for the point_source dataset type. Most distinct
from 3a/3b because **point_source has no `likelihood_function.py`** (the
chi-squared walkthrough lives elsewhere) and because `PointSolver(use_jax=True)`
is the central library deliverable.

**Authoritative design doc:** `admin_jammy/notes/jax_interface.md`.
**Depends on:** Phase 2 shipped, specifically the `PointSolver(use_jax=True)`
change.
**Companion:** `autolens_workspace/jax_docs_imaging.md` (3a — read first
for the canonical structure; this prompt is the diff).
**Run in Opus** per [[feedback_tutorial_prose_opus]].

## Scope

Files to edit, all in `autolens_workspace/scripts/point_source/`:

1. `start_here.py` — refresh existing `__JAX__` sections (lines 41, 246)
   per the Phase 0 contract.
2. `simulator.py` — add `__JAX__` prose + `__JAX Variant__` showing the
   post-Phase-2 `PointSolver(use_jax=True)` pattern.
3. `fit.py` — `__JAX__` prose section (same shape as 3a's fit.py, with
   `AnalysisPoint` in place of `AnalysisImaging`).
4. `modeling.py` — same prose as `fit.py` if applicable.

**No `likelihood_function.py` exists in point_source/.** The cluster
likelihood walkthrough at `scripts/cluster/likelihood_function.py` covers
the source-plane / image-plane chi² math for point sources, but cluster is
out of Phase 3 scope per the design's anchor.

**Out of scope:** `features/`, `simulator_sample.py` (sampling variants).

## Point-source-specific adjustments vs 3a

### 1. `PointSolver(use_jax=True)` is the headline

The point-source simulator pipeline is two steps:

1. Build a `Tracer`.
2. Use `PointSolver.solve(tracer, source_plane_coordinate)` to forward-solve
   multiple-image positions.

It's `PointSolver.solve` that's the slow path (triangle refinement loop),
not the tracer image generation. So `simulator.py`'s `__JAX Variant__`
focuses on `PointSolver(use_jax=True)`:

```python
"""
__JAX Variant__

The expensive step in point-source simulation is the multiple-image
solve — `PointSolver` runs an iterative triangle-refinement loop. On
JAX-jit, this is order-of-magnitude faster.

Pass `use_jax=True` to `PointSolver.for_grid`; the solver handles pytree
registration of `Tracer` internally and the call works with one `@jax.jit`
decorator around your own function.
"""
import jax
import jax.numpy as jnp

solver_jax = al.PointSolver.for_grid(
    grid=al.Grid2D.uniform(shape_native=(100, 100), pixel_scales=1.0),
    pixel_scale_precision=0.001,
    use_jax=True,  # NEW after Phase 2
)

@jax.jit
def solve(tracer, source_coord):
    return solver_jax.solve(tracer=tracer, source_plane_coordinate=source_coord)

positions = solve(tracer, jnp.asarray(source_centre))
# positions is a Grid2DIrregular with jax.Array backing
```

The result is padded with `inf` sentinels where no image was found —
`PointSolver(use_jax=True)` defaults `remove_infinities=False` for JAX
static-shape compatibility. Strip outside the jit:

```python
raw = np.asarray(positions.array)
finite_positions = raw[~np.isinf(raw).any(axis=1)]
```

### 2. `fit.py` framing

`AnalysisPoint(dataset=dataset)` defaults to `use_jax=True` per the Phase 0
audit (PyAutoLens/autolens/point/model/analysis.py:45). Same prose framing
as 3a's `fit.py`, swapping the class name:

```python
"""
__JAX__

The `al.AnalysisPoint(dataset=dataset, solver=solver)` constructed below
defaults to `use_jax=True` — your fit is JAX-accelerated by default if
you installed `autolens[jax]`. The `AnalysisPoint._register_fit_point_pytrees()`
method runs on first `fit_from` call to register `FitPositionsSource`,
`FitPositionsImagePair`, `FitPositionsImagePairAll`, and `Tracer` as JAX
pytrees.

Watch the log for `JAX: Applying vmap and jit to likelihood function` —
that's the JIT compile starting.

Force NumPy with `al.AnalysisPoint(..., use_jax=False)` or
`PYAUTO_DISABLE_JAX=1` for debugging.

See `autolens_workspace/start_here.py` `__JAX__` for the broader principles.
"""
```

### 3. `start_here.py` cross-references

Existing `__JAX__` content at lines 41 and 246 should be refreshed; the
top-level workspace `start_here.py` (Phase 1) carries the conceptual home.

### 4. Forward to `lens_calc.py` for hand-rolled fits

Point-source-style hand-rolled chi-squared (source-plane / image-plane)
shows up in `scripts/cluster/likelihood_function.py`. For users who want
to JIT a similar custom point-source likelihood for their own dataset,
the `lens_calc.py` guide (Phase 5d) is the cross-reference — it covers
the `@jax.jit + xp=jnp` JIT-it-yourself pattern that applies equally to
point-source likelihoods.

## Validation

1. All four scripts run on NumPy end-to-end.
2. The `simulator.py` `__JAX Variant__` runs on JAX (Phase 2 shipped).
3. `scripts/check_sizes.sh` passes.
4. `/smoke_test` passes if any of these scripts are in the curated smoke
   set.

## References

- Phase 0 design doc: `admin_jammy/notes/jax_interface.md`, especially
  §1.2 (`AnalysisPoint._register_fit_point_pytrees` is the analogue to
  `AnalysisImaging._register_fit_imaging_pytrees`), §2.2 (PointSolver
  pattern), §3.4.
- Sibling: `autolens_workspace/jax_docs_imaging.md` (3a — canonical
  template).
- Phase 2 (library dependency): `autoarray/simulator_use_jax.md` —
  `PointSolver(use_jax=True)` implementation.
- `autolens_workspace/scripts/cluster/simulator.py` — pre-Phase-2 manual
  pattern; the `__JAX Variant__` in `point_source/simulator.py` shows
  what that collapses to.
