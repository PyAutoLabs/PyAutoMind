# Phase 4b — `__JAX__` sections in `autogalaxy_workspace/scripts/interferometer/*.py`

Direct mirror of Phase 3b for the autogalaxy workspace. Read Phase 3b
(`autolens_workspace/jax_docs_interferometer.md`) first; this prompt is
the diff.

**Authoritative design doc:** `admin_jammy/notes/jax_interface.md`.
**Depends on:** Phase 2 shipped, Phase 4a recommended-but-not-required.
**Run in Opus** per [[feedback_tutorial_prose_opus]].

## Scope

Files in `autogalaxy_workspace/scripts/interferometer/`:

1. `start_here.py` — `__JAX__` section refresh.
2. `simulator.py` — `__JAX__` prose + `__JAX Variant__`.
3. `fit.py`, `modeling.py` — `__JAX__` prose sections.
4. `likelihood_function.py` (if present) — `__JAX__` section.

**Out of scope:** `features/`, `data_preparation*`.

## Autogalaxy-specific adjustments

Same as 4a (replace Tracer with Galaxies, drop lens framing), plus the
interferometer-specific `Transformer` caveat from 3b:

> Use `TransformerDFT` (the default) under `@jax.jit` — `TransformerNUFFT`
> is faster on large UV sets but is not JAX-traceable.

The autogalaxy workspace is JAX-light here per the Phase 0 audit. Most of
the prose is net-new (rather than refreshing existing content).

`__JAX Variant__` shape:

```python
"""
__JAX Variant__
"""
import jax
import jax.numpy as jnp

simulator_jax = ag.SimulatorInterferometer(
    uv_wavelengths=uv_wavelengths,
    exposure_time=300.0,
    noise_sigma=0.1,
    use_jax=True,
)

@jax.jit
def simulate(galaxies):
    galaxy = ag.Galaxies(galaxies=galaxies)
    image = galaxy.image_2d_from(grid=real_space_grid, xp=jnp)
    return simulator_jax.via_image_from(image=image)

dataset_jax = simulate(galaxies)
```

Same two-step pattern as 3b — image generation + Fourier transform inside
the same `@jax.jit`. The `xp=jnp` thread is the §3.4.1 "JIT-it-yourself"
pattern applied to galaxy image generation.

## Validation

Standard.

## References

- Phase 0 design doc.
- Sibling: `autolens_workspace/jax_docs_interferometer.md` (3b).
- Phase 2 (library dependency): `autoarray/simulator_use_jax.md`.
