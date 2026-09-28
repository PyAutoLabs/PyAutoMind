# Runtime cells' A100 `single_jit` includes the post-compile warm-up — source-plane 0.642 ms vs a steady 0.267 ms on the same node

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
Status: formalised
Consequence: judge
Witness: On `euclid-ral-gpu-2` the release-sweep runtime cells' `full_pipeline_single_jit` for the A100 row agrees with a steady-state median of individually timed calls (≥ 5 warm calls, ≥ 200 timed) to within the median's p10–p90 band — first for `point_source_source/source_plane_solved` (steady 0.267 ms, job 366914), then for each imaging cell the check covers; or, if the decision is to keep the statistic, the dashboard labels the A100 `single_jit` as "first block after compile" and headlines `vmap.per_call` instead.
Review-minutes: 10
Unattended: needs-decision
Epic: point-source-cpu-speed
Filed: 2026-09-28
Updated: 2026-09-28

## Finding

autolens_profiling#349 (2026-09-28) re-ran `scripts/point_source_source/likelihood_runtime/source_plane_solved.py`
on the release-sweep reference node at 2026.9.27.2. The A100 row (job 366912, load 1.16, cache fresh)
recorded `full_pipeline_single_jit` = **0.642 ms**. A same-node diagnostic (job 366914) built the
identical analysis, warmed the AOT `Compiled` executable with 5 calls, then measured:

- the cell's own statistic (mean of 10 consecutive `block_until_ready` calls), 40 times: median
  **0.272 ms** (p10 0.250, p90 0.285);
- 400 individually timed calls: median **0.267 ms** (p10 0.260, p90 0.279);
- scalar `jit(x + 1)` floor 0.132 ms.

So the committed 0.642 ms is the cell's single 10-call block landing in the post-compile transient
(`jit_profile`: one `first_call`, then `steady_x10`), not the likelihood. The RAL CPU row (job 366911)
agrees with earlier medians, so this looks GPU-specific. Logs:
`results/logs/point_source_source/point_source_source_plane_2026_09_28_ral_job_{366912,366914_timing_diag}.out`;
ledger `results/notes/point_source_source_plane_campaign.md` "Runtime refresh on 2026.9.27.2".

## Reach (noted, not measured)

The four imaging release-sweep cells (`scripts/imaging/likelihood_runtime/{mge,pixelization,delaunay,delaunay_nn}.py`)
use the same `jit_profile` (one warm call, mean of 10). Their calls are ms-scale, so a sub-ms
transient matters less in relative terms, but nobody has measured it. The run-time dashboard plots
`single_jit` as the per-call headline for every release-sweep series.

## Decision needed

Changing the statistic (more warm calls, median of N) breaks comparability with every committed row
and the dashboard trend; keeping it means the A100 `single_jit` of light cells is not a trend
quantity. Options: (a) add warm calls + a median field beside the existing one (new field, old one
kept for continuity); (b) keep it and have the dashboard headline `vmap.per_call` on GPU; (c) re-base
all release-sweep cells at the next release.

## Related

Source checkouts report `autolens_version` 2026.8.17.1 at the 2026.9.27.2 tag (build-time stamp),
and 322 committed HPC JSONs carry it. The dashboard versions points by that field, so source-checkout
rows do not separate by release. This is the same release-sweep premise, and it may deserve its own prompt.
