# PyAutoLens mirror of the interferometer primary-beam persistence (docstring + round-trip test)

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Difficulty: small
Autonomy: safe
Priority: low
Parent: complete/2026/10/interferometer-primary-beam-persistence.md
Status: formalised
Consequence: notify
Witness: a beamed array-free save_attributes → aggregator round trip in test_autolens/interferometer/model/test_analysis_interferometer.py reproduces primary_beam_slim and the fit figure_of_merit
Review-minutes: 1
Unattended: ready
Filed: 2026-10-21
Blocked-by: PyAutoLens claim (point-critical-curve-grid, then point-dataset-positions-panel) released

## What

Deferred step 4 of PyAutoGalaxy#654 (merged as #655). PyAutoLens reuses `ag`'s `interferometer_hdu_list_from` and `_interferometer_from`, so no source change: add one line to the `save_attributes` docstring at `autolens/interferometer/model/analysis.py:336-339` ("The primary beam, as a trailing PRIMARY_BEAM HDU, when the dataset carries one") and a beamed round-trip test mirroring `test_autolens/interferometer/model/test_analysis_interferometer.py:220` using `aa.primary_beam_gaussian_from` on the `interferometer_7` mask.
