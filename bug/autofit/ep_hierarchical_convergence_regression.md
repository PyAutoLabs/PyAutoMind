# EP hierarchical test regresses after EP-statistics fix batch (#1351)

Type: bug
Target: PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

`test_autofit/graphical/hierarchical/test_hierarchical.py::test_full_hierachical` fails
**deterministically** on `main` (the test is seeded with `np.random.seed(1)`), and the
same commit is **red in CI**. PyAutoFit's Tests workflow is failing on `main` HEAD.

## Failure

```
assert new_approx.mean_field[mu_logt_].mean == pytest.approx(logt, rel=1.0)
E   assert np.float64(-0.303...) == 2.8719 ± 2.9    # lands just outside the rel=1.0 band
test_autofit/graphical/hierarchical/test_hierarchical.py:310: AssertionError
```

The recovered hierarchical mean for `mu_logt` collapses to ≈ -0.30 instead of ≈ 2.87. The
`mu_x` leg (line 309, same `rel=1.0`) still passes — so the EP fit is converging to a wrong
fixed point for one hierarchical parameter, not failing outright. Reproduces in isolation in
~22 s: `pytest test_autofit/graphical/hierarchical/test_hierarchical.py::test_full_hierachical`.

## Bisect — culprit is #1351

CI Tests workflow history on `main` (linear merges):

| Commit | PR | Tests |
|--------|----|----|
| 2e33b175 | #1347 | ✓ success (last green) |
| **c5c50cca** | **#1351** | ✗ **failure (first red)** |
| ffc04d83 | #1354 | ✗ failure (stayed red) |

So **#1351 `fix(graphical): EP statistics fix batch — F1/F2/F4/F8 from #1332`** introduced
the regression; #1354 (F6/F7(b)) only inherited it. Do **not** waste effort on #1354.

## Fix locus

#1351's squashed commit `fc0152093` changed:

- `autofit/graphical/laplace/newton.py` — **66 lines, heavily rewritten** (prime suspect:
  the Newton/Laplace optimisation step that drives EP convergence for the hierarchical fit)
- `autofit/graphical/mean_field.py` — 15 lines
- `autofit/messages/{abstract,beta,gamma}.py` — smaller message-class changes
- adds `test_autofit/graphical/functionality/test_ep_statistics_fixes.py`

The most likely offender is a behavioural change in `newton.py` (F1/F2/F4/F8) that shifts
where the hierarchical EP iteration settles for `mu_logt`.

## Constraints

- **Fix the library, not the test.** Do not simply loosen the `rel=1.0` tolerance or reseed
  to mask it — the value went from ≈2.87 (correct) to ≈-0.30 (wrong sign/magnitude), which is
  a real convergence regression, not tolerance noise. Only relax the assertion if root-cause
  analysis proves the *new* behaviour is the correct one and the old expectation was wrong —
  and then justify it against the F1/F2/F4/F8 intent.
- The new `test_ep_statistics_fixes.py` must stay green — the fix must reconcile the
  F1/F2/F4/F8 intent with the hierarchical case, not revert #1351 wholesale.
- Cross-check `#1332` (the parent issue for the F-series fixes) for the intended semantics.

## Validation

`pytest test_autofit/graphical/hierarchical/test_hierarchical.py` +
`test_autofit/graphical/functionality/test_ep_statistics_fixes.py` both green, then the full
`autofit/graphical` suite, then confirm CI Tests goes green on the fix branch.

Found 2026-07-10 during a `/health check` green-light sweep: 1 failure across the whole
stack (2474 library tests + 47 workspace smoke scripts otherwise green).
