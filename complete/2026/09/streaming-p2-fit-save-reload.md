## streaming-p2-fit-save-reload
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/638
- completed: 2026-09-30
- epic: streaming-visibilities (phase 2 of 5)
- source: https://github.com/orgs/PyAutoLabs/discussions/13
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/639
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/758
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/639
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/758

### What shipped
- **PyAutoGalaxy#639** (merge 4c834ced) — `FitInterferometer.profile_visibilities` / `profile_subtracted_visibilities` / `inversion_with_data` guard the transformer-less (array-free) dataset: pixelization-only and linear-light fits run, ordinary light profiles raise a typed `DatasetException` until phase 4. New `interferometer_hdu_list_from(dataset)` (+ `SPARSE_TERMS_HEADER_KEYS`, `SPARSE_TERMS_SCALARS_ORDER`): array-free datasets persist their `SparseTerms` in `dataset.fits` as `MASK` / `NUFFT_PRECISION_OPERATOR` / `DIRTY_IMAGE` / `DIRTY_BEAM` plus a lossless float64 `SPARSE_TERMS_SCALARS` HDU (FITS header cards hold ≤20 chars and truncate exponent-form float64; readable header copies kept); in-memory datasets write the same four arrays as before, EXTNAME-tagged. `save_attributes` uses it and writes `transformer_class.json` only with a transformer. The aggregator loader reads by EXTNAME (positional fallback for legacy files) and rebuilds array-free datasets via `aa.Interferometer.from_sparse_terms` with the operator re-attached. Also fixed (pre-existing, found in review): `agg_util.mask_header_from` read `PIXSCAY` for both axes. `test_autogalaxy` 1287 passed.
- **PyAutoLens#758** (merge efd13c4c) — the same fit guards on the tracer; `save_attributes` through autogalaxy's helper; loader shared. `test_autolens` 770 passed, 1 xfailed.
- Witness (1e5 NUFFT vis streamed in 5 chunks, 616-pixel mask on 40×40, 20×20 rectangular source, `af.m.MockSearch` with `save_for_aggregator`, visualization disabled): `dataset.fits` 80,640 B vs 4.8 MB of visibilities; log_evidence in-memory / array-free / reloaded identical (rel 0.0; array-free vs in-memory 1.8e-16 ag, 1.9e-16 al; jit vs numpy 2.6e-14).

### Review and override
- Codex gpt-6-astra review: 3 findings — #1 header float64 truncation (reproduced, fixed with the scalars HDU, red-checked), #3 `PIXSCAY` for both axes (fixed, red-checked with non-square scales), #2 database-path searches never register `dataset.fits` via `save_fits` (pre-existing, filed `draft/bug/autogalaxy/database_paths_dataset_fits_not_registered.md`). Records: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/639#issuecomment-5914868659.
- Shipped under the second human-authorized Heart RED development override (`release validation FAILED (stage integrate)`, unrelated); recorded on the issue, both PR bodies, `active.md`, `autonomy_log.md` (row `red-override`). Merged Galaxy → Lens on a separate human `/prm` with all legs green.

### Deferred (epic ledger)
- Visualization on array-free datasets (`visualize_before_fit` dataset subplot needs `data`) → phase 3; non-linear light profiles → phase 4; the datacube example → phase 5. The witness disabled visualization via `search._visualize_before_fit = False` (no public flag found; `PYAUTO_TEST_MODE=1` does not skip it) — worth a public switch in phase 3.

### Notes
- Bundle `activate.sh` symlink clobbered by other sessions; task used `env_private.sh`.

## Original prompt

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
