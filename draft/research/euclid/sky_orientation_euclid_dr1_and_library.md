# Sky orientation (north/east): euclid_dr1 catalogue, paper and website, plus the PyAutoLens library-wide fix

> **Remainder after phase 1 (done 2026-10-31, record complete/2026/10/sky-orientation-dr1-p1.md). Start at phase 2; read "Phase 1 result + decisions" first.**

Type: research
Target: euclid
Repos:
- euclid_dr1 (science project, /mnt/c/Users/Jammy/Science/active/euclid_dr1; RAL /mnt/ral/jnightin/active/euclid_dr1)
- ECLIPSE_lens_catalogue (lens/ECLIPSE_lens_catalogue, website leg)
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
- HowToLens
- HowToGalaxy
- autolens_workspace
- autogalaxy_workspace
Themes:
- euclid
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: (1) on at least five real DR1 lenses, positions.json overlaid on the VIS image lands on the multiple images, and the catalogue's sky-frame position angle (east of north) of the lens light, lens mass and external shear matches the orientation measured on the north-up FITS through its WCS, with sky-frame centres agreeing with the stored RA/Dec to within a pixel; (2) a simulated lens with known north-up PA, written to FITS with a CD1_1<0/CD2_2>0 WCS, fitted and converted, recovers its PA east of north and RA/Dec centre; (3) every existing WCS-bearing JSON/CSV in the release is byte-identical before and after, or its diff is listed and human-approved; (4) the workspace WCS guide runs end to end in both autolens_workspace and autogalaxy_workspace and its worked example (a simulated lens through a real WCS) prints the same PA east of north and RA/Dec as the library conversion utilities and the COOLEST export.
Review-minutes: 25
Unattended: needs-slicing

Found 2026-10-26 while packaging the Euclid DR1 release. Human wants this STARTED THIS WEEK (week of 2026-10-26);
the DR1 catalogue has ~2 weeks of prep left (release target ~2026-11-09).

## SCOPE MANDATE (human, 2026-10-26): make DR1 as standard as possible, no refits
- Do NOT rerun any lens model (no new non-linear searches). Everything else is allowed.
- Large-scale RAL runs ARE allowed and expected (CPU on `ral` only, never `gpu`): re-render every per-lens PNG,
  rewrite derived products, rebuild the catalogue and release tiers, whatever makes the DR1 products the best
  possible, most standardised format.
- Target end state for DR1 v1.0 (not a later v1.1): every figure north-up, east-left with a correct N/E compass and
  sky-frame axis labels; sky-frame columns throughout; FITS/WCS consistent; COOLEST-consistent conventions;
  documented in one guide. Everything is regenerated from the stored fit results.
- END POINT = CONSISTENCY with COOLEST, lenstronomy and herculens: a reader can take any DR1 orientation quantity
  into those codes without guessing. Consistency is achieved by catalogue-level additions (sky-frame and
  code-convention columns, documented conversions, re-rendered figures), NOT by changing PyAutoArray / PyAutoGalaxy
  / PyAutoLens rotation or coordinate conventions. No library source change to how FITS are loaded, how angles or
  ell_comps are defined, or how (y, x) map to pixels.
- Planned for the strongest model (Fable architect, Opus execution), as a multi-phase epic: survey -> design ->
  RAL re-render campaign -> rebuild -> verify -> release. The full-tier packaging run waits on this (re-rendered
  PNGs supersede the current ones).
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
- rgb.jpg cutouts were flipped 2026-09-20 (preprocess/flip_rgb.py) to match the pipeline frame (north down too);
  the delivered originals are kept as rgb_raw.jpg (north-up, matching the FITS) - use them for the north-up products.
- scripts/tools/build_wcs_package.py says "+y is NOT north"; its wording "+y points along increasing FITS row"
  contradicts its own conclusion and needs correcting (docstring only).
- Under imshow_origin: lower the displayed y axis and the reported model y disagree in sign, so switching the display
  alone swaps one confusion for another.

