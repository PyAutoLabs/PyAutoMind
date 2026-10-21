# Point-source positions panels: extent, markers, noise and titles

Consequence: judge
Autonomy: human-required
Issued: 2026-10-21
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/785

@PyAutoLens @autolens_visualization

## Origin (2026-10-21, Eyes review of the point_source_* figures in scratch)

`point_source_*/visualization/dataset.png` is the old bare positions plot:
- the positions are tiny dots
- points are clipped at the top and right edges (axes ±1.5″, images out to ~±2.2″)
- the `x (")` / `y (")` axis labels overlap the tick labels
- no noise is shown

The human said "I thought we fixed this but maybe not" and agreed to every point below.

## Approved decisions (human, in chat)

1. **Extent.** The positions panel extent is the PointSolver grid's extent when a solver is available. This ties the figure to where the model can find images; zooming out is acceptable and wanted. With no solver, fall back to the #783 critical-curve region (`critical_curve_grid_from`) or the data bounding box plus a margin, so nothing is clipped.
2. **Axis labels.** Remove the `x (")` / `y (")` labels.
3. **Markers.** Use large filled markers for positions.
4. **Noise.** Draw a circle at the true positions noise-map radius (one isotropic σ per position, so a circle, not error-bar crosses), and always put σ in the legend, e.g. `Observed (σ = 0.005″)`. At HST noise (0.005″) and the solver extent (~±5″) the circle is sub-pixel. That is honest; never inflate it.
5. **Titles.** `Dataset Positions (point_0)`; the fit panel is `Fit Positions (point_0)`.
6. **Fit panel.** Apply the same treatment to the "Fit Positions" panel of `fit.png`, with model positions drawn on top. Cluster domains share these functions and change too.

7. **Mass centres** (scope addition, human, 2026-10-21). The "Fit Positions" panel of `fit.png` also marks the centre of every mass profile in the fit's tracer (the image-plane lens galaxies; for cluster/group, all of them) with a distinct marker and a `Mass centre` legend entry, with a test that the centres are plotted.

**Critical curves (#783).** Keep computing them on `critical_curve_grid_from`. If a curve runs past the solver-extent panel edge, that clipping is informative (the curve extends beyond the solver grid), but it must look deliberate and not like broken arcs.

## Shape

Library first: PyAutoLens `autolens/point/plot/point_dataset_plots.py` + `fit_point_plots.py` (+ the plotter/visualizer that knows the solver). Then an autolens_visualization re-render PR (point_source_image_chi_squared, point_source_source_chi_squared, cluster). While iterating, mirror to `PYAUTO_EYES_SCRATCH` (`eyes/autolens/<domain>/`) so the human can comment before CI.
