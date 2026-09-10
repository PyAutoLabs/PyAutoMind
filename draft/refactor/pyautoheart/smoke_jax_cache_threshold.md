# Set `JAX_PERSISTENT_CACHE_MIN_COMPILE_TIME_SECS=0` for the whole smoke leg

Type: refactor
Target: pyautoheart
Repos:
- PyAutoHeart
Themes:
- performance
- ci
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 15
Unattended: ready
Filed: 2026-09-10

`/ci_speedup` (2026-09-10) fixed this per-script for the three slowest JAX smoke
entries. **The general fix is one line, and it is a human's call because of what
it does to the cache artefact.**

## The finding

PyAutoHeart's reusable `smoke-tests.yml` restores/saves `.pyauto_jax_cache` and
exports `JAX_COMPILATION_CACHE_DIR`, but **sets no compile-time threshold**.
JAX's default `jax_persistent_cache_min_compile_time_secs` is **1.0s**
(`jax/_src/config.py:1500`), and `autonerves/jax_wrapper.py` `setdefault`s the
same, so only executables taking longer than a second are ever written to disk.

The JAX smoke scripts are made of *many small* compiles, so almost nothing is
cached and CI re-pays the compile on every run. This is why the board shows
`cache_jax: HIT` beside numbers that match a cold run — the cache it hits holds
1–4 entries.

Measured, cache built and read under each regime (local, smoke profile):

| script | threshold 1.0 (CI today) | threshold 0 | cache entries |
|---|---|---|---|
| autolens `imaging/jax_likelihood/delaunay.py` | 23.4–27.1s | **10.4–10.5s** | 2 → 513 |
| autolens `misc/jax_assertions/delaunay_nn.py` | 27.2–27.8s | **13.0–13.5s** | 4 → 299 |
| autogalaxy `interferometer/jax_likelihood/delaunay_mge.py` | 30.5–31.3s | **18.1–18.4s** | 1 → ~490 |

Compile censuses (`JAX_LOG_COMPILES=1`): 504 executables / 471 cold; 312 / 308
under 1s; 507 with exactly 1 over the threshold.

## Why it is not already done

Three per-script overrides shipped instead (autolens + autogalaxy
`profile_smoke.yaml`, 2026-09-10). Hoisting to `defaults:` or into
`smoke-tests.yml` would pay on **every** `jax_likelihood`/`jax_grad` script in
the leg — but it grows the saved cache artefact by roughly **500 entries /
~3 MB per script**, across two workspaces and both python legs. That is a
cache-size and restore-time trade a human should price, not an agent.

## Not a correctness risk

The threshold governs which XLA executables are persisted, not the graph,
dtypes, backend or arithmetic. A cache hit returns the executable the compiler
would have built. Printed output was diffed byte-for-byte across both regimes on
all three scripts; RC=0 throughout.

## Caveat worth carrying

`misc/jax_assertions/delaunay_nn_caps.py` is genuinely threshold-insensitive
(17.0s vs 15.1s) because four of its six compiles take 1.048–1.094s — they clear
1.0s by under 10%. A faster runner would silently drop them below the threshold
and the script would regress with no code change. That fragility is an argument
for setting the threshold globally rather than per-script.
