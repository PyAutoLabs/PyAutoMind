Merged PyAutoFit#1808 (human /prm, 2026-11-26), from shift 2026-11-26-pm.

Adds a regression test for Nautilus as the EP `default_optimiser` over PriorFactors.

Decision taken (flagged, accepted at /prm): the test asserts that the `AnalysisFactor` step raised no exception (`flag is not StatusFlag.EXCEPTION`), not `success=True`. With the test-mode budget, its tiny sample sometimes projects to an invalid message. This held in about 50 runs.

Witness: 2 passed, 10 of 10 green. Control: an unguarded read raises AttributeError on PriorFactor only. CI GREEN (3 success, 1 non-test skip).

Follow-up, not filed: Nautilus refuses models with fewer than 2 parameters, so every one-parameter `PriorFactor` step fails with `ValueError("Cannot run Nautilus with less than 2 parameters.")`. EP records the failure, skips it and flags those factors STALE, so Nautilus as the EP default never updates them.

## Original prompt

# Regression test: Nautilus as the EP `default_optimiser` over PriorFactors

Type: test
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
- nautilus
Difficulty: medium
Autonomy: safe
Priority: low
Status: formalised
Filed: 2026-11-05
Consequence: glance
Witness: a PyAutoFit unit test builds an `EPOptimiser` with `default_optimiser=af.Nautilus(number_of_cores=1)` over a `FactorGraphModel` with one AnalysisFactor plus its PriorFactors and runs one step without AttributeError (fast settings / a stubbed sampler run are fine).
Review-minutes: 3
Unattended: ready
Lane: any

The bug (Nautilus `_fit` reading `analysis._use_jax` unguarded on a PriorFactor) is gone since
PyAutoFit 196abf39a (`Analysis.is_jax` = `bool(getattr(self, "_use_jax", False))`, inherited by
`PriorFactor`), and its draft was closed 2026-11-05 as superseded
(`complete/2026/11/nautilus-ep-use-jax-guard.md`). The regression test the original draft asked
for was never added, so nothing stops the unguarded read coming back. Add it.

<!-- formalised by the Intake (Conception) Agent on 2026-11-05 from file:/tmp/claude-0/-home-user/ad8c6486-73f7-504b-b742-a7b629366ade/scratchpad/intake/e_ep_nautilus_test.md -->
