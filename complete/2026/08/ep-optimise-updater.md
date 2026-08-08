# ep-optimise-updater

- shipped: 2026-08-08
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1456
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1457 (merged `3b960609`)
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/136 (merged `cf8b4077`)
- repos:
  - PyAutoFit: feature/ep-optimise-updater
  - autofit_workspace: feature/ep-optimise-updater

## Summary

Expose the existing EP updater hierarchy through the declarative
`FactorGraphModel.optimise()` API. The public default remains `updater=None`, so
damping is **opt-in** and existing fits retain their current behaviour. Library
changes and seam tests landed first; the workspace followed with an
undamped-by-default tutorial example showing the optional keyword.

## Ship order and gates

Library-first order was preserved: PyAutoFit #1457 merged before
autofit_workspace #136. Required CI was green on both tested heads.

The workspace gate cleared under **explicit human acknowledgement** rather than
a clean bill of health — sandbox-only notebook IPC, a broad AutoLens runtime,
and branch-sensitive Heart limitations were each documented before shipping.
That acknowledgement covers that reason set only.

## Bookkeeping note

This record was written on 2026-08-08 by the registry-integrity follow-up, not
by `ship_workspace` at merge time. The task finished and its `active.md` entry
was updated to `status: COMPLETE`, but no `complete/` record was written and the
prompt stayed in `active/` — so `lifecycle.py orphans` reported it as unclaimed
and `lifecycle.py issues` would have flagged its closed tracking issue. The
substance above is taken from the contemporaneous `active.md` entry, which was
detailed; there is simply no separate ship-time trap log.

## Original prompt

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
