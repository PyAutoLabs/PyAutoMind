# Should PyAutoArray flip FITS rows at load so +y is north? (after Euclid DR1)

Type: research
Target: libraries
Repos:
- @PyAutoArray
- @PyAutoGalaxy
- @PyAutoLens
- autolens_workspace
- autogalaxy_workspace
- HowToLens
- HowToGalaxy
Themes:
- release
Difficulty: large
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Witness: A written decision (adopt / reject / adopt behind an opt-in) backed by (1) a simulated lens written to a standard north-up FITS (CD1_1<0, CD2_2>0), loaded under the current and the proposed convention, showing centre, position angle, e1/e2 and gamma_1/gamma_2 in each and the sky-frame values; (2) an inventory of everything a row flip would change for existing users (stored results, files/wcs.json, positions files, centre and angle priors, mask centres, saved simulated datasets, aggregator outputs, COOLEST export), each marked breaks / migrates / unaffected; (3) a migration and versioning plan if adopted.
Review-minutes: 15
Unattended: needs-slicing
Filed: 2026-10-30

Do NOT start before Euclid DR1 v1.0 ships (target ~2026-11-09). Split out of
`draft/research/euclid/sky_orientation_euclid_dr1_and_library.md` by human decision on 2026-10-30.

## Problem
PyAutoArray loads FITS with no row flip (`al.Imaging.from_fits`, util.py:1098) and maps row 0 to the top of the arcsec
grid (y = (ny/2 - 0.5 - row) * ps). For a standard north-up FITS (CD2_2 > 0, so row 0 is the southern edge) this
makes **+y = south and +x = west**. That is a mirror of the sky, not a rotation. So:
- Increasing a centre's y moves it **down** (south) on a north-up image, which users find unnatural.
- Angles measured counter-clockwise from +x in the model run clockwise on the sky, so position angles, e2 and the
  shear angle come out mirrored, not just y.
- The COOLEST interop (PyAutoGalaxy `autogalaxy/interop/coolest/conventions.py`, PyAutoLens
  `autolens/interop/coolest.py`) already ASSUMES +y is north, so it is wrong for real FITS loaded as-is.
- Inside the pipeline everything is self-consistent (PNGs draw +y at the top of the screen); the problem appears only
  against the sky or against north-up images.

This applies to essentially every user with real data, not only Euclid.

## Options to compare
- A. Flip rows at load (and the inverse at save) so +y = north and +x = west, matching the sky frame and COOLEST as
  written. Breaking for existing fits, stored results, positions files, priors and mask centres; needs versioning,
  migration and release notes. Simulated data round-trips unchanged if load and save flip together.
- B. Keep the current frame and rely on the additive sky-frame utilities, north-up display option and COOLEST
  correction delivered by the DR1 task's phase 3. No breakage; the native frame stays mirrored.
- C. A per-dataset or global opt-in (e.g. a config or `from_fits` argument) defaulting to the current behaviour, with
  a deprecation path towards A.

## Notes
- Builds on the DR1 task's phase-1 conversion table (PyAutoLens native -> sky -> COOLEST -> lenstronomy -> herculens)
  and its phase-3 utilities; reuse them for the witness.
- Interacts with the workspace WCS guide (DR1 task phase 4): the guide must describe whichever convention wins.
