- summary: Search constructor kwargs that the A0b unknown-kwarg WARNING exposed as silently swallowed are fixed. PyAutoFit#1695 (7f36e16b6, `pending-release`): `test_autofit/graphical/hierarchical/test_optimise.py` drops the stray `dynamic_delta`/`delta` kwargs to DynestyStatic. autofit_workspace#170 (ade6c54af): `scripts/searches/mcmc.py` and `scripts/cookbooks/search.py` use `auto_correlation_settings`; `scripts/searches/nest.py` and the cookbook pass `nlive_init=50` to DynestyDynamic (the argument the installed class takes); the three notebooks regenerated, touched cells only. autofit_workspace_test#112 (e81faaf0b): `Emcee.py`/`Zeus.py` spelling fix, `DynestyDynamic.py` `nlive_init=50` in both calls (CRLF preserved), `Drawer.py` NullPaths workaround removed. Witness: every touched script runs under `PYAUTO_TEST_MODE=1` against released autofit 2026.10.12.1 with zero unknown-keyword warnings (before the fix each logged them). Behaviour change flagged in the PRs: the DynestyDynamic examples now really run with 50 initial live points instead of the silently used 500 default. Merged 2026-10-15 by human /prm, library first, under the recorded Heart RED development override.
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1695
- follow-up: none; the PyAutoFit claim is released, which unblocks `search-ext-a5-capmatrix-cards` (planned.md, PyAutoFit#1694).

## Original prompt

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
Status: formalised
Consequence: judge
Witness: running autofit_workspace `scripts/searches/{mcmc,nest}.py` and autofit_workspace_test `scripts/searches/{Emcee,Zeus,Drawer}.py` under `PYAUTO_TEST_MODE=1` against the installed autofit emits no unknown-kwarg WARNING; the two workspace notebooks are regenerated from the scripts; PyAutoFit `test_autofit/graphical/hierarchical/test_optimise.py` passes without the stray kwargs; the Drawer NullPaths workaround is gone.
Filed: 2026-10-08
Issued: 2026-10-15

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
