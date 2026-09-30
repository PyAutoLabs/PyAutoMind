# Campaign: interferometer streaming (array-free) vs in-memory — memory and time scaling to 2e8 visibilities

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- interferometer
- sparse-operator
- memory
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Consequence: glance
Witness: `scripts/interferometer/streaming_scaling/` holds the campaign cells (accumulator time scaling vs N_vis and chunk size; in-memory `apply_sparse_operator` pushed to failure under a memory cap; streaming at the failing sizes; log_evidence parity), each writing a versioned JSON row under `results/streaming_scaling/` through `_profile_cli.py`; `build_readme.py --check`, `check_results_layout.py`, `check_wiki.py` and `ruff` pass; `wiki/campaigns/interferometer_streaming.md` (from `_template.md`) records the table, the 2e8 extrapolation and the go/no-go on the streaming epic's remaining phases; the dashboard is regenerated.
Review-minutes: 5
Unattended: ready
Epic: streaming-visibilities

Source: the 2026-09-30 go/no-go question on Discussion https://github.com/orgs/PyAutoLabs/discussions/13 (HRSAstro's 2e8-sample ALMA cube). Phases 1-2 of the streaming epic are merged (PyAutoArray#593, PyAutoGalaxy#639, PyAutoLens#758). A scratchpad run of this benchmark was made in the CLI session on 2026-09-30 (`bench_stream.py`); this campaign ports it into the repo so the evidence is versioned and re-runnable per release.

## Scratchpad result to reproduce (2026-09-30)

In-memory `apply_sparse_operator` OOMs at 1e6 visibilities under a 10 GB cap (3.1 GB allocation in `nufft_precision_operator_via_nufft_from`; 2.1 GB peak already at 1e5). Streaming at chunk 65536: 16 / 52 / 174 / 539 s at 1e6 / 4e6 / 1.6e7 / 5e7 (≈11 s per 1e6 vis, linear), peak RSS 1.5–1.8 GB flat; chunk 4096 is 5× slower (per-chunk fixed cost: nufft spread 46 %, JAX recompiles ~73 across 40 chunks, device→host copies). 2e8 ⇒ ~37 min, ~1.8 GB. Verdict GO; the table is on the epic ledger.

## Why

The array-free dataset only earns its maintenance cost (a second dataset kind every interferometer code path branches on) if it makes a real difference at the visibility counts real data reach. In-house datasets are ≤1.1e5 visibilities; the discussion's case is 2e8. The decision on phases 3-5 (visualizer, non-linear light profiles, cubes) rests on measured crossover memory and on the accumulator being linear and fast enough to reach 2e8.

## What

1. Cells under `scripts/interferometer/streaming_scaling/` (dataset-first, task-second layout; use `_profile_cli.py` for JSON/CLI; synthetic seeded per-chunk visibilities generated in memory, 400-px circular mask at 0.05"/pix, `TransformerNUFFT`; each measurement in a fresh child process with a `RLIMIT_AS` cap and per-child timeout):
   - `accumulate.py` — `Interferometer.from_stream` wall time and peak RSS vs N_vis ∈ {1e6, 4e6, 1.6e7, 5e7} × chunk ∈ {4096, 65536}; seconds per 1e6 vis; linearity.
   - `in_memory.py` — `Interferometer(...).apply_sparse_operator()` peak RSS + wall at N_vis ∈ {1e6, 4e6, 1.6e7, 5e7, 1e8}; the first N that fails under the cap is a result.
   - `parity.py` — log_evidence of a 20×20 rectangular sparse inversion, streamed vs in-memory at 4e6.
2. `results/streaming_scaling/` rows + PNG (RSS and wall vs N_vis, both paths) following `check_results_layout.py`; README dashboard via `build_readme.py`; `build_dashboard.py` regenerated.
3. `wiki/campaigns/interferometer_streaming.md` from `_template.md`: table, 2e8 extrapolation (in-memory RSS ≈ 96 B/vis + temporaries vs streaming RSS; accumulation time at the best chunk), a cProfile top-10 of one chunk if any rate exceeds 5 s per 1e6 vis, and the go/no-go for the epic's phases 3-5. Link from `wiki/index.md`.
4. A100 rows (RAL) are optional follow-ups; CPU rows decide the memory question.

Parallel claims: autolens_profiling is claimed by `raw-pdip-forward-polish` (`interferometer-decision-matrix` shipped 2026-09-30, `complete/2026/09/interferometer-decision-matrix.md`); this campaign adds a new task folder and results folder only (shared files: `wiki/index.md` rows + generated README/dashboard).
