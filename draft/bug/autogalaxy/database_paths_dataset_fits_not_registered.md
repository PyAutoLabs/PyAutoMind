# Database-path searches cannot reload dataset.fits (written to disk, never registered via save_fits)

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
Themes:
- aggregator
- interferometer
- database
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: glance
Witness: an `AnalysisInterferometer` (and imaging analogue, if affected) run under `af.DatabasePaths` reloads its dataset through `Fit.value("dataset")` — the aggregator's `_interferometer_from` and `agg_util.mask_header_from` succeed on a database `Fit` — with the same dataset the directory-paths run reloads.
Review-minutes: 3
Unattended: ready

Found 2026-09-30 by the Codex review of streaming phase 2 (PyAutoGalaxy#638). `AnalysisInterferometer.save_attributes`
(`autogalaxy/interferometer/model/analysis.py`, and the autolens mirror) writes `dataset.fits` straight to
`paths.image_path` and never registers it through `DatabasePaths.save_fits`, so under database paths `Fit.value("dataset")`
returns `None` (database `Fit.value` does not scan the image directory, unlike `SearchOutput`) and
`agg_util.mask_header_from` fails on `[0]`. Pre-existing (the in-memory path has always done this); the phase-2
array-free branch inherits it. Fix: route the HDU list through `paths.save_fits(name="dataset", hdu_list=...)`
(check the PyAutoFit API) so both path types see it, and add a database-paths round-trip test.
