# Streaming phase 1: array-free Interferometer.from_stream / from_sparse_terms (PyAutoArray)

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Themes:
- interferometer
- sparse-operator
- memory
Autonomy: supervised
Priority: medium
Status: active
Issued: 2026-09-30
Epic: streaming-visibilities
Phase: 1
Difficulty: medium
Consequence: judge
Witness: `aa.Interferometer.from_stream(chunks, real_space_mask, ...)` and `from_sparse_terms(terms, real_space_mask)` return a dataset whose `data`, `noise_map`, `uv_wavelengths` and `transformer` are all `None` and which carries `sparse_terms`; an `aa` sparse inversion (rectangular mesh, numpy and jax) on it gives log_evidence equal to the in-memory `apply_sparse_operator` inversion at rel 1e-8; every array/transformer property raises a typed `DatasetException` naming `from_stream`; `SparseTerms.__add__` refuses mismatched provenance; a fresh-process RSS witness is flat from 5e5 to 4e6 visibilities (≤ ~40 MB over baseline).
Review-minutes: 8
Unattended: ready
Parent: draft/feature/autoarray/interferometer_from_stream_array_free_dataset.md

Source: https://github.com/orgs/PyAutoLabs/discussions/13 phase 2, sliced 2026-09-30 (design decisions (a), (c), (e) in the ledger).

## Why

After phase 1 the likelihood is array-free but the process is not: `Interferometer.__init__` always builds a
`TransformerNUFFT` from `uv_wavelengths` (~48 B/vis on top of the dataset's 48 B/vis), `AbstractDataset.__init__`
raises on `noise_map=None`, the DFT-limit check reads `uv_wavelengths.shape`, and `apply_sparse_operator_from_chunks`
returns a dataset that still retains every array. The one transformer read on the sparse likelihood path is
`AbstractInversionInterferometer.mask` (`transformer.real_space_mask`).

## What

1. `SparseTerms` gains optional provenance fields (`shape_native`, `pixel_scales`, `origin`, `eps`,
   `transformer_class_name`); `sparse_terms_from_chunks` fills them; `__add__` requires shape / pixel_scales / eps equal.
2. `Interferometer.__init__`: `uv_wavelengths` optional; transformer built only when uv is present (else `None`);
   DFT-limit check skipped when uv is `None`; new `sparse_terms=` kwarg stored. `AbstractDataset.__init__` guards
   `noise_map=None` (no covariance work when both arrays are `None`); `shape_slim` guarded.
3. `Interferometer.from_sparse_terms(terms, real_space_mask, *, batch_size=128)` and
   `from_stream(chunks, real_space_mask, *, transformer_class=TransformerNUFFT, method, eps, chunk_size, chunk_k,
   use_jax, show_progress, batch_size)`; `apply_sparse_operator_from_chunks` also stores the terms.
4. New `dirty_image_natural` (`dirty_image_native / sum_weights`) and `dirty_beam` on both paths. `amplitudes`, `phases`,
   `uv_distances`, `dirty_image`, `dirty_noise_map`, `signal_to_noise_map`, `psf_precision_operator_from`,
   `apply_sparse_operator` raise `exc.DatasetException` naming the array-free dataset when their input is `None`.
5. `AbstractInversionInterferometer.mask` reads the dataset mask (`real_space_mask` / `grids.lp.mask`);
   `mapped_reconstructed_operated_data_dict` raises the typed exception when `transformer is None`.
   `aa.FitInterferometer` `mask`, `transformer`, `dirty_*`, residual/chi-squared maps raise it when arrays are absent.
6. Tests in `test_autoarray/dataset/interferometer`, `inversion/interferometer`, `test_inversion_interferometer_util.py`;
   witness script (fresh process per N_vis) in the PR body. No autogalaxy/autolens change; run their suites for regression.
