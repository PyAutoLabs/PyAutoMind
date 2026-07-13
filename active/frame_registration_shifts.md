# Inter-exposure pixel shifts: quantify accuracy, extract for modeling, decide their role in the lens model

Type: research
Target: pyautoreduce
Repos:
- PyAutoReduce
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Follow-up to the shipped frame-products mode (PyAutoReduce #16 / PR #18): the
per-exposure products exist; multi-frame lens modeling now needs to know how
well the frames are registered to each other.

## Original request (user, 2026-07-10, verbatim)

> we need to work out how well know the pixel shifts are across exposures,
> ensure we extract this information which is a key input to the lens modeling
> (e.g. maybe we outptu it as a .json or something) and assess if the shifts
> need to be part of the lens model or if they are knownperfect, I guess thats
> a choice. Then do the PSF work

## Tasks

1. **Quantify** how well the inter-exposure registration is known, per frame:
   the astrometric solution in the `_flc`/`_flt` headers (WCSNAME family —
   a-priori GSC/Gaia vs FIT-REL/FIT-IMG Gaia fits — plus their RMS_RA/RMS_DEC/
   NMATCH quality keywords), the align stage's tweakreg trigger + residuals,
   and an empirical cross-check on the slacs0008 validation frames (already on
   disk under output/frame_products_validation/). Express everything in native
   pixels (ACS 0.05"/px).
2. **Extract**: audit what the frames output already carries (per-frame SIP WCS
   in each data.fits header + full-distortion `target_pixel` anchor in
   frames/manifest.json) and enrich the manifest so registration is explicit
   modeling input — e.g. a per-frame `registration` block (wcs solution name,
   fit rms in mas and native px, n_matches, relative shift vs the first frame
   at the target position) in the existing frames/manifest.json (it IS the
   .json the request asks for — no new file unless needed).
3. **Decide/recommend**: should the shifts be (a) treated as perfectly known
   (registration rms ≪ the scale lens modeling is sensitive to) or (b) free
   nuisance parameters (per-frame dy,dx with tight Gaussian priors set from
   the recorded rms)? Deliver a criterion, not just a verdict — the choice is
   documented in the design doc (hst_acs_pipeline.md frames section) and feeds
   the future PyAutoLens multi-exposure fitting design. This is a scientific
   judgment checkpoint (supervised): recommendation goes to the human.

Constraint: PyAutoReduce claim is contested (slacs1430-acs-parity plans its
phase-4 ship on it) — analysis on main (keck-ao pattern), branch only at ship.
