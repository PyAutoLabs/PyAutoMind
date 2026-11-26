# Adaptive Delaunay mesh places two mesh pixels 0.001" apart — a degenerate pair carrying a 58.7 reconstruction spike on a real DR1 lens

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Themes:
- source-reconstruction
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: needs re-scope (2026-11-26 research: most spikes are isolated central pixels, not pairs)
Consequence: glance
Witness: A unit test on a synthetic delta-spike weight map asserts no two `source_plane_mesh_grid` points lie closer than 5% of the local mesh spacing, and re-fitting `Tile102008532RA0683486015030DECNEG0642073552911` `initial_lens_model/vis_pix` no longer has a mesh pair under 5% of local spacing nor a reconstructed pixel above 10x the reconstruction's 99th percentile — or, if the decision is that adapt-image saturation must be clipped, the PR records the nearest-neighbour distribution across the dr1_sep1 tiles and the clipping is documented where the adapt image is built.
Review-minutes: 3
Unattended: ready
Lane: wsl-data
Filed: 2026-09-16
Updated: 2026-09-16

## Finding

2026-09-16, euclid_dr1 tile `Tile102008532RA0683486015030DECNEG0642073552911`,
`initial_lens_model/vis_pix`, 530-pixel adaptive Hilbert/Delaunay mesh, local mesh spacing 0.213".
The two brightest reconstructed mesh pixels (58.7 and 6.08; the rest of the reconstruction peaks
around 1.3) sit 0.0011" apart — a near-duplicate mesh pixel pair, ~200x closer than the local
spacing. The pair sits on the source, 0.23" from the vis_lp MGE centre, not on the zeroed edge
ring. Another tile (`Tile102008848...`) has three stacked spikes (20.1, 3.1, 1.6) within 0.03" of
the source centre.

## Why it matters

A degenerate pair gives the inversion two nearly collinear columns, so the regularised solution
can dump large opposite/unequal flux into them. It also breaks any "fraction of the maximum"
diagnostic (source clumps, `reconstruction_vmax_factor` plots), and may affect the
log-det/regularisation term.

## Ask

1. Reproduce. The completed vis_pix zip and dataset are in the science clone
   `/mnt/c/Users/Jammy/Science/euclid_dr1` (`output/<Tile>/initial_lens_model/vis_pix/<hash>.zip`;
   load via `af.Aggregator.from_directory(..., completed_only=True, unzip_temporary=True)` then
   `al.agg.FitImagingAgg`). Measure the nearest-neighbour distance distribution of
   `mapper.source_plane_mesh_grid`, and how often pairs fall below, say, 5% of the local spacing,
   across the dr1_sep1 tiles.
2. Find where near-duplicates arise in the Hilbert/adaptive-density mesh construction
   (`autoarray/inversion/pixelization/mesh`, `image_mesh`) — a weight map with a single very
   bright pixel? KMeans/Hilbert sampling of a delta-like weight? Then decide between
   de-duplicating/merging points closer than a fraction of the local spacing at mesh construction
   time, or documenting that adapt-image saturation must be clipped.
3. A unit test on a synthetic weight map with a delta spike.

## Related

Pipeline issue #78 (clump finder made robust to this), PyAutoArray #526 (edge ring).

## 2026-11-26: measured on 20 datasets — the pairs come from multiple imaging, under any weighting

(Corrects an earlier note of the same day, which read image-plane crowding as this bug.)

`Science/development/adapt_snr_cap`, 20 datasets (SLACS, BELLS, Euclid, COWLS), 1250 Hilbert points
ray-traced with each lens's `source_pix[1]` mass model. Source-plane pairs closer than 5% of the
local spacing (median distance to the 6 nearest neighbours), totals: `HilbertSNR` 83,
`HilbertSNR` with an 8-points-per-image-pixel cap 76, `Hilbert(weight_power=3.5, weight_floor=0.01)`
64. Almost none of them are close in the image plane (image separation < 2 pixels: 9 of 83
uncapped, 8 of 76 capped): they are points on different counter-images that trace to almost the
same source position. So this bug is intrinsic to drawing the mesh in the image plane and is not
caused or fixed by the weighting; the fix belongs in the source-plane mesh construction (Delaunay
`source_plane_mesh_grid`), and must keep JAX's fixed array shapes (merging cannot drop points).

Separately, `HilbertSNR` crowds points in the image plane on faint sources (up to 61 points in one
image pixel; COSJ095950+022057_F150W: 539 points within 0.05 image pixels of another). That is
not this bug (crowded points stay locally spaced in the source plane); a per-pixel cap in
`HilbertSNR` (8 points per image pixel removes it on all 20 datasets) is in PyAutoArray#718
(`max_per_pixel=8`, default on). This prompt stays open: next is research (reproduce on the
Euclid tile; check the unified fits for reconstruction spikes) before a source-plane fix is planned.

## 2026-11-26: research on 230 fits — most spikes are not pairs

The saved `image/source_plane_reconstruction_0.csv` (source-plane mesh y, x, reconstruction, noise)
of every pixelized fit in `Science/development/adapt_snr_cap` (`source_pix[2]`, `light[1]`,
`mass_total[1]`; arms `cap3`, `uncapped`, `peak_share_unified`; A100 and CPU; 230 fits):

- Source-plane pairs closer than 5% of the local spacing (median of the 6 nearest): median 2-4 per
  fit in every arm.
- Spikes as this prompt defines them (largest |reconstruction| > 10x the 99th percentile): 24 of 230
  fits — `uncapped` 17/84, `cap3` 6/97, `peak_share_unified` (the new `HilbertSNR` default) 1/49.
- In only **2** of the 24 is a spike pixel part of a close pair (COSJ095950+022057_F150W cap3,
  COSJ100012+022015_F277W uncapped: pair pixel 11-14x p99).
- The other 22: an **isolated single pixel at the source centre** (1-12% of the source radius from
  the flux-weighted centre), in the **densest part of the mesh** (cell size 2-30% of the median),
  with neighbours at 0-20% of its value, almost all in `mass_total[1]`; per-pixel S/N
  (reconstruction / noise map) 2.5-26. The largest, 179x p99, is the unified arm on
  COSJ100012+022015_F277W `mass_total[1]`, with no close pair at all.

So the dominant failure is a very small, weakly constrained source pixel at the core absorbing
flux, not a near-duplicate pair. Not yet checked: the Euclid tile in "Finding" (its fit is on RAL /
the old science clone, not on the laptop) — whether its 0.001" pair is a true pair or this pattern.

Suggested re-scope before any code: (1) reproduce the Euclid tile on RAL; (2) for the central-spike
pattern, test whether it is regularization (AdaptSplit's inner coefficient letting the smallest
cells float), the mesh density at the core, or the `mass_total[1]` mass model, e.g. by refitting one
spiky `mass_total[1]` max-likelihood model with the mesh coarsened at the core or a regularization
floor; (3) only then decide a fix. The pair fix (merging/nudging near-duplicates, JAX fixed shapes)
addresses 2 of 24 here.
