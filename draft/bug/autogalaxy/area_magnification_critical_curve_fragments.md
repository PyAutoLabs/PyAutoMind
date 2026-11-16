# Area magnification splits lensed images into one- and two-pixel fragments near critical curves

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Epic: cluster-strong-lensing
Filed: 2026-11-02
Consequence: judge
Review-minutes: 20
Unattended: no
Lane: any

## Original request (human, 2026-11-02)

> yes go ahead and file both

(Found in arc phase 7b; record complete/2026/11/magnification-errors-source-science.md, merged in autolens_workspace#613.)

## Problem

`LensCalc.image_masks_from` (`autogalaxy/operate/lens_calc.py`, arc phase 6a, PyAutoGalaxy#685) splits an arc mask
into images by the sign of the Hessian magnification and then `ndimage.label` on each parity. On the
`multi_galaxy/simple` dataset (two deflectors) the truth printout of `scripts/multi_galaxy/source_science.py` returns
4 real images (452, 446, 443, 358 pixels, mu 8–10), one 14-pixel region (mu 0.25) and 14 one- or two-pixel
fragments with mu 65–190 and source-plane area ~0. These are islands where the parity flips next to critical
curves. `area_magnification_list_from` reports every fragment as an image, so the docs print nonsense rows, and the
posterior-draw errors in phase 7b inherit the same split (the number of "images" can change between draws).
The docstring already warns that touching same-parity images and mask-cut images are not distinguished; this case
is not mentioned.

## Expected

Area magnification lists only the real lensed images: fragments that straddle critical curves are merged into the
neighbouring image or dropped, by a documented rule (e.g. a minimum pixel count or minimum source-plane area
argument, or assigning critical-curve pixels to the neighbouring region). The number of returned images is stable
across posterior draws.

Witness: on `multi_galaxy/simple` and `group/simple`, `image_masks_from` returns only the real images, and their
area magnifications match the forward-traced truth used in autolens_workspace_test `scripts/imaging/area_magnification.py`
to within its existing tolerances; the single-lens double/quad tests are unchanged.

Workspace follow-up: re-check the area magnification printouts in the multi_galaxy and group `source_science.py`
scripts (and their MGE / pixelization variants) after the fix.
