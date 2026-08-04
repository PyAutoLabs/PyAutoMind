# Seed `test_variable_and_constant` — its unseeded RNG blocked a live release

Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: high
Status: issued
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1450

## The defect

`test_autofit/interpolator/test_covariance.py:122` builds its sample list from
**unseeded** `np.random.random()` and then asserts a fixed tolerance:

```python
kwargs={
    ("v",): value + 0.1 * (1 - np.random.random()),
    ("x",): 0.5 * (1 - +np.random.random()),
}
...
assert interpolator[interpolator.t == 25.0].v == pytest.approx(25.0, abs=5.0)
```

Nothing seeds the generator, so the assertion is a coin flip whose odds are
unmeasured. It lost one on 2026-08-02.

## Why it matters — this is the Class B release blocker

This test is the entire reason the 2026.8.2.1 **live release** failed. The
nightly readiness gate passed, step 6 dispatched a real release, and PyAutoHands
run 30736527569 failed in
`release_test_pypi (3.12, PyAutoLabs/PyAutoFit, main, PyAutoFit)` at step 9,
Tests:

```
FAILED test_autofit/interpolator/test_covariance.py::test_variable_and_constant
E  assert 30.121646313498022 == 25.0 ± 5
====== 1 failed, 1641 passed, 2 skipped, 425 warnings in 70.32s (0:01:10) ======
```

1641 passed, 1 failed, and the failure is 30.12 against a 30.0 boundary — a
marginal miss, not a real regression.

This closes out the "gate said GREEN, then the live release contradicted it"
question in
`draft/triage/nightly_release_blocked_eight_nights.md`. The gate's evidence was
not stale and the two sides do not disagree about what "the libraries pass"
means. The release run drew a different random sample. That reframing matters
more than the fix: it removes the motive for a gate-vs-release redesign that was
about to be justified by this evidence.

## Proposed work

1. Seed the RNG for this test — `np.random.default_rng(<fixed seed>)` local to
   the test is preferable to a global `np.random.seed`, which leaks into
   whatever runs next in the same process.
2. Before choosing the seed, **measure the failure rate**: run the current test
   a few hundred times and record how often it exceeds `abs=5.0`. If it is
   percent-level rather than one-in-thousands, the tolerance is also wrong and
   seeding alone would be hiding a genuinely mis-calibrated assertion rather
   than fixing it. Record the number either way.
3. Check the siblings in the same file for the same pattern — `test_interpolate`
   and the other `interpolator` fixture consumers — rather than only the one
   script that happened to fail. `test_interpolate` already carries a
   `scipy.linalg.LinAlgError` try/except added by `e29c69ef2` ("handle linalg
   error thrown in test for some python versions"), which is the same
   nondeterminism showing up in a different disguise.

## Exit criteria

The test is deterministic across repeated runs; the pre-fix failure rate is
recorded in the PR; any sibling with the same unseeded-RNG shape is either fixed
or explicitly ruled out.
