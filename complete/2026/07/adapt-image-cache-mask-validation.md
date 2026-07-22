A census-reported "off-by-one in multi-plane adapt-data indexing" turned out to be a stale adapt-image
cache. `mapper_util.adaptive_pixel_signals_from` was correct all along, and the bug was not multi-plane or
double-Einstein-ring specific.

## What shipped

- **PyAutoGalaxy#517** (`64790e7d`) — `_galaxy_image_dict_from_cache` now validates the cached mask against
  the expected one and treats a mismatch as a cache miss, so adapt images are recomputed on the current
  mask. The expected mask comes from `Result.mask` -> `analysis.dataset.mask`, which does not rebuild the
  maximum log likelihood fit, preserving the autolens_profiling#70 caching win. Also corrected a docstring
  that claimed cache staleness was "structurally guarded".
- **PyAutoArray#399** (`c37e478c`) — `Mapper.pixel_signals_from` raises an `InversionException` naming the
  stale-cache cause instead of letting a bare `IndexError` escape from five frames deeper.

No workspace change was required.

## Diagnosis

`IndexError: index 177 is out of bounds for axis 0 with size 177` — index == size — reads as a classic
off-by-one. It is not. Slim indexes are ordered, so when adapt data is too short the *first* out-of-range
index always equals its length. The signature is what a **mask mismatch** looks like from inside the
indexing.

The adapt-image cache (`files/galaxy_images_snr.fits`) lives in a directory keyed by the **search
identifier**, which encodes the model and the search but **not** the dataset. PyAutoArray `656be94b`
(#396, merged 2026-07-19) moved the `PYAUTO_SMALL_DATASETS` cap from 15x15 to 16x16. The 2026-07-21 census
ran against an `output/` holding pre-#396 caches: 177-pixel (15x15) adapt images against a 208-pixel
(16x16) mask, silently loaded because the model was unchanged.

Reproduction matrix (`double_einstein_ring/slam.py`, `PYAUTO_TEST_MODE=2`):

| Data size | `output/` state | Result |
|---|---|---|
| full (100x100) | cleared | PASS (`masks equal: True`, 2828/2828) |
| `PYAUTO_SMALL_DATASETS=1` (16x16) | cleared | PASS (208/208) |
| either | pre-#396 caches present | IndexError: index 177 out of bounds for size 177 |

The decisive step was clearing `output/`, not changing code. Any adapt/SLaM pipeline resumed across a
dataset-shape change is affected; DSPL was simply the script whose stale census output survived.

## Verification

End-to-end with a planted stale cache: stock `main` reproduces the census failure exactly (same frame, same
numbers); the branches exit 0 through `source_pix[2]` with the likelihood actually evaluated. Suites:
PyAutoGalaxy 1006 passed, PyAutoArray 927 passed. CI green on both PRs (unittest 3.12/3.13, docs-build).

## Traps worth remembering

- **Poisoning a cache file on disk is silently undone.** `Paths.restore()` deletes the output directory and
  re-extracts the search `.zip`, so a stale-cache repro must poison the archived copy inside each `.zip` as
  well as the loose `files/` one.
- **A completed pipeline never evaluates the likelihood.** With every search "Fit Already Completed" the
  control passes even with poisoned caches; the downstream search outputs must be deleted to force the
  crash.
- **`glob` reads the brackets in `source_lp[1]` as a character class**, so globbing under a search directory
  silently matches nothing. Build those paths directly.
- Two early "reproductions" used `rm -rf output/slam`, a path that does not exist, leaving the real tree
  `output/test_mode/imaging/slam_dspl` intact. Verify the `rm` actually matched something.
- Two pre-existing PyAutoArray tests passed an unmasked 49-pixel `image_7x7` against a 9-pixel mask, which
  the new guard correctly rejected. The all-ones fixture meant the wrong indexing never showed; both were
  rebuilt on the data's own mask with assertions unchanged.

## Follow-up

**PyAutoFit#1414** — `Paths.preserve_in_zip` only adds a member absent from the zip and never replaces one,
so an invalidated cache is recomputed and written loose but the archived stale copy survives `restore()`.
Such a search misses its cache on every run rather than once: correct, but without the caching win until
its output is cleared. Recorded in the PyAutoGalaxy docstring.

Shipped behind Heart YELLOW (score 52, no RED), human-acknowledged; no reason related to this change.

## Original prompt

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
