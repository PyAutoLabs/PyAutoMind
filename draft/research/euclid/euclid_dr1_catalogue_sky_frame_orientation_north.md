# euclid_dr1 catalogue: sky-frame orientation (north/east) for the catalogue, paper and website

Type: research
Target: euclid
Repos:
- euclid_dr1 (science project, /mnt/c/Users/Jammy/Science/active/euclid_dr1; RAL /mnt/ral/jnightin/active/euclid_dr1)
- ECLIPSE_lens_catalogue (lens/ECLIPSE_lens_catalogue, website leg)
Themes:
- euclid
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: on at least five real DR1 lenses, the catalogue's sky-frame position angle (east of north) of the lens light, lens mass and external shear matches the orientation measured directly on the north-up FITS cutout through its WCS, and every sky-frame centre agrees with the stored RA/Dec to within a pixel; a simulated lens pushed through a CD1_1<0/CD2_2>0 WCS recovers its input PA east of north.
Review-minutes: 25
Unattended: needs-slicing

Found 2026-10-26 while packaging the DR1 release. Separate from the library-wide fix
(draft/research/autolens/sky_orientation_pyautolens_frame_is_a_north.md); this task fixes the euclid_dr1 catalogue,
paper and website without rerunning any lens model.

## Facts established
- DR1 cutout FITS WCS: CD1_1 < 0, CD2_2 > 0, no rotation -> north up, east left in the FITS convention (checked on one
  tile; scan all ~15k headers on RAL to confirm no rotation/flip varies by tile).
- PyAutoArray loads without a row flip and plots imshow origin upper -> every pipeline PNG is north DOWN, east LEFT
  (a vertical mirror of the sky). Model frame: +y = south, +x = west.
- Lensing is parity invariant: scalar quantities (Einstein radii, q, Sersic n, radii, fluxes, magnifications,
  evidences) are unaffected. Oriented quantities (centres/offsets, PAs and e2, shear angle and gamma_2, source-plane
  positions) differ from the sky frame by a fixed sign flip. Models must NOT be rerun.
- rgb.jpg cutouts were flipped 2026-09-20 (preprocess/flip_rgb.py) to match the pipeline frame, so they are north down too.
- scripts/tools/build_wcs_package.py says "+y is NOT north"; its wording "+y points along increasing FITS row"
  contradicts its own conclusion and needs correcting.

## Research
1. Derive the exact sign conversions for every oriented catalogue quantity (PA east of north for lens light, mass,
   shear, source; e1/e2; gamma_1/gamma_2; east/north offsets) and prove them with the Witness tests above.
2. Check whether release model FITS (model.fits, pre_psf.fits, source reconstructions) carry a WCS header that is
   consistent with their pixel order; a copied WCS on an unflipped array would be mislabelled.
3. Scan all cutout WCS headers for rotation or parity outliers.

## Work (after the research is signed off)
- CSV snapshot builder (scripts/tools/csv_snapshot/): add sky-frame columns next to the fitted values, from stored
  results only (no refits); document both frames in master_columns.csv. Required before the PUBLIC release so every
  orientation number in the paper appears verbatim in the catalogue.
- Docs: one paragraph in README / KNOWN_ISSUES / the ECLIPSE website about page: FITS, RA/Dec and sky-frame columns are
  standard; per-lens diagnostic PNGs are in the native pipeline frame (north down, east left).
- Paper (euclid_dr1/paper): render image figures north-up east-left (flip array + overlays, plot origin lower) with a
  standard N/E compass; quote PAs east of north from the new columns; one Methods sentence stating the conversion.
- Website (lens/ECLIPSE_lens_catalogue): north-up thumbnails/colour previews made from the FITS; a correct N/E compass
  overlay on the native-frame pipeline figures.
- Not in scope: pixel-flipping pipeline PNGs (text/ticks invert) and re-rendering the ~15k bulk PNGs; the latter is a
  catalogue v1.1 after the PyAutoLens orientation fix lands.

<!-- formalised by the Intake (Conception) Agent on 2026-10-26 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/c0b2abd0-8361-418f-83e2-031a4c6e94ff/scratchpad/dr1_sky_frame_intake.md -->
