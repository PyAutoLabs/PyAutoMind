# Unit-test and import timing go live by ingestion — no cron, no new cloud leg

PyAutoHeart#207 → `cb1d500`, closing PyAutoHeart#206, merged 2026-09-05 on
branch `claude/ci-test-timing-epic-ke2lul`. Phase 3 of the
`ci-timing-fast-tests` epic (`draft/feature/pyautoheart/ci_timing_fast_tests_epic.md`).
Fable-planned on the issue (the epic ledger's review had already recorded
"ingestion-first" as the default), implemented by an Opus subagent under the
Brain's delegation ladder from a web session (issue, PR and merge through the
GitHub MCP surface; no task worktree).

- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/206
- completed: 2026-09-05
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/207

## What shipped

- **The execution home is ingestion.** Every library's `Tests` workflow
  (PyAutoNerves, PyAutoFit, PyAutoArray, PyAutoGalaxy, PyAutoLens, PyAutoCTI)
  is a thin caller of the Heart's reusable `lib-tests.yml`, which already
  installs the source stack and runs pytest on every push and PR — so one
  change there emits the dataset for all six, and no daily job has to
  source-install five libraries to measure them.
- **`lib-tests.yml`** (`unittest` matrix job only): a `continue-on-error`
  step times a **fresh-process** `import <package>` (`seconds: null` on
  failure, never a fabricated 0; the returncode travels with it), pytest gains
  `--junitxml` (built-in, every test, no console scraping), both uploaded as
  `unit-timings-<py>` with `if: always()` / `if-no-files-found: ignore` and no
  retention cap. The `unittest-nojax` job is untouched.
- **`heart/checks/unit_timings.{sh,py}`** — the sixth cloud-safe check, in
  the `smoke_timings` shape (`select_artifacts` is shared, parametrised by
  name pattern). Per library repo and leg: suite wall-clock and counts, the 25
  slowest tests (`top_n`), import seconds. Test drift: both gates (≥2.0× AND
  ≥2 s vs the previous recorded run of the same test; run id must differ).
  Import drift: the existing `import_time` doctrine — ratio to the median of
  the last 7 recorded runs, `building` until 3 samples, 1.5×/3.0×
  yellow/red. Rows carry `/hygiene perf` prompts (the hygiene conductor owns
  dev-loop cost).
- **The dead board sections come alive unchanged.** The check also writes
  `unit_test_timing.json` and `import_time.json` in exactly the shapes the
  dev-box checks produce (`python: "ci"`), so "Unit-test timing" and "Import
  timing" render as designed and gain per-leg detail lines. `import_time`,
  `unit_test_timing` and `workspace_testmode_timing` left `LOCAL_ONLY_FAMILIES`
  and `UNOBS_WATCHES`.
- **`workspace_testmode_timing` retired from the board** as superseded: the
  smoke gates already run the workspace scripts in `PYAUTO_TEST_MODE=2` with
  small datasets on every PR, and the Smoke scripts row (#203) is that
  measurement. The module stays runnable on demand; its docstring says so.
- **Record**: `timings/unit/<repo>.jsonl` (one line per python leg × run id:
  suite totals, the slowest tests, import seconds), same append-only and
  run-id dedupe rules; `heart.timings append --unit-timings`; `performance.unit`
  is an additive `board.json` key emitted only when observed.
- Tests 767 → 841 (48 in `test_unit_timings.py`, 5 in
  `test_lib_tests_wiring.py`, 2 shell tests with stub `gh`/`unzip`); one
  existing census assertion widened for the two new census keys; fake names
  throughout; tenant firewall OK.

## Key traps / findings

- **Look for the reusable workflow before planning a cloud leg.** The phase
  prompt offered "a dedicated workflow leg with the source-installed stack" as
  one of two options; the cheaper one only became obvious on reading a
  library's `main.yml`, which is eleven lines of `uses:
  PyAutoLabs/PyAutoHeart/.github/workflows/lib-tests.yml@main`. The Heart
  already owned the place every library's tests run.
- **A reusable workflow referenced `@main` is a six-gate blast radius.** Every
  new step in `lib-tests.yml` is non-fatal (`continue-on-error`, `if: always()`,
  `if-no-files-found: ignore`) and the pytest exit path gained one flag and
  nothing else. A wiring test pins it.
- **The package name reaches the heredoc through the environment**, never a
  `${{ }}` expansion inside the Python source — an expansion there is
  substituted before Python parses the line.
- **Legacy summaries as projections.** One producer, three files: the rollup
  plus the two summary shapes the existing sections read. The dev-box checks
  keep writing the same shapes, so the board cannot tell the vantages apart
  except by the honest `python: "ci"` field.
- **Import baselines need a window, not a previous run.** An import is a few
  seconds and jitters; the median-of-7 with a 3-sample floor is the existing
  `import_time` doctrine, kept verbatim so a ratio means the same thing from
  either vantage. The first three CI runs therefore render `building`, which
  is the truth, not a bug.

## Follow-ups (tracked, not started here)

- Phase 4 of the epic: `draft/test/pyautoheart/legacy_baseline_timing_round.md`
  — the labeled LEGACY snapshot + digest, no earlier than the day after a live
  heart-health run has seeded `timings/`; it writes `timings/epochs.jsonl`.
- Per the epic ledger's review, phase 7 (CI caches) follows phase 4, before
  the rebuild waves.
- The `HEART_TIMINGS_TOKEN` secret if the first live run shows the library
  repos as unavailable (cross-repo artifact 403 — same caveat as #203).

## Original prompt

# Bring the dead timing legs live: unit_test_timing, import_time, workspace_testmode_timing

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: ci-timing-fast-tests
Phase: 3
Issued: 2026-09-05

Bring the dead timing legs live: unit_test_timing, import_time, workspace_testmode_timing on a real schedule.

Three Heart checks are built, tested, and documented as "OFF-TICK, run on a daily cron" —
but no cron exists anywhere (not in `tick.sh`, `daemon.sh`, `bin/`, nor any workflow):
`heart/checks/unit_test_timing.py` (pytest --durations over the 5 libraries; state dir has
0 files, never run), `heart/checks/import_time.py` (ran once 2026-07-11, only 4 packages,
autolens "unavailable"), `heart/checks/workspace_testmode_timing.py` (never run). The
dashboard sections for them exist (`heart/dashboard.py:626-672`) and render "not observed".

Decide the execution home and wire it: either a scheduled cloud job (these run local
suites — a dedicated workflow leg with the source-installed stack) or ingestion of CI
`pytest --durations` output from the libraries' own CI runs, whichever is cheaper to keep
honest. Fix the import_time coverage (all installed packages incl. autolens — recent work
already reduced autolens import time, so the check should now pass and become the
regression guard for it). Their observations join the phase-2 durable history and the
board sections come alive: unit-test run-time stats with slowest-test bottlenecks
highlighted, and import times per package — the "what generally drives run time" surface
the user asked for.
