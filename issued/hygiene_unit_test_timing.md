# PyAutoHeart — unit_test_timing leg (hygiene perf phase 4a)

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 4a of the hygiene `perf` mode — the first of three capabilities from the
original hygiene prompt that the shipped perf mode (import timing only) does NOT
yet cover. This one: **unit-test speed** — time the library unit suites, track a
rolling per-test (and per-suite) baseline, flag slow-test regressions, and let
hygiene `perf` surface + route them. Mirrors the shipped `import_time` leg
(PyAutoHeart#62): a tracked signal lives in Heart; hygiene acts.

**Research grounding (2026-07-11):** there is **no** unit-test-timing
infrastructure today. No `--durations` in any library pytest config
(`[tool.pytest.ini_options]` in each `pyproject.toml` sets only `testpaths` +
`filterwarnings`). Heart's `test_run` leg reads PyAutoBuild `report.json`, which
carries pass/fail counts + `slow_skips`/`needs_fix_skips` — **not per-test
durations**. So this is greenfield.

**Design decision to settle first — "run it" vs "read it":**
- **(a) Read, don't run (preferred, mirrors script_timing).** Add
  `--durations=0 --durations-min=<X>` (or a JSON-durations plugin) to the CI
  test job's pytest invocation so CI **emits** per-test durations into an
  artifact; a stdlib-only Heart check parses that artifact, keeps a rolling
  baseline, classifies. Cheap in the tick; the heavy pytest run already happens
  in CI. This is the script_timing architecture ("read produced data").
- **(b) Off-tick self-run.** A Heart check that runs `pytest --durations` per
  library in a **subprocess** (rule 4 — never import the test stack into Heart;
  inject the runner so the stdlib-only tests use fixtures). Running the full
  suites is minutes (test_autofit ~1471 tests) → strictly **off-tick** (daily
  cron / on demand), like `import_time`. Simpler to own, heavier to run.

Recommended: **(a)** if the CI surface is easy to extend (cheapest, always
fresh); fall back to **(b)** otherwise. Settle in the plan.

**Build (whichever source):**
- `heart/checks/unit_test_timing.py` — rolling per-test baseline in
  `~/.pyauto-heart/timings-unit/`, ratio-vs-median classification (reuse the
  1.5/3.0 `script_timing` thresholds pattern, config-driven), writes
  `~/.pyauto-heart/unit_test_timing.json`, colored summary. **Advisory** —
  surfaced on the dashboard (a local-only family, mirror the `import_time`
  section in `heart/dashboard.py` + `heart/state.py` aggregate) but **absent
  from the readiness gating set** (test speed is not release-blocking).
- stdlib-only tests (`tests/test_unit_test_timing.py`) with an injected
  duration source — never run pytest-in-pytest or import the science stack.
- **PyAutoBrain follow-on:** wire hygiene `perf` to read
  `unit_test_timing.json` when present (surface slowest/regressed tests, route
  to `/refactor`/`/bug`), fallback silent when absent — exactly as PyAutoBrain#93
  did for `import_time`.

**Boundary:** this is developer-loop cost (unit-suite speed), squarely hygiene —
distinct from `/profiling` (likelihood/modeling compute on the science grid) and
from `test_run` (pass/fail release signal). Slow-test *regressions* route to
`/refactor`; a genuinely-slow-but-correct test may just be marked (a `slow`
pytest marker) rather than optimized — judgement, surfaced not forced.

**Done when:** a `unit_test_timing` signal exists with a rolling baseline +
regression classification, surfaced advisory on the board, tests green, and
hygiene `perf` reads it. Siblings: [[hygiene_workspace_testmode_timing]] (4b),
[[hygiene_function_profiling]] (4c).

<!-- filed 2026-07-11 from the hygiene perf-scope reopening: the shipped perf
     mode covers import timing only; unit-test timing was in the original prompt
     and is unbuilt. Phase 4a of 3. -->
