# Findings — hierarchical EP is *unstable* on the parent scale hyperparameter (toy repro)

**Task:** slope_hierarchy#1 goal-2 follow-up. Decide whether EP's too-low parent
scatter + far-too-tight scatter error is **problem-specific** (N=5 / boundary /
lensing / identifiability) or a **framework property** of PyAutoFit hierarchical EP.

**Verdict: framework property — and the mechanism is *stochastic instability*, not a
clean bias.** On the HowToFit chapter-3 hierarchical toy (5 low-SNR 1-D Gaussians,
per-Gaussian `centre` drawn from parent `N(mean=50, sigma=10)`; **scatter truth σ=10,
far from the σ→0 boundary**), repeated EP fits of the *identical* problem land in three
qualitatively different states. The slope_hierarchy pathology (tiny scatter + over-tight
error) is one of them, so it reproduces off-lensing and off-boundary — but it is **not
the deterministic outcome**; a single EP run's parent scatter cannot be trusted.

PyAutoFit @ `f83f2f493` (includes the #1383 projection fix). Numpy-only, CPU, minutes.
Repro: `ep_toy_diagnostic.py`. Joint reference = `Dynesty` on the *same* global graph.

## The three EP outcomes on identical data

| outcome | parent scatter (EP) | vs truth 10 | note |
|---------|---------------------|-------------|------|
| **RECOVER** | ~9.1–12.8 ± ~0.9–2.4 | ✓ truth in CI | matches the joint sampler |
| **COLLAPSE** | 0.003 – 0.80, err ≈ 0 | ~0–8 % of truth, **error ~0** | the slope_hierarchy pathology |
| **CRASH** | — | — | `InitializerException`: a factor's Dynesty init degenerates mid-EP |

**Frequencies (30 identical-problem runs across max_steps ∈ {20,25,30,50,60}):
21 RECOVER (70 %) / 7 CRASH (23 %) / 2 COLLAPSE (7 %).**

| max_steps | runs | RECOVER | COLLAPSE | CRASH |
|-----------|------|---------|----------|-------|
| 20 | 11 | 7 | **2** | 2 |
| 25 | 10 | 8 | 0 | 2 |
| 30 | 5  | 3 | 0 | 2 |
| 50 | 1  | 1 | 0 | 0 |
| 60 | 3  | 2 | 0 | 1 |

Two facts stand out: **both COLLAPSEs occurred only at the shortest setting (max_steps=20)**
— none at 25–60 — and the collapse there is deep (one run hit scatter=0.0030 ± 0.0000,
mean pushed to 54.4). **CRASH, by contrast, appears at every max_steps** (~1-in-4),
independent of collapse.

The joint fit (Dynesty on `factor_graph.global_prior_model`, N=5) is stable and correct
every time — mean 51.3 [45.8, 57.0], scatter 12.8 [9.9, 16.3]. **The graph and data are
fine; EP is the sole source of the instability.**

## Why it is unstable (mechanism)

1. **Stochastic bistability driven by the per-factor sampler.** Each `AnalysisFactor` is
   fitted by a `DynestyStatic` (a nested sampler); its Monte-Carlo noise feeds the EP
   moment-match. Two runs of the same data diverge completely — one descends 10→0.80 and
   plateaus collapsed; another dips to 8 then recovers to ~10.7 and stays. The scale
   update has (at least) two basins and the noisy messages decide which one is reached.
2. **The COLLAPSE basin is over-shrinkage feedback.** When it collapses, the five
   per-group `centre` posterior *means* cluster to a spread of ~0.6 (45.4–46.05) though
   the true centres span ~±10: EP shrinks each centre toward the common mean, the parent
   factor then sees near-identical centres and infers a tiny scatter, which tightens the
   shrinkage further. The tiny error bar is a faithful readout of that genuinely
   over-confident collapsed fixed point.
3. **Delta-method-near-boundary is refuted as the cause.** Truth σ=10; the base-space
   scatter message in the collapsed run is `TruncatedNormal(mean=0.80, sigma=0.11,
   lower=-inf, upper=inf)` — unbounded, nowhere near σ→0. `TransformedMessage.variance`
   is reading a genuinely narrow posterior faithfully; it is not a Jacobian artefact.
4. **Instability signatures.** `ep_history.csv` shows recurring `BAD_PROJECTION` on the
   `HierarchicalFactor` even with #1383 merged, log-evidence swinging wildly
   (223 → −63 → …), and the F10 sigma-collapse guard did *not* flag the collapsed run.

## Transient vs terminal basin — and correcting an earlier reading

- **Not a monotonic collapse / "more steps = worse".** An intermediate max_steps=20
  snapshot looked like a monotonic 10→0.8 descent, but max_steps=50 on the same setup
  recovers to 10.75 — the descent was one stochastic trajectory, not the fixed point.
- **On the clean toy, COLLAPSE is largely a short-run / early-stop phenomenon.** It
  occurred only at max_steps=20 (2/11) and never at 25–60 (0/19). More EP sweeps mostly
  escape the collapse basin. But it is a *real* basin, not mere under-convergence-toward-
  truth: a collapsed run plateaus at ~0 with an over-confident ~0 error, not a value
  crawling upward.
- **slope_hierarchy's 0.026 is the same failure mode, but stickier.** There the scatter
  truth (0.1) hugs the σ→0 boundary and the likelihood is the full lensing model; the
  collapse persisted at both max_steps=5 and 12. A near-boundary truth plus a harder
  likelihood plausibly *deepens* the collapse basin so EP cannot escape it in the step
  budgets tried — the clean toy escapes by 25 steps, the boundary problem did not.

## Answering the task's questions directly

- **(a) Does EP recover the parent-sigma point estimate on the toy?** Usually yes
  (70 % of runs, ~9–13 vs truth 10) — but not reliably: 7 % collapse to ~0, 23 % crash.
- **(b) Are EP's parent error bars sane?** In RECOVER runs, roughly (±1–2 vs joint
  half-CI ~3.2 — a bit tight but same order). In COLLAPSE runs they are catastrophic
  (~0), which is the slope_hierarchy readout. The error is only as trustworthy as the
  (unstable) point estimate.
