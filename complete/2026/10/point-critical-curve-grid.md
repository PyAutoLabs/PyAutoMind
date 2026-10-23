Critical-curve grids for point-source and weak-lensing visualization (PyAutoLens#783). Follow-up to complete/2026/10/point-source-image-overlay.md and point-image-fit-filename.md.


## What shipped
- **PyAutoLens#784:**
  - New `critical_curve_grid_from(dataset, shape_native, scale, buffer)` in `autolens/lens/plot/critical_curves.py`. It builds a square grid centred on the positions' bounding box, with half-width = scale × half-span, in x-first extent order.
  - The point visualizer and plotter use scale 2, so curves that extend beyond the images are no longer clipped into arcs or lost.
  - The weak visualizer uses scale 1, so its field grid is no longer transposed.
  - `PointDataset` / `WeakDataset.extent_from()` are unchanged.
- **autolens_visualization#10:** point `fit_image_with_points.png` re-rendered; the curve is now one closed loop.
- **PyAutoEyes:** refresh run 39598563590 (1010f5c).

## Diagnosis
- The grid was `Grid2D.from_extent(extent=dataset.extent_from())`.
- `extent_from()` returns `[y_min, y_max, x_min, x_max]`, but `from_extent` takes `(x0, x1, y0, y1)`.
- For point data the box only covered the images (+0.1"), while critical curves often extend beyond them. The human confirmed point-source visualization usually needs a bigger grid.

## Original prompt

# Point-source critical curves render as disconnected arcs

@PyAutoLens @autolens_visualization @PyAutoEyes

Consequence: judge
Autonomy: human-required
Issued: 2026-10-21
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/783

Follow-up to PyAutoLens#779 / #781.

## Original request (verbatim)

fix the critical curve

## Diagnosis (2026-10-21)

- **The grid clips the curve.** `VisualizerPoint.visualize` (and `PlotterPoint`'s fallback, plotter.py:119) computes critical curves on `Grid2D.from_extent(extent=fit.dataset.extent_from(), shape_native=(100, 100))`. That grid is the images' bounding box plus 0.1". On the autolens_visualization dataset it spans about [-1.14, 1.71]". The true tangential curve is a closed loop of radius 1.6", so it is clipped into 4 arcs. A 200×200 grid at 0.03" gives one closed line of 257 points.
- **The axes are swapped.** `PointDataset.extent_from()` returns `[y_min, y_max, x_min, x_max]`, but `Grid2D.from_extent` expects `(x0, x1, y0, y1)`. This is hidden while the box is near-symmetric.
