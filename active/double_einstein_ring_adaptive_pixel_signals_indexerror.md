# Stale adapt-image cache silently loaded across a dataset-shape change (IndexError in pixel signals)

Type: bug
Target: autogalaxy
Repos:
- PyAutoGalaxy
- PyAutoArray
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised (diagnosis corrected 2026-07-22)

## Original census report (diagnosis was WRONG — kept verbatim for the record)

> Surfaced by the 2026-07-21 census AFTER a parallel chat un-parked the double_einstein_ring SLaM
> scripts (the old opaque FitException is gone — this is the sharp underlying bug). Genuine PyAutoArray
> library off-by-one in adaptive regularization:
>
> ```
> autolens_workspace/scripts/imaging/features/advanced/double_einstein_ring/slam.py  (also group/ variant)
>   PyAutoArray/autoarray/inversion/regularization/adapt.py:210 regularization_weights_from
>   -> mappers/abstract.py:469 pixel_signals_from
>   -> mappers/mapper_util.py:62 adaptive_pixel_signals_from
>      flat_data_vals = xp.take(adapt_data[slim_index_for_sub_slim_index], I_sub, axis=0)
>   IndexError: index 177 is out of bounds for axis 0 with size 177
> ```
>
> index == size ⇒ classic off-by-one. Likely the multi-plane (double-Einstein-ring) adapt-data indexing
> in `adaptive_pixel_signals_from` builds `slim_index_for_sub_slim_index` / `I_sub` off the wrong
> plane's pixel count.

## Corrected diagnosis (reproduced 2026-07-22)

`mapper_util.adaptive_pixel_signals_from` is **correct**. There is no off-by-one, and the bug is not
multi-plane / double-Einstein-ring specific.

Reproduction matrix — `scripts/imaging/features/advanced/double_einstein_ring/slam.py`,
`PYAUTO_TEST_MODE=2`:

| Data size | `output/` state | Result |
|---|---|---|
| full (100x100) | cleared | PASS (exit 0, `masks equal: True`, 2828/2828) |
| `PYAUTO_SMALL_DATASETS=1` (16x16) | cleared | PASS (208/208) |
| either | census `output/` left in place | IndexError: index 177 out of bounds for size 177 |

The failing expression is the subscript `adapt_data[slim_index_for_sub_slim_index]`, not the
`xp.take` (the traceback's `~~~~^^^^` marker pins it).

**Root cause.** `galaxy_name_image_dict_via_result_from`
(`PyAutoGalaxy/autogalaxy/analysis/adapt_images/adapt_images.py:145`) caches per-galaxy adapt images to
`files/galaxy_images_snr.fits`, keyed only by the **search identifier** (model + search). The dataset
mask is not part of that key.

PyAutoArray `656be94b` (#396, merged 2026-07-19, current `main` HEAD) changed the
`PYAUTO_SMALL_DATASETS` cap from 15x15 to 16x16. The 2026-07-21 census ran against an `output/`
holding pre-#396 caches:

- cached adapt image: 15x15 mask, **177** pixels
- current dataset mask: 16x16 mask, **208** pixels
- identical model => identical search identifier => stale cache silently loaded
- slim indices run to 207 against 177-length data; the first out-of-range index is 177, producing
  `index 177 ... size 177`, which only *looks* like an off-by-one

The docstring at `adapt_images.py:127` claims *"Staleness is structurally guarded: changing the
upstream model or search produces a new search identifier and therefore a fresh output directory with
no cache file."* That guarantee does not cover dataset/mask changes, and this is the failure it lets
through. Any adapt/SLaM pipeline resumed across a dataset-shape change is affected; DSPL is simply the
script whose stale census output survived.

## Fix

1. `PyAutoGalaxy` — `_galaxy_image_dict_from_cache(cache_path, mask=...)`: compare the cached HDU-0
   mask against the expected mask and return `None` (cache miss => recompute + overwrite) on mismatch.
   The expected mask comes from `result.mask` -> `analysis.dataset.mask`, which is cheap and does not
   rebuild the max-log-likelihood fit, preserving the caching win (autolens_profiling#70).
2. `PyAutoGalaxy` — correct the false staleness claim in the docstring.
3. `PyAutoArray` — `Mapper.pixel_signals_from`: raise a clear exception when
   `len(adapt_data) != over_sampler.mask.pixels_in_mask`, naming the stale-cache cause, instead of a
   bare `IndexError`. A loud crash, not a silent guard.
4. Numpy-only unit tests both sides (no JAX in library unit tests).
5. Verify by planting a deliberately stale cache and re-running the DSPL SLaM script.
6. Clear the pre-#396 adapt caches from the census `output/`, re-run to confirm green, and
   correct/remove the NEEDS_FIX marker recording the real diagnosis.
