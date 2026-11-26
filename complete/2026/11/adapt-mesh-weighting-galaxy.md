## adapt-mesh-weighting-galaxy
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/762
- completed: 2026-11-26
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/718
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/763
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/897
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/718
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/763
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/897
- heart-red-override: authorized by the live human 2026-11-26 ("Override, proceed") but not exercised: the scoped dev gate was GREEN for every repo at PR-open; merged on the human's /prm ("prm all three") with every check green.
- what shipped: the S/N-map adapt API settled with the human — `ag/al.galaxy_snr_maps_from`, `soft_snr_maps_from`, `AdaptImages.from_result(result, image_mesh={"source": ...})`, short galaxy keys ("source", "galaxies.source"; ambiguous raises, unknown ignored as before), `galaxy_name_image_dict_via_result_from(minimum_percent=)` flooring a copy; PyAutoArray `HilbertSNR(background=, peak=, max_per_pixel=8, frame_independent=True, edge_pixels=0)`, `edge_pixels=` on Hilbert/Overlay, `Hilbert(frame_independent=False)` opt-in, `image_mesh.soft_snr_map_from`. Hilbert and AdaptSplit unchanged (BC, as the human asked).
- evidence: PyAutoArray 2632, PyAutoGalaxy 1692, PyAutoLens 1184 passed; test-mode SLaM fit with AdaptImages.from_result equals the science project's reference (0.0); cap: no points within 0.05 px on 20 datasets (was 539 on the faintest), median source share 0.71 -> 0.70; frame: same mesh in any frame to 1e-9 (was up to 6-9 px). Science project: `Science/development/adapt_snr_cap` (`wiki/project/state.md`, `results/snr_range/`).
- also fixes: `draft/bug/autoarray/hilbert_image_mesh_frame_independent.md` (retired with its own record).
- follow-up: phase 3 `draft/feature/autolens_workspace/adapt_mesh_weighting_workspace_default.md`; `draft/bug/autoarray/adaptive_mesh_degenerate_pixel_pair.md` needs re-scope (spikes are mostly isolated central pixels, not pairs).

## Original prompt

# Adapt mesh weighting phase 2: one call for the HilbertSNR mesh input and soft AdaptSplit image

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: medium
Autonomy: supervised
Priority: high
Consequence: judge
Parent: complete/2026/11/adapt-mesh-weighting-library.md (PyAutoArray#716, phase 1 PR PyAutoArray#717)
Filed: 2026-11-26
Issued: 2026-11-26
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/762

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
