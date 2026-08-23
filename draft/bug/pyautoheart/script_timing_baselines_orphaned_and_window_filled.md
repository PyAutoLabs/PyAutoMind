# Heart script_timing baselines are orphaned by path moves and filled with one repeated value

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-08-04 (backfilled from git)

Two independent defects in `PyAutoHeart/heart/checks/script_timing.py`, both found
while diagnosing the jax_grad smoke timeouts (PyAutoHands#226). Neither is fixed by
that task — it needed the baselines and found them unusable.

## 1. Slugs are path-derived, so any script move orphans its history

`slug_for()` (`heart/checks/script_timing.py:59`) builds the history filename from the
script's full workspace-relative path:

```
autolens_test__scripts__jax_grad__imaging_lp.json
```

The autolens_workspace_test #216 restructure moved `scripts/jax_grad/imaging_lp.py` to
`scripts/imaging/jax_grad/lp.py`. The slug changed with it, so:

- every pre-restructure baseline is stranded under a filename nothing writes to again,
- no new-layout slug exists for ANY of these scripts, so Heart has been accumulating
  **no** timing history for them since 2026-07-24,
- the regression check silently has nothing to compare against — it does not report
  "no baseline", it just never fires.

Verify: `ls ~/.pyauto-heart/timings/ | grep jax_grad` returns only old-layout names;
`grep -E "imaging__jax_grad|point_source__jax_grad"` returns nothing.

The docstring already anticipates collisions ("so scripts in nested subdirs do not
collide on a shared leaf name") but not moves. A rename-aware scheme, or at minimum a
loud "no baseline for this slug" signal, would have surfaced this immediately.

## 2. Every history is one value repeated 7 times

Every file in `~/.pyauto-heart/timings/` holds the same number `baseline_window` (7)
times:

```
autolens_test__scripts__jax_grad__imaging_lp.json => [45.99, 45.99, 45.99, 45.99, 45.99, 45.99, 45.99]
autolens_test__scripts__jax_grad__point_source.json => [39.24, 39.24, 39.24, 39.24, 39.24, 39.24, 39.24]
```

`update_history()` appends one duration per call and truncates to the window, so seven
identical values means the window was seeded/filled from a single observation rather
than accumulated across seven runs.

Consequence: `classify()` compares the latest duration against
`median(rolling_window)`, and a median over seven copies of one number IS that number.
So the yellow/red ratio is a **single-observation comparison** wearing the clothes of a
7-run median — it will read as stable regardless of real variance, and one unlucky run
becomes a "regression".

## Why it matters

These two combine badly. #226 needed exactly this data to answer "real slowdown, or a
cap that never fitted?" and could not: the only stored baseline for
`point_source/jax_grad/gradient.py` (39.24s) was both orphaned by the move AND a
single observation — and it turned out to describe a script that had since grown ~8x
by design. The diagnosis had to be rebuilt from CI job logs by hand.

## Suggested scope

- Decide the slug policy (rename-aware, or accept moves but emit a loud no-baseline
  signal instead of silently skipping).
- Fix history accumulation so a window of 7 means 7 distinct runs; do not seed a
  window by repetition.
- Consider recording the source run id alongside each duration so a baseline is
  traceable to the run that produced it.

<!-- Split out of PyAutoHands#226 (jax_grad smoke timeouts) on 2026-08-04; that task
     deliberately did not absorb these. -->
