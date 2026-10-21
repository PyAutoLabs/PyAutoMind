# Point-source fit: source-plane panel showing how closely the positions trace

Consequence: judge
Autonomy: human-required
blocked-by: draft/feature/autolens/point_dataset_positions_panel.md (shares the fit_point_plots.py styling: markers, σ legend, titles, solver extent)

@PyAutoLens @autolens_visualization

## Request (human, 2026-10-21)

> A follow up issue would be to do a source plane plot of the fit showing how close things trace, which is relevent for image chi and source chi.

## Intent

Add a source-plane panel to the point-source `fit.png`, possibly also as its own figure. It shows:
- every observed position ray-traced to the source plane through the fit's tracer
- the model source centre
- the caustics

How tightly the traced positions bunch around the source centre is the quantity `FitPositionsSource` (source chi-squared) minimises. For image chi-squared (`FitPositionsImagePair` and its variants) it is the intuitive check that the model is self-consistent.

## Open design questions (settle in /start_dev)

- **Scale bar for the scatter.** Options are the source-plane noise from magnification-scaled σ (what source chi-squared uses, roughly σ/√μ), a circle per traced position, or a σ annotation.
- **Extent.** Zoom to the traced positions plus a margin, the caustic extent, or both as an inset. Too zoomed out and the scatter is invisible; too zoomed in and the caustic context is lost.
- **Multiple planes.** For multi-plane and cluster fits, either one panel per source plane or only the point's own plane.
- **Figure placement.** In `fit.png` for both image and source chi-squared, or a separate `fit_source_plane.png` toggled by config.
- **Re-render set.** point_source_image_chi_squared, point_source_source_chi_squared and cluster in autolens_visualization.
