# Drawer crashes under NullPaths: `self.timer` is None when `_fit` records time

Type: bug
Target: autofit
Repos:
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

Running `af.Drawer` with no output path (`NullPaths`, the default when `paths` is omitted) raises
`AttributeError: 'NoneType' object has no attribute 'time'` from `Drawer._fit`
(`autofit/non_linear/search/mle/drawer/search.py:147`, `"time": self.timer.time`). Under NullPaths the
search's timer is `None`. Every other search survives NullPaths. Found 2026-10-08 while writing
`autofit_workspace_test/scripts/searches/Drawer.py` (A0c part 1), which writes to `output/searches/Drawer`
to dodge it and says why.

## Fix

Guard the timer read (record `None`/skip the key when `self.timer is None`) or give NullPaths searches a
timer like the others; add a unit test that runs Drawer with default paths. Fold into A0b (search hygiene)
or ship alone. When fixed, drop the workaround and its comment from the workspace_test `Drawer.py`.

## Original request (verbatim)

Reported by the A0c part 1 implementation worker; no human words yet.
