# `PlotterEllipse.fit_ellipse` writes every variant to `ellipse_fit.png`, so only the last survives

Type: bug
Target: autogalaxy
Repos:
- @PyAutoGalaxy
Difficulty: small
Priority: normal
Status: draft
Consequence: judge
Witness: rendering `autogalaxy_visualization/scripts/ellipse/visualization.py` yields four distinct `fit_ellipse` variants on disk (data, data without ellipses, and their log10 versions), not one `ellipse_fit.png`.
Filed: 2026-09-29

## Symptom

In `PlotterEllipse.fit_ellipse` (`autogalaxy/ellipse/model/plotter.py`) the
`data`, `data_no_ellipse` and log10 variants all write the same filename,
`ellipse_fit.png`. Each call overwrites the previous one, so only the last
variant survives on disk and the others are silently lost.

## Provenance

Found 2026-09-29 while rendering the new `autogalaxy_visualization` project
repo (PyAutoEyes phase 3, PyAutoMind#452): the ellipse producer toggles four
`fit_ellipse` variants but the gallery only ever holds one PNG. Candidate
PyAutoEyes critique.

## Fix sketch

Give each variant its own filename (e.g. `ellipse_fit`, `ellipse_fit_no_ellipse`,
`ellipse_fit_log10`, `ellipse_fit_no_ellipse_log10`), then re-render
`autogalaxy_visualization` so its manifest picks up the extra figures.
