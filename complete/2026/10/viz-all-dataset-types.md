## Outcome
autolens_visualization and PyAutoEyes now cover every PyAutoLens dataset type. There is one `scripts/<domain>/visualization.py` per dataset type, each writing only `dataset.png` + `fit.png`:
- imaging and interferometer (unchanged)
- interferometer_datacube (per channel)
- point_source_image_chi_squared and point_source_source_chi_squared (shared dataset)
- multi_galaxy and group
- cluster (one pair per source plane)
- multi_dataset (one pair per band)
- weak

Datasets are small, seeded simulations under `dataset/`. Each simulator and its producer share the same model from `true_models/`.

The PyAutoEyes board orders the lens domains canonically, with one browser per domain.

## Decisions
- Variants get their own top-level folder rather than an extra producer inside the parent domain. Human call 2026-10-21 ("it feels strange having a one off nested folder"). This trades a little symmetry with autolens_workspace for one producer per folder.
- The cluster producer calls PlotterPoint directly. VisualizerPoint's critical-curve step cost ~100 s and is unused by the two subplots (byte-identical output).
- Shipped under the Heart RED development override (recorded on issue #4, both PRs and autonomy_log).

## Follow-up
Bespoke point-source, cluster and weak visualizations, driven by the human through the Eyes dashboard.

## Original prompt

# Visualize every PyAutoLens dataset type (dataset.png + fit.png) in autolens_visualization + PyAutoEyes

Type: feature
Target: autolens_visualization
Repos:
- autolens_visualization
- PyAutoEyes
Difficulty: medium
Autonomy: human-required
Priority: normal
Status: formalised
Consequence: judge
Issued: 2026-10-21
Issue: https://github.com/PyAutoLabs/autolens_visualization/issues/4

## Original request (verbatim)

PyAutoEyes and autolens_visualization are set up to allow me to see all visualization used for imaging and interferometer data. I now want us to extend them to contain all types of datasets in PyAutoLens:

imaging
interferometer
point source image chi squared
point source source chi squared
multi_galaxy
group
cluster
multi dataset
datacube (inside interferometry)
weak

, noting that we should retain the structure whereby in scripts these datasets are folder names (none go in misc) mirrorin the structure of autolens_workspace. This structure pairs nicely to how datasets are grouped and displayed on the PyautoEyes dashboard, which will need extending. For now, I only want you to add two images per dataset, its dataset.png file and its fit.png file. Note that for many datasets, including point sources, cluster and weak, we either won't have a dediciated and bespoke visualization yet (which the follow up issue will be me fixing via the Eyes dashboard) or it will use a visualization from another scale (e.g. cluster uses galaxy scale plots) and look rubbish, again for now I just want the infrastructue in place and we iterate from there).

## Notes

- Heart was RED at start_dev (2026-10-21); human invoked the development-only Heart RED override.
- Follow-up (human, via Eyes dashboard): bespoke point / cluster / weak visualizations.
