## jax-substructure-simulator
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/542 (CLOSED — core delivered; 2 follow-up gaps queued)
- completed: 2026-06-09
- epic: jax_substructure/ (prompts 1-4: vmap deflections → lax.scan multi-plane → e2e jit simulate → vmap batched)
- library-prs:
  - https://github.com/PyAutoLabs/PyAutoLens/pull/543
  - https://github.com/PyAutoLabs/PyAutoLens/pull/544
- workspace-prs:
  - https://github.com/PyAutoLabs/autolens_workspace_test/pull/127
  - https://github.com/PyAutoLabs/autolens_workspace_test/pull/128
  - https://github.com/PyAutoLabs/autolens_workspace_test/pull/129
- repos: PyAutoLens, PyAutoGalaxy, autolens_workspace_test
- notes: Retroactive close-out — the 4 `jax_substructure/` prompts shipped to `main` over PRs PyAutoLens #543 (scan) + #544 (e2e), additional PyAutoLens commits `b744801` (batched_simulate) / `4e93ecc` (parameterize lens/source/light), PyAutoGalaxy direct commits (`8a317dfc` jnp.where NaN-safe mask, `a4b8ce22`) for the generic `vmapped_deflections_from` classmethod on the abstract mass profile, and workspace_test #127/#128/#129, but the work was never recorded here and issue #542 was left OPEN. Delivered: `autolens/lens/substructure_util.py` (`precompute_scaling_matrix`, `galaxies_to_halo_arrays`, `traced_grids_via_scan`, `simulate_substructure`, `los_realizations_to_arrays`, `batched_simulate_substructure`), the generic `Profile.vmapped_deflections_from` (covers any mass profile exposing `radial_deflection_from`), and 3 workspace_test scripts (`test_scan_multiplane.py`, `test_simulate_e2e.py`, `test_batched_simulate.py`). **Two prompt sub-items were sidestepped/deferred and are now queued as follow-up prompts:** (1) `jax_substructure/5_prng_key_vmap_noise.md` — prompt 3's Gap 1: `preprocess.poisson_noise_via_data_eps_from` still derives its `PRNGKey` internally from the int `seed` (`seed=-1` → `int(time.time())`), so the OO `SimulatorImaging` path can't be vmapped over a batch of noise keys; the standalone `simulate_substructure` sidesteps this by calling `jax.random.poisson(prng_key, ...)` directly. The fix is an optional `prng_key` param (PyAutoArray, → /ship_library). (2) `jax_substructure/6_deflection_equivalence_test.md` — prompt 1's dedicated old-vs-vmapped deflection-equivalence test (all 4 dark-matter profile types + masked-slot-zero) was never authored as a standalone script; validation is only folded into the scan/e2e tests. Note `galaxies_to_halo_arrays` only branches `cNFWSph` vs. truncated, so that test may surface a small MCR-variant extension (workspace_test, → /ship_workspace). Prompt-4 stretch memory-estimator / sub-batching helper remains unbuilt (not requested).

## Lifecycle note — the four prompts retired from `draft/` on 2026-08-09

Record backfilled behaviour, second pass. This record was itself written as a
"retroactive close-out" on 2026-06-09 and states plainly that "the 4
`jax_substructure/` prompts shipped to `main`" — yet all four prompt files stayed
in `draft/feature/jax_substructure/` for a further two months, indistinguishable
from unstarted work. The draft/ sweep retired them here; their bodies are folded
in below so nothing is lost.

**Re-verified against upstream `main` before retiring** (2026-08-09), rather than
trusting this record's own claim:

- **PyAutoLens** — `autolens/lens/substructure_util.py` exists and defines all six
  named deliverables: `precompute_scaling_matrix`, `galaxies_to_halo_arrays`,
  `traced_grids_via_scan`, `simulate_substructure`, `los_realizations_to_arrays`,
  `batched_simulate_substructure`.
- **PyAutoGalaxy** — `vmapped_deflections_from` is present on the abstract mass
  profile (`autogalaxy/profiles/mass/abstract/abstract.py`).
- **autolens_workspace_test** — all three scripts exist, at
  `scripts/imaging/substructure/{test_scan_multiplane,test_simulate_e2e,test_batched_simulate}.py`.
  Note the path: they are **not** under `misc/`, and a lookup there 404s. Same
  path-drift trap as the health_fixes cluster.

