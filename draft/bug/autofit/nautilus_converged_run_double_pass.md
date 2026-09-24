# Nautilus: a converged single-chunk fit still runs a second no-op `run()` pass with a during_analysis update

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: a converged single-chunk Nautilus fit calls the sampler's run() once and performs no during_analysis update.
Filed: 2026-09-24

## Finding

`autofit/non_linear/search/nest/nautilus/search.py` (~600-630, the
`while not finished:` loop) has the same finished-detection shape as
Dynesty's: `finished` is only set when `total_iterations == iterations_after_run`
or the global `n_like_max` is hit, so a first pass that converges is never
recognised as finished and every fit does a `perform_update(during_analysis=True)`
followed by a second no-op `run()`. The Dynesty side is fixed under
https://github.com/PyAutoLabs/PyAutoFit/issues/1642 (PR 1a).

The Dynesty fix cannot be copied verbatim: Nautilus's `iterations_from`
counts posterior samples, not likelihood calls, so the Dynesty budget
comparison (`iterations_after_run - total_iterations <= iterations`) would
wrongly mark budget-limited runs as finished.

## Fix options

- Compare against an `n_like`-based budget (the sampler's likelihood-call
  counter) rather than the posterior-sample count, or
- guard: set `finished = True` after the first pass when
  `iterations_per_full_update >= ITERATIONS_NEVER` (the default no-intermediate-update
  cadence), leaving finite cadences on the existing loop.

Test: mock/wrap `search_internal.run` with a counter on a small converged fit
and assert one call and zero `during_analysis=True` updates; a finite-cadence
case still loops.

## Links

- Sibling fix: https://github.com/PyAutoLabs/PyAutoFit/issues/1642 (`active/ep_factor_search_wrapper_overhead.md`)
