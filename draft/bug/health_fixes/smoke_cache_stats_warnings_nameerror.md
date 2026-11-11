# Smoke cache-stats step fails with NameError: warnings

Type: bug
Target: PyAutoHeart
Repos: @PyAutoHeart
Difficulty: easy
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Filed: 2026-11-11

## Evidence

`.github/workflows/smoke-tests.yml` ~line 777, in the `if: always()` /
`continue-on-error: true` cache-stats step, calls
`warnings.simplefilter("ignore", SyntaxWarning)` without importing `warnings`.
It came in with fe22b65 (#326, 2026-11-08), copied from the untimed-download
scanner step (which does import it). Every smoke run since then logs
`NameError: name 'warnings' is not defined` there (seen in autocti_workspace run
42883685928), and the cache-stats report is silently lost. Because the step is
`continue-on-error`, it never turns a run red.

## Repair scope

Remove the stray line (the step parses no workspace scripts), or import
`warnings` if it is needed. Extend `tests/test_workflow_wiring.py` so stdin
Python blocks in workflows are at least compiled and checked for undefined
names. Split out of PyAutoHeart#330 (the corrective arcticpy fix) to keep that
PR to a single scope.