**The two follow-ups this record queued are still genuinely open** and stay in
`draft/feature/jax_substructure/` — confirmed, not assumed:

- `5_prng_key_vmap_noise.md` — `preprocess.poisson_noise_via_data_eps_from` still
  has the signature `(data_eps, exposure_time_map, seed=-1, xp=np)` on PyAutoArray
  `main`. No `prng_key` parameter. Unchanged.
- `6_deflection_equivalence_test.md` — no standalone deflection-equivalence script
  exists in `autolens_workspace_test`; `scripts/imaging/substructure/` holds only
  the three e2e/scan/batched scripts plus `subhalo.py`, and no workspace script
  references `vmapped_deflections_from`. Unchanged.

The prompt-4 stretch memory-estimator / sub-batching helper remains unbuilt, as
recorded above — deliberately not requested, so not filed as a follow-up.


## Original prompt — `1_vmap_subhalo_deflections.md`

# Context: PyAutoLens issue #542 asks for a JIT/vmap-able multi-plane substructure

Type: feature
Target: jax_substructure
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Context: PyAutoLens issue #542 asks for a JIT/vmap-able multi-plane substructure
forward simulator. This is prompt 1 of 4 — building the vectorized per-plane
deflection computation that everything else stacks on top of.

## Background

Today, when a Tracer has N subhalos on a single plane, their deflections are
summed via a Python generator loop:

```python
# tracer_util.py line 262
deflections_yx_2d = sum(
    (g.deflections_yx_2d_from(grid=scaled_grid, xp=xp) for g in galaxies)
)
```

Under `jax.jit`, JAX unrolls this into N separate traced operations. For 5
galaxies that's fine. For 1000 halos it produces a massive XLA graph (slow
compilation) and recompiles whenever N changes between realizations.

The fix is a **vmapped deflection function** that takes stacked parameter arrays
and computes all N deflections in a single GPU launch, then sums them.

All four dark matter profiles already accept `xp=jnp` and produce correct
JAX-traced outputs — the individual deflection math is ready. What's missing
is the batching orchestration.

## What to build

A pure-function module (suggest `autolens/lens/substructure_util.py` or similar)
containing functions like:

```python
def deflections_nfw_truncated_sph_from(
    grid,        # (M, 2) image-plane grid
    params,      # (N, 4) — mass_at_200, concentration, centre_y, centre_x
    mask,        # (N,) boolean — which slots are active halos
    cosmology,   # for MCR variants that need kappa_s / scale_radius
    redshift,    # halo redshift (scalar, shared across the batch)
    xp=jnp,
):
    """Compute summed deflections from N NFWTruncatedSph halos via vmap."""
    ...
```

The inner single-halo function should call the existing deflection math from
the profile classes. Look at how `NFWTruncatedSph.deflections_yx_2d_from`
works in `autogalaxy/profiles/mass/dark/nfw_truncated.py` — it calls through
the `@aa.decorators.transform` and `@aa.decorators.to_vector_yx` decorator
chain. For the vmapped path you'll want to call the underlying math directly
(pre-transform the grid by subtracting `centre`, call the radial deflection
functions, post-transform back) to avoid the decorator overhead that wraps
results in autoarray objects.

The key profiles to cover:

- `NFWTruncatedSph` — `autogalaxy/profiles/mass/dark/nfw_truncated.py`
- `cNFWSph` — `autogalaxy/profiles/mass/dark/cnfw.py`
- Their MCR Ludlow variants (`nfw_truncated_mcr.py`, `cnfw_mcr.py`) which
  derive `kappa_s` and `scale_radius` from `mass_at_200` via
  `autogalaxy/profiles/mass/dark/mcr_util.py`

For the MCR variants, the Ludlow concentration-mass relation
(`mcr_util.kappa_s_and_scale_radius_for_ludlow` and
`mcr_util.kappa_s_scale_radius_and_core_radius_for_ludlow`) is already
JAX-native — it auto-detects JAX arrays and uses `jnp` internally. So you
can vmap through the full MCR → deflection chain.

The `mask` parameter handles the padding: pad `params` to `max_N` rows, set
`mask=False` for unused slots, and zero out their deflection contribution
before summing. This way the array shape is fixed regardless of the actual
number of halos, so `jax.jit` compiles once.

