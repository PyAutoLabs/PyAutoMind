# Clear stale NEEDS_FIX parked-script markers

**Work type:** maintenance (workspace hygiene)
**Targets:** @autofit_workspace @autogalaxy_workspace @autolens_workspace @autolens_workspace_test

## Original request (verbatim)

"what are the 58 stale parked scripts we can prob clear a lot of them" →
"yeah i think some will already be fixed but let's sort them" → un-park 4 +
reclassify 2, ship via ship_workspace PRs.

## Context

`autobuild/slow_skip_check.py` surfaces `NEEDS_FIX`/`SLOW` markers in each
workspace's `config/build/no_run.yaml`. Live scan = 30 parked / 17 stale (the
"58" in the 2026-07-20 readiness snapshot was itself stale). The 6 NEEDS_FIX
markers were investigated by reproducing each on clean `main` under the faithful
harness mode `PYAUTO_TEST_MODE=2`.

## Findings (all reproduced 2026-07-21)

| Script | Parked reason | Verdict |
|--------|---------------|---------|
| autofit_workspace `features/interpolate` | IndexError @ t=1.5 | FIXED (exit 0) |
| autogalaxy_workspace `imaging/modeling` | KeyError after API drift | FIXED (exit 0) |
| autolens_workspace `group/slam` | PriorException upper<lower | FIXED (exit 0) |
| autolens_workspace_test `database/scrape/general` | `__hash__` TypeError | FIXED (exit 0) |
| autolens_workspace_test `jax_likelihood_functions/imaging/delaunay_mge` | "timeout in benchmark" | MISLABELED — SLOW, not a bug |
| autolens_workspace_test `jax_likelihood_functions/imaging/mge_group` | "timeout in benchmark" | MISLABELED — SLOW, not a bug |

## Plan

1. Un-park the 4 verified-fixed scripts: delete the `# NEEDS_FIX …` markers from
   each workspace's `config/build/no_run.yaml` so the scripts run in validation.
2. Reclassify the 2 JAX-benchmark entries `NEEDS_FIX` → `SLOW` (date 2026-07-21,
   honest 1800s-cap reason) — they are legitimately slow, not broken.
3. Ship each affected workspace via `ship_workspace` (branch + PR per repo).

Leaves NEEDS_FIX at 0 stale. The 24 SLOW markers (11 stale) are out of scope —
genuinely slow-by-design, tracked separately (Heart#72/#74).

**Autonomy:** human-required
