# Phase 4a — `__JAX__` sections in `autogalaxy_workspace/scripts/imaging/*.py`

Direct mirror of Phase 3a for the autogalaxy workspace. Scope is simpler
because autogalaxy doesn't have lens-equation / tracer / multi-plane
framing. Read Phase 3a (`autolens_workspace/jax_docs_imaging.md`) first
for the canonical structure; this prompt is the diff.

**Authoritative design doc:** `admin_jammy/notes/jax_interface.md`.
**Depends on:** Phase 2 shipped.
**Run in Opus** per [[feedback_tutorial_prose_opus]].

## Scope

Files in `autogalaxy_workspace/scripts/imaging/`:

1. `start_here.py` — refresh existing `__JAX__` content (the Phase 0
   audit found `use_jax=True` mention but no top-level `__JAX__` block).
   Add per the Phase 0 contract.
2. `simulator.py` — `__JAX__` prose + `__JAX Variant__` code block.
3. `fit.py` — `__JAX__` prose section.
4. `likelihood_function.py` — `__JAX__` section.
5. `modeling.py` — same prose as `fit.py`.

**Out of scope:** `features/`, `data_preparation*`.

## Autogalaxy-specific adjustments vs 3a

- Replace every mention of `Tracer` with `Galaxies`.
- Replace `AnalysisImaging` references — the class name is the same
  (`ag.AnalysisImaging`) but the import is `import autogalaxy as ag`.
- Drop multi-plane framing, drop `Tracer.ray_tracing` framing.
- The `__JAX Variant__` in `simulator.py`:

```python
"""
__JAX Variant__

For fast repeated simulations, wrap `via_galaxies_from` (or `via_image_from`)
in `@jax.jit` and pass `use_jax=True` to the simulator. The simulator
handles pytree registration of `Galaxies` and the constituent profile
classes internally.
"""
import jax

simulator_jax = ag.SimulatorImaging(
    exposure_time=300.0, psf=psf, background_sky_level=0.1, use_jax=True
)

@jax.jit
def simulate(galaxies):
    return simulator_jax.via_galaxies_from(galaxies=galaxies, grid=grid)

dataset_jax = simulate(galaxies)
```

- The `fit.py` `__JAX__` prose references `ag.AnalysisImaging(dataset=dataset)`
  defaulting to `use_jax=True` — same story as autolens, just with `ag` prefix.
- The `likelihood_function.py` walk-through is simpler (no source-plane chi²,
  no Einstein-radius normalization) — the `__JAX__` section adapts 3a's
  example to wrap `ag.FitImaging` instead of `al.FitImaging`.
- Cross-reference: link to the autogalaxy guides (`scripts/guides/api/`)
  for further reading. The autogalaxy `lens_calc.py` equivalent doesn't
  exist (no lensing) — `data_structures.py` and `galaxies.py` are the
  canonical advanced guides for the JIT-it-yourself path; Phase 5e
  authors those.

## Validation

Same as 3a, with `autogalaxy` in place of `autolens`.

## References

- Phase 0 design doc.
- Sibling: `autolens_workspace/jax_docs_imaging.md` (3a — canonical template).
- Phase 2 (library dependency): `autoarray/simulator_use_jax.md`.
- Downstream: Phase 5e (`autogalaxy_workspace/jax_docs_guides.md`) for the
  autogalaxy guide-level docs.
