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
Issued: 2026-09-29
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1651

## Finding

`autofit/non_linear/search/nest/nautilus/search.py` (~600-630, the
`while not finished:` loop) has the same finished-detection shape as
Dynesty's: `finished` is only set when `total_iterations == iterations_after_run`
or the global `n_like_max` is hit, so a first pass that converges is never
recognised as finished and every fit does a `perform_update(during_analysis=True)`
followed by a second no-op `run()`. The Dynesty side was fixed under
https://github.com/PyAutoLabs/PyAutoFit/issues/1642 (PR 1a, merged 2026-09-24 as
PyAutoFit#1643 `0e2c09748`; record `complete/2026/09/ep-factor-search-overhead.md`).

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

- Sibling fix: https://github.com/PyAutoLabs/PyAutoFit/issues/1642 (shipped 2026-09-24, PyAutoFit#1643; record `complete/2026/09/ep-factor-search-overhead.md`)

## Handoff — 2026-09-29

Latest: human authorized the named override and same-turn `/prm` ("yeah, and then do a $prm"). All 160 downstream scripts + 6 notebooks passed across 8 workspace groups. Commit `84ae77fc0`, pending-release PR https://github.com/PyAutoLabs/PyAutoFit/pull/1652. CI judgment / merge / close-out next. The earlier uncommitted/paused state below is superseded.

- Human approved implementation after the explanation: “ok, do it.” Issue #1651 holds the plan.
- Worktree: `/home/jammy/Code/PyAutoLabs/.worktrees/ep-nautilus-single-pass/PyAutoFit`; branch `feature/ep-nautilus-single-pass`, base `69bb11d54`; two source/test files modified, not committed.
- `Nautilus.call_search` now uses `Sampler.run()`'s convergence return; finite cumulative budgets use `n_like`, and global limits stop on batch overshoot. No public signature change.
- Tests: full serial suite 2934 passed / 2 skipped (300.23 s); targeted Nautilus 16 passed. All 8 new cases fail against baseline methods.
- Two seeded real fits: run calls 2 → 1, intermediate updates 1 → 0; parameters, likelihoods and weights bit-identical. Removed intermediate update measured 68–75 ms/search; overall timing gain not established.
- Autofit workspace smoke: 8/8 scripts and 2/2 notebooks passed. Wider smoke stopped during autogalaxy environment preparation after fresh Heart RED; no process remains running. Disposable workspace clones are under `.smoke-root/` beside the library worktree.
- Evidence beside library checkout: `full-suite.log`, `nautilus-tests.log`, `benchmark.py`, `benchmark.log`, `benchmark-instrumented.log`, `smoke.log`, `vitals.log`, `pr-body.md`.
- Runtime: source task `activate.sh`, use `/home/jammy/venv/PyAuto/bin/python`, assert `autofit.__file__` points into this task. The worktree helper made activate.sh a symlink to canonical activation (known shared-activation hazard).
- Fresh Heart at 2026-09-29T19:22:53Z is RED: `PyAutoFit: 1 commit(s) behind origin`; `PyAutoLens: 1 commit(s) behind origin`. Task branch already starts at latest origin/main; these refer to canonical checkouts. Published board had older YELLOW evidence and is superseded by this tick.
- Next: human development-only override (or cleared Heart), finish remaining smoke checks as applicable, then ship-library commit/push/pending-release PR. No commit, PR, merge or release performed.
