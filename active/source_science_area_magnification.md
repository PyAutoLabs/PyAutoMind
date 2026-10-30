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
