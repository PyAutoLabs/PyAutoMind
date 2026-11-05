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

The bug (Nautilus `_fit` reading `analysis._use_jax` unguarded on a PriorFactor) is gone since
PyAutoFit 196abf39a (`Analysis.is_jax` = `bool(getattr(self, "_use_jax", False))`, inherited by
`PriorFactor`), and its draft was closed 2026-11-05 as superseded
(`complete/2026/11/nautilus-ep-use-jax-guard.md`). The regression test the original draft asked
for was never added, so nothing stops the unguarded read coming back. Add it.

<!-- formalised by the Intake (Conception) Agent on 2026-11-05 from file:/tmp/claude-0/-home-user/ad8c6486-73f7-504b-b742-a7b629366ade/scratchpad/intake/e_ep_nautilus_test.md -->