## Integration test

This is the key validation: build a Tracer the normal way with ~10 subhalos
(using the existing Galaxy/profile API), compute deflections via the
Python-loop path, then compute the same deflections via the new vmapped
path, and assert they match to numerical tolerance.

Put this in `autolens_workspace_test/scripts/jax_substructure/` (new directory).
Something like:

```python
# 1. Build 10 NFWTruncatedSph halos as Galaxy objects
halos = [ag.Galaxy(redshift=0.5, mass=ag.mp.NFWTruncatedSph(...)) for _ in range(10)]
tracer = al.Tracer(galaxies=[macro_galaxy, *halos, source_galaxy])

# 2. Get deflections via existing path
deflections_old = tracer_util.traced_grid_2d_list_from(..., xp=jnp)

# 3. Stack same parameters into arrays
params = jnp.array([[mass_i, conc_i, cy_i, cx_i] for ...])
mask = jnp.ones(10, dtype=bool)

# 4. Get deflections via new vmapped path
deflections_new = deflections_nfw_truncated_sph_from(grid, params, mask, ...)

# 5. Assert match
assert jnp.allclose(deflections_old, deflections_new, atol=1e-8)
```

Do this for all four profile types. Also test that masked-out slots contribute
zero deflection.

## Scope boundaries

- This prompt covers **single-plane** vectorized deflections only. Multi-plane
  scan is prompt 2.
- Don't modify the existing Tracer or Galaxy classes. This is a parallel path.
- The macro lens (PowerLaw + ExternalShear) doesn't need vmapping here — there's
  only one macro lens per realization. It will be called directly in prompt 2.
- Light profiles (source image) are also not in scope here — just mass deflections.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->

## Original prompt — `2_tracer_lax_scan.md`

# Context: PyAutoLens issue #542, prompt 2 of 4. Prompt 1

Type: feature
Target: jax_substructure
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Context: PyAutoLens issue #542, prompt 2 of 4. Prompt 1 built vmapped per-plane
deflection functions. This prompt wires them into a `jax.lax.scan` over redshift
planes to replace the Python loops in multi-plane ray-tracing.

## Background

The current multi-plane ray-tracing lives in
`autolens/lens/tracer_util.py : traced_grid_2d_list_from` (lines 174-268).
It has three nested Python loops:

1. **Outer loop** (line 232): `for plane_index, galaxies in enumerate(planes):`
2. **Scaling loop** (line 238): `for previous_plane_index in range(plane_index):`
   — applies cosmological scaling factors from all previous planes
3. **Galaxy sum** (line 262): `sum(g.deflections_yx_2d_from(...) for g in galaxies)`
   — sums deflections from all galaxies on the current plane

For the substructure use case (~8 planes, ~1000 total halos), these Python loops
unroll into a huge XLA graph and recompile whenever the galaxy count changes.

## What to build

A standalone pure-function that does the same multi-plane ray-tracing but using
`jax.lax.scan` over planes and the vmapped deflection functions from prompt 1.
Suggest placing this in the same module as prompt 1
(`autolens/lens/substructure_util.py`).

### Input representation

The key design decision is how to represent the per-plane halo populations as
fixed-shape arrays. The natural structure is:

```python
# Per-plane halo parameters, padded to max_halos_per_plane
halo_params: jnp.array     # shape (n_planes, max_halos_per_plane, n_halo_params)
halo_mask: jnp.array       # shape (n_planes, max_halos_per_plane) — bool
plane_redshifts: jnp.array # shape (n_planes,)
```

The macro lens (PowerLaw + ExternalShear) should be handled separately from the
halo stacks — it's a single galaxy evaluated directly, not vmapped. The source
light profile is also separate (evaluated on the final traced grid).

### Precomputed scaling-factor matrix

The cosmological scaling factors between all plane pairs can be precomputed
**outside jit** as a `(n_planes, n_planes)` matrix:

```python
# scaling_matrix[i, j] = scaling_factor from plane j to plane i (0 if j >= i)
scaling_matrix = precompute_scaling_matrix(plane_redshifts, cosmology)
```

