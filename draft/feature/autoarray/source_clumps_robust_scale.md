# `Inversion.source_clumps_from` needs a robust scale — thresholding against the raw maximum finds nothing on real adaptive-mesh reconstructions

Type: feature
Target: autoarray
Repos:
- PyAutoArray
Themes:
- source-reconstruction
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 10
Unattended: ready
Filed: 2026-09-16
Updated: 2026-09-16

## Origin

euclid_strong_lens_modeling_pipeline issue #78 (2026-09-16). `Inversion.source_clumps_from`
(`autoarray/inversion/inversion/abstract.py:1328`) keeps mesh pixels above
`threshold * max(reconstruction)`. On four real Euclid DR1 Hilbert/Delaunay reconstructions
(530 mesh pixels) the brightest pixel is an isolated spike 5-33x its brightest neighbour, so at
the default threshold 0.5 / min_pixels 3 the finder returns `[]` on 4/4 tiles. `subplot_mappings`
inherits the same blindness.

## Measured

On those same tiles, thresholding against the reconstruction's 99th percentile (`0.5 * p99`,
min 3 pixels) finds a compact 3-7 pixel clump on the source, 0.03-0.23" from the independent
MGE centre, on all four. Alternatives tried and rejected: neighbour-median smoothing annihilates
a compact 3-pixel source (one tile drops to no clump at all); neighbour-mean smoothing drifts the
peak onto a second knot; p95 swells the clump out to the whole bright region.

## Ask

Add a `scale` option to `source_clumps_from`, threaded through `mappings_from` and the
`visualize/general.yaml` `inversion:` block:

- `scale="max"` — today's behaviour, the default for back-compatibility.
- `scale="percentile"` with `scale_percentile=99.0`.

Consider making percentile the default after checking what it does to the autolens_workspace
`subplot_mappings` figures.

Unit test with an isolated spike plus a broad faint source on a hand-built `Neighbors` mesh; the
pipeline's `tests/test_wcs_dict.py` has one to mirror.

The pipeline currently implements this itself via the `pix_indexes=` bypass; once this is
released, switch the pipeline over to the library option.
