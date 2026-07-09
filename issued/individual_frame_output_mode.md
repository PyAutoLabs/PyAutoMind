# Optional individual-frame output mode (HST _flc/_flt) for per-exposure modeling in PyAutoLens

Type: feature
Target: pyautoreduce
Repos:
- PyAutoReduce
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Working in the PyAutoReduce repository — the data-reduction library that builds the HST (and future JWST) pipelines that turn raw imaging into modeling-ready datasets for PyAutoLens/PyAutoGalaxy.

Add functionality that supports outputting the individual exposure frames — the calibrated per-exposure images produced before drizzling — so that these individual frames can ultimately be modeled in PyAutoLens, rather than only the final drizzled mosaic. For HST these individual frames are the `_flc` / `_flt` products. Introduce this as an optional mode that is off by default (it is slow), and when switched on, outputs all of these extra per-exposure frames before they are drizzled together by the standard pipeline.

Per-frame cosmic-ray detection uses deepCR (Zhang & Bloom 2020; Chen et al. 2024 WFC3/UVIS retrain) — user-directed during planning ("recent AI cosmic ray removal tool"); mask-only, optional dependency, documented as a deviation from STScI defaults.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user prompt (intaken via /intake; target corrected autogalaxy->pyautoreduce in review — the classifier resolved the downstream consumers rather than the home repo.) -->
<!-- split at start_dev 2026-07-09: the JWST per-frame feasibility + literature-scan sub-part moved to research/pyautoreduce/jwst_individual_frame_feasibility.md, per the Brain Feature Agent's research-first read of the bundle. PyAutoLens dropped from Repos: this task emits products only; consuming them in PyAutoLens is future work. -->
<!-- v1 scope (user-approved plan): per-frame data cutout + ERR noise map + DQ/deepCR CR masks + WCS manifest; per-frame native PSF deferred to the PyAutoReduce roadmap. -->

