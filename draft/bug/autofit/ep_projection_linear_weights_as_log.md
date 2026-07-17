# EP sampler-factor projection feeds LINEAR weights into log-weight moment matching → boundary attractor → sigma-collapse

Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

## Symptom (end-to-end, reproduced on slope_hierarchy)

Any EP fit whose `AnalysisFactor`s are optimised by a nested-sampling search projects
per-factor posteriors to messages pinned near a prior boundary with tiny std, after which
the graph (hierarchical or not) locks up; with an `af.HierarchicalFactor` this presents as
the F10 sigma-collapse (`ep_diagnostics.results` flags it — the diagnostics are correct).
Damping does not help (verified at delta=0.5, RAL job 330532).

Cleanest repro (Jammy2211/slope_hierarchy, RAL job 330591 — 1 imaging lens, 1 EP step):

- the factor's own Nautilus fit: `slope = 2.0448 (2.0150, 2.0748)` (correct; matches the
  standalone fit of the same dataset),
- the projected mean-field message for the same variable: `2.9875 ± 0.011` — at the
  UniformPrior(1.5, 3.0) upper bound; step flagged `BAD_PROJECTION`, per-factor
  `log_evidence` 19–148 where the standalone logZ is ~6600, later steps exploding to 3e12.

## Cause (code seam)

`Result.projected_model` (autofit/non_linear/result.py ~341):

```python
weights = self.samples.weight_list          # LINEAR importance weights
prior.project(samples=..., weights=weights)
```

`Prior.project` (mapper/prior/abstract.py ~201) forwards as `log_weight_list=weights`, and
`AbstractMessage.project` (messages/abstract.py ~266) computes
`w = exp(log_weight_list - max)` — i.e. it *documents and requires log weights*
(`w̃_s = exp(log w_s − max log w)`, per the #1334 formal spec docstring).

Feeding linear weights (∈[0,1], mostly ≪1) through `exp(·)` yields near-uniform weights
over the **entire** nested-sampling run, prior-exploration phase included. Moment matching
happens in the message's canonical (transformed) space, where samples near the physical
bounds map to extreme values — so the near-uniformly-weighted moments are dominated by the
boundary tail, and the projected message lands at a bound with spuriously small std. That
poisons the cavity for every subsequent factor update; with a hierarchical factor the
parent then honestly infers sigma→0 from N identical wrong slopes (mean_field_history.csv
shows the full trajectory: dataset factors land ~2.97–2.99 at steps 0–4, HierarchicalFactor
collapses sigma from step 5).

## Fix sketch

- Pass log weights: `np.log(weights)` with a floor for zero weights (or change
  `AbstractMessage.project` to accept linear weights and log them internally — pick one
  convention and rename the kwarg so the type is unambiguous).
- Regression test: draw a weighted sample set from a known Gaussian posterior under a
  `UniformPrior`, project, assert the projected mean/std match the sample moments (this
  fails loudly today).
- Audit other `.project(` call sites for the same linear/log confusion.
- Archaeology: check when `weight_list` semantics and `project` diverged — concr-era EP
  H0 runs may have silently suffered the same bias.

## Context

Found by slope_hierarchy goal 4 (deliberately exercising the 2026-07 EP wave on a
realistic lensing case) — full forensics on Jammy2211/slope_hierarchy#1. The #1335
diagnostics behaved perfectly throughout; the related API gap
(`draft/feature/autofit/ep_optimise_expose_updater_delta.md`) is separate. slope_hierarchy
goal 2 (EP-vs-NUTS parity) is blocked on this fix.
