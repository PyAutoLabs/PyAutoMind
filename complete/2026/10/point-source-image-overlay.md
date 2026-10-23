Point-source positions overlaid on a dataset image, and shown on PyAutoEyes (PyAutoLens#779).


## What shipped
- **PyAutoLens#780:**
  - `AnalysisPoint` stores `image` (it was previously accepted and dropped).
  - `aplt.plot_image_with_points` writes `image_with_points.png`: hollow white rings for observed positions; red crosses for model positions, on image-plane fits only (a source-plane fit's model data is the source centre); optional critical curves.
  - `VisualizerPoint` emits it before and after the fit, including on `quick_update`.
  - `plots.yaml` keys: `point_dataset` / `fit_point_dataset` `image_with_points`.
- **autolens_workspace#591:**
  - `point_source/simulator.py` builds its imaging from `lp.PointSource` images at the dataset positions (intensity = flux × |magnification|), on a lens-redshift image-plane galaxy, with a normalized PSF.
  - Six modeling/feature scripts pass `image=data`.
- **autolens_visualization#6:**
  - The point simulator writes `data`/`psf`/`noise_map` FITS (seeded).
  - Both point producers keep `image_with_points.png` (`keep_dataset_and_fit(extra_pngs=)`).
  - The `ensure_dataset` sentinel is now `data.fits`; the manifest grew from 64 to 66 figures.
- **PyAutoEyes:** `dashboard_refresh` (workflow_dispatch) re-rendered the board; both figures are listed. No Eyes PR was needed.

## Gotchas
- Viz CI clones library mains, so the viz PR's lint stays red until the library PR merges. Re-run the failed job after merging (human-approved).
- The Heart door read RED at start. The human authorized the development override; readiness was YELLOW when the PRs shipped (unrelated euclid diagnose_latent, manifest drift, no rehearsal).

## Follow-up
- The critical curve renders as 4 disconnected arcs on the 100×100, 0.05" point grid (pre-existing critical-curve computation).

## Original prompt

# Point-source positions overlaid on a dataset image (+ PyAutoEyes)

@PyAutoLens @autolens_workspace @autolens_visualization @PyAutoEyes

Consequence: judge
Autonomy: human-required
Issued: 2026-10-21
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/779

Heart RED override invoked by the human 2026-10-21 (development only).

## Original request (verbatim)

For point source modeling in general I also expect that when a user passes an image of the dataset (e.g. of the lensed quasar)
The points are clearly plotted over the top. I want to implement this (I think the workspace has some inputs descriptions for it).
I want our PyAutoEyes dashboard images for point_source_image_chi_squared and point_source_source_chi_squared to include
this image in addition to dataset.png and fit.png. This also means the workspace needs to simulate an image with what
look like actual point components (e.g. delta function point sources of slight with PSF convolution)? Lets scop this
out and do this, getting to the point where the image is in PyautoEyes.
