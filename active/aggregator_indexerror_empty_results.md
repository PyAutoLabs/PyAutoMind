# Aggregator scripts crash with IndexError (empty results) on release wheels

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Surfaced burning down the 2026-07-13 release-validation tail (PyAutoHeart#72). On the
release wheels under the release profile, both aggregator guide scripts fail fast with the
same error:

```
scripts/guides/results/aggregator/galaxies_fits.py        ... FAIL (13.8s) IndexError: list index out of range
scripts/guides/results/aggregator/samples_via_aggregator.py ... FAIL (4.5s) IndexError: list index out of range
```

`IndexError: list index out of range` = the aggregator queried results and got an **empty
list**, then indexed `[0]`. These run in `autolens_workspace` (a **user** workspace, so the
release profile is `PYAUTO_TEST_MODE=1` — reduced-iteration *real* sampler, NOT the `=0` case
that the database bug PyAutoFit#1368 fixed).

**Before assuming a new bug, VERIFY it still fails on current main** — the sibling bugs
`minimal_output.py` and the `modeling_visualization_jit` scripts turned out to be the *same*
`PYAUTO_TEST_MODE` output-misrouting root cause fixed by PyAutoFit#1368 (`is_test_mode()`
replacing string-truthy `PYAUTO_TEST_MODE`). This aggregator failure is at `TEST_MODE=1`
(not `=0`), so #1368 may not cover it — but confirm first. Reproduce under the release
profile (`autolens_workspace/config/build/env_vars_release.yaml`, `PYAUTO_TEST_MODE=1`) from
the `autolens_workspace` checkout on current main; the aggregator reads the output of a prior
modeling run, so ensure that prerequisite output exists (or that the release-validation job
order produces it) — the empty-list may be a **missing/misrouted prerequisite output** rather
than an aggregator bug.

If it reproduces: get the full traceback (which list is empty — searches? samples? galaxies?)
and fix the producer (the missing output, or the query that returns empty), not the `[0]`
access ([[feedback_no_silent_guards]]). Likely in `autofit.database`/aggregator or the
workspace script's assumption about available results. Release run: PyAutoHeart
workspace-validation `29279095224`, TestPyPI `2026.7.13.1.dev65601`. See
[[project_release_2026_07_13_blocked_3bugs]] and PyAutoHeart#72.
