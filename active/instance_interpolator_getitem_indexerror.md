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
