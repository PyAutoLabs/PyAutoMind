# ep-projection-weights — EP projection fixed (two stacked defects)

- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1382 (closed)
- pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1383 (MERGED 2026-07-17, b32e58b16)
- repo: PyAutoFit (feature/ep-projection-weights, worktree removed post-merge)

Every sampler-driven EP factor update projected its posterior to a message pinned
near a prior bound (boundary attractor → cavity poisoning → hierarchical F10
sigma-collapse). Root-caused by the slope_hierarchy science project deliberately
exercising the 2026-07 EP wave (Jammy2211/slope_hierarchy#1).

Two stacked defects, both fixed:
1. PRIMARY — `TransformedMessage.project` never transformed samples into the base
   message's space (every other method routes through `@transform`; project alone
   didn't). Equal-weighted samples at 2.05 inside UniformPrior(1.5,3.0) projected
   to 2.97 — 0.2s unit repro, no sampler needed.
2. Secondary — `Result.projected_model` fed LINEAR `weight_list` into the
   log-weight moment match (`w = exp(log_w − max)`); now converted (zeros → −inf
   drop out, all-zero raises). `Prior.project` kwarg renamed to `log_weight_list`.

Regression test `test_projected_model_moments` (nested-sampling-shaped weights
through a UniformPrior) fails on either defect alone. test_autofit 1494p/1s.
Shipped through acked Heart RED (6 pre-existing unrelated reasons) on explicit
user PR-open + merge instructions.

Traps/lessons: the diagnosis "linear-as-log weights" from forensics alone was
incomplete — implementing the regression test exposed the deeper transform defect
(verify-the-fix empirically before filing). Historic sampler-driven EP results
(concr-era H0) may carry the same projection bias.

Follow-ups: slope_hierarchy goal-2 parity rerun (unblocked); related API-gap
prompt draft/feature/autofit/ep_optimise_expose_updater_delta.md still in draft.

## Original prompt

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
