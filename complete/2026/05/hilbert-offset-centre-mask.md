## hilbert-offset-centre-mask
- completed: 2026-05-15
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/313
- summary: |
    Fixed a user-reported bug where Hilbert image-mesh raised PixelizationException
    for circular masks with offset centres that didn't align with pixel half-integers.
    Root cause was twofold: Mask2D.is_circular used pixel-quantization-sensitive row
    vs column counts (rejecting valid offset circles, false-accepting annular masks),
    AND hilbert.image_and_grid_from sampled the image around (0,0) regardless of mask
    centre. Rewrote is_circular with a bbox-square + centre-pixel-unmasked + reference
    mask reconstruction check, and made image_and_grid_from translate Hilbert points
    by mask_centre (no-op for centred masks, so existing smoke tests bit-identical).
    Confirmed via 165 inversion unit tests + 13 workspace smoke tests.
