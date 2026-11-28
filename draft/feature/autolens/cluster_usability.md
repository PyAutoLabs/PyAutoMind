# Cluster usability — from the first plot to a paper-scale fit

Type: feature
Target: PyAutoLens
Epic: cluster-usability
Priority: high
Status: Simple, Pandora and MACS J0416 figures live on PyAutoEyes. Simple CPU profiling (both likelihoods and a paired starting-grid comparison) merged 2026-11-28 in autolens_profiling#537. Phase 3.2 (solver grid default) and phase 3.5 (Pandora profiling, now unblocked) are filed.
Consequence: judge

Prioritise this work ahead of the [cluster strong-lensing science epic](source_cluster_arc.md). The goal is to make today's cluster modelling usable at three scales. A reader should be able to see the constraints, identify which multiple-image family fits poorly, and follow that family into a diagnostic figure. The same examples should tell developers how runtime and inference behave as the science case gets harder. New lensing methods belong in the science epic.

## Three datasets shared across projects

| Dataset | Science case | What it should demonstrate |
| --- | --- | --- |
| **Simple** | The simulated introductory cluster with two multiple-image families. Use it throughout the core workspace walkthrough. | A newcomer can load the catalogue, recognise each family in the image and interpret a first fit. It also provides a quick baseline for all three projects. |
| **Intermediate** | Pandora (Abell 2744), with seven observed gold families, 24 catalogued images and 188 scaling members. Use it as the first real-data example. | Family markers and the legend stay readable in a crowded field. Profiling and inference exercise multiple source redshifts and a larger galaxy population. |
| **Complex** | MACS J0416, the PyAutoLens II cluster case. Use the [Bergamini et al. published best model](https://www.fe.infn.it/astro/lensing/M0416_Bergamini22/) with 237 images across 88 families and 222 mass components. | Figures, runtime measurements and inference runs exercise the family catalogue and member population of the paper fit. Pin the model revision and input checksums. Use the case study’s download procedure while redistribution terms are checked. Record the fit configuration for any reduced pilot. |

For each tier, record the input provenance, family IDs and redshifts, member catalogue, model configuration and image scale. Use those identifiers across the workspace, visualization, profiling and inference projects so that a result labelled “intermediate” can be traced to the same Pandora case. Distinguish observed constraints, simulated truth and paper reference models when judging a fit.

## Proposed work in priority order

1. **Establish the datasets and protect profiling inputs.** Inventory the existing examples against the three tiers. Profiling issue [#445](https://github.com/PyAutoLabs/autolens_profiling/issues/445) closed with [PR #532](https://github.com/PyAutoLabs/autolens_profiling/pull/532). Before reusing Simple, the cache guard checks that the member CSV exists and deserializes the tracer. The follow-up in [profiling #537](https://github.com/PyAutoLabs/autolens_profiling/pull/537) validates a present but unusable scaling catalogue with the consuming reader before profiling. A missing or unusable catalogue, or a tracer that fails to deserialize, should stop the run with the offending path and instructions to preserve the directory and regenerate a fresh copy. Exercise stale and current fixtures, checking that rejected fixtures remain intact and a current fixture reaches profiling.

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

The Simple family diagnostics, cluster dataset and walkthrough figures, and standalone point-source styling merged in [PyAutoLens #884](https://github.com/PyAutoLabs/PyAutoLens/pull/884). The production gallery merged in [autolens_visualization #20](https://github.com/PyAutoLabs/autolens_visualization/pull/20). With a 0.003″ offset in the first source’s y coordinate, image 4 contributes 66.44 of the family’s 88.22 source-plane χ² and 66.11 of its 86.80 image-plane χ². The saved figures and the interactive figure construction were checked on Simple.

[PyAutoEyes #36](https://github.com/PyAutoLabs/PyAutoEyes/pull/36) published the updated [live Eyes dashboard](https://pyautolabs.github.io/PyAutoEyes/). At publication it offered 311 distinct figures, including 86 PyAutoLens figures. All 30 cluster and standalone point-source PNGs matched their gallery manifest checksums.

## Pandora publication

The [workspace catalogue](https://github.com/PyAutoLabs/autolens_workspace/blob/ba7f7738538069ea4c725a3797b10582eb970d0e/dataset/cluster/a2744/point_datasets.csv) has 24 observed positions across seven families. In catalogue order the image counts are 3, 4, 4, 3, 3, 3 and 4. The dataset README and walkthrough now use the measured count.

The first review uses the cached 600 × 600 HST H-band cutout at 0.3″ per pixel. The catalogue axes increase east and north. The cutout’s FITS columns increase west and its rows increase north. The review reoriented the raster and used its reference pixel to place the catalogue origin. Across all 24 positions the largest difference between the catalogue’s tangent-plane approximation and the FITS WCS was 0.0036″. The workspace and gallery now share this registration.

The source-plane diagnostic uses the two CSV dPIE galaxies, the CSV NFW halo and all 188 scaling members. The lens parameters are fixed at a starting configuration, with member reference velocity dispersion 150 km/s and an analytically solved centre for each source. At this starting point, `point_6` contributes 14,234.79 to the position χ², including 6,397.30 from image 4. The author approved this diagnostic and the registered overlay.

[Workspace #686](https://github.com/PyAutoLabs/autolens_workspace/pull/686) merged the HST registration, the corrected image count and the pinned cutout download. [Gallery #21](https://github.com/PyAutoLabs/autolens_visualization/pull/21) merged four cluster overviews and seven source-plane family figures. [PyAutoEyes #37](https://github.com/PyAutoLabs/PyAutoEyes/pull/37) published all eleven under `PyAutoLens → cluster_pandora` on the [live Eyes dashboard](https://pyautolabs.github.io/PyAutoEyes/). At publication the dashboard had 322 distinct figure choices, including 97 PyAutoLens figures. The eleven live Pandora PNGs matched the gallery manifest by size and SHA-256. Pandora profiling and inference remain open.

The public panel API merged in [PyAutoLens #890](https://github.com/PyAutoLabs/PyAutoLens/pull/890). The [workspace walkthrough and notebook](https://github.com/PyAutoLabs/autolens_workspace/pull/687) introduce each panel separately on `point_6`: find the family on the sky, rank the contributions, inspect Image 4, and compare all four back-traced images at their common source plane. The final call assembles the same panels into the family subplot. The walkthrough depends on the library release.

## MACS J0416 publication

The scratch review uses all 237 observed positions in 88 knot families and the 222-component [Bergamini et al. model release](https://www.fe.infn.it/astro/lensing/M0416_Bergamini22/). The catalogue uses north/west offsets. All 237 positions fall on the [HST F160W mosaic](https://archive.stsci.edu/pub/hlsp/frontier/macs0416/images/hst/v1.0-epoch2/), registered using the FITS sky coordinates. The review pins the input checksums and preserves the catalogue image IDs.

The overview uses source redshift for colour. The published image-plane offsets from `chires.dat` give an all-image RMS of 0.430″ and place family 101 first by family RMS (1.081″). For the fixed published masses and analytically solved source centres, family 210.4 has the largest PyAutoLens source-plane χ² (11.70). Separate family views show those two diagnostics and exercise the six-image layout on family 14.1. The author approved the catalogue IDs throughout, tighter spacing around the image zooms and the “All back-traced images” panel. The nine figures comprise three source-plane family subplots, four standalone panels for family 210.4, and two comparisons with the published image-plane offsets for families 101 and 14.1. Image 210.4c contributes 9.49 of its family’s 11.70 source-plane χ². Image 101c has the largest published separation in its family at 1.75″. Profiling and inference for this tier remain open.

[PyAutoLens #891](https://github.com/PyAutoLabs/PyAutoLens/pull/891) merged the catalogue-labelled panels. [Gallery #22](https://github.com/PyAutoLabs/autolens_visualization/pull/22) published the producer and nine figures, and [Eyes #38](https://github.com/PyAutoLabs/PyAutoEyes/pull/38) added them to the [live Eyes dashboard](https://pyautolabs.github.io/PyAutoEyes/). At publication the board had 331 distinct figure choices, including all nine under `PyAutoLens → cluster_macs_j0416`. Each live PNG matched its manifest size and SHA-256 and was byte-for-byte identical to the author-approved scratch file.

## Simple profiling

[Profiling #537](https://github.com/PyAutoLabs/autolens_profiling/pull/537) aligns Simple with the reviewed gallery. The simulator and both likelihoods now use the gallery's velocity-dispersion dPIE model, with two main galaxies, ten scaling members and an NFW halo. All five `point_0` observations at z = 1 and both `point_1` observations at z = 2 match the pinned gallery catalogue exactly, including their 0.005″ uncertainties. At the fitted prior medians the back-traced coordinates agree exactly on both source planes for the seven observations and 256 additional test rays.

| Likelihood | First call after compile (ms) | Warm median (ms) | Warm p10–p90 (ms) | Absolute JAX–NumPy log L difference |
| --- | ---: | ---: | ---: | ---: |
| Source plane | 2.67 | 0.518 | 0.467–0.594 | 4.58e-09 |
| Image plane | 13.66 | 8.918 | 8.271–10.401 | 1.75e-10 |

Times are per likelihood evaluation over both families on the local i9-10885H CPU using JAX FP64. Both source centres are solved analytically. The warm median uses five warm-ups and 200 synchronized calls. The earlier three-plus-three `b0` measurements use a different catalogue and parameter vector and are archived separately.

The standard image-plane solver starts at 1″ per pixel on a 100 × 100 grid. It returns four predictions for the five `point_0` observations and two for `point_1`. The second `point_0` observation at (y, x) = (10.362″, 8.143″) lies 2.764″ from its nearest prediction. At the same solved source centre, field size and 0.001″ refinement precision, 0.5″ also misses it. Both 0.25″ and 0.2″ starting grids recover it, at separations of 0.00745″ and 0.00672″ respectively. The standard-grid image-plane time is diagnostic because it measures an incomplete solve.

A paired run then timed the full solved image-plane likelihood at both starting grids. Both runs used the same fitted prior-median mass model, solved source centres, 100″ field width and 0.001″ refinement precision.

| Starting grid | `point_0` matched | `point_1` matched | Warm median (ms) | Warm p10–p90 (ms) | Absolute JAX–NumPy log L difference |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1.0″ · 100 × 100 | 4/5 | 2/2 | 11.778 | 8.840–17.609 | 1.75e-10 |
| 0.25″ · 400 × 400 | 5/5 | 2/2 | 51.101 | 43.292–80.163 | 2.13e-13 |

The 0.25″ grid took 4.34× as long per evaluation as the 1″ control measured alongside it. The 8.918 ms figure above came from a separate run. Each matched image has a distinct prediction within 0.01″, twice the catalogue positional uncertainty. For the second `point_0` observation the nearest prediction moved from 2.764″ to 0.00745″. The comparison covers one fitted mass model and two solved source centres. The results and driver are in [the starting-grid experiment](https://github.com/PyAutoLabs/autolens_profiling/tree/feature/simple-cluster-profiling/results/cluster/image_plane/simple/jax_cpu_na_fp64/local_laptop/experiments/starting_grid_spacing). The profiling solver settings are unchanged in #537. Following the author's 2026-11-26 ruling, [phase 3.2](cluster_usability_p3_2_solver_grid_default.md) chooses the coarsest default grid that recovers every image on each tier and states the per-solve cost of the change. [Phase 3.5](cluster_usability_p3_5_pandora_profiling.md) profiles Pandora and re-times Simple on that grid once #537 merges.
