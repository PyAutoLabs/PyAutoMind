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
