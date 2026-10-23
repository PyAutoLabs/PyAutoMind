Shipped the source-plane fit panel for point-source fits, with each panel matched to its Fit class.

**Fit classes**

| Fit class | Panel content |
|---|---|
| Image-plane χ² (ImagePair, PairRepeat, PairAll, and the Solved variants) | Context only: traced positions numbered 1..N, model source centre, own-plane caustic and inset. No noise footprints and no χ². |
| Source-plane χ², magnification weighting | σ/\|μ\| circles (primary), plus a dashed A·σ "propagated noise (reference)" ellipse. |
| Source-plane χ², jacobian weighting | A·σ ellipses. |

- Centre markers: ★ free centre; ◆ solved β* (also used for the image-plane Solved fits, with "Model (from solved β*)" on the Fit Positions panel).
- One χ² (the fit's own) appears in the legend. Legend-only fit-type cues; no subtitles.
- PairAll residual lines are dashed and labelled "Residual (nearest, soft pairing)".

**Layout and code**
- `subplot_fit` is 1×2, or 1×3 with fluxes.
- New `autolens/point/plot/source_plane_panel.py`. Label placement is shared in `positions_panel.py` (with `point_solver_plots.py`).
- PyAutoArray `_round_ticks` now uses adaptive precision.
- Tests: test_autoarray 2184 passed; test_autolens point 277 passed.

Merged 2026-10-21 via a human /prm (judge tier), order #653 → #790 → #13.


**Known follow-ups**
- PairAll legend auto-placement can cover the mass centre: the longer "Residual (nearest, soft pairing)" label pushes it mid-panel (seen in the scratch render; no tracked PNG uses PairAll). Place the legend in the emptiest corner, as the source-plane panel does. Fold this into the cluster figures pass.
- The image-plane critical curves of multi-plane points are still drawn from the last plane: `draft/bug/autolens/point_fit_critical_curves_ignore_source_redshift.md`.
- The FitPositionsSource default weighting: `draft/bug/autolens/fitpositionssource_default_magnification_weighti.md`.
- The workspace `point_source/plot.py` crash with 5 model images vs 4 observed: `draft/bug/autolens/point_source_plot_script_residual_shape_mismatch.md`.

## Original prompt

# Point-source fit: source-plane panel showing how closely the positions trace

Consequence: judge
Issued: 2026-10-21
Autonomy: human-required
builds-on: complete/2026/10/point-dataset-positions-panel.md (shipped 2026-10-21; shares the fit_point_plots.py styling: markers, σ legend, titles, solver extent)

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

## Prototype findings + recommended defaults (2026-10-21; NOT yet approved — confirm at /start_dev)

**Prototypes.** `/mnt/c/Users/Jammy/Science/scratch/eyes/autolens/source_plane_prototype/` (19 PNGs; producer in `producer/`). The best views are `S3_fit_mockup_image_chi_perturbed_RE.png` and `S3_fit_mockup_source_chi_truth.png`.

**Recommended design.** `fit.png` gets a second panel, "Fit Source Plane (point_0)", for every positions fit (image- and source-χ²):
- **Zoom:** the traced observed positions plus the model source centre, with a 30% margin.
- **Inset:** the full caustic in the emptiest corner, with a box marking the zoom.
- **Traced positions:** numbered black dots.
- **Model source centre:** red ★.
- **Noise ellipse:** an orange A·σ ellipse on every traced point (the honest propagated noise).
- **Noise circle:** the σ/|μ| purple circle as well, but only when the fit uses `weighting="magnification"`.
- **χ² box:** the fit's χ², plus the Jacobian χ².

**Other recommendations:**
- Move the source-χ² "Model (source plane)" ✕ off the image-plane panel into this one.
- Number images 1–N to match the PointSolver figure (the prototype used 0–N−1).
- No model-image markers for image-χ² fits (they all land on the ★).
- Absolute arcsec ticks, with an `apply_extent` precision fix: at mas zoom its 2-sig-fig rounding collapses all ticks to one value ("1.2″" ×3 on cluster point_1).
- Cluster inset frames only the tangential caustic.
- With fluxes, `fit.png` becomes 1×3.
- Multi-plane: the point's own plane (`LensCalc.from_tracer(..., plane_j=fit.plane_index)` works today for caustics). This pairs with the critical-curve redshift bug and the cluster pass.

**Related.** The default-weighting question is filed separately as `draft/bug/autolens/fitpositionssource_default_magnification_weighti.md` (check against Gravity.jl).

**Side note (uninvestigated).** At truth, the image-pair point_source model solves 5 images for 4 observed.

## Human approval (2026-10-21)

Points 1–6 and all of the recommendations above are APPROVED.

**Additional binding principle: pair each figure to its Fit class.**
- **Image-plane χ² fits** (FitPositionsImagePair / PairRepeat / PairAll / …): the source-plane panel is context only (traced positions, model source ★, caustic, inset). Draw nothing that looks like a χ²: no noise circles or ellipses, no χ² box. Subtitle e.g. "Image-plane χ² — traced positions for context".
- **Source-plane χ² fits:** clearly indicate WHICH source-plane χ².
  - The subtitle names it, e.g. "Source-plane χ² (magnification weighting)" or "(jacobian weighting)".
  - The footprint the χ² actually uses is primary: the σ/|μ| circle for magnification, the A·σ ellipse for jacobian.
  - Under magnification weighting, the A·σ ellipse is also shown, faint or dashed, as "propagated noise (reference)" (approved point 1).
  - Free-centre and solved-β* (FitPositionsSourceSolved) fits use visibly different centre markers (★ vs ◆), with legend text naming them.
  - The χ² box appears only on source-plane fits.
- Enumerate every positions Fit class in autolens/point/fit/positions/ and map each to one of these presentations, covered by tests.
