## database-dataset-fits
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/744
- completed: 2026-11-22
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/745
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/878

Dataset FITS products now round-trip through SQLite and directory-backed imaging and interferometer searches. Repeated saves keep one registration. Tests covered imaging plus in-memory and array-free interferometry in both libraries.

GitHub CI at the approved heads: PyAutoLabs/PyAutoGalaxy#745: 4 successful checks, 1 skipped. PyAutoLabs/PyAutoLens#878: 4 successful checks, 1 skipped. Any skipped checks were non-test Heart-feed refreshes.

## Original prompt

# Database-path searches cannot reload dataset.fits (written to disk, never registered via save_fits)

Type: bug
Issued: 2026-11-22
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
Lane: any

Found 2026-09-30 by the Codex review of streaming phase 2 (PyAutoGalaxy#638). `AnalysisInterferometer.save_attributes`
(`autogalaxy/interferometer/model/analysis.py`, and the autolens mirror) writes `dataset.fits` straight to
`paths.image_path` and never registers it through `DatabasePaths.save_fits`, so under database paths `Fit.value("dataset")`
returns `None` (database `Fit.value` does not scan the image directory, unlike `SearchOutput`) and
`agg_util.mask_header_from` fails on `[0]`. Pre-existing (the in-memory path has always done this); the phase-2
array-free branch inherits it. Fix: route the HDU list through `paths.save_fits(name="dataset", hdu_list=...)`
(check the PyAutoFit API) so both path types see it, and add a database-paths round-trip test.
