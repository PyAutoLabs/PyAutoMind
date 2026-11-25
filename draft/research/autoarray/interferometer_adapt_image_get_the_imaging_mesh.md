# Interferometer adapt image: get the imaging mesh / AdaptSplit adaptation on visibility…

Type: research
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
- autolens_workspace
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Lane: ral

Follow-up to PyAutoLabs/PyAutoArray#714 (Mind `active/make_the_source_adapt_image_hilbert_image.md`,
science project `~/Science/Science/development/adapt_snr_cap`), filed at the human's request on
2026-11-25.

## The human's words

> I also want you to intake a follow up where we work out how to get the same adaption to
> interferometer data, whether that be producing a S/N map or some other scaling.

## Background

- The imaging work in @PyAutoArray #714 replaces the peak-normalised Hilbert weighting
  (`(|adapt| / max) ** weight_power`, floored at `weight_floor`) and the workspace's S/N 3.0 cap
  with a weighting in absolute S/N units. The candidate status quo is `peak_share` in
  `adapt_snr_cap/scripts/mesh_weighting.py`: 25% of the mesh points even over the mask, 5% to the
  pixels nearest the peak S/N, the rest in proportion to `(x / (x + 3)) ** 2` with `x = S/N - 2`.
  AdaptSplit is given the same soft transform of the S/N map (`regularization_image_from`).
  Every number in it (the noise threshold 2, the scale 3) is an S/N.
- Imaging adapt images are S/N maps: `galaxy_name_image_dict_via_result_from` in @PyAutoGalaxy
  (`autogalaxy/analysis/adapt_images/adapt_images.py`) returns (data - other galaxies) / noise.
- Interferometer pipelines cannot use that. The 7 interferometer scripts in @autolens_workspace
  (24 `AdaptImages` sites) pass `use_model_images=True`, so their adapt image is a model image in
  flux units, and they clip a copy of it at the flux where the beam-smoothed S/N crosses 3.0, with
  the image-plane noise taken as `sqrt(0.5 * sum |noise_map| ** 2)` (Mind
  `complete/2026/09/adapt-image-snr-cap.md`; e.g.
  `scripts/interferometer/features/pixelization/slam.py:201-209`).
- The S/N-image route was tried and rejected on 2026-09-02: the interferometer "S/N" image divides
  by `dirty_noise_map`, which is sigma times the dirty beam (55% of pixels <= 0).

## What to do

1. Work out what an interferometer adapt image in S/N units should be. Candidates, not
   requirements: the model source image divided by one image-plane noise level (the
   `sqrt(0.5 * sum |noise_map| ** 2)` already used for the clip, or a noise level per
   resolution element from the dirty beam); a matched-filter S/N of the dirty image; or no S/N
   map at all and a scaling of the weighting's two S/N numbers into flux units per dataset.
2. Measure before proposing, as `adapt_snr_cap` did: on the workspace interferometer datasets
   (and a real ALMA lens if one is to hand), build the Hilbert mesh each option gives offline
   and compare its coverage with the imaging meshes of the same kind of source (background
   share, mesh points per pixel by S/N band, points on compact clumps).
3. Confirm the chosen option with fits against the current clipped-model-image behaviour, using
   residual checks first and the evidence second, and show the human the comparison without a
   verdict.
4. Deliver the option as the interferometer default: library support in @PyAutoGalaxy /
   @PyAutoArray if an S/N adapt image is produced there, and the interferometer SLaM scripts of
   @autolens_workspace updated to use the same mesh weighting and AdaptSplit input as imaging.

## Rules

- Plan first and wait for approval before editing library or workspace code.
- Depends on the imaging default landing first (PyAutoArray #714).
- Show the evidence; the human judges.

<!-- formalised by the Intake (Conception) Agent on 2026-11-25 from file:/tmp/claude-1000/-home-jammy-Science/8bf66d7b-2128-41e7-86f0-68d09386bd8e/scratchpad/followup_interferometer.md -->
