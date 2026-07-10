# `@PyAutoFit` test_full_hierachical is flaky — EP hierarchical fit lands at wrong mu_logt

Type: bug
Target: autofit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Found 2026-07-10 while shipping the EP statistics fix batch (#1350).

## Symptom

`test_autofit/graphical/hierarchical/test_hierarchical.py::test_full_hierachical`
fails on clean `main` (post-#1349, `1a06bbc14`):

    assert new_approx.mean_field[mu_logt_].mean == pytest.approx(logt, rel=1.0)
    Obtained: -0.6935  Expected: 2.8719 ± 2.9

The EP fit converges to the wrong log-precision hyperparameter. Reproduced
3× consecutively as a single test on clean main (also with each #1350 fix
individually reverted — stash-proven unrelated to that batch).

## The confusing part

The identical content passed inside two full-suite runs earlier the same
day (1447-pass and 1457-pass runs). The `data` fixture seeds
(`np.random.seed(1)`) so data is deterministic; runs were serial pytest.
Suspect the LaplaceOptimiser/EP loop is timing- or thread-sensitive
(graphical tests emit `os.fork()`/multithreading warnings), or hidden
cross-test state. The test's `rel=1.0` tolerance is already very loose —
this is not a marginal miss but a qualitatively different fixed point.

## What to do

1. Re-run on clean main to confirm current state (flakes age).
2. Instrument: capture EPHistory / per-factor evidence for a failing vs
   passing run (the #1349 diagnostics module now makes this easy —
   `EPDiagnostics` + `graph_factors.png`).
3. Determine whether the fit has multiple EP fixed points reachable from
   the same start (damping / update-order sensitivity) or whether state
   leaks between tests.
4. Fix the source (or, if genuinely multi-modal, tighten the test's setup
   — never widen the tolerance to paper over it).

Related: #1332 F6 (truncated KL approximation degrades near bounds) may
interact with convergence checks; the F10 sigma-collapse guard (#1349) can
report whether sigmas collapsed in the failing run.
