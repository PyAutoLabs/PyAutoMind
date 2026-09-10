# Demo `subplot_ellipse_errors` from a real ellipse model-fit

Type: docs
Target: workspaces
Repos:
- autogalaxy_workspace
Themes:
- visualization
Difficulty: large
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 25
Unattended: ready
Filed: 2026-09-09

Split from `plot_coverage_followups.md` on 2026-09-09 (item 2 of 4). That file
was a container of four independent follow-ups and said so — "do **not**
bulk-issue them as a series" — so it has been split into one prompt per item and
archived.

## Why

`ag.plot.subplot_ellipse_errors` is demonstrated nowhere in autogalaxy_workspace.

## What

It takes `fit_pdf_list: List[List[FitEllipse]]` — outer list one entry per
posterior sample, inner list one `FitEllipse` per ellipse. A standalone
`plot.py` runs no search, so this needs a real ellipse model-fit to produce
genuine samples. Do **not** fake it by perturbing parameters: the figure's whole
point is the inference-derived error region.

Likely home: an ellipse results/`fit.py`-adjacent script that already has a
`Result`, rather than `scripts/ellipse/plot.py`.

- @autogalaxy_workspace

## Sizing note

Sized `large` / `supervised` on the split (2026-09-09), against the `medium`
the container implied: the demo cannot be written without running a real
ellipse model-fit to obtain posterior samples, so it needs compute and a
judged figure, not just an example script.
