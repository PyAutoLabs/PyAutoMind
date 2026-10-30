# Area magnification validated against forward-traced truth (arc phase 6b)

Type: test
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Epic: cluster-strong-lensing
Phase: 6b
Parent: draft/feature/autolens/area_magnification_leggos.md
Difficulty: small
Autonomy: supervised
Priority: high
Consequence: judge
Filed: 2026-10-30
Issued: 2026-10-30
Issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/351
Witness: `scripts/imaging/area_magnification.py` runs in smoke and asserts, for a 2-image and a 4-image uniform-disk source (disk clear of every caustic), that `LensCalc.area_magnification_list_from` finds the right number of images and recovers each image's forward-traced area magnification and the disk's area within per-resolution tolerances that tighten from 0.05″ to 0.025″ pixels.

## Original request (human, 2026-10-30)

> keep going with 6b, ship it when tests pass

## Work

Validate 6a (PyAutoGalaxy#685, `LensCalc` area magnification) end to end. Truth: a uniform disk of known area,
placed so no image crosses a caustic, so every image maps from the whole disk and its true magnification is its
image area (forward ray-traced on a 0.004″ grid) over the disk area. Recovered: an image-plane mask of the pixels
whose area is mostly inside the traced disk, at 0.1″ / 0.05″ / 0.025″, split with `image_masks_from`. Report the
fragmentation of small images at coarse pixels (a documented limitation of the parity + connectivity split).
Register in `smoke_tests.txt`.
