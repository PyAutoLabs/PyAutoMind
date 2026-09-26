# Interferometer likelihood campaign: chunk TransformerNUFFT.transform_mapping_matrix over columns and visibilities

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- interferometer
- mge
- jax-gpu
- vram
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: draft
Consequence: glance
Witness: `jax.jit(FitInterferometer)` of the dense MGE-20 cell on the RAL A100 completes at alma (1M vis) instead of RESOURCE_EXHAUSTED (library_path.status == "ok" in `results/breakdown/interferometer/mge_hpc_a100_fp64.json`), with log_likelihood within 1e-6 nats of the laptop CPU value.
Review-minutes: 8
Epic: interferometer-likelihood-campaign

Source: `autolens_profiling/results/notes/interferometer_mge_breakdown_2026_09.md`, lever 2
(autolens_profiling#308).

## Why

`TransformerNUFFT.transform_mapping_matrix` (`autoarray/operators/transformer.py:505`) is
one `nufft2d2` over every column and every visibility and ignores `chunk_size`. On the A100
a single `jax.jit(FitInterferometer)` for MGE-20 asks for 65.9 GB at alma, 322 GB at
alma_high and 1.61 TB at jvla (recorded `library_path.requested_bytes`). On CPU the same
transform fits under XLA fusion. The #308 cell's measurement-only chunked arm (4 columns
per batch, 1M-visibility chunks) runs every instrument: step 3 0.915 s alma, 3.75 s
alma_high, 23.17 s jvla.

## What

- Honour `chunk_size` (visibilities) and add a column batch in the JAX branch of
  `transform_mapping_matrix`, via `lax.map`/`lax.scan` so the memory peak is
  O(column_batch * vis_chunk * kernel width).
- Keep the one-call path where it fits (CPU, sma) — measure before changing the default.
- Applies to every dense interferometer inversion (MGE-only until the W~ route lands,
  mixed mapper + MGE, pixelized dense), not only MGE.

## Watch

- Lever 1 (W~ route) is faster at every instrument for MGE-only fits; this lever is for
  the dense paths lever 1 does not cover.
- Combine with the real-scatter fix (`interferometer_transform_mapping_matrix_real_scatter`);
  chunking repeats the scatter per batch.

<!-- filed from autolens_profiling#308 phase C (PR #312), 2026-09-26 -->