- **(c) Push max_steps up — climb or fixed point?** Neither monotonic: it is *basin
  selection*. Collapse is confined to max_steps=20; ≥25 escapes it. So "run more steps"
  helps on the clean toy but is not a guarantee near the boundary (slope).
- **Delta-method vs over-counting vs under-convergence:** over-shrinkage (over-counting)
  in the collapse basin; delta-method-boundary refuted; under-convergence present only as
  the transient into/out of basins, not as a bias toward truth.

## Verdict & recommendation

**Fixable/reportable PyAutoFit issue, not merely an inherent EP caveat.** Two distinct
defects surfaced, both on a clean known-answer toy:

1. **Scale-hyperparameter COLLAPSE** — hierarchical EP can settle into an over-shrinkage
   basin where the parent scatter → ~0 with an over-confident ~0 error, undetected by the
   F10 sigma-collapse guard. This *is* the slope_hierarchy pathology, reproduced
   off-boundary and off-lensing.
2. **`InitializerException` CRASH** — ~1-in-4 runs hard-abort mid-EP when a factor's
   Dynesty init degenerates (all initial samples equal FoM). A robustness bug independent
   of (1); should degrade to a flagged BAD_PROJECTION, not kill the fit.

Deliverables:
1. **Report to slope_hierarchy#1** (unblocks goal-2 write-up): the too-low-scatter /
   over-tight-error result is a framework instability that reproduces on the toy; frame
   goal 2 as *EP unreliability for the parent scale hyperparameter* (recover/collapse/
   crash across identical runs), with NUTS/nested sampling the trustworthy headline.
2. **File a PyAutoFit bug prompt** with this minimal repro (`ep_toy_diagnostic.py`).
   Triage questions for the owner: is COLLAPSE curable by a deterministic/damped
   `HierarchicalFactor` scale moment-match; should F10 fire on it; and should the
   `InitializerException` be caught as a bad projection. The toy makes all three cheap.

Corollary for the standing diagnostics hint "consider damping, delta < 1": damping made
slope_hierarchy *worse*; the failure here is basin-selection instability, which damping
does not obviously cure. The hint mis-diagnoses this mode and should be revised.
