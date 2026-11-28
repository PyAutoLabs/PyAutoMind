# CPU-fed GPU Nautilus fits on the COSMOS-Web Ring — merged

Merged 2026-11-25 under the human's `/prm`: [autolens_inference#75](https://github.com/PyAutoLabs/autolens_inference/pull/75), CI green, head an ancestor of origin/main.

## Delivered

- Eight complete conditional fits to the observed JWST COSMOS-Web Ring transferred the ordered-feeder experiment from autofit_profiling#43 to a real imaging likelihood.
- CPU feeders increased whole-fit time by 12.8% and 13.6% against serial full-batch GPU; CPU-only finished fastest on both seeds. Native posterior-derived output took 39.8–42.6 s on GPU vs 9.4–10.4 s on CPU.
- Keep native sampler defaults; a matched posterior replay would be needed to establish any hybrid placement benefit.

## Original prompt

# Do CPU feeders shorten a complete Nautilus fit on JWST ring imaging?

Type: research
Target: @autolens_inference
Epic: nautilus-fast-likelihoods
Consequence: judge
Lane: local-dev

> continue

Run the bounded phase 4 transfer test from profiling PR #43 on the committed COSMOS-Web Ring JWST F444W imaging and single-Sérsic-source tracer. Reuse its 2.1 arcsec mask, contaminant noise scaling, 4/2/2 oversampling and PSF. Hold the archived mass, field and light parameters fixed except Einstein radius and the source centre coordinates, with uniform priors of ±0.05 arcsec about the reference values. This conditional engineering fixture does not refit the published lens. Use native AnalysisImaging, serial training, native cadence, 200 live points and logical batches of 100 as in #43.

Compare full-batch CPU, full-batch GPU, serial split GPU and two CPU feeders with one GPU on the RTX 2060, seeds 1 and 2 in reverse order. Reuse #43's ordered geometry/transform feeder and fixed-width compilation controls. If GPU memory limits device width, retain logical batches and document the pre-timing width selection. Verify CPU/GPU and ragged-batch likelihoods on common near-reference and off-centre points (absolute 1e-6 or relative 1e-10). Require both seeds to improve whole-fit wall by 5% against serial full-batch GPU and beat the matched split control. Check complete outputs, counts, ESS, evidence within 0.1 and posterior means within 0.1 serial posterior SD. Record failures, hardware and bounds on interpretation. Publish a draft PR, human merge.

[Predecessor](https://github.com/PyAutoLabs/autofit_profiling/pull/43) · [Insight's imaging inference task](https://github.com/PyAutoLabs/PyAutoInsight/blob/main/tasks/hst_mass_samplers_wave1.md) · [Pulse profiling task](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/autofit_profiling_bootstrap.md). This is a local engineering pilot using separate JWST data. Campaign ownership and promotion remain unchanged.

Issue: https://github.com/PyAutoLabs/autolens_inference/issues/74

## Outcome

[Draft PR #75](https://github.com/PyAutoLabs/autolens_inference/pull/75) awaits human review. Eight completed conditional fits. CPU-only finished fastest in both seeds and CPU-fed GPU missed the promotion threshold. [Timings, precision exceptions and posterior-output follow-up](https://github.com/PyAutoLabs/autolens_inference/blob/573bf267e22a13c195966747f71c3350a78d984d/results/misc/nautilus_ring_gpu_feed/README.md).
