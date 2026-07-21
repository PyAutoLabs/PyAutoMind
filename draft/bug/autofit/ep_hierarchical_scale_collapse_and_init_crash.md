# Hierarchical EP: parent scale hyperparameter collapses (over-confident ~0) and can hard-crash

Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

## Summary

A hierarchical EP fit of a parent scale hyperparameter (the `sigma` of a
`HierarchicalFactor` parent Gaussian) is **unstable**: repeated fits of an *identical,
known-answer* problem land in three qualitatively different outcomes. On a clean CPU toy
(no JAX, no lensing, parent scatter truth σ=10 sitting far from the σ→0 boundary):

- **RECOVER (~70%)** — scatter ≈ 9–13, sane errors, matches a joint nested-sampler fit.
- **COLLAPSE (~7%)** — scatter → ~0 (0.003–0.80) with an **over-confident ~0 error**;
  the F10 sigma-collapse guard does **not** flag it. This is the exact readout seen in
  the `slope_hierarchy` science project (parent scatter 4–12× too low, errors ~1000×
  too tight).
- **CRASH (~23%)** — `InitializerException` ("initial samples all have the same figure
  of merit") hard-aborts mid-EP when a factor's Dynesty init degenerates.

Measured over 30 identical-problem runs across max_steps ∈ {20,25,30,50,60}:
21 RECOVER / 2 COLLAPSE / 7 CRASH. Both COLLAPSEs were at the shortest setting
(max_steps=20); zero collapse at 25–60. CRASH appears at every max_steps.

The joint fit — `Dynesty` on `factor_graph.global_prior_model` for the same graph — is
stable and correct every time (scatter 12.8 [9.9, 16.3]). **The graph and data are fine;
EP is the sole source of the instability.**

This is on PyAutoFit `f83f2f493` (i.e. *includes* the #1383 projection fix). It is a
distinct, deeper issue than #1383.

## Two distinct defects

1. **Scale-hyperparameter COLLAPSE (over-shrinkage basin).** When it collapses, the
   per-group drawn-variable posterior *means* cluster far tighter than truth (spread ~0.6
   vs true ~±10); the parent factor then sees near-identical draws and infers a tiny
   scatter, tightening the shrinkage further — positive feedback to a fixed point at
   scatter ≈ 0 with ~0 reported error. It is **not** a delta-method/boundary artefact:
   truth σ=10, the base-space scatter message is unbounded
   (`TruncatedNormal(mean≈0, lower=-inf, upper=inf)`), so `TransformedMessage.variance`
   is faithfully reading a genuinely over-confident posterior. `ep_history.csv` shows
   recurring `BAD_PROJECTION` on the `HierarchicalFactor` and wildly swinging
   log-evidence during collapse.
2. **`InitializerException` CRASH.** ~1-in-4 runs hard-abort when EP drives a factor to a
   degenerate all-equal-likelihood state its per-factor `DynestyStatic` cannot initialise
   (`autofit/non_linear/initializer.py:185`). Should degrade to a flagged BAD_PROJECTION
   / skipped update, not kill the whole fit.

## Minimal repro

`ep_scale_collapse_assets/ep_toy_diagnostic.py` (self-contained; run from the HowToFit
repo root, numpy-only, minutes on CPU). It builds the HowToFit chapter-3 hierarchical toy
(5 low-SNR 1-D Gaussians, `centre ~ N(50, 10)`), runs EP and a joint Dynesty fit on the
same graph, and prints an `OUTCOME:` tag. Reproduce the distribution:

```bash
cd HowToFit
export NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib PYAUTO_SKIP_VISUALIZATION=1
for r in $(seq 1 10); do TOY_MAX_STEPS=20 TOY_JOINT=0 TOY_TAG=rep_$r \
  python3 /path/to/ep_toy_diagnostic.py 2>/dev/null | grep OUTCOME; done
```

Full forensics + trajectories: `ep_scale_collapse_assets/EP_TOY_FINDINGS.md`.

## Triage questions for the fix owner

- Is COLLAPSE curable by a **more robust / damped `HierarchicalFactor` scale
  moment-match** (or a deterministic per-factor optimiser to cut the sampler noise that
  drives basin selection)? Note: naive damping (delta=0.5) made `slope_hierarchy` *worse*
  — so the standing diagnostics hint "consider damping, delta < 1" likely mis-diagnoses
  this mode and should be revised alongside the fix.
- Should the **F10 sigma-collapse guard** fire on the COLLAPSE run? It currently passes a
  scatter≈0 / error≈0 parent silently.
- Should the **`InitializerException`** be caught inside the EP loop and recorded as a bad
  projection rather than aborting the fit?

## Origin

Cheap CPU diagnostic spun out of `slope_hierarchy#1` goal 2 (private repo
Jammy2211/slope_hierarchy) to decide whether the EP scale-parameter pathology there was
problem-specific (N=5 / boundary / lensing) or a framework property. It is a framework
property — reproduced here off-boundary and off-lensing. Companion research prompt:
`draft/research/graphical_ep/ep_scale_parameter_error_diagnostic.md`.
