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
