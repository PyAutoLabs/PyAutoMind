## alma-interferometer
- completed: 2026-07-09
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/14 (closed)
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/15 (merged 11a2484, squash)
- summary: ALMA interferometer reduction live (phase 5) — first visibility-domain product family: calibrated MS → al.Interferometer triplet ((Nvis,2) data/uv_wavelengths/noise_map) via acquire→split→extract→assemble→package on headless modular CASA; grounded in Aris's continuum recipe + WEIGHT-column noise he didn't export; weighted Stokes-I combine; 143 tests; --auto safe run, review gate fixed 2 real bugs (cache-lifecycle KeyError, Stokes-I non-finite bias)
- followups: G09v1.40 end-to-end validation (prototypes/alma_g09v140_spike.py) once Aris's reference exports or a calibrated-MS delivery arrive (needs pip casatools/casatasks); design-doc open items: scriptForPI restore automation, line/cube extraction (reduction side of alma-datacube)
