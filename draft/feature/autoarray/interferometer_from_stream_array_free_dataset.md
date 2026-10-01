# Array-free streamed interferometer dataset (streaming visibilities, phase 2)

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
Themes:
- interferometer
- sparse-operator
- memory
Difficulty: large
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Witness: an `Interferometer.from_stream(chunks, real_space_mask, ...)` dataset with `data`, `noise_map` and `uv_wavelengths` all `None` and no transformer runs a pixelization-only `ag.FitInterferometer` under `AnalysisInterferometer` end to end (log_likelihood, `jax.jit`, result save + aggregator reload, visualizer output) with log_evidence equal to the in-memory `apply_sparse_operator` fit at rel 1e-8, and peak RSS independent of N_vis (flat across 5e5..4e6 visibilities, ~36 MB over baseline as in the discussion's table).
Review-minutes: 15
Unattended: needs-slicing
Epic: streaming-visibilities
Ledger: true
Parent: complete/2026/09/interferometer-streaming-visibilities.md

Source: GitHub Discussion https://github.com/orgs/PyAutoLabs/discussions/13 (HRSAstro,
"Streaming visibilities for memory efficiency"); phase 1 = PyAutoArray#588 (PRs on
PyAutoArray + PyAutoGalaxy, branch `feature/interferometer-streaming-visibilities`).
Reference: https://github.com/HRSAstro/pyuvimage `src/pyuvimage/streaming.py`.

## Why

The discussion's memory table: the sparse path keeps 48 B/visibility resident (data 16 B,
noise_map 16 B, uv_wavelengths 16 B) — ~10 GB at 2e8 visibilities, the difference between
a laptop and a node for an ALMA MFS cube. pyuvimage's streamed accumulation stays flat at
36 MB over baseline from 5e5 to 4e6 visibilities.

Phase 1 shipped the sums and their consumers: `aa.SparseTerms`,
`sparse_terms_from_chunks(chunks, *, real_space_mask, transformer_class, method, eps,
chunk_size, chunk_k, use_jax, show_progress)`, `InterferometerSparseOperator.data_term /
.noise_normalization / .from_sparse_terms`, `Interferometer.apply_sparse_operator_from_chunks`,
`DatasetInterface(data=None)`, `fast_chi_squared` / `noise_normalization` reading the
scalars, and in autogalaxy `uses_precomputed_data_term_from`,
`FitInterferometer.inversion_with_data` and the visualizer switch. The likelihood no longer
touches visibilities — but the process still holds them, because:

- `Interferometer.__init__` always builds a `TransformerNUFFT` from `uv_wavelengths`
  (`autoarray/dataset/interferometer/dataset.py` ~L120), itself ~48 B/vis, and
  `apply_sparse_operator_from_chunks` still retains the arrays.
- `AnalysisInterferometer.save_attributes`
  (`autogalaxy/interferometer/model/analysis.py` ~L216-280) writes data / noise_map /
  uv_wavelengths to `dataset.fits`; the aggregator reload reads uv back
  (`autogalaxy/aggregator/interferometer/interferometer.py` ~L73-82).
- Dataset and fit subplots need `uv_distances`, `amplitudes`, `dirty_image`
  (unweighted), `dirty_noise_map`; `mapped_reconstructed_operated_data_dict` and
  `model_data` need `transformer.visibilities_from`.
- Light-profile fits still form `profile_visibilities` over N_vis.

pyuvimage works around all of this with `stub_dataset_from_terms`, a fake `Interferometer`
with 8 zero visibilities and a `TransformerDFT`. The upstream design should not need a stub.

## Phases (ledger — issued ONE at a time as each predecessor merges)

