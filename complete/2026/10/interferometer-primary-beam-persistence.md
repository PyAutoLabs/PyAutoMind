## interferometer-primary-beam-persistence
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/654
- completed: 2026-10-21
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/655 (merge e00b5e7d)
- parent: complete/2026/10/interferometer-primary-beam.md
- community: https://github.com/PyAutoLabs/.github/discussions/35 (@HRSAstro)
- summary: |
    Follow-up of PyAutoArray#644. One commit f7f6d79e on `feature/interferometer-primary-beam-persistence`
    (3 files, +343/-4): `interferometer_hdu_list_from` appends the beam as a trailing `PRIMARY_BEAM`
    HDU in both layouts (legacy positions unchanged; beamless files byte-identical); the aggregator's
    `_interferometer_from` detects it by name (`_has_hdu`) and passes `primary_beam=` into
    `from_sparse_terms` and `aa.Interferometer`. Five new round-trip tests (in-memory, array-free,
    beamless layout pinned at 4 HDUs, old outputs without the HDU, control that disabling the reload
    fails). Worktree: test_autogalaxy 1362 passed. CI: docs-build + unittest 3.12/3.13/nojax green
    on both runs; CLEAN; not frozen; glance auto-merge.
- witness: |
    MET — beamed datasets saved by AnalysisInterferometer and rebuilt by the aggregator carry an
    identical primary_beam_slim (dataset, transformer, sparse operator) and identical log_likelihood /
    log_evidence / figure_of_merit (rel 1e-10), differing from the beamless fit; beamless and legacy
    outputs load unchanged. All in CI.
- heart-ack: "YELLOW acknowledged by human 2026-10-21 — manifest drift (1 mismatch); release validation stale: source moved since rehearsal (PyAutoArray)"
- deferred: PyAutoLens docstring (autolens/interferometer/model/analysis.py:336-339) + mirror test next to test_autolens/interferometer/model/test_analysis_interferometer.py:220 — PyAutoLens claimed by point-critical-curve-grid at the time; file as a small prompt when free. Pre-existing gap (not this task): an in-memory dataset saved after apply_sparse_operator is rebuilt without the operator.

## Original prompt

# Persist the interferometer primary beam through analysis save and aggregator rebuild

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
Difficulty: small
Autonomy: safe
Priority: medium
Parent: complete/2026/10/interferometer-primary-beam.md
Status: formalised
Consequence: glance
Witness: a test asserting an Interferometer with a primary beam saved by AnalysisInterferometer and rebuilt by the aggregator carries an identical primary_beam_slim
Review-minutes: 3
Unattended: ready
Filed: 2026-10-21
Issued: 2026-10-21

## What (survey of main 2026-10-21, PyAutoArray at 034a616f incl. #644/#645)

The beam is saved nowhere today. `interferometer_hdu_list_from` (`autogalaxy/interferometer/model/analysis.py:76-218`) writes one FITS: in-memory branch HDUs MASK, DATA, NOISE_MAP, UV_WAVELENGTHS (:117-126); array-free branch MASK, NUFFT_PRECISION_OPERATOR, DIRTY_IMAGE, DIRTY_BEAM, SPARSE_TERMS_SCALARS (:129-217). `save_attributes` (:400-455) writes `image/dataset.fits` and `transformer_class`. The aggregator `_interferometer_from` (`autogalaxy/aggregator/interferometer/interferometer.py:161-235`) rebuilds via `from_sparse_terms` (:206-213) or `aa.Interferometer(...)` (:215-231); `_hdu()` falls back to legacy positional indices, so a new HDU must be detected with `_has_hdu`. PyAutoLens reuses both functions (no source change). `FitInterferometer` passes the dataset's transformer and sparse_operator to `DatasetInterface`, so passing `primary_beam=` back into the constructor is sufficient.

1. `analysis.py`: helper `_primary_beam_native_from(dataset)` → None or the float64 native array (masked pixels 0) of `primary_beam_slim` on `real_space_mask`; append it as a trailing `PRIMARY_BEAM` HDU in both branches (legacy indices 0-3 unchanged); docstrings.
2. `aggregator/interferometer/interferometer.py`: `_primary_beam_from(hdu_list)` via `_has_hdu`; pass `primary_beam=` into `from_sparse_terms` and `aa.Interferometer`; docstrings.
3. Tests in `test_autogalaxy/interferometer/model/test_analysis_interferometer.py` (extend the round-trip patterns at :148, :172-255, :258-285 with a Gaussian beam spanning ~0.3-1 on `interferometer_7`): (a) in-memory beamed round trip — PRIMARY_BEAM present, `primary_beam_slim` and `transformer.primary_beam_slim` identical, `FitInterferometer.log_likelihood` equal (rel 1e-10) for light-profile and pixelization galaxies, and different from the beamless fit; (b) array-free beamed round trip via `from_stream(primary_beam=)` — `sparse_operator.primary_beam_slim` identical, log_evidence / figure_of_merit equal; (c) beamless writes no PRIMARY_BEAM HDU, HDU count pinned at 4, reload gives `primary_beam is None`; (d) old outputs without the HDU still load with `primary_beam=None` for both layouts.
4. PyAutoLens: docstring line at `autolens/interferometer/model/analysis.py:336-339` and a mirror beamed round-trip test next to `test_autolens/interferometer/model/test_analysis_interferometer.py:220` (optional, do it).

Not in scope: the pre-existing gap that an in-memory dataset with `apply_sparse_operator` comes back without the operator (likelihood still matches via the beamed transformer); the forced-numba fallback and repeated P=0 warning (PyAutoArray side, separate small prompt if wanted).
