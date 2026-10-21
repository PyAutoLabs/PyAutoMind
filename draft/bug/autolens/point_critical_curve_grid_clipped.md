# Point-source critical curves render as disconnected arcs

@PyAutoLens @autolens_visualization @PyAutoEyes

Consequence: judge
Autonomy: human-required

Follow-up to PyAutoLens#779 / #781.

## Original request (verbatim)

fix the critical curve

## Diagnosis (2026-10-21)

- **The grid clips the curve.** `VisualizerPoint.visualize` (and `PlotterPoint`'s fallback, plotter.py:119) computes critical curves on `Grid2D.from_extent(extent=fit.dataset.extent_from(), shape_native=(100, 100))`. That grid is the images' bounding box plus 0.1". On the autolens_visualization dataset it spans about [-1.14, 1.71]". The true tangential curve is a closed loop of radius 1.6", so it is clipped into 4 arcs. A 200×200 grid at 0.03" gives one closed line of 257 points.
- **The axes are swapped.** `PointDataset.extent_from()` returns `[y_min, y_max, x_min, x_max]`, but `Grid2D.from_extent` expects `(x0, x1, y0, y1)`. This is hidden while the box is near-symmetric.