The cosmology module at `autogalaxy/cosmology/model.py` already has
`scaling_factor_between_redshifts_from(redshift_0, redshift_1, redshift_final, xp)`
which is xp-threaded. Call it for each `(j, i)` pair where `j < i`.

This matrix is a static input to the jitted function — it only depends on
redshifts, which are fixed for a given realization.

### The scan function

```python
def traced_grids_via_scan(
    grid,              # (M, 2) image-plane grid
    macro_params,      # dict or array of PowerLaw + ExternalShear params
    halo_params,       # (n_planes, max_N, n_halo_params)
    halo_mask,         # (n_planes, max_N)
    scaling_matrix,    # (n_planes, n_planes)
    source_params,     # Sersic params for the source
    ...
):
    def scan_step(carry, plane_inputs):
        # carry: (current_grid, all_prev_deflections as (n_planes, M, 2) buffer)
        # plane_inputs: (this_plane_halo_params, this_plane_mask, scaling_row)

        grid, deflection_buffer, plane_idx = carry
        plane_halo_params, plane_mask, scaling_row = plane_inputs

        # 1. Apply scaled deflections from all previous planes
        #    scaling_row is (n_planes,) — entries for j >= plane_idx are 0
        scaled_deflections = jnp.einsum('p,pmd->md', scaling_row, deflection_buffer)
        current_grid = grid - scaled_deflections

        # 2. Compute macro deflections (if this is the lens plane)
        #    ... call PowerLaw + ExternalShear deflection directly ...

        # 3. Compute halo deflections via vmapped function from prompt 1
        halo_deflections = deflections_nfw_truncated_sph_from(
            current_grid, plane_halo_params, plane_mask, ...
        )

        # 4. Store total plane deflections in buffer
        total_deflections = macro_deflections + halo_deflections
        deflection_buffer = deflection_buffer.at[plane_idx].set(total_deflections)

        return (grid, deflection_buffer, plane_idx + 1), current_grid

    init_carry = (grid, jnp.zeros((n_planes, M, 2)), 0)
    _, traced_grids = jax.lax.scan(scan_step, init_carry, plane_stack)
    return traced_grids
```

The exact API will need refinement — the sketch above shows the idea. The macro
lens only contributes on one plane (the main lens plane), so use `jax.lax.cond`
or `jnp.where` to conditionally add its deflections based on `plane_idx`.

### Where the macro lens fits

The macro galaxy (PowerLaw + ExternalShear) is evaluated directly — not vmapped,
since there's only one. Its deflection function is already JAX-traceable
(`autogalaxy/profiles/mass/total/power_law.py` uses a `jax.lax.scan` series
expansion). Call it on the lens-plane grid and add it to that plane's deflection
buffer alongside the halo contribution.

### Where the source fits

After the scan produces `traced_grids` for all planes, evaluate the source light
profile (e.g. `SersicCore`) on the final plane's traced grid to produce the
lensed image. `SersicCore.image_2d_via_radii_from` already accepts `xp` — call
it directly on the source-plane grid.

## Integration test

Extend the test from prompt 1. Build a Tracer with:
- 1 PowerLaw + ExternalShear macro at z=0.5
- 10 NFWTruncatedSph subhalos at z=0.5 (lens plane)
- 5 NFWTruncatedSph LOS halos at z=0.25 (foreground plane)
- 5 NFWTruncatedSph LOS halos at z=0.75 (background plane)
- 1 Sersic source at z=1.0

Compute the final source-plane grid via both paths:
1. `tracer_util.traced_grid_2d_list_from(planes, grid, cosmology, xp=jnp)`
2. `traced_grids_via_scan(grid, macro_params, halo_params, ...)`

Assert the source-plane grids match to numerical tolerance. This validates that
the scan + vmap path reproduces the existing Python-loop path.

Also test that the scan path compiles once and reuses the compiled code when
only parameter values change (same shapes, different halo masses/positions).

Put tests in `autolens_workspace_test/scripts/jax_substructure/`.

## Scope boundaries

- This covers multi-plane ray-tracing and source-plane grid computation.
- PSF convolution and noise are prompt 3.
- The LOSSampler output stays as-is — it runs outside jit and produces the
  parameter arrays that feed into this function. The conversion from
  `LOSSampler.galaxies_from()` output to `(halo_params, halo_mask)` arrays
  is a small helper, not a refactor of LOSSampler itself.
