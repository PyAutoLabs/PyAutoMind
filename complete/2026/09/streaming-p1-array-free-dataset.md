## streaming-p1-array-free-dataset
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/592
- completed: 2026-09-30
- epic: streaming-visibilities (phase 1 of 5)
- source: https://github.com/orgs/PyAutoLabs/discussions/13
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/593

### What shipped
- **PyAutoArray#593** (merge bd03e09e) — the array-free interferometer dataset: `Interferometer.from_stream(chunks, real_space_mask, ...)` and `from_sparse_terms(terms, real_space_mask)` build a dataset whose `data`, `noise_map`, `uv_wavelengths` and `transformer` are all `None`, carrying `sparse_terms` and the sparse operator with its cached scalars; `is_array_free`; `SparseTerms` provenance (`shape_native`, `pixel_scales`, `origin`, `eps`, `transformer_class_name`) with mismatch refusal in `__add__` and in `from_sparse_terms`, and recorded-value merge when one operand is unrecorded; `AbstractInversionInterferometer.mask` read from the dataset (the one transformer read on the sparse likelihood path); typed `exc.DatasetException` / `exc.InversionException` from every array- or transformer-dependent property; `dirty_image_natural` and `dirty_beam` on both dataset kinds (in-memory `dirty_image` unchanged). `test_autoarray` 1783 passed; sibling interferometer suites unchanged (43 / 29).
- Parity: sparse inversion on the array-free dataset vs in-memory `apply_sparse_operator` at rel 1e-8 (numpy + jax); 5e5-vis witness log_evidence rel 1.5e-16.
- Memory witness (fresh process per N, NUFFT, 400×400 mask = 125k pixels, 4096-vis chunks): peak RSS 821 / 776 / 831 / 929 MB at 5e5 / 1e6 / 2e6 / 4e6 vis (import baseline 171 MB, one-chunk 536 MB) — flat in N_vis, set by the image size; the held arrays would add 24→192 MB (+ the transformer's copy). Not the discussion's 36 MB, which is pyuvimage's own accumulator over its own baseline.

### Review and override
- Codex gpt-6-astra review before PR-open: 4 findings — #1 geometry guard in `from_sparse_terms`, #2 `origin` in `__add__`, #3 provenance merge, all fixed in-branch with red-checked tests; #4 (`AnalysisInterferometer.save_attributes` / aggregator cannot handle an array-free dataset) is phase 2 by design. Record: https://github.com/PyAutoLabs/PyAutoArray/pull/593#issuecomment-5913414871.
- Shipped under the human-authorized Heart RED development override (`release validation FAILED (stage integrate)`, unrelated); recorded on the issue, PR body, `active.md` and `autonomy_log.md` (row `red-override`). Merged on a separate human `/prm` with all legs green.

### Deferred (noted on the epic ledger)
- Mild +100 MB drift at 4e6 vis and super-linear witness wall time (2× N ≈ 3× time above 1e6; likely the witness's per-chunk npz reads) — look at in phase 2.
- Analysis lifecycle (save/reload) → phase 2 `draft/feature/autogalaxy/streaming_p2_fit_save_reload.md`; visualizer → phase 3; non-linear light profiles → phase 4; cubes/phase centre → phase 5.

### Notes
- Bundle `activate.sh` is a symlink to the root file that other sessions rewrite; this task used a private `env_private.sh`.

## Original prompt

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
