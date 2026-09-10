## smoke-jax-cache-threshold
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/221 (closed 2026-09-10)
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/222 (merged 30af9f9e -> main; branch head b1afb3e7)
- completed: 2026-09-10

### What shipped

`PyAutoHeart/.github/workflows/smoke-tests.yml`, the reusable workflow every
workspace's smoke gate calls `@main`, restored and saved a JAX compilation
cache but set no compile-time threshold, so `autonerves/jax_wrapper.py`'s
`setdefault("JAX_PERSISTENT_CACHE_MIN_COMPILE_TIME_SECS", "1")` won (it
mirrors JAX's own 1.0s default) and only executables that took over a second
were ever persisted. The smoke scripts are hundreds of sub-second compiles
each, so a `cache_jax: HIT` leg held 1-4 entries and every run re-paid the
compile — the reason the board showed HIT beside cold-run numbers.

The runner step's `env:` now carries `JAX_PERSISTENT_CACHE_MIN_COMPILE_TIME_SECS:
"0"` immediately after `JAX_COMPILATION_CACHE_DIR`, so every script subprocess
inherits it (the runner copies the job env). The `run:` body is byte-identical
(a workspace owns its runner; the wiring test pins that). One new wiring test,
`test_the_runner_persists_every_compile_it_makes`, asserts the key, its exact
value `"0"`, and the untouched command. No `PYAUTO_CACHE_EPOCH` bump: the
restore-keys prefix still matches the existing entries and the next save is
the superset. Heart suite 966 passed; CI green on both legs.

Measured locally under the smoke profile before shipping (from the prompt):
autolens `imaging/jax_likelihood/delaunay.py` 23.4-27.1s -> 10.4-10.5s (2 -> 513
entries); autolens `misc/jax_assertions/delaunay_nn.py` 27.2-27.8s -> 13.0-13.5s
(4 -> 299); autogalaxy `interferometer/jax_likelihood/delaunay_mge.py`
30.5-31.3s -> 18.1-18.4s (1 -> ~490). Printed output byte-identical across
both regimes — the threshold governs which executables are persisted, never
what is compiled.

### The trade, and why it merged without measuring it first

The prompt called the cache-artefact growth (~500 entries / ~3 MB per JAX
script, per workspace, per Python leg) a human's call. It cannot be measured
before merge: workspaces call the workflow `@main`, and Heart's own CI on the
PR runs only the wiring tests. The human priced it by typing `/prm`. The
observation point is the board's per-repo `[jax cache hit|miss]` lines and
`cache_state.json`'s `jax_mb` / `jax_n` before/after; rollback is deleting the
one line, or bumping `PYAUTO_CACHE_EPOCH` to drop the fat caches.

### Key traps / findings

- **A preset value wins.** `autonerves` uses `os.environ.setdefault`, and its
  own `test_min_compile_time_respects_preset_value` covers it — so the
  workflow env is the right layer and needs no Nerves change.
- **"Exactly 0", not "small".** `delaunay_nn_caps.py` clears the 1.0s threshold
  by under 10% on four of six compiles; any nonzero threshold leaves a faster
  runner able to silently drop a compile below it with no code change. The
  test asserts the literal `"0"` for that reason.
- **The `cache_jax: HIT` column was true and useless** under the 1s regime:
  a hit on a 1-4 entry cache. The sidecar's `jax_n` is the number that says
  whether the cache holds anything.
- Shipped from a web session (no `gh`, no task worktree): PyAutoHeart was
  outside the session's initial repo scope and was attached with `add_repo`;
  the shallow single-branch clone hides the pushed branch from `git status`
  until the branch is added to `remote.origin.fetch` — the stop hook's
  "unpushed commit, no remote branch" was that, not a missing push.

### Follow-ups — done the same day, on the human's ask

- The per-script overrides were never on `main`: they sat in two open
  `/ci_speedup` PRs, autolens_workspace_test#314 and autogalaxy_workspace_test#121.
  Both closed unmerged as superseded (#314's other half, the `test-results/`
  gitignore, had already landed as #313).
- `lib-tests.yml`: PyAutoHeart#223 exports the same `"0"` in the unit gate's
  `Run tests` step, with a wiring test; merged 6afdbd4c -> main (2026-09-10). Unmeasured —
  same mechanism, priced by the same board sidecar.

### Follow-ups as first written (superseded by the block above)

- autolens_workspace_test / autogalaxy_workspace_test `profile_smoke.yaml`: the
  three per-script `JAX_PERSISTENT_CACHE_MIN_COMPILE_TIME_SECS` overrides from
  `/ci_speedup` (2026-09-10) are now redundant; harmless while they stay.
- `lib-tests.yml` (the libraries' unit gate) restores the same cache with the
  same missing threshold — a separate pricing, since its suites are a
  different compile profile.

## Original prompt

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
Issued: 2026-09-10
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/221

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
