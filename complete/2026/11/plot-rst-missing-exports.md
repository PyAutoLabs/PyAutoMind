Shift task from M3.1 shift B `2026-11-14-pm3` (PyAutoMind#571). Shipped as PyAutoGalaxy#716 (253df876e) and PyAutoLens#863 (4e62a6ccc), merged 2026-11-16 in-turn on the human's merge command, both `ci-verdict` GREEN with Heart dev-ship GREEN. Issue PyAutoLens#862.

**Built (shift worker):** `docs/api/plot.rst` in both libraries now lists every `aplt` export. PyAutoLens gains 44 missing entries and a new "Dataset Subplots" section. PyAutoGalaxy gets the same change plus `|mu|` docstring fixes, which keep the sphinx warning count at its baseline.

**Close-out:** the watcher refused both PRs for an unattended merge. The worker took two decisions and labelled them `decision-taken`: the extra docstring fixes, and filing `subplot_fit_interferometer_tracer` with the fit subplots instead of under "Dataset Subplots" as the Witness said. The human reviewed both PRs (5 min for shift B) and said to merge them as they are.

**Follow-up (worker suggestion):** have `/audit_docs` check the `plot.rst` autosummary blocks against the live `aplt` namespace.

## Original prompt

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
Consequence: glance
Witness: A diff of the names `autolens.plot` exports against the autosummary entries in `docs/api/plot.rst` is empty, the six named dataset/fits symbols sit under a new 'Dataset Subplots' heading, the same diff is empty for `autogalaxy.plot` and its `plot.rst`, and the sphinx warning count stays at baseline.
Review-minutes: 3
Unattended: ready
Verified: 2026-11-14 93b236fc (PyAutoGalaxy), d9a22748 (PyAutoLens)
Lane: any
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
