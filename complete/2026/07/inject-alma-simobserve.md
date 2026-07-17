## inject-alma-simobserve
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/56
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/57 (squash 85893f692)
- Phase 3 (FINAL) of simulate.md: simobserve acquire-alternative on the visibility branch. inject_image (Jy/pixel) → 4-axis Jy/pixel skymodel (RA---SIN/DEC--SIN/STOKES/FREQ) → headless simobserve (alma_sim_* dials; pwv=0 noiseless) → existing split/extract/assemble/package unchanged → al.Interferometer.from_fits. Sim MS: single field id 0, spw 0 — alma_uids/field/spws not required in sim mode; cache lifecycle bypassed (source=simobserve). Imaging gate admits visibility-domain injection; cutout domain stays rejected. Suite 260/3skip (10 new casatools-free tests).
- DEFERRED with recorded reason (simulate.md): uv-plane injection into a real MS (true Balrog analogue) — needs FT-at-uv-points + phase-centre machinery; file as own prompt if real-MS calibration systematics matter.
- Trap: the phase-2b gate test asserting alma+inject raises became stale by design — the rejection WAS the old contract; updated to cutout-rejection.
- OPEN evidence across the inject arc: COSMOS-Web JWST recovery, B1938+666 Keck recovery + re-registration check, casatasks spike (prototypes/inject_alma_simobserve_spike.py; casatasks not in dev venv, rides the alma extra).
- The simulate.md verdict is now FULLY BUILT: #45 verdict, #47 HST (validated 0.971), #53 JWST, #55 Keck, #57 ALMA.

## Original prompt

# Inject stage phase 3: ALMA — simobserve acquire-alternative + uv-plane injection

Type: feature
Target: pyautoreduce
Repos:
- pyautoreduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Phase 3 of the simulated-data verdict (`docs/design/simulate.md`;
phases 1–2 cover imaging injection). ALMA is the one instrument where
fully-synthetic raw data is cheap and supported: CASA `simobserve`
turns a sky-model FITS into a MeasurementSet with thermal/atmospheric
noise for a chosen array configuration.

Two modes for the visibility branch (`docs/design/alma.md`):

1. **`simobserve` acquire-alternative** (fully synthetic): a
   `TargetSpec` dial pointing at an input image (reuse the phase-1
   input contract — plain FITS, flux units, pixel scale; here the FITS
   needs realistic spatial axes + flux density per simobserve's model-
   image requirements) plus array-config/integration dials; the branch
   runs simobserve headlessly (casatools/casatasks, same modular-CASA
   pattern as the existing extract stage), then the existing
   `split → extract → assemble → package` runs unchanged on the
   simulated MS.
2. **uv-plane injection into a real MS** (the Balrog analogue,
   optional/stretch): FT the input image at the MS's uv points and add
   to the real visibilities — real noise and calibration systematics
   for free, mirroring the imaging inject stage's philosophy. Decide
   in planning whether this lands in phase 3 or gets deferred with a
   recorded reason.

Provenance must carry the same never-masquerade contract as imaging
injection (`inject`/`simulated` block in `reduction.json`; phase 1's
`INJECTED` header stamp has an MS-level analogue to design).

Unit tests stay casatools-free per repo policy (pure helpers only);
the real run is a prototypes/ spike against the G09v1.40 anchor's
array config. Note casatools availability rides the existing ALMA
optional dependency (`docs/design/alma.md`).

<!-- filed 2026-07-16 on user request, per the simulate.md phasing -->
