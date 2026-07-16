## survey-cutouts
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/50
- completed: 2026-07-16
- library-pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/51 (squash 81f8a42c9)
- Third adapter domain "cutout" — ground-based colour context, fetch+package never reduce: SurveyCutoutAdapter + legacy_surveys/sdss/panstarrs, autoreduce/surveys/ (verified-live URL builders, per-band data.fits, noise_map.fits from Legacy &invvar HDU only), reduce_target dispatch, TargetSpec.survey_bands. Noise/PSF optional BY DESIGN with a products_optional provenance block so cutouts never masquerade as modeling data. Design + coverage assessment in docs/design/surveys.md.
- Key facts: DES rides Legacy DR10 (covers DECam footprint; no DESDM integration needed); Legacy &invvar appends an ivar HDU to the same request (verified live); PS1 = ps1filenames.py table (col 4 filter, col 7 filename) + fitscut.cgi; HSC deferred (STARs auth); unWISE+GALEX = cheapest extensions (same Legacy endpoint, layer= dial).
- Validation: 240/3skip suite (11 new, monkeypatched fetchers — no network in unit tests); real-network spike delivered slacs0008 from all 3 services.
- Closes the 2026-07-16 intake triple: research verdict (#44/#45) → inject stage (#46/#47, recovery 0.971±noise) → refactor sweep (#48/#49) → this (#50/#51).

## Original prompt

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
