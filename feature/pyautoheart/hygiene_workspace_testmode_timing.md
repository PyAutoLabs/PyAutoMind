# PyAutoHeart — workspace test-mode script-timing leg (hygiene perf phase 4b)

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 4b of the hygiene `perf` mode — the second uncovered capability from the
original hygiene prompt: **workspace-script speed in integration test mode**
(`PYAUTO_TEST_MODE=2` + `PYAUTO_WORKSPACE_SMALL_DATASETS=1`). Run the curated
workspace scripts in that mode, time them, track a rolling baseline, flag
regressions, and let hygiene `perf` surface + route them.

**Research grounding (2026-07-11):**
- Heart's `script_timing` leg **already** tracks per-script `duration_seconds`
  — but from PyAutoBuild `run_all`, which runs scripts with `env =
  os.environ.copy()` (`autobuild/run_all.py`): it inherits whatever mode **CI**
  sets and is the release/validation path, **not** an explicit, hygiene-controlled
  `PYAUTO_TEST_MODE`+`SMALL_DATASETS` run. So test-mode timing is a **distinct**
  signal, not what `script_timing` observes.
- The exact env + curated-script pattern already exists in the `cli_noise_clean`
  skill (`PYAUTO_TEST_MODE=2 PYAUTO_WORKSPACE_SMALL_DATASETS=1
  NUMBA_CACHE_DIR=… MPLCONFIGDIR=…`, per-workspace `start_here` scripts) — reuse
  it. Each workspace also has a curated `smoke_tests.txt` to source the list
  from (do **not** grow those lists — the smoke-subset doctrine).

**Design decision to settle first:** extend `script_timing` with a **test-mode
profile** (a second baseline keyed by mode) vs a **new sibling leg**
`workspace_testmode_timing`. Prefer the sibling leg for a clean boundary
(different mode, different cadence, hygiene-owned) unless sharing `script_timing`'s
slug/rolling machinery is clearly cheaper. Either way the *runner* is off-tick.

**Build:**
- The measurement runs the curated scripts in a **subprocess** with the test-mode
  env (rule 4 — Heart never imports the science stack; inject the runner so the
  stdlib-only tests use fixtures). Running scripts costs seconds–minutes →
  strictly **off-tick** (daily cron / on demand), like `import_time`. Honour a
  per-script timeout; a timeout is a finding, not a crash.
- `heart/checks/workspace_testmode_timing.py` — rolling baseline in
  `~/.pyauto-heart/timings-ws-testmode/`, ratio classification (1.5/3.0),
  writes `~/.pyauto-heart/workspace_testmode_timing.json`, colored summary.
  **Advisory** dashboard section (local-only family; mirror `import_time` in
  `state.py` + `dashboard.py`), **not** in the readiness gating set.
- stdlib-only tests with an injected runner (never execute real workspace
  scripts in the suite).
- **PyAutoBrain follow-on:** hygiene `perf` reads
  `workspace_testmode_timing.json` when present, surfaces regressed scripts,
  routes to `/refactor`/`/bug`; fallback silent when absent (as PyAutoBrain#93).

**Boundary:** developer-loop cost (dev-mode script wall-clock) — hygiene, not
`/profiling` (likelihood/modeling compute) and not autobuild's release-mode
`script_timing`. A slow script whose cost is a genuine dataset/model choice is
marked, not force-optimized (judgement).

**Done when:** a test-mode workspace-timing signal exists (rolling baseline +
regression), surfaced advisory, tests green, hygiene `perf` reads it. Siblings:
[[hygiene_unit_test_timing]] (4a), [[hygiene_function_profiling]] (4c).

<!-- filed 2026-07-11 from the hygiene perf-scope reopening; phase 4b of 3.
     Distinct from the shipped script_timing leg (release mode) — this is the
     PYAUTO_TEST_MODE+SMALL_DATASETS run named in the original prompt. -->
