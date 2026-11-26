## grid-search-cores-auto
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1805
- completed: 2026-11-26
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1806
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1806
- epic: likelihood-lifecycle (R6 follow-up)

`GridSearch` now defaults to `number_of_cores="auto"`. The hang R6 avoided was in the `Process` job pool (shared with Sensitivity):
- a result that could not be pickled was dropped by `multiprocessing.Queue`'s feeder thread;
- a dead worker lost its job;
- workers stopping on `job_queue.empty()` raced the parent's feeder.

Fix: workers pickle each result themselves and queue a `JobError` on failure, stop on `StopCommand` sentinels, and the parent raises a `JobError` once every worker has exited with jobs still owed (it waits on sentinels, cancels the feeder join). An exception result now counts once instead of twice. A database-backed grid search runs its jobs in turn, because `DatabasePaths` drops its session on pickling.

Validation:
- full suite with JAX: 4403 passed; without JAX (uv venv): 4076 passed (both serial; the xdist `-n 6` failures came from tests sharing output folders);
- new `test_process_pool.py` with a SIGALRM guard;
- 4 workspace grid scripts pass in test mode (subhalo detect took `"auto"`, 12 cores);
- ci-verdict GREEN.

Follow-up: run `HPCPullPyAuto` (human-approved) so the shared RAL install picks this up.

## Original prompt

# GridSearch hangs with number_of_cores="auto"

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: low
Status: active
Issued: 2026-11-26
Consequence: judge
Epic: likelihood-lifecycle
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-26

## Context

R6 (PyAutoLabs/PyAutoGalaxy#759, PyAutoFit#1800) flipped every search's default to `number_of_cores="auto"` except `GridSearch`. With `"auto"`, the PyAutoFit test suite hung inside the grid search's own `Process` job pool (`autofit/non_linear/grid/grid_search/__init__.py`, with a `MockMLE` sub-search), also with JAX absent. Human ruling 2026-11-26: keep `GridSearch` at 1 for now and file this bug.

## Ask

Find why the nested job pool hangs when the grid search resolves `"auto"` (likely the parent pool and per-job sub-search pools both taking all cores, or a fork/pickling deadlock), make `"auto"` safe (e.g. resolve the grid-level count once and force sub-searches to 1), then flip `GridSearch`'s default to `"auto"` with a test that would have hung.
