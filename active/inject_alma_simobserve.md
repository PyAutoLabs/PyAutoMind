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
