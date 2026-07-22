The parked NEEDS_FIX blamed an `IndexError` in `InstanceInterpolator.__getitem__` when querying a
between-samples time (1.5), across two victims. **Both markers were stale.** The library bug was
fixed by PyAutoFit `c8511b553` (2026-04-12) — two days AFTER the 2026-04-10 park — which added the
`if not self.instances: raise IndexError` guard at `autofit/interpolator/abstract.py:98`.

Reproduced on clean `main` with `output/` moved aside so nothing came from cache: autofit_workspace
`features/interpolate` exits 0 both real and under `PYAUTO_TEST_MODE=1`, and HowToFit `tutorial_5`
exits 0.

The prompt's premise was wrong twice. It is NOT a bracketing/off-by-one bug — `t == 1.5` always
worked and `test_interpolator.py` covers it in four places. And HowToFit `tutorial_5` contains ZERO
interpolator code, so the "likely related to InstanceInterpolator" attribution was never true. The
real cause was an empty `instances` list reaching `self.instances[0]`.

Residual gap closed: `c8511b553` shipped the guard with no test. Added `test_no_instances`.

SCOPE CORRECTION mid-run: autofit_workspace needed no change at all — its marker was already removed
upstream by autofit_workspace PR#103 (`7154e8a`). The first grep hit a stale local `main`; caught
when the edit failed, reset that repo and dropped the branch.

MERGED: PyAutoFit#1412 (test), HowToFit#24 (un-park). Issue PyAutoFit#1411 closed.

NOTE: HowToFit `no_run.yaml` now has zero entries — safe, both PyAutoHands loaders (`run.py:53`,
`run_python.py:46`) do `no_run_data or []`.

## Original prompt

# InstanceInterpolator.__getitem__ IndexError when querying an interpolated time (parked NEEDS_FIX)

Type: bug
Target: autofit
Repos:
- PyAutoFit
- autofit_workspace
- HowToFit
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Parked since 2026-04-10; still parked after the 2026-07-21 census. Likely ONE PyAutoFit library bug
with two downstream victims:
- autofit_workspace `features/interpolate` — `IndexError in InstanceInterpolator.__getitem__ when
  querying time == 1.5` (an interpolated, non-sample time).
- HowToFit `chapter_1_introduction/tutorial_5_results_and_samples` — "IndexError in samples access,
  likely related to the InstanceInterpolator bug" (confirm it is the same root cause).

Fix in PyAutoFit's interpolator (bounds/bracketing when the query time falls between stored samples,
or an off-by-one selecting the upper index), add a numpy unit test at a between-samples query, then
remove BOTH NEEDS_FIX markers from the two repos' config/build/no_run.yaml once green.
