# PSF Convolution docstring section in simulator.py examples

Type: docs
Target: workspaces
Repos:
- autogalaxy_workspace
- autolens_workspace
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

The new workspaces document the PSF convolution. Document it like this:

"""
All CCD imaging data (e.g. Hubble Space Telescope, Euclid) are blurred by the telescope optics when they are imaged.

The Point Spread Function (PSF) describes the blurring of the image by the telescope optics, in the form of a
two dimensional convolution kernel. The lens modeling scripts use this PSF when fitting the data, to account for
this blurring of the image.

In this example, use a simple 2D Gaussian PSF, which is convolved with the image of the lens and source galaxies
when simulating the dataset.
"""
# PSF convolution runs at the image resolution (sub size 1), which is the fastest
# option and accurate for well-sampled PSFs. Supplying a PSF at a multiple of the
# image resolution and raising this value improves blurring fidelity for
# undersampled PSFs (e.g. HST / Euclid VIS) at extra compute cost — see
# `guides/advanced/over_sampling.py` and the simulator's `__Oversampled PSF__` section.
psf_convolve_over_sample_size = 1

Requirements:
- For each simulator.py script this now comes under a section header in the docstring called __PSF Convolution__ (make sure it's in the Contents / __Start Here__ contents list).
- The over-sample comment must be INSIDE the docstring following the same prose style as everything else, NOT hashtag comments in a row.
- Applies to all simulator.py examples.
- Other simulator.py examples that capture it all under __Simulate__ do not need the header, but they should list the input as =1 in this part:
  """
  Simulate a simple Gaussian PSF for the image.
  """
  psf = al.Convolver.from_gaussian(
      shape_native=(11, 11), sigma=0.1, pixel_scales=grid.pixel_scales
  )
- No docs explaining it are needed there (we assume users read the base simulator.py).
- group/simulator.py needs the same doc as imaging/simulator.py.
- This must be set up for autogalaxy_workspace as well as autolens_workspace.

<!-- formalised by the Intake (Conception) Agent on 2026-07-10 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/48ab0519-a9f8-4f41-9a60-0a0479e7694e/scratchpad/psf_intake.txt -->
