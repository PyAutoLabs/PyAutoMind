# Sky orientation (north/east): euclid_dr1 catalogue, paper and website, plus the PyAutoLens library-wide fix

Type: research
Target: euclid
Repos:
- euclid_dr1 (science project, /mnt/c/Users/Jammy/Science/active/euclid_dr1; RAL /mnt/ral/jnightin/active/euclid_dr1)
- ECLIPSE_lens_catalogue (lens/ECLIPSE_lens_catalogue, website leg)
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
- HowToLens
Themes:
- euclid
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: (1) on at least five real DR1 lenses, positions.json overlaid on the VIS image lands on the multiple images, and the catalogue's sky-frame position angle (east of north) of the lens light, lens mass and external shear matches the orientation measured on the north-up FITS through its WCS, with sky-frame centres agreeing with the stored RA/Dec to within a pixel; (2) a simulated lens with known north-up PA, written to FITS with a CD1_1<0/CD2_2>0 WCS, fitted and converted, recovers its PA east of north and RA/Dec centre; (3) every existing WCS-bearing JSON/CSV in the release is byte-identical before and after, or its diff is listed and human-approved.
Review-minutes: 25
Unattended: needs-slicing

Found 2026-10-26 while packaging the Euclid DR1 release. Human wants this done THIS WEEK (week of 2026-10-26).
Replaces the two separate prompts filed earlier the same day (sky_orientation_pyautolens_frame_is_a_north,
euclid_dr1_catalogue_sky_frame_orientation_north). Order: euclid_dr1 legs first (they feed the paper and the
public catalogue), library-wide fix after.

## HARD RULE: WCS-bearing JSON files are watched
The human gives these catalogues to people who use the WCS information. Any change to a .json file (and to
wcs.csv) must be monitored carefully:
- Files in scope: per-lens wcs_vis_lp.json / wcs_vis_pix.json (byte copies of each fit's files/wcs.json),
  dataset positions.json / positions_meta.json / info.json, the result zips' files/wcs.json, and wcs.csv.
- Default is ADD, never modify: new sky-frame quantities go in new columns / new files or new keys, existing
  keys and values stay byte-identical. Never rewrite a stored result's files/wcs.json.
- If any existing JSON must change: stop and ask the human first; then snapshot the originals (sha256 manifest),
  produce a per-file diff report, validate before/after on sample lenses, bump the catalogue version, and write a
  CHANGELOG entry that WCS users can read. No silent overwrite, ever.
- Packaging (scripts/tools/package_release.py) copies JSON byte-identical; keep it that way and check
  file_manifest.csv sha256 against the previous release for every JSON.

## Facts established (2026-10-26)
- DR1 cutout FITS WCS: CD1_1 < 0, CD2_2 > 0, no rotation -> north up, east left in the FITS convention (checked on
  one tile only; scan all ~15k headers on RAL for rotation/parity outliers).
- PyAutoArray loads FITS with no row flip and plots imshow origin upper (config/visualize/general.yaml) -> every
  pipeline PNG is north DOWN, east LEFT, a vertical mirror of the sky. Model frame: +y = south, +x = west.
- Data, noise, PSF, mask and segmentation were all read the same way, so every fit is self-consistent in the
  mirrored frame. Lensing is parity invariant: scalar quantities (Einstein radii, q, Sersic n, radii, fluxes,
  magnifications, evidences) are unaffected; oriented quantities (centres/offsets, PAs and e2, shear angle and
  gamma_2, source-plane positions) differ from the sky frame by a fixed sign flip. NO lens model is rerun.
- rgb.jpg cutouts were flipped 2026-09-20 (preprocess/flip_rgb.py) to match the pipeline frame (north down too).
- scripts/tools/build_wcs_package.py says "+y is NOT north"; its wording "+y points along increasing FITS row"
  contradicts its own conclusion and needs correcting (docstring only).
- Under imshow_origin: lower the displayed y axis and the reported model y disagree in sign, so switching the display
  alone swaps one confusion for another.

## Phase 1 — euclid_dr1 research (gates everything)
1. FIRST: confirm every external input to the fits was in the pixel frame. How was positions.json made (pixel
   picks or RA/Dec -> arcsec with +y north)? Overlay positions on asymmetric lenses. Same for any angle/position
   priors. If any input was sky-frame, the no-remodel conclusion fails for those fits: stop and report.
2. Derive the exact sign conversions for every oriented catalogue quantity and prove them with the Witness tests.
3. Check that release model FITS (model.fits, pre_psf.fits, source reconstructions) carry WCS headers consistent with
   their pixel order (a copied WCS on an unflipped array would be mislabelled).
4. Scan all cutout WCS headers for rotation or parity outliers.

## Phase 2 — euclid_dr1 work (after phase 1 is signed off)
- CSV snapshot builder (scripts/tools/csv_snapshot/): ADD sky-frame columns (PA east of north for lens light, mass,
  shear, source; east/north offsets) next to the fitted values, from stored results only; document both frames in
  master_columns.csv. Required before the PUBLIC release so every orientation number in the paper appears verbatim
  in the catalogue. Existing columns unchanged.
- Docs: one paragraph in README / KNOWN_ISSUES / the website about page: FITS, RA/Dec and sky-frame columns are
  standard; per-lens diagnostic PNGs are in the native pipeline frame (north down, east left).
- Paper (euclid_dr1/paper): image figures north-up east-left (flip image + overlays together, sky-frame axis labels
  or none) with a standard N/E compass; PAs east of north from the new columns; one Methods sentence.
- Website (lens/ECLIPSE_lens_catalogue): north-up thumbnails/colour previews from the FITS; a correct N/E compass
  overlay on the native-frame pipeline figures.
- Not in scope: pixel-flipping pipeline PNGs (text and ticks invert).

## Phase 3 — library-wide (PyAutoArray / PyAutoGalaxy / PyAutoLens / HowToLens, all users)
- Decide the convention: row flip at FITS load so +y = north, or keep the current frame and make it explicit.
- Sky-frame conversion utilities for oriented quantities (PA east of north; e1/e2; gamma_1/gamma_2; centres to RA/Dec
  via the dataset WCS), with sign tests on a simulated lens through a real WCS.
- Optional N/E compass overlay on visualizer figures when a WCS is known; consistent axis labelling.
- Document the convention in workspace / HowToLens docs.
- Backwards compatible or an explicit opt-in switch: existing fits and result files (including files/wcs.json)
  stay valid and unchanged.
- Follow-on: once it lands, re-render the DR1 bulk per-lens PNGs north-up as catalogue v1.1 (visualisation only,
  from stored results, no refits), under the JSON hard rule above.
