# The unit-test + import-time bottleneck census — where library CI time goes, and nine ranked options

PyAutoHeart#214 → `20eea5b`, closing PyAutoHeart#213, merged 2026-09-06 on branch
`claude/ci-test-timing-epic-ke2lul`. Phase 9 of the `ci-timing-fast-tests` epic — the
research verdict that closes it. Fable-planned on the issue; measured and written by an
Opus subagent from a web session; no library source changed. Document: PyAutoHeart
`timings/unit_import_census_2026-09.md`.

- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/213
- completed: 2026-09-06
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/214

## What shipped
- Sources: the first CI `unit-timings` rows — PyAutoNerves run 34038040174, PyAutoArray
  34039841741, PyAutoFit 34039848597 (the phase-8c PR runs, ingested by a dispatched
  heart-health run) — plus local serial `--durations` for PyAutoGalaxy / PyAutoLens,
  `-X importtime` trees, a JAX-cache A/B, and the phase 5/6/8 diagnoses.
- Seven findings: (1) library CI is compile-bound — `lib-tests.yml` restores no JAX and no
  numba cache while `smoke-tests.yml` has both since phase 7 (10 of PyAutoArray's 25
  slowest CI tests are 24.8 s cold-numba, ≤ 0.02 s warm; a persistent JAX cache halves the
  local PyAutoArray suite 43 → 21 s); (2) `--cov` is a third of the legs at identical pass
  counts; (3) one PyAutoGalaxy test is 52 % of its suite (the kaplinghat scalar `quad`
  lambda, 2.2 million density evaluations for three grid points); (4) three imports paid
  and not needed at import — pyplot via `potential_correction/visualize.py:19`,
  `scipy.special` via the module-level literal `messages/normal.py:678`, `scipy.integrate`
  via `kaplinghat.py:5` — times 494 script processes per board round; (5) PyAutoFit cannot
  run under `-n auto` (parametrized ids embed a memory address); (6) the interferometer
  "numpy" NUFFT path is JAX; (7) fixture cost is not a finding, the two 8c fixes are
  confirmed from the CI side, 7 blackjax tests are 33.6 s of PyAutoFit's CI leg and
  invisible locally.
- Nine ranked options (O1 caches for `lib-tests.yml` first), each with impact, risk,
  validation route and guard; an explicit exclusion list keeping the compile-time verdict;
  a gaps section (no CI rows yet for Galaxy/Lens; blackjax absent locally; the ~1.8×
  CI/local factor on three repos only; no option trialled end-to-end).

## Key traps / findings
- Measure warm, or do not measure: cold numba inflated three scripts 4–6× in phase 8 and
  is the dominant term in library CI here.
- Per-test numbers under `-n auto` are not comparable (6.8 s vs 0.5 s serial on the same
  PyAutoLens tests); use xdist only for suite walls.

## Follow-ups (each option the human accepts becomes its own prompt)
- O1 caches for `lib-tests.yml` is the recommended first pick.

## Original prompt

# Unit-test + import-time bottleneck census and shared-source hot-spot options

Type: research
Target: workspaces
Repos:
- PyAutoFit
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
- autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: ci-timing-fast-tests
Phase: 9
Issued: 2026-09-06

Unit-test + import-time bottleneck census and shared-source hot-spot options.

With phase 3's unit_test_timing and import_time legs live and phase 2's history
accumulating: analyse where library unit-test time and import time actually go, and
whether small refactors to often-used parts of the source code (numpy or JAX mode) could
produce performance increases across the board — the user's hypothesis that a few hot
shared paths drive CI, unit-test AND workspace run times simultaneously.

Deliverable is a written census + ranked options list (a research verdict, not a merged
refactor): slowest unit tests per library with why (fixture cost, real fits in tests,
compile in tests — note the standing `no JAX in unit tests` rule as the guard); import-time
composition per package (what the recent autolens import reduction left behind); shared
source hot spots that per-script CI timings and unit-test timings agree on; for each
candidate refactor an expected board-wide impact, risk, and validation route (unit tests +
`autolens_profiling` / `*_workspace_developer` as the independent check). Respect the
closed jax-compile-time arc verdict: never restructure likelihoods/samplers for compile
time — settings and caches only; anything upstream-JAX-bound is out of scope. Each option
the human accepts gets filed as its own follow-up prompt; this phase itself changes no
source.
