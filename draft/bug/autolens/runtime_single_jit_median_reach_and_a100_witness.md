# Runtime cells' steady single-JIT median: wire the imaging release-sweep cells and witness on the A100

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- jax
Difficulty: small
Autonomy: supervised
Priority: low
Consequence: judge
Epic: point-source-cpu-speed
Status: draft
Filed: 2026-10-04

Remainder of `complete/2026/10/runtime-single-jit-median.md` (autolens_profiling#374, merged
2026-10-04). That PR shipped option (a): `steady_median_profile`, the opt-in
`jit_profile(median_n_warm=, median_n_timed=)` and the dashboard label "first block after compile". It
wired only the source-plane witness cell, `scripts/point_source_source/likelihood_runtime/source_plane_solved.py`.
Contract: PyAutoPulse `tasks/runtime_cell_single_jit_gpu_warmup.md`.

## Remaining

1. **A100 witness, at the next release sweep** on euclid-ral-gpu-2. The source-plane cell's new
   `full_pipeline_single_jit_median_ms` should agree with job 366914's steady 0.267 ms to within its p10–p90.
   The existing `full_pipeline_single_jit` should still read the first-block value (~0.64 ms).
2. **Then wire the contract's "Reach"**, the four imaging release-sweep runtime cells. Pass
   `median_n_warm=` / `median_n_timed=` so each writes the `_median_ms` / `_p10_ms` / `_p90_ms` fields
   beside the unchanged `full_pipeline_single_jit`. Do not re-base committed rows.

Do step 2 only once step 1 confirms the median removes the post-compile transient.

## Re-scoped 2026-11-05 — what is left (draft-queue sweep)

- **Done:** Step 2 "Reach": autolens_profiling#408 (2026-10-09, record `complete/2026/10/timing-noise-audit-p6-median-headline-gpu-marker.md`) — 11 runtime cells write `_median_ms/_p10/_p90`.
- **Remaining:** Step 1 only: the A100 witness — no committed row carries a median yet (per that record).

_Evidence from the 2026-11-05 read-only sweep (Mind ledger + GitHub search); remaining items are the live scope of this prompt._
