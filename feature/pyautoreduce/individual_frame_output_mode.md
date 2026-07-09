# Optional individual-frame output mode (HST _flc/_flt) for per-exposure modeling in PyAutoLens, plus a JWST feasibility scan

Type: feature
Target: pyautoreduce
Repos:
- PyAutoReduce
- PyAutoLens
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Working in the PyAutoReduce repository — the data-reduction library that builds the HST (and future JWST) pipelines that turn raw imaging into modeling-ready datasets for PyAutoLens/PyAutoGalaxy.

Add functionality that supports outputting the individual exposure frames — the calibrated per-exposure images produced before drizzling — so that these individual frames can ultimately be modeled in PyAutoLens, rather than only the final drizzled mosaic. For HST these individual frames are the `_flc` / `_flt` products. Introduce this as an optional mode that is off by default (it is slow), and when switched on, outputs all of these extra per-exposure frames before they are drizzled together by the standard pipeline.

Then investigate whether the equivalent per-frame image output is possible and meaningful for JWST data. It is less clear how this should be done for JWST. Include a literature scan of galaxy-formation papers that do detailed analysis, plus AGN and weak-lensing work, to assess whether people actually model individual JWST frames or whether the standard mosaic is sufficient.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user prompt (intaken via /intake; target corrected autogalaxy->pyautoreduce in review — the classifier resolved the downstream consumers rather than the home repo. Note: bundles an HST feature with a JWST research/literature-scan sub-part; may split at start_dev.) -->