| Phase | Member prompt | Repos | Status |
|---|---|---|---|
| 1 | complete/2026/09/streaming-p1-array-free-dataset.md | PyAutoArray | SHIPPED 2026-09-30 — PyAutoArray#593 (merge bd03e09e), pending release |
| 2 | complete/2026/09/streaming-p2-fit-save-reload.md | PyAutoGalaxy, PyAutoLens | SHIPPED 2026-09-30 — PyAutoGalaxy#639 (4c834ced) + PyAutoLens#758 (efd13c4c), pending release |
| 3 | complete/2026/09/streaming-p3-visualizer.md | PyAutoArray, PyAutoGalaxy, PyAutoLens | SHIPPED 2026-09-30 — PyAutoArray#597 (c1d85810) + PyAutoGalaxy#640 (6d522ce4) + PyAutoLens#761 (a2fbe881), pending release |
| 4 | complete/2026/10/streaming-p4-light-profile-identity.md | PyAutoArray, PyAutoGalaxy, PyAutoLens | SHIPPED 2026-10-01 — PyAutoArray#599 (176f61e7) + PyAutoGalaxy#642 (574743ab) + PyAutoLens#762 (bcf2ab6f), pending release |
| 5 | `active/streaming_p5_cubes_phase_centre.md` | PyAutoArray, PyAutoGalaxy, autolens_workspace | SHIPPED 2026-10-01 — PyAutoArray#601 + PyAutoGalaxy#643 + autolens_workspace#582 (issue #600), awaiting merge |

Deferred from phase 1: mild +100 MB RSS drift at 4e6 vis and super-linear witness wall time (likely per-chunk npz reads) — look at in phase 2.

Deferred from phase 2: no public switch to disable `visualize_before_fit` (the witness used `search._visualize_before_fit = False`; `PYAUTO_TEST_MODE=1` does not skip it) — add one in phase 3; the database-path `save_fits` gap is filed as `draft/bug/autogalaxy/database_paths_dataset_fits_not_registered.md`.

Deferred from phase 4: `galaxy_image_dict` dict-merge drops a mixed ordinary+linear galaxy's ordinary light (pre-existing; `draft/bug/autogalaxy/galaxy_image_dict_mixed_galaxy_overwrites_ordinary_light.md`); in-memory sparse fits with ordinary light could also take the identity (would relax exact-equality tests).

Deferred from phase 3: a public switch to skip `visualize_before_fit` only (before-fit-only visualization) → a PyAutoFit draft; the accumulator's per-chunk JAX recompile → the profiling campaign (`draft/research/autolens_profiling/interferometer_streaming_scaling.md`).

Design decisions taken with the phase plan (2026-09-30, human-approved): (a) array-free datasets carry
`transformer=None` (no stub class); `AbstractInversionInterferometer.mask` reads the dataset mask;
consumers gate and raise a typed `DatasetException`. (b) `SparseTerms` persists as FITS extensions in
`dataset.fits` (EXTNAME lookup), never npz. (c) in-memory `dirty_image` (unweighted adjoint) is unchanged;
new `dirty_image_natural` / `dirty_beam` on both paths; array-free plots use them, labelled. (d) reload
re-attaches the operator for array-free datasets; the in-memory sparse reload gap is
`draft/bug/autogalaxy/aggregator_reload_drops_sparse_operator.md`. (e) `SparseTerms` carries provenance
(mask shape/pixel_scales/origin, eps, transformer class). Public commitment: the reply on Discussion #13
promises a follow-up post when this lands.

## Go/no-go benchmark (2026-09-30, laptop CPU, 15 GB RAM, 10 GB address-space cap per run)

400-px circular mask at 0.05"/pix (125,676 pixels), TransformerNUFFT, synthetic visibilities generated per chunk in memory (no disk). Scratchpad `bench_stream.py`; to be ported as the `interferometer_streaming_scaling` campaign in autolens_profiling.

| N_vis | path | chunk | peak RSS | wall | s per 1e6 vis | outcome |
|---|---|---|---|---|---|---|
| 1e5 | in-memory `apply_sparse_operator` | — | 2068 MB | 6.9 s | 69 | OK |
| 1e6 | in-memory `apply_sparse_operator` | — | 6611 MB | 9.0 s | — | **OOM** (3.1 GB allocation in `nufft_precision_operator_via_nufft_from` L615) |
| 4e6 | in-memory (parity run) | — | 4385 MB | — | — | **OOM** (6.3 GB allocation) |
| 1e5 | stream | 4096 | 850 MB | 16.7 s | 167 | OK |
| 1e6 | stream | 4096 | 872 MB | 77.7 s | 78 | OK |
| 4e6 | stream | 4096 | 884 MB | 178 s | 45 | OK |
| 1.6e7 | stream | 4096 | 990 MB | 647 s | 40 | OK |
| 1e6 | stream | 65536 | 1498 MB | 15.8 s | 16 | OK |
| 4e6 | stream | 65536 | 1509 MB | 52.2 s | 13 | OK |
| 1.6e7 | stream | 65536 | 1493 MB | 174 s | 11 | OK |
| 5e7 | stream | 65536 | 1755 MB | 539 s | 11 | OK |

