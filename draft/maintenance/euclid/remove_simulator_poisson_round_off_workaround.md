# Remove the pipeline-side Poisson round-off workaround once PyAutoArray#687 is released

Type: maintenance
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- simulation
- hygiene
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: judge
Witness: `simulated_image_from` hands the raw image to `SimulatorImaging.via_image_from` without pre-convolving or clipping (`image_is_convolved` no longer forced), and resimulating the four tiles that failed on 2026-09-13 (indices 10, 62, 63, 69 of the sorted `dr1_sep1_sersics` sample) succeeds on the release containing PyAutoArray#687.
Review-minutes: 5
Lane: any
Filed: 2026-11-10

## Why

PyAutoArray#687 (merged 2026-11-10 as PR #688; record `complete/2026/11/simulator-poisson-flag-guard.md`) made `SimulatorImaging` draw Poisson noise only when it is
used, and clip PSF-convolution round-off negatives before the draw. The pipeline carries a guard for the old
behaviour: euclid_strong_lens_modeling_pipeline PR #87 (issue #77, merge `dc91d9a`). `simulated_image_from`
convolves the image itself, clips the round-off and passes `image_is_convolved=True`.

**Gate:** PyAutoArray#688 merged 2026-11-10; start only once it is released, and the pipeline's dependency floor includes that
release.

## Work

1. Remove the pre-convolution and clip in `simulated_image_from`, and let the simulator convolve.
2. Keep or remove the `-1e-10 * maximum` raise depending on whether the library's `DatasetException` covers it
   (it does on the NumPy path).
3. Check that simulated outputs are unchanged for a seeded tile, apart from the round-off pixels now being clipped
   inside the library.
