# EP: cure the hierarchical parent-scale collapse basin (and make F10 fire on it)

Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Issue: (none yet — parent report is https://github.com/PyAutoLabs/PyAutoFit/issues/1405)

## The defect

Defect 1 of the two filed on PyAutoFit#1405. A hierarchical EP fit of a parent
**scale** hyperparameter (the `sigma` of a `HierarchicalFactor` parent Gaussian)
is stochastically unstable: repeated fits of an *identical, known-answer*
problem land in qualitatively different basins.

Measured over 30 identical-problem runs of a clean CPU toy (no JAX, no lensing;
parent scatter truth **σ=10**, far from the σ→0 boundary):

| outcome | freq | parent scatter (truth 10) |
|---|---|---|
| RECOVER | 70% | 9–13, sane errors — matches the joint sampler (12.8 [9.9, 16.3]) |
| **COLLAPSE** | 7% | **0.003–0.80 with an over-confident ≈0 error** |
| CRASH | 23% | `InitializerException` (split out — see the sibling prompt) |

The joint fit — `Dynesty` on `factor_graph.global_prior_model` for the same
graph — is stable and correct every time. **The graph and the data are fine; EP
is the sole source of the instability.** On PyAutoFit `f83f2f493`, i.e. this is
*downstream* of the #1383 projection fix and is a distinct, deeper issue.

## Mechanism (already established — do not re-derive)

Three candidate causes were tested; two are settled and one is confirmed:

- **Delta-method / boundary artefact → REFUTED.** Truth σ=10 with the base-space
  scatter message unbounded (`TruncatedNormal(mean≈0, lower=-inf, upper=inf)`),
  so `TransformedMessage.variance` is faithfully reporting a genuinely
  over-confident posterior — not a Jacobian linearization breaking down near a
  bound.
- **Over-shrinkage feedback → CONFIRMED as the collapse basin.** Per-group
  drawn-variable posterior *means* cluster far tighter than truth (spread ~0.6
  vs true ±10); the parent factor then sees near-identical draws, infers a tiny
  scatter, and tightens the shrinkage further — positive feedback to a fixed
  point at scatter ≈ 0 with ≈0 reported error. `ep_history.csv` shows recurring
  `BAD_PROJECTION` on the `HierarchicalFactor` and wildly swinging log-evidence
  through the collapse.
- **Under-convergence → transient only.** It explains movement *into and out of*
  basins, not a slow crawl toward truth. Both toy COLLAPSEs were at the shortest
  setting (`max_steps=20`); zero collapse at 25–60. But note the science case
  (`slope_hierarchy`, N=5 lenses) has a *stickier near-boundary variant* that
  converged to a stable wrong fixed point at σ≈0.026 vs truth 0.1 — it plateaued
  for the last ~2 of 12 sweeps and did not recover. So "just run longer" is not
  the fix.

## The task

1. **Make the collapse detectable before making it curable.** The **F10
   sigma-collapse guard** (`check_sigma_collapse`, from the #1335 diagnostics
   wave) passes a scatter≈0 / error≈0 parent **silently** today. That is the
   most defensible first deliverable and it is independently shippable: a
   hierarchical parent whose scatter has collapsed with a ~0 error should be
   flagged loudly. Decide whether F10's threshold is wrong or whether parent
   scale hyperparameters need their own check.
2. **Then attack the basin.** Candidate levers, in the order the evidence
   favours:
   - a **more robust / damped `HierarchicalFactor` scale moment-match** — the
     moment match is where near-identical draws get converted into a tiny
     scatter;
   - a **deterministic per-factor optimiser** in place of the per-factor nested
     sampler, to cut the sampler noise that appears to drive basin selection
     (the instability is stochastic across identical inputs — that noise has to
     enter somewhere).
3. **Revise the diagnostics' standing hint.** `ep_diagnostics` currently
   suggests "consider damping, delta < 1". **Naive damping made this worse**:
   on `slope_hierarchy`, delta=0.5 gave full collapse, 67 `BAD_PROJECTION`, and
   log-evidence blowing up to 5e7. The hint mis-diagnoses this mode and must be
   corrected alongside whatever the real fix turns out to be — otherwise the
   framework actively points users at the wrong lever.

Note `factor_graph.optimise()` still cannot pass an `updater`/`delta` through
(filed: `draft/feature/autofit/ep_optimise_expose_updater_delta.md`); damping
experiments need the private `_make_ep_optimiser` workaround, pattern in
`slope_hierarchy/scripts/ep.py`.

## Repro and evidence

- Toy repro: `complete/2026/07/ep_scale_collapse_assets/ep_toy_diagnostic.py`,
  full forensics in `EP_TOY_FINDINGS.md` alongside it. Numpy-only, CPU, minutes.
  Collapse is only ~7% per run, so any verdict needs a **loop of runs**, not one
  — a fix that "works" on a single run proves nothing here
  (`feedback_flaky_test_sample_size`).
- Science case: Jammy2211/slope_hierarchy#1 (converged parity table, N=5 lenses,
  the stickier near-boundary variant).

## Acceptance

The honest bar is **not** "collapse never happens" — it is that a collapsed
parent scale is *never silently reported as a confident answer*. F10 firing on
the 7% is a pass; curing the basin outright is the stretch goal. If the basin
proves inherent to EP for scale hyperparameters, the deliverable converts to a
documented methods caveat (EP is fast and correct for the parent **mean**; use
a joint sampler for the **scatter**) plus the guard.

<!-- filed 2026-07-22 as the wrap-up follow-up of the ep-hierarchical-scale-collapse
task (report-only; PyAutoFit#1405). Sibling: ep_initializer_exception_should_not_abort.md -->
