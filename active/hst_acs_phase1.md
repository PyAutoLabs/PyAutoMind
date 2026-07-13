# PyAutoReduce phase 1: implement the HST/ACS reduction pipeline

Type: feature
Target: PyAutoReduce
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Implement the HST/ACS pipeline designed and validated in
`PyAutoReduce/docs/design/hst_acs_pipeline.md` (the authoritative spec — read
it first; it carries the parity appendix and the spike-taught rules). The
spike `prototypes/slacs_f814w_spike.py` proved every joint end-to-end on
slacs0008-0004; phase 1 turns it into production `autoreduce` code.

Scope (per the design doc, defaults-first with documented lensing deviations):

- **acquire/**: MAST query filtered to direct calibration-level-2 observations
  grouped by proposal/visit (HAP-skycell products excluded; HAPCut is its own
  path), `_flc` download, CRDS best-references sync (`jref$`), transient
  size-capped per-target cache with manifest; reference files are the
  non-evicted component.
- **align/**: a-priori WCS by default; alignment diagnostic + TweakReg as a
  triggered fallback.
- **drizzle/**: AstroDrizzle to 0.05″/pix north-up cps mosaics with IVM
  weights; `final_pixfrac`/`final_kernel` are **user-facing dials** (default
  0.8/square) — every run reports the WHT RMS/median uniformity diagnostic
  (≲0.2) and the correlated-noise factor R. Single-exposure branch per the
  SLACS-V caveat (rectify + L.A. Cosmic, or single-image drizzle — decide
  here).
- **noise/**: σ = √(N/W + σ²_sky) with R applied (spike-validated: legacy
  SLACS noise is consistent with R applied); loud failure on NaN/zero weights
  in the cutout.
- **psf/**: tier 1 ePSF (photutils) + tier 2 TinyTim/focus-diverse-ePSF
  fallback, drizzle-consistent by construction; tier 3 back-ends stay
  optional extras.
- **package/**: 281×281-default cutouts with intact WCS/units headers +
  `reduction.json` provenance.
- **instruments/**: the ACS/WFC adapter — nothing outside it may name a
  detector (the roadmap's WFC3/JWST obligation).

Acceptance (design doc "Validation"): parity on 2–3 SLACS lenses including
slacs0008-0004 with sub-pixel WCS registration and the exact legacy exposure
set — chase the spike's residual ~7% flux offset to ground truth — plus
PyAutoLens fits on both reductions agreeing within statistical errors.
Unit tests numpy/astropy-only; anything needing network/drizzlepac lives in
integration scripts. Env: extend `~/venv/PyAuto` under the existing pins
(constraints file), never a separate venv.