- The in-memory sparse path **cannot build the operator above ~1e6 visibilities on a 16 GB laptop**: its one-shot NUFFT precision build allocates ~3 kB per visibility of temporaries (3.1 GB at 1e6, 6.3 GB at 4e6). Streaming is flat at 1.5–1.8 GB to 5e7 and linear in time.
- Chunk size is the lever: 65536 is 5× faster than 4096 (per-chunk fixed cost — one chunk profiles at ~0.57 s: 46 % nufft spread, ~4 s of JAX recompiles across 40 chunks (73 compiles → likely a recompile per chunk), ~5 s device→host `np.asarray`). Room for a further 2–3× if the recompile is removed.
- **2e8 extrapolation:** streaming ≈ 11 s/1e6 → ~37 min on this laptop CPU at chunk 65536, ~1.8 GB RSS; in-memory ≈ 600 GB of temporaries — impossible on any node.
- Parity: established earlier at 5e5 (log_evidence rel 1.5e-16) and 4e6 in the phase-1 tests; the 4e6 parity child here OOMed on the *in-memory* side, not the streamed one.
- **Verdict: GO.** The array-free dataset is the only route to sparse fits above ~1e6 visibilities on a laptop, not just to 2e8. Phases 3–5 proceed; the campaign prompt `draft/research/autolens_profiling/interferometer_streaming_scaling.md` versions this evidence.

## What (original scope, now sliced above)

1. **Constructor.** `Interferometer.from_stream(chunks, real_space_mask, ...)` and/or
   `Interferometer.from_sparse_terms(terms, real_space_mask)` with optional
   `data` / `noise_map` / `uv_wavelengths` and a transformer-less mode — either
   `transformer=None` with every consumer guarded, or a `StreamedTransformer` that
   exposes only the W~ FFT-multiply (`operated_matrix_slim_from`) and raises clearly on
   `visibilities_from`. Decide which in the plan (API call — judge).
2. **Save/load contract.** Persist `SparseTerms` (npz or fits: W~ kernel, dirty image,
   dirty beam, sum w, data_term, noise_normalization, mask) instead of visibilities;
   `save_attributes` writes it when arrays are absent and the aggregator rebuilds the
   dataset from it. Keep the visibility path unchanged when arrays are present.
3. **Visualizer.** Dirty images from terms (`dirty_beam_native` normalises); residual
   dirty image = dirty(data) − W~·(M s) via `operated_matrix_slim_from`; skip uv-plane
   panels (amplitudes, uv_distances, dirty_noise_map) when arrays are absent rather than
   raising.
4. **Light-profile identity** so light-profile fits also run array-free:
   Σ|d−p|²/σ² = data_term − 2 i_pᵀ d~ + i_pᵀ W~ i_p with p = F i_p. This is the same
   substitution `sparse_dirty_image_from` already applies to the data vector; extend it
   to chi_squared and the linear-light-profile blocks so `profile_visibilities` is never
   formed.
5. **Per-channel cubes.** MFS terms are the sum of channel terms (`SparseTerms.__add__`);
   phase-centre shifts applied chunk by chunk. Test sum-of-channels == MFS to 1e-12.
6. **PyAutoLens parity.** Same `save_attributes` / aggregator / visualizer changes in
   `autolens/interferometer/model/` and `autolens/aggregator/`; builds on the PyAutoLens
   phase-1 parity, now merged (PyAutoLens#757) —
   `complete/2026/09/interferometer-sparse-precomputed-data-term.md`.

Slicing suggestion: (1)+(2) PyAutoArray/PyAutoGalaxy; (3); (4); (5); (6). Measure RSS with
a fresh process per N_vis (as the discussion did), not in-process deltas.

## Reply to the discussion

After phase 2 ships, answer HRSAstro on Discussion #13 via `/community` (human-approved
reply): what landed in phase 1 and 2, the `from_stream` API, the parity and RSS witness,
and that `stub_dataset_from_terms` is no longer needed.
