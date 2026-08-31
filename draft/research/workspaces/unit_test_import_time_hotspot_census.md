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
