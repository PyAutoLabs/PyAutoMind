# Adaptive rectangular meshes: repeat the adapt-image experiment and compare with Delaunay

Type: research
Target: PyAutoArray
Repos:
- PyAutoArray
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

> Intake another follow up which does the same experiment but figures out what the behaviour for
> adaptive rectangular meshes are. I think these do zoom in using fitted for lens model parameters
> but we need to confirm that we get a level of adaption which is optimal and comparable to the
> Delaunay fits.

## Background

- `adapt_snr_cap` ran the autolens_workspace Delaunay SLaM (Hilbert image mesh, 1250 points,
  AdaptSplit) on 5 SLACS, 5 BELLS GALLERY, 4 Euclid DR1 and 5 COWLS lenses (F150W and F277W),
  with arms that differ only in the source adapt image and its mesh weighting: `cap3`,
  `uncapped`, and the candidate status quo `peak_share_unified`
  (`scripts/slam.py`, `scripts/mesh_weighting.py`, `scripts/mesh_metrics.py`,
  `scripts/compare.py`). The Hilbert draw is deterministic, so meshes could be compared offline
  before any fit.
- The adaptive rectangular meshes in @PyAutoArray adapt in the source plane, not the image
  plane: `autoarray/inversion/mesh/mesh/rectangular_rtu_adapt_image.py` and
  `rectangular_bilinear_adapt_image.py` (`mesh_weight_map_from`: the adapt image clipped, raised
  to `weight_power`, floored at `weight_floor`, peak-normalised) and
  `rectangular_rtu_adapt_density.py`, with a rank-CDF transform in
  `autoarray/inversion/mesh/interpolator/rectangular.py:186`. Their `weight_power` /
  `weight_floor` are free parameters of the lens model fit, unlike the Hilbert mesh, which is
  fixed before the search.
- The @autolens_workspace S/N 3.0 cap (autolens_workspace #522) is applied to the adapt image
  these meshes read too, so removing the cap for the Delaunay default changes their input.

## What to do

1. Measure before proposing. On the same lenses, for the rectangular adaptive meshes: how much
   the mesh zooms on the source (source-plane pixel size across the source against the
   magnified image pixel, pixels on the source against pixels on empty sky), which
   `weight_power` / `weight_floor` values the fits choose, and how both change between a capped,
   an uncapped and a soft-transformed (`regularization_image_from`) adapt image.
2. Put those numbers next to the Delaunay fits of `adapt_snr_cap` on the same lenses: the same
   coverage measurements where they carry over, the residual checks of `compare.py` (mean
   squared normalized residual by data S/N, fraction above 3 sigma, lag-1 autocorrelation) and
   the evidence as a secondary column.
3. Say whether the rectangular meshes reach a level of adaptation comparable to the Delaunay
   fits by fitting their weighting, or need the same kind of default (an S/N transform that is
   not peak-normalised, a guaranteed background share) and a documented knob. Show the human
   the comparison without a verdict.
4. If a change is needed, propose it for @PyAutoArray and the rectangular SLaM scripts of
   @autolens_workspace through the dev workflow.

## Rules

- Plan first and wait for approval before editing library or workspace code.
- Run as new arms in `adapt_snr_cap` or a successor science project; ask before RAL submissions
  and record runs in the Cortex.
- Show the evidence; the human judges.

<!-- formalised by the Intake (Conception) Agent on 2026-11-25 from file:/tmp/claude-1000/-home-jammy-Science/8bf66d7b-2128-41e7-86f0-68d09386bd8e/scratchpad/followup_rectangular.md -->
