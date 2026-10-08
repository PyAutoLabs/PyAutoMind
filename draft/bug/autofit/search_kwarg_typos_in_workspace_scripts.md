# Search constructor typos silently ignored in workspace scripts (`auto_correlations_settings`, `nlive`, `dynamic_delta`)

Type: bug
Target: autofit
Repos:
- autofit_workspace
- autofit_workspace_test
- PyAutoFit
Themes:
- searches
Difficulty: small
Autonomy: safe
Priority: normal
Epic: search-extensibility
Status: draft
Filed: 2026-10-08

## Symptom

The unknown-kwarg WARNING added in A0b (PyAutoFit#1672) fires on existing scripts, showing that these settings have
always been silently swallowed by `**kwargs`:
- autofit_workspace `scripts/searches/mcmc.py:108,188` and autofit_workspace_test `scripts/searches/{Emcee,Zeus}.py:93`
  pass `auto_correlations_settings=` (the argument is `auto_correlation_settings`), so the autocorrelation settings
  shown to users never applied.
- autofit_workspace `scripts/searches/nest.py:106,190` pass `nlive=` to `DynestyDynamic`, which ignores it.
- `test_autofit/graphical/hierarchical/test_optimise.py:12` passes `dynamic_delta`/`delta` to `DynestyStatic`.
Also: autofit_workspace_test `scripts/searches/Drawer.py` carries a NullPaths workaround and comment that A0b makes
unnecessary.

## Fix

Correct the argument names (regenerate the two workspace notebooks), drop the test's stray kwargs, remove the Drawer
workaround. Verify no WARNING fires when the scripts run under `PYAUTO_TEST_MODE=1`. Workspace work after #1672 is
released (the warning itself is harmless before then).

## Original request (verbatim)

Found by the A0b implementation worker (search-extensibility); no human words yet.
