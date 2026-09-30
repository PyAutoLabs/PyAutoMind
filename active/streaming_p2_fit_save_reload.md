# Streaming phase 2: pixelization-only fits, save_attributes and aggregator reload on array-free datasets

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
Themes:
- interferometer
- sparse-operator
- memory
Autonomy: supervised
Priority: medium
Status: active
Issued: 2026-09-30
Epic: streaming-visibilities
Phase: 2
Difficulty: medium
Consequence: judge
Witness: a pixelization-only `ag.FitInterferometer` and `al.FitInterferometer` on an `aa.Interferometer.from_stream` dataset evaluate `figure_of_merit` (numpy and `jax.jit`) equal to the in-memory sparse fit at rel 1e-8; an `AnalysisInterferometer` run on it completes, `save_attributes` writes `dataset.fits` with `SparseTerms` FITS extensions (EXTNAME lookup) instead of visibilities, and the aggregator rebuilds the dataset via `from_sparse_terms` with the sparse operator re-attached so the reloaded fit's log_evidence equals the original at 1e-8.
Review-minutes: 8
Unattended: ready
Parent: draft/feature/autoarray/interferometer_from_stream_array_free_dataset.md

Source: https://github.com/orgs/PyAutoLabs/discussions/13 phase 2, sliced 2026-09-30 (decisions (b), (d)).

## What
1. `profile_visibilities` (ag + al) must not form `Visibilities.zeros(N_vis)` when `transformer is None`; `galaxies_to_inversion` /
   `tracer_to_inversion` accept a missing transformer (`GalaxiesToInversion.transformer` already tolerates it).
2. `save_attributes` (ag `interferometer/model/analysis.py` ~L216-276; al ~L320-380): when the dataset has no arrays, write
   EXTNAMEs `MASK`, `NUFFT_PRECISION_OPERATOR`, `DIRTY_IMAGE`, `DIRTY_BEAM` and header scalars `SUM_W`, `DATA_TERM`,
   `NOISE_NORM`, `N_VIS`, `EPS`, `TRANSFORMER_CLASS`; keep the visibility layout (now also EXTNAME-tagged) when arrays exist.
3. `autogalaxy/aggregator/interferometer/interferometer.py` `_interferometer_from` (autolens imports it): switch from positional
   HDUs to EXTNAME lookup; rebuild via `from_sparse_terms` when the terms extensions are present.
4. Tests in `test_autogalaxy/interferometer` (+ model/analysis save/reload round-trip, which has no test today) and the autolens mirrors.
