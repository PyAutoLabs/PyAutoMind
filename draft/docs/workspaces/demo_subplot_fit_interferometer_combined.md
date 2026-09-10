# Demo `subplot_fit_interferometer_combined` in a multi-dataset example

Type: docs
Target: workspaces
Repos:
- autolens_workspace
Themes:
- visualization
Difficulty: medium
Autonomy: safe
Priority: normal
Status: draft
Consequence: notify
Witness: `aplt.subplot_fit_interferometer_combined` is called from a multi-dataset interferometer example under `autolens_workspace/scripts/multi/` with a `fit_list` of genuinely distinct fits (not `[fit, fit]`), and that script runs to completion under the smoke profile.
Review-minutes: 0
Unattended: ready
Filed: 2026-09-09

Split from `plot_coverage_followups.md` on 2026-09-09 (item 1 of 4). That file
was a container of four independent follow-ups and said so — "do **not**
bulk-issue them as a series" — so it has been split into one prompt per item and
archived.

## Why

PyAutoLens#668 **exported** `aplt.subplot_fit_interferometer_combined` for API
symmetry — imaging's `subplot_fit_combined` was exported, the interferometer
equivalent was not — but nothing demonstrates it.

## What

It takes a `fit_list`, so its home is a multi-dataset interferometer example,
not the single-fit `scripts/interferometer/plot.py`. Passing `[fit, fit]` there
would teach a wrong idiom (the same reasoning that kept the `*_x1_plane` pair
out of the originating task).

Candidate home: `autolens_workspace/scripts/multi/` — `multi/plot.py` already
demonstrates the imaging combined subplots (`subplot_fit_combined`,
`subplot_fit_combined_log10`), and `multi/features/imaging_and_interferometer/`
provides a real multi-interferometer fit context.

- @autolens_workspace
