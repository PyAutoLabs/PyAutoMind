# PositionsLH should warn when the input positions do not trace together

Type: feature
Target: PyAutoLens
Repos:
- PyAutoArray
- PyAutoLens
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: on a simulated lens, positions.json with y negated (the old flip_for_ds9 frame) triggers the new warning when traced through the true model, and the correctly-framed positions do not.
Review-minutes: 3
Unattended: ready
Lane: local-dev

PositionsLH should warn when the input positions do not trace together. Found 2026-11-26: SLACS/BELLS positions.json written under the old fits flip_for_ds9 loader (pre PyAutoArray a0144abd) were y-negated relative to the current frame. For slacs0946+1006 they traced 0.167 arcsec apart in the source plane through the fitted model (0.044 arcsec when corrected), yet passed the PositionsLH threshold of 0.3 arcsec silently. Proposal (additive, PyAutoLens): when positions are checked against a model (e.g. the first PositionsLH evaluation, or positions_likelihood_from on a result), log a warning if the user-supplied positions trace much worse than their y-negated mirror; optionally an autolens dataset frame-check utility mirroring Science/dataset/frame_check.py (extra-galaxy centres vs mask_extra_galaxies, high-pass flux at JSON coordinates, stored vs y-negated). No change to FITS loading conventions. Relates to active/sky_orientation_euclid_dr1_and_library.md phase 3 and draft/research/libraries/plus_y_north_at_fits_load.md.

<!-- formalised by the Intake (Conception) Agent on 2026-11-26 from user-intake -->
