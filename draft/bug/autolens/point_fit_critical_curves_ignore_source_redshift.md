# Point fit panels: critical curves ignore the point's source redshift (multi-plane)

Consequence: judge
Autonomy: human-required

@PyAutoLens @autolens_visualization

## Finding (2026-10-21, while shipping PyAutoLens#786 / autolens_visualization#11)

On the multi-plane cluster example, `point_0` (z=1) and `point_1` (z=2) draw identical critical curves in `fit.png`. They appear to be the final plane's curves, because `_compute_critical_curve_lines` does not take the source redshift. On `point_0` the images therefore do not sit on the drawn curve, which is misleading.

This was pre-existing; #786 only made the curves visible on the Fit Positions panel.

## Intent

Compute the critical curves (and caustics) for each point dataset at that dataset's source plane, i.e. for its own source galaxy's redshift. Thread that redshift through `_compute_critical_curve_lines`, the visualizer and `subplot_fit`. Then re-render cluster in autolens_visualization and check that each point's images lie on its own curve.
