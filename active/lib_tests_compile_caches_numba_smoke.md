# Cache the compile work in library CI: JAX + numba caches for lib-tests.yml, and a numba cache for smoke-tests.yml

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: glance
Witness: the PyAutoHeart wiring test for the lib-tests/smoke-tests cache steps passes, and the first post-merge daily rows in `timings/unit/<repo>.jsonl` and `timings/scripts/<repo>.jsonl` carry `cache.numba` = `hit` on the second `main` run
Review-minutes: 3
Unattended: ready
Filed: 2026-09-06
Issued: 2026-09-06

Census option O1 of the ci-timing-fast-tests epic (PyAutoHeart
`timings/unit_import_census_2026-09.md` §6), widened by one finding made while
reading the workflows afterwards.

**What the record says.** Library CI is compile-bound: `lib-tests.yml` (the
reusable workflow every PyAuto* library `Tests` gate calls `@main`) restores no
JAX compile cache and no numba cache. Ten of PyAutoArray's 25 slowest CI tests
are 24.8 s of a 101 s leg cold-numba and ≤ 0.02 s warm; a persistent JAX cache
halves the local PyAutoArray suite 43 → 21 s (census §5.3). Across six library
repos × two Python legs this is the largest single measured number in the
census.

**The widening.** The census states that `smoke-tests.yml` "has both since
phase 7". It does not: phase 7 (PyAutoHeart#211) added `actions/cache` for the
JAX compile cache and the simulated datasets only. `NUMBA_CACHE_DIR` is set to
`/tmp/numba_cache` (smoke-tests.yml ~line 289/327) and nothing restores or saves
it, so every smoke run compiles numba cold — the exact cold-numba term phase 8
found inflating three user-workspace scripts 4–6× and misattributing the
local-vs-CI gap.

**Do.**
1. In `lib-tests.yml`: restore/save a JAX compile cache and a numba cache with
   the same discipline `smoke-tests.yml` already uses — `actions/cache/restore`
   + `actions/cache/save`, run-id-suffixed keys with a prefix `restore-keys`
   (accumulating superset), keyed on `(runner.os, python leg, jaxlib version,
   PYAUTO_CACHE_EPOCH)` for JAX and on `(runner.os, python leg, library HEAD
   sha of the repo under test + its dependency chain, epoch)` for numba (numba's
   cache index is keyed on source file mtime/contents, so a stale entry is a
   recompile, never a wrong answer — but say so in the comment). Set
   `JAX_COMPILATION_CACHE_DIR` and `NUMBA_CACHE_DIR` to explicit workspace
   paths in the pytest step env. Every new step `continue-on-error: true`;
   the pytest command byte-identical apart from env.
2. In `smoke-tests.yml`: add the numba cache beside the JAX one (same key
   shape; the chain SHAs are already computed in the `Resolve cache keys`
   step), and extend the `Record cache state` sidecar so `cache_state.json`
   carries `numba: hit|miss` next to `jax` and `datasets`. `smoke_timings`
   ingests the new field; the drift rule ("never compare two known but
   different cache states") extends to it; rows from before the field read
   `unknown` as today.
3. `unit_timings` rows: carry a `cache` field too (jax + numba hit/miss) from a
   sidecar in `lib-tests.yml`, so the unit-test baseline never compares a cold
   leg against a warm one — the same lesson phase 7 wrote for scripts.
4. Correct the census sentence in `timings/unit_import_census_2026-09.md` §5.3
   (append a dated note; the census is a record, do not rewrite its verdict).
5. Measure honestly: the deliverable is the workflow change plus a wiring test
   (step order, non-fatality, key components) like the one #211 added; the
   hot-vs-cold numbers land in `timings/unit/<repo>.jsonl` with the next daily
   run and are read back, not claimed. Remember GitHub cache scoping: a
   PR-branch save is invisible to `main`, so the first `main` run after merge
   misses and seeds; the hit shows on the run after.

**Guard.** Settings and caches only — the compile-time verdict of the closed
jax-compile-time arc is honoured exactly; no test, likelihood or sampler
changes. Keep `--xla_cpu_multi_thread_eigen=false` wherever it is set.

**Validation.** PyAutoHeart suite (`python3 -m pytest -q -n auto`); the wiring
test; a dispatched `lib-tests.yml` run on the branch (the workflow is consumed
`@main`, so the caller repos see it only after merge).