- Don't modify the existing Tracer class or tracer_util. This is a parallel path.

## Existing patterns to follow

- `jax.lax.scan` is already used in `autogalaxy/profiles/mass/total/jax_utils.py`
  (omega series expansion) and `autoarray/operators/transformer.py` (chunked
  NUFFT). Look at those for the carry/accumulator pattern.
- `jax.lax.fori_loop` is used in `autoarray/inversion/mesh/interpolator/knn.py`.
- Pytree registration: `autoarray/abstract_ndarray.py` has `register_instance_pytree`.
  The new function takes raw arrays, so pytree registration isn't needed for
  the function itself — just ensure inputs are plain `jnp.arrays`.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->

## Original prompt — `3_simulator_jax_e2e.md`

# Context: PyAutoLens issue #542, prompt 3 of 4. Prompts 1-2

Type: feature
Target: jax_substructure
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Context: PyAutoLens issue #542, prompt 3 of 4. Prompts 1-2 built the vectorized
deflection and scan-based ray-tracing. This prompt wires them through PSF
convolution and Poisson noise to produce the end-to-end `jax.jit(simulate)`
function.

## Background

The existing simulator call chain is:

```
SimulatorImaging.via_tracer_from(tracer, grid)
  -> tracer.padded_image_2d_from(grid, psf_shape_2d)
       -> image_2d_from (sum light profiles on traced grids)
  -> SimulatorImaging.via_image_from(image)
       -> PSF convolution (FFT or real-space, both JAX-ready)
       -> add background sky
       -> Poisson noise via jax.random.poisson (when xp=jnp)
       -> return Imaging dataset
```

The downstream half (PSF convolution onward) is already JAX-friendly. The
upstream half (image from traced grids) is now handled by the scan path from
prompt 2. This prompt connects them and fixes the remaining gaps.

## Gap 1: PRNGKey support for Poisson noise

`autoarray/dataset/preprocess.py : poisson_noise_via_data_eps_from` (line 455)
currently takes an integer `seed` parameter. On the JAX path (line 488) it
converts this to a PRNGKey:

```python
effective_seed = seed if seed != -1 else int(time.time() * 1e6) & 0xFFFFFFFF
key = jax.random.PRNGKey(effective_seed)
```

This works for single calls but blocks `vmap` over noise seeds — you can't
vmap a function that calls `int(time.time())` inside.

Add an optional `prng_key` parameter:

```python
def poisson_noise_via_data_eps_from(
    data_eps, exposure_time_map, seed=-1, prng_key=None, xp=np
):
    ...
    if prng_key is not None:
        key = prng_key
    elif xp is not np:
        effective_seed = seed if seed != -1 else int(time.time() * 1e6) & 0xFFFFFFFF
        key = jax.random.PRNGKey(effective_seed)
    ...
```

Thread this parameter through `data_eps_with_poisson_noise_added` (line 500)
and up through `SimulatorImaging.via_image_from` in
`autoarray/dataset/imaging/simulator.py`.

## Gap 2: Over-sampler xp threading

`Grid2D.padded_grid_from` in `autoarray/structures/grids/uniform_2d.py`
(line 1140) uses `np.pad` which is not xp-aware. Similarly the OverSampler
binning path uses numpy operations.

For the substructure fast path, the simplest approach is to **skip the
autoarray grid/over-sampler machinery entirely** and handle padding and
sub-gridding with plain jnp operations in the standalone simulate function.
The grid is uniform and the over-sample factor is fixed, so this is
straightforward:

```python
# Pad grid for PSF
padded_shape = image_shape + psf_shape - 1
padded_grid = make_uniform_grid(padded_shape, pixel_scale)  # pure jnp

# Evaluate source on sub-grid if over_sample > 1
sub_grid = make_sub_grid(padded_grid, over_sample_size)  # pure jnp
sub_images = source_image_fn(sub_grid, source_params)
image = sub_images.reshape(...).mean(axis=-1)  # bin down
```

This avoids modifying the autoarray grid classes while giving us a fully
jnp-native path.

## The end-to-end simulate function

Combine everything into a single jittable function:

