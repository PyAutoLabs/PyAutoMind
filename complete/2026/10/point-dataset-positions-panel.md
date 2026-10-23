Shipped the point-source positions panels (phase 1 of the point-source figures work).

- **Positions panels:**
  - extent set by the PointSolver grid; the fallback contains every position
  - no x/y axis labels
  - large markers, a true-radius noise circle and σ in the legend
  - titles `Dataset Positions (point_0)` / `Fit Positions (point_0)`
- **Fit Positions panel also shows:**
  - the mass centres
  - critical curves (`critical_curve_grid_from(solver=)` grows to cover the solver grid, so no broken arcs)
  - observed→model residual lines, paired per fit class
  - unmatched model images
- **Code:** new `autolens/point/plot/positions_panel.py`. `solver=` is threaded through the plotter and visualizer. 12 new tests; the full suite gives 859 passed.
- **Re-render:** autolens_visualization re-rendered the point_source_* and cluster figures.

Merged 2026-10-21 via a human /prm (judge tier), library first.


Follow-ups:
- `draft/feature/autolens/point_solver_refinement_figure.md` (phase 2)
- `draft/docs/autolens/point_solver_figure_workspace_placement.md` (phase 3)
- `draft/feature/autolens/point_fit_source_plane_panel.md`
- `draft/bug/autolens/point_fit_critical_curves_ignore_source_redshift.md`

## Original prompt

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

8. **Critical curves on the Fit Positions panel** (scope addition, human, 2026-10-21) — not only on `fit_image_with_points.png`, because a user may not supply an image. Computed with `critical_curve_grid_from` (#783); the same deliberate-clipping rule at the solver-extent panel edge applies. Thin and light, so they do not swamp the residual lines.
9. **Residual lines** (scope addition, human, 2026-10-21). A thin line from each observed position to its paired/matched model position, using the pairing the fit's chi-squared actually uses (`FitPositionsImagePair` / `PairRepeat` / `PairAll` each by its own matching). Source-plane chi-squared fits have no image-plane pairing: skip the lines and say so in the docstring. Legend entry `Residual`.
10. **Unmatched model images** (scope addition, human, 2026-10-21). Model positions with no observed counterpart (see `n_unmatched_model_positions` in `autolens/point/fit/positions/image/pair_repeat.py`) drawn in a distinct style (e.g. hollow grey crosses), legend `Unmatched model image`.

Explicitly out of scope: per-position chi-squared numbers. Tests cover 8-10, and they are judged visually in the scratch renders (point_source_image_chi_squared shows lines; source_chi_squared must still look right without them; cluster must stay readable).

**Critical curves (#783).** Keep computing them on `critical_curve_grid_from`. If a curve runs past the solver-extent panel edge, that clipping is informative (the curve extends beyond the solver grid), but it must look deliberate and not like broken arcs.

## Shape

Library first: PyAutoLens `autolens/point/plot/point_dataset_plots.py` + `fit_point_plots.py` (+ the plotter/visualizer that knows the solver). Then an autolens_visualization re-render PR (point_source_image_chi_squared, point_source_source_chi_squared, cluster). While iterating, mirror to `PYAUTO_EYES_SCRATCH` (`eyes/autolens/<domain>/`) so the human can comment before CI.