## Decisions and evidence (human, 2026-10-30)
- ORIENTATION CHECKED on 10 random catalogue lenses against the human's north-up RGB set
  (`PyAutoLabs/scratch/jpegs_uniform_AB.zip`, 15,073 JPEGs named `EUCL-DR1-L<id>.jpg`, 100x100; covers all 15,071
  included A+B catalogue lenses plus 2 extra IDs). Shown row 0 at the top, they are NORTH UP, EAST LEFT, with no left-right
  mirror: identical layout to `rgb_raw.jpg` (5 tiles; corr 0.70-0.95, stretch differs) and to the VIS FITS drawn with
  origin=lower; the VIS array drawn the pipeline way (origin=upper) is their vertical flip (corr 0.91-0.99, all 10).
  Every sampled WCS has CD1_1 = -0.1"/px, CD2_2 = +0.1"/px, no rotation. The per-tile `<tile>.png` in the dataset is a
  greyscale VIS preview in the pipeline frame (north DOWN), not an RGB.
- One by-eye check of a pipeline `subplot_fit_lp.png` (L002962) agrees: +y ticks rise upward on screen while +y = south on
  the sky, +x = west. The facts above stand.
- RGB COVERAGE: locally only 9,476 / 15,034 dr1_sep1 tiles have `rgb.jpg` (9,472 `rgb_raw.jpg`; 4 tiles have a flipped
  `rgb.jpg` but no `rgb_raw.jpg` marker, so a flip_rgb.py rerun would flip those back); ~5,560 tiles have no RGB.
- AGREED: for DR1 v1.0 the native frame stays as fitted (+y = south, +x = west, documented as such); north-positive values
  are delivered through the phase-2 sky-frame catalogue columns. No library convention change before release.
- AGREED: north-up RGBs with the orientation above are the reference for every DR1 user-facing product. The human says the
  RGBs are already in `dataset/euclid_dr1` on RAL (`/mnt/ral/jnightin/active/euclid_dr1/dataset/`, possibly PNGs):
  use those, after checking each one's orientation against VIS by correlation (the phase-1 orientation check). They feed
  the north-up re-rendered RGB panels, the release tiers and the Cloudflare ECLIPSE website (lens/ECLIPSE_lens_catalogue)
  thumbnails/previews.
- AGREED: the old rgb-flip bug draft (draft/bug/euclid/euclid_dr1_flip_rgb_jpg_upside_down.md) is superseded by this task.
- OPEN, after DR1: whether the library should flip rows at load so +y = north
  (draft/research/libraries/plus_y_north_at_fits_load.md). Out of scope here.
- Fit PNG re-render requirement (phase 2) restated: flip the image arrays AND negate y on every overlay (critical curves,
  caustics, positions, centres, mask), source-plane panels too, sky-frame axis labels and an N/E compass. Never pixel-flip
  an existing PNG, and never switch only imshow_origin (labels and model y would disagree).
- AGREED: start phase 1 (approved 2026-10-30; not yet started, next step is /start_dev on this prompt).