```python
@jax.jit
def simulate_substructure(
    macro_params,        # PowerLaw + ExternalShear parameters
    halo_params,         # (n_planes, max_N, n_halo_params)
    halo_mask,           # (n_planes, max_N)
    source_params,       # Sersic parameters
    # --- static / precomputed (passed via jax.jit static_argnums or closure) ---
    grid,                # (M, 2) image-plane grid (padded for PSF)
    psf_kernel,          # (K, K) PSF array
    scaling_matrix,      # (n_planes, n_planes)
    exposure_time,       # scalar
    background_sky,      # scalar
    prng_key,            # jax.random.PRNGKey for Poisson noise
):
    # 1. Multi-plane ray-trace (from prompt 2)
    traced_grids = traced_grids_via_scan(
        grid, macro_params, halo_params, halo_mask, scaling_matrix
    )

    # 2. Evaluate source light on final traced grid
    source_grid = traced_grids[-1]
    image = sersic_image_from(source_grid, source_params)

    # 3. PSF convolution (FFT)
    image = jax.scipy.signal.fftconvolve(image, psf_kernel, mode='same')

    # 4. Add background sky
    image = image + background_sky

    # 5. Poisson noise
    image_counts = image * exposure_time
    noisy_counts = jax.random.poisson(prng_key, image_counts)
    noisy_image = noisy_counts / exposure_time

    # 6. Subtract sky
    noisy_image = noisy_image - background_sky

    return noisy_image
```

The PSF convolution can use `jax.scipy.signal.fftconvolve` directly — the
existing Convolver FFT path in `autoarray/operators/convolver.py` already
does essentially this with `jnp.fft.rfft2 / irfft2`, so either approach works.
For the standalone function, the scipy one-liner is simpler.

## Integration test / smoke test

Build a representative substructure configuration and verify the end-to-end
simulate function against the existing OO path:

```python
# Build via existing API
tracer = al.Tracer(galaxies=[macro, *subhalos_10, source])
simulator = al.SimulatorImaging(
    exposure_time=300.0, background_sky_level=1.0,
    psf=al.Kernel2D.from_gaussian(shape_native=(11, 11), sigma=0.1, ...),
    noise_seed=42,
)
imaging_old = simulator.via_tracer_from(tracer=tracer, grid=grid)

# Build via new pure-function path (same parameters, same seed)
key = jax.random.PRNGKey(42)
image_new = simulate_substructure(
    macro_params, halo_params, halo_mask, source_params,
    grid, psf_kernel, scaling_matrix, 300.0, 1.0, key,
)

# Compare (tolerance for Poisson noise RNG differences — compare
# the deterministic part first, then the noisy part with the same seed)
assert jnp.allclose(image_new, imaging_old.data, atol=1e-6)
```

Also verify that `jax.jit(simulate_substructure)` compiles successfully
and that calling it a second time with different parameter values (same
shapes) reuses the compiled code (no recompilation).

Put tests in `autolens_workspace_test/scripts/jax_substructure/`.

## Scope boundaries

- This prompt produces a working `jit(simulate)` for a single realization.
- `vmap` over a batch of parameter vectors is prompt 4.
- The LOSSampler conversion helper (Galaxy list -> padded arrays) should be
  a small utility, not a refactor. If it's simple enough, include it here;
  otherwise defer to prompt 4.
- Don't modify the existing SimulatorImaging class beyond adding the
  `prng_key` parameter to the noise functions in preprocess.py.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->

## Original prompt — `4_vmap_batched_simulation.md`

# Context: PyAutoLens issue #542, prompt 4 of 4 (stretch goal).

Type: feature
Target: jax_substructure
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Context: PyAutoLens issue #542, prompt 4 of 4 (stretch goal). Prompts 1-3 built
`jax.jit(simulate_substructure)` for a single realization. This prompt extends
it to `vmap(jit(simulate))(thetas, keys)` for batched evaluation — ~1024 lensed
images per GPU launch.

## Background

The issue author's use case evaluates `theta -> noisy image` of order 10^6
times. After prompt 3, each call is a single jitted GPU kernel. The next
speedup is batching: evaluate many theta vectors in one launch, saturating
GPU parallelism.

## What to build

### Batched simulate function

