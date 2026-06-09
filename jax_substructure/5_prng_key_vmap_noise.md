Context: PyAutoLens issue #542 follow-up (Gap 1, deferred during the original
4-prompt substructure-simulator series). Prompt 3 (`3_simulator_jax_e2e.md`)
asked for a `prng_key` parameter on the Poisson-noise path so the OO
`SimulatorImaging` can be `vmap`-ed over a batch of noise keys. The standalone
`simulate_substructure` (now shipped in `autolens/lens/substructure_util.py`)
sidestepped this by calling `jax.random.poisson(prng_key, ...)` directly, so the
library function itself was never given the parameter. This prompt closes that
gap. Single-library change → `/ship_library`.

## Background

`PyAutoArray/autoarray/dataset/preprocess.py` (line ~455):

```python
def poisson_noise_via_data_eps_from(data_eps, exposure_time_map, seed=-1, xp=np):
    ...
    else:  # JAX path
        import jax.random
        effective_seed = seed if seed != -1 else int(time.time() * 1e6) & 0xFFFFFFFF
        key = jax.random.PRNGKey(effective_seed)
        noisy_eps_array = jax.random.poisson(key, image_counts) / exposure_time_map.array
```

The `PRNGKey` is derived *internally* from the integer `seed`. Two problems for
batched simulation:

1. `seed=-1` calls `int(time.time())`, which cannot be traced — `vmap` over a
   function that hits this fails.
2. Even with a fixed `seed`, every batch element would share one key (identical
   noise), because there's no way to pass a pre-split per-element key in.

The `xp=np` parameter and the internal-`PRNGKey(seed)` JAX branch were added
earlier by the `simulator-use-jax-pr2-imaging` task (see `complete.md`); this
prompt extends that same function with an explicit key input.

## What to build

### 1. `preprocess.poisson_noise_via_data_eps_from`

Add an optional `prng_key=None` parameter. On the JAX branch, a supplied
`prng_key` takes precedence over the seed:

```python
def poisson_noise_via_data_eps_from(
    data_eps, exposure_time_map, seed=-1, prng_key=None, xp=np
):
    ...
    if xp is np:
        # unchanged numpy path; prng_key is ignored (assert it is None if you
        # want to be strict, or just document that it is numpy-irrelevant)
        ...
    else:
        import jax.random
        if prng_key is not None:
            key = prng_key
        else:
            effective_seed = seed if seed != -1 else int(time.time() * 1e6) & 0xFFFFFFFF
            key = jax.random.PRNGKey(effective_seed)
        noisy_eps_array = jax.random.poisson(key, image_counts) / exposure_time_map.array
```

### 2. Thread it through the callers

- `preprocess.data_eps_with_poisson_noise_added` (line ~500): add
  `prng_key=None`, forward it to `poisson_noise_via_data_eps_from`.
- `autoarray/dataset/imaging/simulator.py` — `SimulatorImaging.via_image_from`
  (def line ~128, call site ~186-189): add `prng_key=None` and forward it to
  `data_eps_with_poisson_noise_added`. This is the minimum surface needed to let
  a caller `vmap` over keys via `via_image_from`.

Surfacing `prng_key` further up (`SimulatorImaging` constructor, or PyAutoLens
`via_tracer_from` / PyAutoGalaxy `via_galaxies_from` overrides) is optional — do
it only if it stays a clean pass-through. Keep the default `None` everywhere so
existing seed-based behaviour is byte-for-byte unchanged.

## Tests

**Unit tests stay numpy-only** (library convention — cross-xp checks live in
`*_workspace_test`, never in `test_autoarray`). In PyAutoArray, add a numpy-only
unit test that asserts the new `prng_key` parameter exists and is forwarded
(e.g. monkeypatch / spy that `poisson_noise_via_data_eps_from` receives the key
passed to `via_image_from`), and that the numpy path is unaffected when
`prng_key=None`.

The real validation — that `jax.vmap` over a batch of `prng_key`s produces
per-element-distinct noise and that `prng_key` overrides `seed` — belongs in a
new `autolens_workspace_test` (or `autoarray`-equivalent workspace) script, NOT
in the library unit suite. Add a small script that builds one noiseless image
and runs `jax.vmap(lambda k: poisson_noise_via_data_eps_from(..., prng_key=k, xp=jnp))(keys)`,
asserting the rows differ.

## Scope boundaries

- PyAutoArray only (plus the small workspace_test validation script). No change
  to the standalone `simulate_substructure` — it already passes `prng_key`.
- Default `None` preserves all existing seed-based call sites exactly.
- Do not refactor the broader noise/over-sampler machinery (prompt 3's Gap 2 was
  intentionally bypassed by going jnp-native in the standalone path).
