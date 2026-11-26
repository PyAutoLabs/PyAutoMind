# Adapt mesh weighting phase 2: one call for the HilbertSNR mesh input and soft AdaptSplit image

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: medium
Autonomy: supervised
Priority: high
Consequence: judge
Parent: active/adapt_mesh_weighting_library_default.md (PyAutoArray#716, phase 1 PR PyAutoArray#717)
Filed: 2026-11-26

Phase 2 of making the adapt-mesh-weighting result the default everywhere (human, 2026-11-26:
"make this the default everywhere (but keep BC via `Hilbert` ..., ensure `AdaptSplit` retains BC
too), so all workspaces use the new one and a user doesnt need to supply weight_power=3.5 and
weight_floor=0.01"). Needs PyAutoArray#717 merged (`image_mesh.HilbertSNR`,
`image_mesh.soft_snr_from`, `image_mesh.adapt_image_soft_from`).

## Problem

`autogalaxy/analysis/adapt_images/adapt_images.py` `galaxy_name_image_dict_via_result_from`
floors every adapt image at `adapt_minimum_percent` (1%) of its maximum. `HilbertSNR` and the
soft AdaptSplit image need the source S/N map **before** that floor (above a peak S/N of 200 the
floor lifts empty sky over S/N 2 and it is weighted as source). The raw map is already cached
(`files/galaxy_images_snr.fits`, `_galaxy_image_dict_from_cache`), but only private helpers
reach it. A workspace script today has to do what the science project's `slam.py`
`unfloored_source_snr_from` does by hand.

## What to do

- A public way to get the per-galaxy S/N maps before the floor (e.g. a
  `galaxy_name_image_dict_via_result_from(result, minimum_percent=None)` override, or a sibling
  function), reading the existing cache, negatives set to 0.
- A one-call helper for SLaM / workspace scripts returning both what the mesh needs (the
  unfloored S/N map, for `HilbertSNR.image_plane_mesh_grid_from`) and the adapt-image dict whose
  source entry is `adapt_image_soft_from` of it (for `AdaptImages` → `AdaptSplit`). Other
  galaxies' entries keep the floored map.
- Backward compatibility: the existing function's default output is unchanged, so every
  current `AdaptSplit` fit is unchanged.
- Tests; and check the science project's `slam.py` unified arm can be rewritten onto these
  calls with the same mesh and adapt image (0.0 difference on a test-mode lens).

Reference: `~/Science/Science/development/adapt_snr_cap/scripts/slam.py`
(`unfloored_source_snr_from`, `galaxy_name_image_dict_from`, `source_pix_2`).