```python
batched_simulate = jax.vmap(simulate_substructure, in_axes=(
    0,     # macro_params: (batch, n_macro_params) — varies per realization
    0,     # halo_params: (batch, n_planes, max_N, n_halo_params) — varies
    0,     # halo_mask: (batch, n_planes, max_N) — varies (different N per draw)
    0,     # source_params: (batch, n_source_params) — varies
    None,  # grid: shared across batch
    None,  # psf_kernel: shared
    None,  # scaling_matrix: shared (same redshift structure)
    None,  # exposure_time: shared
    None,  # background_sky: shared
    0,     # prng_key: (batch,) — different key per realization
))
```

Call with:

```python
keys = jax.random.split(master_key, batch_size)
images = jax.jit(batched_simulate)(
    macro_params_batch,   # (1024, n_macro)
    halo_params_batch,    # (1024, n_planes, max_N, n_halo)
    halo_mask_batch,      # (1024, n_planes, max_N)
    source_params_batch,  # (1024, n_source)
    grid, psf_kernel, scaling_matrix, exposure_time, background_sky,
    keys,                 # (1024,)
)
# images shape: (1024, H, W)
```

### LOSSampler → padded array conversion

The LOSSampler at `autolens/lens/los.py` produces a `List[ag.Galaxy]` per
realization. For the batched path, we need a helper that converts many
realizations into padded arrays:

```python
def los_realizations_to_arrays(
    realizations: List[List[ag.Galaxy]],
    max_halos_per_plane: int,
    n_planes: int,
    plane_redshifts: np.ndarray,
):
    """Convert a batch of LOSSampler outputs to padded arrays.

    Returns:
        halo_params: (batch, n_planes, max_halos_per_plane, n_params)
        halo_mask: (batch, n_planes, max_halos_per_plane)
    """
    ...
```

This runs in numpy (outside jit) and produces the fixed-shape arrays that
feed into the vmapped function. The LOSSampler itself doesn't need to change.

### Memory considerations

1024 images of size 100x100 at float32 = 1024 * 100 * 100 * 4 bytes = ~40 MB.
Fine for any GPU. But the intermediate arrays (per-halo deflections across all
batch elements) can be larger: 1024 * max_N * M * 2 * 4 bytes. For max_N=200
and M=10000 grid points, that's ~16 GB — may exceed GPU memory.

Mitigation strategies:
- Process in sub-batches (e.g. 128 at a time) and concatenate results
- Reduce max_N by using separate halo types per plane (most planes have
  few halos; only the lens plane has many subhalos)
- Use `jax.checkpoint` to trade compute for memory on the scan steps

Include a utility that estimates peak memory for a given configuration and
suggests a batch size.

### What varies vs what's shared across the batch

For the issue author's use case (fixed lens macro, varying substructure):

| Input | Varies? | Notes |
|-------|---------|-------|
| macro_params | Maybe | Could be fixed or sampled |
| halo_params | Yes | Different SHMF draw per realization |
| halo_mask | Yes | Different N per draw |
| source_params | Maybe | Could be fixed or sampled |
| grid | No | Same image grid |
| psf_kernel | No | Same instrument |
| scaling_matrix | No | Same redshift planes (if plane structure is fixed) |
| prng_key | Yes | Different noise per realization |

If the plane redshift structure also varies between realizations (different
LOS plane redshifts per draw), then `scaling_matrix` would need to be batched
too. But the issue author mentions 8 fixed planes, so it's likely shared.

## Integration test

Verify batch consistency:

```python
# Single-image results
images_single = [simulate_substructure(p, h, m, s, ..., k)
                 for p, h, m, s, k in zip(params...)]

# Batched results
images_batch = batched_simulate(params_stacked..., keys)

# Must match
for i in range(batch_size):
    assert jnp.allclose(images_single[i], images_batch[i], atol=1e-6)
```

Also benchmark: measure wall-clock time for 1024 sequential calls vs one
batched call. The batched version should be significantly faster (the whole
point).

Put tests in `autolens_workspace_test/scripts/jax_substructure/`.

## Scope boundaries

- This is the final prompt in the series. After this, the user has a complete
  `vmap(jit(simulate))(thetas, keys)` path.
- If memory is a hard constraint, the sub-batching utility is sufficient —
  don't try to implement gradient checkpointing in this prompt.
- The LOSSampler conversion helper is simple numpy reshaping, not a refactor
  of the sampler itself.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
