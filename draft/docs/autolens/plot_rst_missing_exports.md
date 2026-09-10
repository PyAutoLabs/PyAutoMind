# `docs/api/plot.rst` omits already-exported plot symbols

Type: docs
Target: autolens
Repos:
- PyAutoLens
- PyAutoGalaxy
Themes:
- visualization
Difficulty: medium
Autonomy: safe
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 15
Unattended: ready
Filed: 2026-09-09

Split from `plot_coverage_followups.md` on 2026-09-09 (item 3 of 4). That file
was a container of four independent follow-ups and said so — "do **not**
bulk-issue them as a series" — so it has been split into one prompt per item and
archived.

## Why

PyAutoLens#668 added its two new exports to `docs/api/plot.rst`, but the file
was already missing several symbols that `autolens.plot` exports.

## What

Add the missing symbols:

- `subplot_imaging_dataset`
- `subplot_imaging_dataset_list`
- `fits_imaging`
- `fits_interferometer`
- `subplot_fit_interferometer_tracer`
- `subplot_interferometer_dirty_images`

There is no "Dataset Subplots" heading in the rst at all — the dataset-level
functions have no home in it. Check the autogalaxy equivalent for the same class
of drift, and consider whether `/audit_docs` should cover `plot.rst`
autosummary blocks against the live `aplt` namespace.

- @PyAutoLens (and probably @PyAutoGalaxy)