> PHASE 1 DONE 2026-10-31 (euclid#113 / PR #114; record complete/2026/10/sky-orientation-dr1-p1.md).
> This draft is the remainder: start at phase 2. The human decisions below are binding for phase 2.

## Phase 1 result + decisions (2026-10-31, euclid#113)
- Phase 1 shipped (docs/sky_orientation/phase1.md + conventions.md in the euclid repo). Frame confirmed; PA east of
  north = (90 - phi) mod 180; wcs.json RA/Dec correct; pipeline coolest.json MIRRORED (phi = -PA, center_y sign);
  result FITS carry no WCS; 15,032/15,032 cutout WCS identical (Tile102012389... has no local cutout FITS).
- HUMAN 2026-10-31: (1) REGENERATE coolest.json in phase 2 (approved JSON change: snapshot, diff, validate,
  version bump, CHANGELOG; coolest.json only, every other JSON byte-identical); (2) ADD a WCS to the release model
  FITS; (3) cutouts regenerated after the fits judged fine; (4) fix the build_wcs_package.py docstring (on
  ral-path-v5-catalogue) when possible.

## Phase 1 — euclid_dr1 research (gates everything)
1. FIRST: confirm every external input to the fits was in the pixel frame. How was positions.json made (pixel
   picks or RA/Dec -> arcsec with +y north)? Overlay positions on asymmetric lenses. Same for any angle/position
   priors. If any input was sky-frame, the no-remodel conclusion fails for those fits: stop and report.
2. Derive the exact sign conversions for every oriented catalogue quantity and prove them with the Witness tests.
3. Check that release model FITS (model.fits, pre_psf.fits, source reconstructions) carry WCS headers consistent with
   their pixel order (a copied WCS on an unflipped array would be mislabelled).
4. Scan all cutout WCS headers for rotation or parity outliers.
5. Research lenstronomy and herculens conventions from their source and docs (cite file:line / doc URL): pixel ->
   angle mapping (lenstronomy's transform_pix2angle / ra_at_xy_0, whether +x is west or east, whether they flip FITS
   rows), position-angle origin and direction, e1/e2 and gamma1/gamma2 definitions, centre conventions; herculens
   (follows lenstronomy closely - confirm where it differs). Also re-read the COOLEST standard's own axis/angle
   definitions. Produce one conversion table: PyAutoLens native frame (+y south, +x west for DR1) -> sky
   (PA east of north, RA/Dec, east/north offsets) -> COOLEST -> lenstronomy -> herculens, with a round-trip test on
   a simulated lens for each (research-only scripts; no library edits).
6. Positions frame: RESOLVED 2026-10-26 from the code. positions.json = peaks of segmentation/source_flux.fits read
   with fits.getdata (no row flip), pixel_to_arcsec y = (ny/2 - 0.5 - row) * ps (positions_finder.py:477), the same
   as al.Imaging.from_fits (no row flip, util.py:1098); segmentation matches VIS. All fit inputs share one frame, so
   no fit is invalid. Still overlay positions on a few asymmetric lenses as the Witness. Fix the finder docstring
   "(y up, x right)" wording (true on screen, +y is south on the sky).

## Phase 2 — euclid_dr1 work (after phase 1 is signed off)
- CSV snapshot builder (scripts/tools/csv_snapshot/): ADD sky-frame columns (PA east of north for lens light, mass,
  shear, source; east/north offsets) next to the fitted values, from stored results only; document both frames in
  master_columns.csv. Where the phase-1 table shows lenstronomy/herculens/COOLEST conventions differ from the sky
  frame, add their columns too (or a documented one-line conversion each), so the catalogue is directly usable in
  all three. Required before the PUBLIC release so every orientation number in the paper appears verbatim
  in the catalogue. Existing columns unchanged.
- Docs: one paragraph in README / KNOWN_ISSUES / the website about page: FITS, RA/Dec and sky-frame columns are
  standard; per-lens diagnostic PNGs are in the native pipeline frame (north down, east left).
- Paper (euclid_dr1/paper): image figures north-up east-left (flip image + overlays together, sky-frame axis labels
  or none) with a standard N/E compass; PAs east of north from the new columns; one Methods sentence.
- RAL re-render campaign (in scope for DR1 v1.0): regenerate EVERY per-lens PNG (vis_lp, vis_pix, Sersic, SED,
  inspect/RGB panels) north-up east-left from the stored results, image and overlays flipped together, sky-frame
  axis labels, N/E compass. Visualisation only: load stored results, never search. Chunked arrays on `ral`, with
  a pilot on ~50 lenses reviewed by the human before the full run; then merge -> CSV snapshot -> package all tiers.
- Website (lens/ECLIPSE_lens_catalogue): thumbnails and previews from the re-rendered north-up products; the
  figures need no compass overlay once they carry their own.
- Not in scope: pixel-flipping existing PNGs (text and ticks invert) - re-render instead.

## Phase 3 — library-wide (PyAutoArray / PyAutoGalaxy / PyAutoLens / HowToLens, all users)
- KEEP the current conventions (no row flip at load, angles and ell_comps unchanged, (y, x) mapping unchanged):
  no source change to rotations or coordinate conventions. Make the frame explicit instead.
- Additive only: sky-frame conversion utilities for oriented quantities (PA east of north; e1/e2; gamma_1/gamma_2; centres to RA/Dec
  via the dataset WCS), with sign tests on a simulated lens through a real WCS.
- Optional N/E compass overlay on visualizer figures when a WCS is known; consistent axis labelling.
- Document the convention in workspace / HowToLens docs.
- Backwards compatible and additive: existing fits and result files (including files/wcs.json) stay valid and
  unchanged; any north-up plotting is a display option, never a change to the data or model frame.
- COOLEST interop (PyAutoGalaxy autogalaxy/interop/coolest/conventions.py, PyAutoLens autolens/interop/coolest.py)
  ASSUMES PyAutoGalaxy +y is north: phi_coolest_from() returns angle - 90 as "East-of-North" and
  center_from_centre() only reorders (y, x) -> (x, y) with "y increasing upwards". For data loaded like DR1
  (+y = south) a COOLEST export would carry mirrored PAs/centres. Verify against the COOLEST standard's own
  axis definitions. Do NOT change the COOLEST conversion maths in this task; document the assumption, and if it is
  wrong for unflipped data, provide the correction as an additive wrapper/argument (or file a separate prompt),
  tested together with the sky-frame utilities.
- Timing: the DR1 re-render needs the north-up plotting path within the 2-week window. Land the minimal library
  pieces it needs first (orientation-aware plotting + sky-frame conversion utilities), or, if the library design
  cannot land in time, implement the flip in the euclid_dr1 re-render scripts and port it to the library after;
  decide this in the design phase. Either way, under the JSON hard rule above.

## Phase 4 — the go-to reader guide (autolens_workspace AND autogalaxy_workspace)
One guide per workspace (mirrored content, lens vs galaxy examples), the single resource a reader needs on
coordinates and orientation. It must fully explain:
- WCS basics: what a FITS WCS is, CRPIX/CRVAL/CD matrix, the sign of CD1_1/CD2_2, rotation and parity, how to
  read the orientation of any cutout, and how pixel (row, column) maps to (RA, Dec).
- PyAutoLens / PyAutoGalaxy conventions: (y, x) ordering, arcsec grid centred on the image, which way +y and +x
  point relative to FITS rows and columns, the imshow origin config and what it does and does not change, angle
  definitions (counter-clockwise from +x), ell_comps and shear components.
- The explicit mapping from north/south/east/west to pixel and arcsec units, for data loaded as-is and for data
  loaded under whatever convention phase 3 adopts, with a worked example on a simulated lens through a real WCS.
- Converting results to the sky frame: PA east of north, centres to RA/Dec, using the phase-3 utilities.
- COOLEST, lenstronomy and herculens: link to the COOLEST standard (https://github.com/aymgal/COOLEST), the
  PyAutoLens/PyAutoGalaxy COOLEST interop and the lenstronomy / herculens convention docs; include the phase-1
  conversion table and show on one example that the guide, the utilities, the COOLEST export and the
  lenstronomy/herculens conventions agree.
- Placement: follow the workspace's guides/ conventions (consult the Workspace Agent for target folder, sibling
  to mirror and format; scripts with notebooks generated as usual). Link it from the workspace README / docs index.

## Phase 5 — HowToLens / HowToGalaxy follow-up and a scan for other places
- HowToLens (and HowToGalaxy) mention these conventions EARLY (the first chapter that loads or plots imaging):
  a short paragraph on (y, x), which way north points, and a link to the workspace guide.
- Scan for other suitable places and add a short pointer to the guide where readers meet coordinates: data
  loading / preparation examples, positions and point-source examples, plotting and visualization docs, results /
  aggregator examples that report centres or angles, the COOLEST interop docs, and the assistant skills/wiki
  (autolens_assistant, autogalaxy_assistant). Report the scan as a list (file, why, proposed one-line pointer)
  for human approval before editing.
