# Cluster usability — from the first plot to a paper-scale fit

Type: feature
Target: PyAutoLens
Epic: cluster-usability
Priority: high
Status: draft for human review
Consequence: judge

Prioritise this work ahead of the [cluster strong-lensing science epic](source_cluster_arc.md). The goal is to make today's cluster modelling usable at three scales. A reader should be able to see the constraints, identify which multiple-image family fits poorly, and follow that family into a diagnostic figure. The same examples should tell developers how runtime and inference behave as the science case gets harder. New lensing methods belong in the science epic.

## Three datasets shared across projects

| Dataset | Science case | What it should demonstrate |
| --- | --- | --- |
| **Simple** | The introductory cluster with two multiple-image families. Use it throughout the core workspace walkthrough. | A newcomer can load the catalogue, recognise each family in the image and interpret a first fit. It also provides a quick baseline for all three projects. |
| **Intermediate** | Pandora, with seven multiple-image families and a richer lens-member catalogue. | Family markers and the legend stay readable in a crowded field. Profiling and inference exercise multiple source redshifts and a larger galaxy population. |
| **Complex** | The Hubble Frontier Fields (HFF) lens and existing model used in the PyAutoLens II paper. | Figures, runtime measurements and inference runs exercise the family catalogue and member population of the paper fit. Confirm the exact cluster, model revision and distributable inputs before adopting it. |

For each tier, record the input provenance, family IDs and redshifts, member catalogue, model configuration and image scale. Use those identifiers across the workspace, visualization, profiling and inference projects so that a result labelled “intermediate” can be traced to the same Pandora case. Distinguish observed constraints, simulated truth and paper reference models when judging a fit.

## Proposed work in priority order

1. **Establish the datasets and protect profiling inputs.** Inventory the existing examples against the three tiers. Continue the stale-data fix on the existing profiling issue. Before profiling an existing cluster, validate the scaling catalogue with the consuming reader and load the tracer. A missing or unusable catalogue, or a tracer that fails to deserialize, should stop the run with the offending path and instructions to preserve the directory and regenerate a fresh copy. Exercise stale and current fixtures, checking that rejected fixtures remain intact and a current fixture reaches profiling. [autolens_profiling #445](https://github.com/PyAutoLabs/autolens_profiling/issues/445)

2. **Make the first figure worth opening.** Keep the cluster-level `dataset.png` and add a view of the observed family positions over the cluster image. Use that overlay as the first workspace view when imaging is available. Compare the stretch, colormap, figure size and field framing on all three tiers. On a field spanning −30″ to +30″ the arcs, lens galaxies and family markers should be individually recognisable. Also inspect the larger Pandora cutout shown by the current example. Reproduce the sequence of empty Matplotlib windows in an interactive run and verify that every window the introductory script opens contains an intended figure.

3. **Show which family drives a poor fit.** In the cluster fit overview, including the image-backed and points-only views, keep the family redshift and replace the legend's error-bar value with that family's total χ² from the fitted likelihood. Label source-plane χ² explicitly when that is the quantity fitted. Use one value per family. Check the displayed values against the fit object with a deliberately poor family, then follow it into the per-image diagnostic. Suppress the default per-family dataset and old summary plots. The detailed `point_#/fit_per_image.png` becomes `point_#/fit.png`. Review the saved and interactive figures together through `autolens_visualization` and Eyes.

4. **Measure and improve the slow paths.** Time `scripts/cluster/start_here.py` and `scripts/cluster/simulator.py` separately. For the tutorial, distinguish first download, cached load, first useful figure and fit time. For the simulator, distinguish setup, first JAX compilation, synchronised warm execution and file output. Record dataset, backend and hardware. Optimise the measured bottleneck, then repeat the timings and compare outputs on the same inputs.

5. **Exercise real workloads in Pulse and Insight.** Run the profiling and inference examples on each tier. Through `autolens_profiling` and Pulse, measure the likelihood and solver workloads used by the corresponding fit. Through `autolens_inference` and Insight, run the searches and record convergence, cost and agreement with simulated truth or the paper reference where applicable. Report which tiers completed and any run limits alongside the results.

6. **Review the workspace examples with the author.** Use Brain's workspace documentation agent to compare the cluster scripts with established introductory examples. First review a proposed reading order and a before/after excerpt from `start_here.py` with Jammy. Then review each example in turn. Teach the CSV API through the walkthrough, retain `csv_api.py` as a separate reference away from the core entry points, and propose where the mass-parameterization material belongs once readers have fitted Simple. Settle the sequence and level of detail together before rewriting the package.

## First review

Review the proposed Simple → Pandora → HFF progression and identify the paper model for Complex. For the first visual comparison, show the current introductory figure beside the proposed image overlay, then show a cluster fit overview beside the detailed fit for its worst-fitting family. These comparisons give the author concrete figures and tutorial text to revise before the defaults are adopted.
