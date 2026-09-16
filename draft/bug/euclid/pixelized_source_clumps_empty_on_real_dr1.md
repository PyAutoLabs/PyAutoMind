# `wcs.json` records no pixelized-source clumps on real DR1 lenses — the clump thresholds only work on the smooth simulation

Type: bug
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- source-reconstruction
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 15
Unattended: ready
Epic: euclid-dr1-prep
Filed: 2026-09-16
Updated: 2026-09-16

**Gates:** the `euclid_dr1` wcs.json reload pass (re-run of the 10 `dr1_sep1`
lenses with `force_pickle_overwrite: true`, then the 15,032-tile DR1 pass). That
pass is held until this lands and is merged to pipeline `main`.

## Original request (verbatim)

> I next want to ensure the files/wcs.json output file is correct. We updated
> euclid_strong_lens_modeling_pipeline to update this with source positions in
> both vis_lp and vis_pix, using work which improves source and image pixel
> locations. Can you work that implementation into this euclid_dr1 project,
> rerun the lenses so the wcs.json files are updated [...] and then download
> results so I can check them.

The assessment that preceded the rerun (2026-09-16) found the rerun mechanism
sound but the `vis_pix` payload empty, which is this bug.

## The finding

PRs #71–#73 made `util.AnalysisImaging.save_results` write the lensed source's
positions into `files/wcs.json`: for `vis_lp` from the MGE centre via the point
solver, for `vis_pix` from `util.pixelized_source_clumps_from(fit)`, which calls
`Inversion.source_clumps_from` / `mappings_from` with

```
SOURCE_CLUMP_THRESHOLD = 0.5      # util.py:768
SOURCE_CLUMP_MIN_PIXELS = 3       # util.py:769
SOURCE_CLUMP_TOTAL = 5
```

Reloading four of the nine completed `dr1_sep1` fits through the production
entry script with the merged `util.py` (`force_pickle_overwrite: true`,
`--stage all --use_cpu`) produced correct `vis_lp` records (2–4 lensed images
each) and, for every `vis_pix` fit, this and nothing more:

```json
{"crpix_x": …, "crpix_y": …, "crval_ra_deg": …, "crval_dec_deg": …,
 "source_model": "pixelized", "source_clumps": []}
```

No exception, no log line — the finder returned an empty list, so
`source_centre_*` and the lensed-image positions are never written
(`util.py:1025-1029`). Reconstructing the fits with `FitImagingAgg` and probing
the mapper explains why:

| Tile (vis_pix) | mesh pixels | recon max | pixels > 0.5·max | clumps @0.5, min 3 | @0.2, min 3 | @0.1, min 3 | @0.5, min 1 |
|---|---|---|---|---|---|---|---|
| Tile102005065… | 530 | 1.48 | 2 | 0 | 1 | 3 | 1 |
| Tile102007899… | 530 | 1.99 | 1 | 0 | 0 | 2 | 1 |
| Tile102008532… | 530 | 58.7 | 1 | 0 | 0 | 0 | 1 |
| Tile102008848… | 530 | 20.1 | 1 | 0 | 0 | 2 | 1 |

On the real adaptive Hilbert/Delaunay reconstructions the brightest mesh pixel
stands alone: only one or two of 530 pixels clear half the maximum, so
`min_pixels=3` rejects everything. Two tiles have a reconstruction maximum an
order of magnitude above their neighbours (58.7 and 20.1 against ~1.5–2 for the
others), which points at a single noisy mesh pixel setting the scale — a
threshold expressed as a fraction of the raw maximum is fragile against exactly
that, and one tile yields nothing even at `threshold=0.1`.

The thresholds were tuned on the committed smooth-Sersic simulation, where the
run-level test asserts exactly one clump of ≥3 pixels
(`tests/test_latent_run_level.py:421-445`) and the unit tests derive the clump
peak and its images from `truth.json` (`tests/test_wcs_dict.py:480-566`). That
coverage passes while the real-data payload is empty for the whole sample.

## What is asked

1. **Make the pixelized clump finder produce a source centre and lensed-image
   positions on real DR1 reconstructions.** Judge the method, not only the
   numbers. Candidates, in rough order of preference:
   - find clumps on a *smoothed* source-plane surface brightness rather than the
     raw per-mesh-pixel values — e.g. the inversion's interpolated
     reconstruction on a regular source-plane grid
     (`Inversion.interpolated_reconstruction_list_from` / the mapper's
     `interpolated_array_from`), or a neighbour-averaged reconstruction over the
     mesh graph — so a single bright pixel cannot set the scale;
   - a robust scale (a high percentile, or the max after neighbour averaging)
     instead of the raw maximum;
   - only as a fallback, lower `SOURCE_CLUMP_MIN_PIXELS` to 1 — this finds one
     clump on all four tiles at `threshold=0.5` but leaves the noisy-spike
     problem in place and should be justified against the spike tiles.

   If the right fix lives in `Inversion.source_clumps_from` (PyAutoArray) rather
   than the pipeline's constants, say so and route it library-first; the
   pipeline change then follows once the API impact is known.

2. **Witness on real data, not the simulation.** The four probed tiles' datasets
   and completed `vis_pix` zips are on disk in the science clone
   (`/mnt/c/Users/Jammy/Science/euclid_dr1/dataset/dr1_sep1/<Tile>/` and
   `/mnt/c/Users/Jammy/Science/euclid_dr1/output/<Tile>/initial_lens_model/vis_pix/<hash>.zip`,
   both gitignored/untracked there). Reconstruct with `FitImagingAgg` and show,
   per tile, the clumps found and that the brightest clump's peak sits on the
   visible source (compare against the `vis_lp` record's `source_centre_*` for
   the same tile, which is a good independent check — the MGE centre and the
   pixelized peak should agree to within the source's size). Tile102008532… and
   Tile102008848… (the spike tiles) are the ones that must be shown to work.

3. **Lock it in.** Add a test that exercises the finder on a reconstruction with
   an isolated bright pixel (a spike) and a broad faint source, asserting the
   clump lands on the source; keep the existing simulation tests passing (the
   "exactly one clump" assertion at `test_latent_run_level.py:439` may need its
   expectation revisited if the method changes — say so explicitly rather than
   loosening it silently). Also add the missing `force_pickle_overwrite`
   round-trip test: fit, blank `files/wcs.json`, re-run with the flag on,
   assert the file is regenerated — there is no coverage of this path anywhere
   today, and the 10,000-lens pass depends on it.

4. **Document the choice** in `util.py`'s constants block and `catalogue/README.md`
   (which describes the wcs.json record), including what a `source_clumps: []`
   now means if it can still occur.

## Evidence

- Assessment session 2026-09-16 (memory `euclid-dr1-wcs-reload-fpo-assessment`).
  Probe script and reload logs were under the session scratchpad
  (`scratchpad/ral/agg_probe.py`, `reload_<Tile>.log`) and may be gone; the
  table above is the record. The probe's method: `Aggregator.from_directory(…,
  completed_only=True, unzip_temporary=True)` → `FitImagingAgg` →
  `inversion.mappings_from(mapper_index=0, threshold=…, min_pixels=…)`.
- `Inversion.source_clumps_from`: `PyAutoArray/autoarray/inversion/inversion/abstract.py:1328`.
- Writer: `euclid_strong_lens_modeling_pipeline/util.py:829-894` (`pixelized_source_clumps_from`),
  `util.py:895-1055` (`wcs_dict_from`), `util.py:707-747` (`AnalysisImaging.save_results`).
