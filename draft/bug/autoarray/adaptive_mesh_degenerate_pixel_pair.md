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
Status: formalised
Consequence: judge
Review-minutes: 10
Unattended: ready
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
