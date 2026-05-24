# Phase 3b — `__JAX__` sections in `autolens_workspace/scripts/interferometer/*.py`

Mirrors Phase 3a's pattern for the interferometer dataset type. Same
structure, with three interferometer-specific adjustments.

**Authoritative design doc:** `admin_jammy/notes/jax_interface.md`.
**Depends on:** Phase 2 shipped (`SimulatorInterferometer(use_jax=True)`
introduced + the `via_image_from(xp=...)` signature symmetry fix).
**Companion:** `autolens_workspace/jax_docs_imaging.md` (3a) — read first
for the canonical pattern; this prompt is the diff against it.
**Run in Opus** per [[feedback_tutorial_prose_opus]].

## Scope

Files to edit, all in `autolens_workspace/scripts/interferometer/`:

1. `start_here.py` — `__JAX__` section refresh per the Phase 0 contract.
2. `simulator.py` — `__JAX__` prose + `__JAX Variant__` code block, using
   `SimulatorInterferometer(use_jax=True)`.
3. `fit.py` — `__JAX__` prose section (same shape as 3a's fit.py).
4. `likelihood_function.py` — `__JAX__` section (same shape as 3a's).
5. `modeling.py` — same prose as `fit.py` if appropriate.

**Out of scope:** `features/`, `data_preparation*`, `casa_reduction.py`.

## Interferometer-specific adjustments vs 3a

### 1. `Transformer` is the JIT-safety pivot

The interferometer likelihood goes through a `Transformer*` (DFT or NUFFT).
Today:

- `TransformerDFT` — JAX-safe and JIT-traceable. Slow on large
  visibility sets but the default for compatibility.
- `TransformerNUFFT` (via pynufft) — fast but NOT differentiable under
  JAX. The existing `autolens_workspace_test/scripts/interferometer/nufft.py`
  has the cross-check with `nufftax` (a JAX-native NUFFT) for the future
  drop-in.

The `__JAX Variant__` in `simulator.py` should use `TransformerDFT` for the
small example and add a one-paragraph caveat:

> For interferometer simulations under `@jax.jit`, use `TransformerDFT`
> (the default). `TransformerNUFFT` is faster on large UV sets but is not
> JAX-traceable. A future drop-in (`nufftax`) is being evaluated — see
> `autolens_workspace_test/scripts/interferometer/nufft.py` for the parity
> work.

### 2. `simulator.py` `__JAX Variant__` shape

Adapted from 3a; key differences are the constructor (`SimulatorInterferometer`),
the input (`uv_wavelengths`), and the return (`Interferometer` with
visibility-based `.data` not image-based):

```python
"""
__JAX Variant__

For fast repeated visibility simulations, wrap `via_image_from` in
`@jax.jit` and pass `use_jax=True` to the simulator. Internally the
simulator threads `xp=jnp` and handles pytree registration.

Use `TransformerDFT` (the default) — `TransformerNUFFT` is faster on large
UV sets but not JAX-traceable.
"""
import jax

simulator_jax = al.SimulatorInterferometer(
    uv_wavelengths=uv_wavelengths,
    exposure_time=300.0,
    noise_sigma=0.1,
    use_jax=True,
)

@jax.jit
def simulate(tracer):
    image = tracer.image_2d_from(grid=real_space_grid, xp=jnp)
    return simulator_jax.via_image_from(image=image)

dataset_jax = simulate(tracer)
```

Note the `xp=jnp` on `tracer.image_2d_from` — this is the §3.4.1
"JIT-it-yourself" pattern from the design doc, surfaced here because the
simulator pipeline for interferometer is two steps (image generation +
Fourier transform) and the user is composing both inside one `@jax.jit`.
The 3a imaging variant doesn't show this because `SimulatorImaging.via_tracer_from`
encapsulates both steps in one library call.

If this two-step pattern feels too advanced for `simulator.py`, an
alternative is to add `SimulatorInterferometer.via_tracer_from(tracer, grid)`
to PyAutoLens (mirror of imaging) as part of Phase 2's library work, and
the variant becomes a one-liner like 3a's. Decide during implementation.

### 3. `likelihood_function.py` cross-references

The hand-rolled likelihood walk-through for interferometer is shorter than
imaging (no PSF, no Poisson noise — just complex visibility chi-squared).
The `__JAX__` section maps directly to 3a's pattern; the validation
example uses `FitInterferometer` instead of `FitImaging`.

### 4. `start_here.py` cross-references

Existing interferometer `__JAX__` content should be refreshed to align with
the Phase 0 contract. Keep the `from autoconf import jax_wrapper` import
line at the top of the file if it's already there — it sets `JAX_ENABLE_X64=1`
and must precede any JAX import (design doc §4.6).

## Validation

Same as 3a, with `interferometer` in place of `imaging`. The
`simulator.py` `__JAX Variant__` should produce visibilities numerically
equivalent (within seed-noise) to the NumPy path; verify against the parity
script in `autolens_workspace_test/scripts/interferometer/` if one exists
post-Phase 2.

## References

- Phase 0 design doc: `admin_jammy/notes/jax_interface.md`, especially
  §1.3 (Simulator status quo — flags the `SimulatorInterferometer` signature
  asymmetry that Phase 2 fixes) and §3.4.
- Sibling: `autolens_workspace/jax_docs_imaging.md` (3a — the canonical
  template).
- `autolens_workspace_test/scripts/interferometer/nufft.py` — the NUFFT
  parity script that documents the `TransformerNUFFT` JAX caveat.
- Phase 2 (library dependency): `autoarray/simulator_use_jax.md`.
