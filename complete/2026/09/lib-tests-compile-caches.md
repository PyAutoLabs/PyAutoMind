# JAX + numba caches in library CI, a numba cache in the smoke gate, and the content-stamped mtimes that make numba hit

PyAutoHeart#217 → `af03c75`, closing PyAutoHeart#215, merged 2026-09-07. Census option O1
of the `ci-timing-fast-tests` epic, widened by one finding: `smoke-tests.yml` cached JAX
and datasets only — numba sat at `/tmp/numba_cache` with no restore and no save. Fable-planned
from a web session (no task worktree); implemented by an Opus subagent under the delegation
ladder; no library source changed.

- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/215
- completed: 2026-09-07
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/217

## What shipped
- `lib-tests.yml` (`unittest` job only): job-level `PYAUTO_CACHE_EPOCH`, JAX compile cache
  per (OS, py leg, jaxlib), numba cache per (OS, full python version), the `cache_state.json`
  sidecar riding the existing `unit-timings-<py>` artifact, saves gated on a measured change
  and saving on red too; every new step `continue-on-error`, the pytest command byte-identical
  apart from env. `unittest-nojax` untouched (its wiring test asserts that).
- `smoke-tests.yml`: the numba cache beside the JAX one, the runner's `NUMBA_CACHE_DIR` moved
  under the workspace, a `numba` section and `numba_changed` in the recorder.
- Both workflows stamp every source `.py`'s mtime from a hash of its content before anything
  compiles.
- Ingest/record/board: `numba` in the sidecar parse (absent section → `unknown`), unit legs and
  `timings/unit/<repo>.jsonl` lines carry `cache: {jax, numba}`, scripts lines gain `numba`, the
  unit drift rule refuses two known but different combined states (`heart.timings.unit_cache_state`,
  carried as `cache_state`), the board brackets the state on both line kinds. README schemas
  updated; a dated correction appended to the census §5.3. Tests 893 → 924.

## Key traps / findings
- **numba stamps each cache entry with its source file's `(st_mtime, st_size)`** and stores it
  under `<parentdir>_<sha1(abs dirname)>`. A fresh clone or `pip install` gives every `.py` a new
  mtime, so a plain `actions/cache` on the numba dir would restore and miss every entry. Setting
  the mtime to a function of the content hash turns the stamp into a content fingerprint, makes
  the prefix `restore-keys` fallback safe and lets the numba key carry no library commit.
- GitHub cache scoping: a PR-branch save is invisible to `main`, so every 2026-09-06 record row
  read `miss`; the first `main` run after merge seeds and the second hits. The first same-branch
  hot-vs-cold data point from the Actions API: autolens_workspace_test runner 397 → 334 s
  (py3.12) and 383 → 320 s (py3.13), ~16%, dataset save skipped on the warm run.
- A unit leg's `cache_view` reads `datasets: "miss"` for a cache that workflow does not have;
  contained (the unit record and line carry jax + numba only), flagged on the PR.

## Follow-ups
- Read the hot-vs-cold numbers back from `timings/unit/<repo>.jsonl` and
  `timings/scripts/<repo>.jsonl` after two daily runs, and confirm the numba stamp is hitting
  (`entries_before` > 0 on the second `main` run). If numba still misses, the site-packages path
  (which carries the patch version, hence `pyfull` in the key) or the stamp roots are the first
  things to check.

## Original prompt

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
