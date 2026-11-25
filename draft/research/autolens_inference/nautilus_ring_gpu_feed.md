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
