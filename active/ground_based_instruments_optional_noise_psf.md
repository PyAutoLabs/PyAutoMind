# Ground-based instrument products (DES/SDSS/HSC) with optional noise map + PSF

Type: feature
Target: pyautoreduce
Repos:
- pyautoreduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Make it so that PyAutoReduce can also produce data for ground based instruments (e.g. DES, SDSS, HSC) when available.
Often, these are not really going to be used for modeling, just to give color information on lenses which may be
missing on occasions (especially for ALMA). So, RMS noise map and PSF should be optional. Then assess if there
is any other multi wavelength coverage that would be easy to add to PyAutoReduce.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/59a19942-c45f-4f2a-ad18-6bcc3dd8a7ba/scratchpad/chunk3_feature.md -->
<!-- hand-fixed in review: work-type test->feature, difficulty small->medium (multi-instrument acquisition + optional-products plumbing + coverage assessment) -->
