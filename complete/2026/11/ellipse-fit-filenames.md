# ellipse-fit-filenames — ellipse fit plots no longer overwrite one another

- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/698
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/699
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/699
- completed: 2026-11-10

## What happened
- Held on 2026-11-10 because Galaxy main was red (11 pixelization figure-of-merit tests). That cause was confirmed as
  PyAutoArray#683 and fixed by pseudo-det-rebaseline (PyAutoGalaxy#701).
- After #701 merged and Galaxy main was green, main was merged into the branch (8dbb25d). Exact-head CI was green on
  unittest 3.12, 3.13, nojax and docs-build, then merged via the human-authorized /prm (merge 6a5e022).
- Earlier gates (from the ship): test_autogalaxy 1468 passed apart from the 11 known main failures; smoke 154/0;
  independent review CLEAN after the duplicate no_ellipse variants were dropped.
- Local worktree ~/Code/PyAutoLabs-wt/ellipse-fit-filenames is on the dev box, not this cloud session, and needs
  removing there with worktree_remove.

## Original prompt

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
Issued: 2026-11-10

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
