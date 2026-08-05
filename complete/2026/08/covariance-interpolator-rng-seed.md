- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1450 (auto-closed by the merge)
- completed: 2026-08-05
- prs: PyAutoFit#1451 MERGED 2026-08-05 (282d8e1e, merge commit) — one file, +53/−2, test-only · PyAutoMind#127 MERGED (acc4a7dd, squashed) — routing state
- summary: Made `test_autofit/interpolator/test_covariance.py` deterministic. `test_variable_and_constant` was failing ~1 CI run in 60 and was the SOLE reason the 2026.8.2.1 LIVE release died (PyAutoHands run 30736527569, `release_test_pypi (3.12, PyAutoFit, main)` step 9: 1641 passed, 1 failed, `assert 30.121646313498022 == 25.0 ± 5`). Green on Python 3.12 AND 3.13 before merge. Class B release blocker: CLEARED.
- THE PROMPT'S PREMISE WAS WRONG — this is the finding worth more than the fix. The prompt blamed the unseeded `np.random.random()` calls in the test body and called seeding "a one-liner". Measurement says that is a MINOR contributor: replacing those two calls with a fixed-seed local `Generator` leaves std at 1.95 of 2.05, and the test still fails. Do not repeat the one-liner reflex on the next flake in this family.
- measured pre-fix failure rate (the prompt's step 2, done BEFORE touching anything): 2000 independent runs under CI conditions → 33/2000 = 1.65% miss `abs=5.0`, 95% Wilson CI 1.18–2.31%. Also 5.45% at `abs=4.0`, 14.65% at `abs=3.0`. Recovered value mean 25.24, std 2.05, range 17.82–32.04 — the observed 30.12 sits comfortably inside it, a marginal miss not a regression. Percent-level, so by the prompt's own criterion seeding alone would have been papering over something.
- BUT the tolerance is NOT mis-calibrated, and this is the distinction the prompt could not make without the measurement: with a FULL untruncated search the same test recovers 25.0496 ± 0.0039 (n=20) — 500× tighter, nowhere near the `abs=5.0` boundary. `abs=5.0` is correct and must NOT be loosened. The ESTIMATOR is what is broken.
- root cause: the autouse `limit_maxcall` fixture (added with PyAutoFit#1386 for speed) caps every search in the module at ONE likelihood call, so the "recovered" value is an unconverged draw whose spread is set entirely by the search's randomness. Stage-wise proof: with all seeds fixed the interpolator's inputs (`x`, `y`, inverse covariance matrix) are BIT-IDENTICAL across runs — 100% of the variance is inside `search.fit(...)`.
- THREE generators feed it, so seeding any one is insufficient — the trap that makes this look like a one-liner: (1) `numpy.random`, the test body's two calls, NOT dominant; (2) the stdlib `random` module, used by `autofit/non_linear/initializer.py:301` (`random.uniform`) for the search's initial unit values; (3) **dynesty's `rstate`**, which `NestedSampler` defaults to `np.random.Generator(PCG64(None))` — OS entropy, reachable from NEITHER of the above (`dynesty/dynesty.py:607-608`, `814`). (3) is DOMINANT. Empirically: seeding (1) alone → still fails; seeding (1)+(2) → 3 distinct values in 30 draws; seeding all three → bit-identical.
- SIBLING WAS WORSE (the prompt asked to check siblings, and this is why that mattered): `test_single_variable` contains NO `np.random` call at all, yet gave 500 DISTINCT values over 500 runs and missed its `abs=2.0` tolerance 18/500 = 3.6% — more than double the test that got blamed. It rides on source (3) alone. Seeding `np.random` would never have touched it. Fixed by the same fixture.
- RULED OUT explicitly (the prompt's third hypothesis, and it was wrong): the `scipy.linalg.LinAlgError` try/except guards on `test_interpolate` / `test_relationships` / `test_interpolate_other_field` / `test_linear_analysis_for_value` (added by `e29c69ef2`) are NOT this nondeterminism in disguise. The `interpolator` conftest fixture uses no RNG whatsoever; its covariance matrix is bit-identical across builds and RANK-DEFICIENT — rank 6 of 9, each 3×3 block rank 2 of 3, condition number 1.3e17. Those guards cover inverting a SINGULAR matrix: deterministic input, platform-LAPACK dependent. Separate defect, do not fold the two together.
- the fix: module-level `SEED = 20260802`; a new autouse `seed_search_randomness(monkeypatch)` fixture beside `limit_maxcall` that patches `dynesty.dynesty.get_random_generator` (the binding both `NestedSampler` and `DynamicNestedSampler` resolve at call time, imported at `dynesty/dynesty.py:18`) and seeds both global generators, RESTORING their state in a `finally` after `yield` so nothing leaks into later tests in the same process; plus `test_variable_and_constant` building its samples from a local `np.random.default_rng(SEED)`. `limit_maxcall` left unchanged — module still runs in ~1s.
- verification: recovered values bit-identical across 8 pytest invocations AND in both selection contexts (whole module vs `-k` filtered) — `test_single_variable` 24.577316739353 (dev 0.42 vs tol 2.0), `test_variable_and_constant` 22.718814166116 (dev 2.28 vs tol 5.0). Full local suite 1642 passed, 6 skipped. Both CI legs (3.12, 3.13) green.
- sandbox artefact, NOT a defect: `test_nautilus.py::test__single_core_builds_no_pool` failed locally with `ModuleNotFoundError: No module named 'nautilus'` (optional sampler absent from the cloud sandbox). Control-tested by stashing the change — reproduces identically on pristine main. CI has the optional deps and it PASSED there on both legs. Expect this locally in any sandbox without `nautilus-sampler`; do not chase it.
- KNOWN LIMITATION — do not read "seeded" as "the assertion is now meaningful": under `maxcall=1` both assertions are now frozen-RNG REGRESSION checks, not accuracy checks. A seeded draw 2.28 away from the true 25.05 still "passes" at `abs=5.0`. The merged fixture docstring says so, so it cannot be silently misread. Restoring real meaning costs suite time — measured `maxcall=200` → std 1.06 @ 0.76 s/draw; `maxcall=1000` → std 0.46 @ 2.67 s/draw; full → std 0.004 @ ~25 s/draw. Left as a reviewer judgement call, deliberately not taken unilaterally.
- FOLLOW-UP OPEN: `draft/feature/autofit/search_seed_reproducibility.md` — PyAutoFit has NO supported way to seed a search. `AbstractDynesty.search_kwargs` is a closed eleven-key dict, so `rstate` cannot be threaded through even though `dynesty` accepts it. Two consequences: this fix must monkeypatch a THIRD-PARTY module from a test (fragile across dependency upgrades), and USERS CANNOT REPRODUCE A FIT — a real gap for an inference library, not only test hygiene. The prompt flags the identifier/serialization trap: store the integer seed not a `Generator` (not JSON-serializable), and decide deliberately about `__identifier_fields__` since including it changes identifiers for existing runs.
- release-context: this closes the "gate said GREEN, then the live release contradicted it" question in `draft/triage/nightly_release_blocked_eight_nights.md`. The gate's evidence was not stale and the two sides do not disagree about what "the libraries pass" means — the release run simply drew a different random sample. That reframing removes the motive for a gate-vs-release redesign that was about to be justified by this evidence.
- session-notes: cloud/web session — no `gh` CLI (issue and PRs via the GitHub MCP surface), no worktree (worked in the canonical `/home/user/PyAutoFit` checkout on the mandated `claude/covariance-interpolator-rng-seed-8zexp3` branch). Measurement needed a Python 3.12 venv built from scratch; the ambient interpreter is 3.11 and `autonerves>=2026.7.29.2` requires >=3.12, so `pip install -e .` fails on the default interpreter with a misleading "no matching distribution" for autonerves.

## Original prompt

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
