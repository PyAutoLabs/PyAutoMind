# autolens_profiling: drop the D12 eigen flag from CPU campaign legs (deferred)

Type: maintenance
Target: autolens_profiling
Repos: @autolens_profiling @PyAutoPulse
Difficulty: easy
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Filed: 2026-11-12
Blocked-by: delaunay-nn-numba-remeasure, gradient-correctness-sweep (autolens_profiling claims)
Lane: any

Phase 2 of PyAutoHeart#335 (record complete/2026/11/eigen-flag-removal.md), deferred by
the human on 2026-11-12 until those tasks release autolens_profiling, so a timing
remeasure is not broken mid-campaign.

Remove `XLA_CPU_WORKAROUND_FLAG` (`--xla_cpu_multi_thread_eigen=false`, decision D12,
human 2026-10-29) from `scripts/misc/campaigns/_common.py` and its preamble, and update
`scripts/misc/campaigns/test/test_xla_cpu_workaround.py`. KEEP the research arm in
`scripts/misc/jax_version_policy/run_matrix.py`. New timing rows are then not like-for-like
with D12 rows: record the break in Pulse (a row field or note "no eigen flag"), and say in
the campaign docs which rows predate it.
