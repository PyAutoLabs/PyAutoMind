# Cluster usability — from the first plot to a paper-scale fit

Type: feature
Target: PyAutoLens
Epic: cluster-usability
Priority: high
Status: Simple family fit figures in review. Pandora and MACS J0416 reviews pending.
Consequence: judge

Prioritise this work ahead of the [cluster strong-lensing science epic](source_cluster_arc.md). The goal is to make today's cluster modelling usable at three scales. A reader should be able to see the constraints, identify which multiple-image family fits poorly, and follow that family into a diagnostic figure. The same examples should tell developers how runtime and inference behave as the science case gets harder. New lensing methods belong in the science epic.

## Three datasets shared across projects

| Dataset | Science case | What it should demonstrate |
| --- | --- | --- |
| **Simple** | The simulated introductory cluster with two multiple-image families. Use it throughout the core workspace walkthrough. | A newcomer can load the catalogue, recognise each family in the image and interpret a first fit. It also provides a quick baseline for all three projects. |
| **Intermediate** | Pandora (Abell 2744), with seven observed gold families, 25 images and 188 scaling members. Use it as the first real-data example. | Family markers and the legend stay readable in a crowded field. Profiling and inference exercise multiple source redshifts and a larger galaxy population. |
| **Complex** | MACS J0416, the PyAutoLens II cluster case. Use the [Bergamini et al. published best model](https://www.fe.infn.it/astro/lensing/M0416_Bergamini22/) with 237 images across 88 families and 222 mass components. | Figures, runtime measurements and inference runs exercise the family catalogue and member population of the paper fit. Pin the model revision and input checksums. Use the case study’s download procedure while redistribution terms are checked. Record the fit configuration for any reduced pilot. |

For each tier, record the input provenance, family IDs and redshifts, member catalogue, model configuration and image scale. Use those identifiers across the workspace, visualization, profiling and inference projects so that a result labelled “intermediate” can be traced to the same Pandora case. Distinguish observed constraints, simulated truth and paper reference models when judging a fit.

## Proposed work in priority order

1. **Establish the datasets and protect profiling inputs.** Inventory the existing examples against the three tiers. Profiling issue [#445](https://github.com/PyAutoLabs/autolens_profiling/issues/445) closed with [PR #532](https://github.com/PyAutoLabs/autolens_profiling/pull/532). Before reusing Simple, the cache guard checks that the member CSV exists and deserializes the tracer. The remaining case is a present but malformed scaling catalogue: validate it with the consuming reader before profiling. A missing or unusable catalogue, or a tracer that fails to deserialize, should stop the run with the offending path and instructions to preserve the directory and regenerate a fresh copy. Exercise stale and current fixtures, checking that rejected fixtures remain intact and a current fixture reaches profiling.

2. **Make the first figure worth opening.** Keep the cluster-level `dataset.png` and add a view of the observed family positions over the cluster image. Use that overlay as the first workspace view when imaging is available. Compare the stretch, colormap, figure size and field framing on all three tiers. On a field spanning −30″ to +30″ the arcs, lens galaxies and family markers should be individually recognisable. Also inspect the larger Pandora cutout shown by the current example. Reproduce the sequence of empty Matplotlib windows in an interactive run and verify that every window the introductory script opens contains an intended figure.

3. **Show which family drives a poor fit.** In the cluster fit overview, including the image-backed and points-only views, keep the family redshift and replace the legend's error-bar value with that family's total χ² from the fitted likelihood. Label source-plane χ² explicitly when that is the quantity fitted. Use one value per family. Check the displayed values against the fit object with a deliberately poor family, then follow it into the per-image diagnostic. Suppress the default per-family dataset and old summary plots. The detailed `point_#/fit_per_image.png` becomes `point_#/fit.png`. Review the saved and interactive figures together through `autolens_visualization` and Eyes.

4. **Measure and improve the slow paths.** Time `scripts/cluster/start_here.py` and `scripts/cluster/simulator.py` separately. For the tutorial, distinguish first download, cached load, first useful figure and fit time. For the simulator, distinguish setup, first JAX compilation, synchronised warm execution and file output. Record dataset, backend and hardware. Optimise the measured bottleneck, then repeat the timings and compare outputs on the same inputs.

5. **Exercise real workloads in Pulse and Insight.** Run the profiling and inference examples on each tier. Through `autolens_profiling` and Pulse, measure the likelihood and solver workloads used by the corresponding fit. Through `autolens_inference` and Insight, run the searches and record convergence, cost and agreement with simulated truth or the paper reference where applicable. Report which tiers completed and any run limits alongside the results.

6. **Review the workspace examples with the author.** Use Brain's workspace documentation agent to compare the cluster scripts with established introductory examples. First review a proposed reading order and a before/after excerpt from `start_here.py` with Jammy. Then review each example in turn. Teach the CSV API through the walkthrough, retain `csv_api.py` as a separate reference away from the core entry points, and propose where the mass-parameterization material belongs once readers have fitted Simple. Settle the sequence and level of detail together before rewriting the package.

## Author review of the Simple figures

The author approved the Simple → Pandora → MACS J0416 progression and reviewed the two-family Simple simulation. Keep the greyscale image stretch and distinguish the two families by both colour and shape (amber circles and cyan diamonds in Simple). Check the palette and legend on Pandora and MACS J0416 as their catalogues are added.

The default family fit figure has four panels:

| | Left | Right |
| --- | --- | --- |
| Top | Cluster overview with family redshifts, the fitted statistic, and image numbers for the selected family. | One equally scaled zoom per image. For an image-plane fit, draw the observation, paired model position and positional uncertainty. For a source-plane fit, draw the back-traced observation, its propagated uncertainty and the fitted source centre. |
| Bottom | Per-image contributions ranked from largest to smallest. | All images of the selected family back-traced to their source plane, with the fitted source centre marked. Keep this context for either likelihood. |

Use PyAutoLens spatial-axis conventions in arcseconds. Centre each individual zoom on its actual observed or back-traced coordinates. Keep the two lower plotting areas the same size. Offer a single shared-coordinate detail panel as an option.

Up to six image zooms fit on one page in image-number order. For larger families, put the six largest contributions on page one and continue in groups of six. Preserve original image numbers, repeat the overview, full ranking and source-plane summary, and highlight the images on each page. The scratch renderer exercised six- and seven-image synthetic layouts in both planes.

Use the statistic supplied by the fitted likelihood. In particular, a nearest-image displacement alone cannot represent an all-pairs mixture. If a repeat-pairing fit penalizes an unmatched prediction, identify that penalty separately so the reader can reconcile the plotted contributions with the family total.

The Simple family diagnostics and gallery renders are open for review in [PyAutoLens #884](https://github.com/PyAutoLabs/PyAutoLens/pull/884) and [autolens_visualization #20](https://github.com/PyAutoLabs/autolens_visualization/pull/20). With a 0.003″ offset in the first source’s y coordinate, image 4 contributes 66.44 of the family’s 88.22 source-plane χ² and 66.11 of its 86.80 image-plane χ². The saved figures and the interactive figure construction were checked on Simple. Review on Pandora and MACS J0416 remains open.
