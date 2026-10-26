# Sky orientation: PyAutoLens frame is a north-down mirror of the sky…

Type: research
Target: PyAutoLens
Repos:
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
- HowToLens
Difficulty: too-large
Autonomy: supervised
Priority: normal
Memory: reading-queue.md; wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/massive-ellipticals.md
Status: formalised
Consequence: judge
Witness: a simulated lens with known north-up position angle, written to FITS with a CD1_1<0/CD2_2>0 WCS, fitted and converted, recovers its PA east of north and RA/Dec centre to within errors (one sign test per oriented quantity: light PA, mass PA, shear angle, centre).
Review-minutes: 25
Unattended: needs-slicing

Found 2026-10-26 while packaging the Euclid DR1 catalogue (euclid_dr1). Nothing changes now; this files the
proper fix for later. The euclid_dr1 catalogue/docs leg is deferred and will be picked up with catalogue building.

## What is happening
- Euclid DR1 cutout FITS have a standard WCS: CD1_1 < 0, CD2_2 > 0, no rotation, so north up, east left in the
  FITS convention (row 1 at the bottom, ds9 / imshow origin="lower").
- PyAutoArray loads FITS with no row flip and plots with `imshow_origin: upper` (autoarray/config/visualize/general.yaml),
  so row 0 (the southern FITS row) is drawn at the top. Every visualizer PNG shows north DOWN, east LEFT: a
  top-to-bottom mirror of the sky, not a rotation.
- The modelling frame is therefore +y = south, +x = west. euclid_dr1 already notes "+y is NOT north" in
  scripts/tools/build_wcs_package.py (whose wording "+y points along increasing FITS row" contradicts its own
  conclusion and should be fixed).
- Lensing is parity invariant, so fits are physically valid: Einstein radii, axis ratios, Sersic indices, radii,
  fluxes, magnifications and evidences are unaffected. Only oriented quantities differ from the sky frame by a fixed
  sign flip: centres/offsets, position angles and e2, external-shear angle and gamma_2, source-plane positions.
- Under `imshow_origin: lower` the displayed y axis and the reported model y parameters disagree in sign (config
  comment), so just switching the display swaps one confusion for another.

## Goal (PyAutoLens / PyAutoGalaxy / PyAutoArray, all users, not only Euclid)
Decide and implement a principled sky-orientation story:
- Decide the intended convention: either load FITS so +y = north (row flip at load) or keep the current frame and
  make it explicit everywhere.
- Provide sky-frame conversion utilities for oriented quantities (position angle east of north for light, mass and
  shear; ellipticity/shear components; centres to RA/Dec via the dataset WCS), verified with sign tests on a
  simulated lens pushed through a real WCS.
- Optionally a N/E compass overlay on visualizer figures when a WCS is known.
- Document the convention in the workspace/HowToLens docs.
- Do not break existing fits: result parameters stay as fitted; any change must be backwards compatible or a
  documented, opt-in switch.

## Deferred euclid_dr1 leg (catalogue building + docs, later, no changes now)
- Add sky-frame PA columns (east of north) to the CSV snapshot builder from stored results (no refits), after
  verifying signs on real lenses.
- One paragraph in README / KNOWN_ISSUES / ECLIPSE website about page stating the pipeline frame.
- Website: north-up thumbnails/RGB made from FITS; N/E compass overlay on pipeline figures.
- No lens models are rerun and pipeline PNGs are not pixel-flipped (text and tick labels would invert).

<!-- formalised by the Intake (Conception) Agent on 2026-10-26 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/c0b2abd0-8361-418f-83e2-031a4c6e94ff/scratchpad/sky_orientation_intake.md -->
