# EP declarative optimise() cannot apply the damping its own diagnostics recommend

Type: feature
Target: autofit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised

## Problem

`ep_diagnostics.results` (the #1335 sigma-collapse guard) tells users to "consider
damping, e.g. delta < 1" — but the public declarative API cannot do it:
`AbstractDeclarativeFactor.optimise()` → `_make_ep_optimiser()` hardwires the default
`SimplerUpdater(delta=1.0)`; neither `optimise()` nor `EPOptimiser.run()` accepts an
`updater`/`delta`, even though `EPOptimiser.__init__` supports `updater=` and the
`SimplerUpdater`/`FactorUpdater`/`DynamicUpdater` hierarchy exists.

Found on slope_hierarchy (Jammy2211/slope_hierarchy#1): the undamped EP fit of 5
power-law lenses sigma-collapsed (every drawn slope pinned at the prior edge, std
~1e-19, parent sigma → 0; RAL job 330495). The diagnostics flagged it perfectly and
recommended the one knob the API doesn't expose. The project works around it by
replicating the optimise() glue with `_make_ep_optimiser` + `opt.updater = SimplerUpdater(delta)`
(`slope_hierarchy/scripts/ep.py`) — private-API use that should not be needed.

## Ask

Thread an `updater: Optional[ApproxUpdater] = None` (or a plain `delta: float = 1.0`)
kwarg through `AbstractDeclarativeFactor.optimise()` → `_make_ep_optimiser()` →
`EPOptimiser`. Additive, default-preserving. Update the EP feature docs
(`autofit_workspace/scripts/features/expectation_propagation.py`) and the
sigma-collapse warning text to name the now-reachable kwarg.

## Secondary (same wave, may split)

Diagnostics label variables `uniformprior_19`-style; on a realistic 65-parameter
lensing graph the sigma-collapse warnings and `mean_field_summary` are unreadable —
consider propagating model path names into `EPDiagnostics`/`mean_field_summary`.
