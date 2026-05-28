I just used autolens_asssitant to produce the file @autolens_assistant/work/hst_lens_model.py

It produced good code but the comment style was as follows:

# ---------------------------------------------------------------------------
# 1. Load imaging + mask + adaptive over-sampling
# ---------------------------------------------------------------------------
# source: PyAutoArray:autoarray/dataset/imaging/dataset.py  (Imaging.from_fits / apply_mask / apply_over_sampling)
# source: PyAutoArray:autoarray/mask/mask_2d.py             (Mask2D.circular)

dataset = al.Imaging.from_fits(
    data_path=DATASET_PATH / "data.fits",
    noise_map_path=DATASET_PATH / "noise_map.fits",
    psf_path=DATASET_PATH / "psf.fits",
    pixel_scales=PIXEL_SCALES,
)


If you look through the autolens_workspace/scripts, youll see we have a distinct style as follows:

"""
__Dataset__

We begin by loading the dataset. Three ingredients are needed for lens modeling:

1. The image itself (CCD counts).
2. A noise-map (per-pixel RMS noise).
3. The PSF (Point Spread Function).

Here we use James Webb Space Telescope imaging of a strong lens called the COSMOS-Web ring. Replace these FITS paths 
with your own to immediately try modeling your data.

The `pixel_scales` value converts pixel units into arcseconds. It is critical you set this
correctly for your data.
"""
dataset = al.Imaging.from_fits(
    data_path=DATASET_PATH / "data.fits",
    noise_map_path=DATASET_PATH / "noise_map.fits",
    psf_path=DATASET_PATH / "psf.fits",
    pixel_scales=PIXEL_SCALES,
)

This style is the PyAutoLens style, and it also allows us to do clever script to Notebook conversions which I think
we will want to make part of autolens_assistant.

Furthermore, autolens style has pairs these headers to a Contents section at the top:

"""
Start Here: Imaging
===================

Strong gravitational lenses are often observed with CCD imaging, for example using HST, JWST,
or ground-based telescopes.

This script shows you how to model such a lens system using **PyAutoLens** with as little setup
as possible. In about 15 minutes you’ll be able to point the code at your own FITS files and
fit your first lens.

We focus on a *galaxy-scale* lens (a single lens galaxy). If you have multiple lens galaxies,
see the `start_here_group.ipynb` and `start_here_cluster.ipynb` examples.

__Contents__

- **JAX:** JAX acceleration for fast GPU/CPU model-fitting.
- **Google Colab Setup:** The introduction `start_here` examples are available on Google Colab, which allows you to run them.
- **Imports:** Import the required Python libraries.
- **Dataset:** Load and plot the strong lens dataset.
- **Extra Galaxy Removal:** There may be regions of an image that have signal near the lens and source that is from other.
- **Masking:** Lens modeling does not need to fit the entire image, only the region containing lens and source.
- **Model:** Compose the lens model fitted to the data.
- **Model Fit:** Perform the model-fit using the search and analysis.
- **Iterations Per Update:** Every `iterations_per_quick_update`, the non-linear search outputs the maximum likelihood model and.
- **Live Visual Update:** Opt-in live matplotlib window (scripts) or Jupyter cell refresh (notebooks) during the fit.
- **Result:** Overview of the results of the model-fit.
- **Extra Galaxy Removal GUI:** The model-fit above removed a region of the image to the south-east of the lens, which contains.
- **Model Your Own Lens:** If you have your own strong lens imaging data, you are now ready to model it yourself by adapting.
- **Simulator:** Let’s now switch gears and simulate our own strong lens imaging.
- **Sample:** Often we want to simulate *many* strong lenses — for example, to train a neural network or to.
- **Wrap Up:** Summary of the script and next steps.
"""

Can you update autolens_assistant to use this style for all code it writes? 