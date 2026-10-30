# Source science: area magnification of each lensed image (arc phase 6c)

Issue autolens_workspace#607 → PR autolens_workspace#608 merged 2026-10-30. Epic `cluster-strong-lensing`, phase 6c.
New `__Area Magnification__` section in `scripts/{imaging,interferometer,group,multi_galaxy}/source_science.py`:
arc mask (pixels >10% of lensed-source peak; on data `imaging/data_preparation/gui/mask_arcs.py`), `image_masks_from`,
per-image `area_magnification_list_from` + `source_plane_area_from` (LEGGOS II Eq. 6-7). Full text in imaging, short
pointer versions elsewhere. Depends on PyAutoGalaxy#685/#687 (merged, pending release; human authorized merging first).

Full-size output: imaging two symmetric pairs (10.93, 12.78) + a 2-px critical-curve sliver; interferometer 7.60/5.77
(source areas 0.668/0.676); group 5 images incl. central μ 0.60 (source areas 0.85-0.98); multi_galaxy 4 images ~0.11
arcsec² + central μ 0.25. CI green but CI smoke does NOT run source_science scripts (not in smoke_tests.txt) — run
locally full + smoke mode, all rc=0. Next: 6d autolens_assistant LEGGOS II ingest.

## Original prompt

# Source science: area magnification and source-plane area of each lensed image (arc phase 6c)

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Epic: cluster-strong-lensing
Phase: 6c
Parent: draft/feature/autolens/area_magnification_leggos.md
Difficulty: small
Autonomy: supervised
Priority: high
Consequence: judge
Filed: 2026-10-30
Issued: 2026-10-30
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/607
Witness: the four `scripts/<imaging|interferometer|group|multi_galaxy>/source_science.py` gain an `__Area Magnification__` section (contents list updated) that builds an arc mask, splits it into images with `LensCalc.image_masks_from` and prints each image's `area_magnification` and `source_plane_area`; all four run clean in smoke; prose follows TUTORIAL_WRITING_STYLE.md with no PR numbers.

## Original request (human, 2026-10-30)

> keep going with 6c, ship it when tests pass

## Work

Document the 6a API (PyAutoGalaxy#685/#687, validated in 6b) where users do source science: what the area
magnification is (LEGGOS II Eq. 6-7: arc area over the source area it maps from, each piece dA from dA/|mu|),
that it needs only the lens model and an arc outline, how it differs from the flux-weighted source magnification,
that a mask must cover one image (hence `image_masks_from`), the source-plane area as the link to source size, and
the small-image fragmentation limit. Full text in imaging, short pointer versions in the other three.
