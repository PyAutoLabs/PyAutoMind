- summary: superseded — PyAutoFit 196abf39a (2026-10-08) "Analysis.is_jax as the single JAX probe": Nautilus reads `analysis.is_jax`, whose body is `bool(getattr(self, "_use_jax", False))`, and `PriorFactor(FactorKW, Analysis)` inherits it, so the unguarded `_use_jax` read that crashed EP prior-factor steps is gone.
- not done: the EP regression test the draft asked for (Nautilus as default_optimiser over a FactorGraphModel with PriorFactors, one step) was not found; re-file as a small test task if wanted.
- found by: draft-queue sweep 2026-11-05 (read-only audit against the Mind ledger + GitHub commit/PR/code search); closure approved by the human.

## Original prompt

# Nautilus as an EP default_optimiser crashes on PriorFactors (reads analysis._use_jax unguarded)

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
- nautilus
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: an EP fit whose EPOptimiser is built with default_optimiser=af.Nautilus(number_of_cores=1) over a FactorGraphModel with PriorFactors runs its prior-factor steps instead of raising AttributeError on _use_jax; a test builds that optimiser over one AnalysisFactor plus its priors and runs one step.
Review-minutes: 3
Unattended: ready
Filed: 2026-09-17

Found while building the memory witness for PyAutoFit#1631.

A `FactorGraphModel` contains `PriorFactor`s whose `.analysis` is the
`PriorFactor` itself, which has no `_use_jax` attribute. `AbstractSearch.optimise`
already reads it defensively (`getattr(analysis, "_use_jax", False)`), but the
Nautilus `_fit` (`autofit/non_linear/search/nest/nautilus/search.py`, the
`if self.force_x1_cpu or analysis._use_jax:` branch) reads it unguarded, so
`af.Nautilus` handed to `EPOptimiser` as the `default_optimiser` raises
`AttributeError` the first time a prior factor is stepped. The workaround in
the #1631 witness was a per-factor `optimiser=af.Nautilus(...)` on each
`AnalysisFactor` with `default_optimiser=af.LaplaceOptimiser()` for the priors.

Fix: read `_use_jax` through `getattr(..., False)` in the Nautilus `_fit`, and
grep the other searches' `_fit` bodies for the same unguarded read. Add a small
EP test that drives one step with Nautilus as the default optimiser.
