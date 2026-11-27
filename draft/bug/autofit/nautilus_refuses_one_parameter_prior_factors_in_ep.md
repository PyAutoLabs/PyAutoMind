# Nautilus refuses one-parameter PriorFactors, so EP never updates them

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
- nautilus
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-27
Consequence: judge
Witness: an EPOptimiser with `default_optimiser=af.Nautilus(...)` over a FactorGraphModel with an AnalysisFactor and its one-parameter PriorFactors runs one step and every PriorFactor's message is updated (not STALE); the test fails on the base commit.
Review-minutes: 10
Unattended: needs-slicing
Lane: any

Found by the PyAutoFit#1808 worker (shift 2026-11-26-pm; record `complete/2026/11/regression-test-nautilus-ep-default.md`).

Nautilus refuses models with fewer than 2 parameters. A `PriorFactor` has 1 parameter, so every PriorFactor step under Nautilus as the EP `default_optimiser` raises `ValueError("Cannot run Nautilus with less than 2 parameters.")`. EP records the failure, skips it and flags those factors STALE, so Nautilus as the EP default never updates them.

The fix needs a decision: route sub-2-parameter factors to a different optimiser (analytic or a 1D search), or make Nautilus handle the 1D case. That choice is why this is `judge` and needs slicing before a shift can take it.
