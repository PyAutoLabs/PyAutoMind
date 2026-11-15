# Heart: one runner-speed factor inflates compile-bound JAX unit tests

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Filed: 2026-11-15
Consequence: judge
Review-minutes: 15
Unattended: never
Lane: any

Remainder of `complete/2026/11/unit-timing-monitoring-min-delta.md` (point 2; the human ruled option A for point 1, shipped PyAutoHeart#349).

`heart/checks/unit_timings.aggregate` divides every test's seconds by one `run_speed_factor` — the median seconds/baseline ratio over a leg's slowest-25 shared tests. On a fast runner (2026-11-15 PyAutoArray 3.13 leg: factor 0.753) the numpy/numba tests speed up but compile-bound JAX tests (`test_coordinate_jax.py::test__step0_route…`, `test_matrix_free_util`, `test_kmeans`) do not, so their normalised time reads 1.5–1.8× while their raw CI seconds sit inside their historical bimodal range (step0 nopad 7.5–9.2 s or 11.1–15.4 s, 2026-10-29 → 11-15, `timings/unit/PyAutoArray.jsonl`).

Since #349 these rows are green (under `slow_factor` 2.0), so this is no longer a monitoring finding; it matters only if a real 2× JAX slowdown could be masked or a fast runner could push one over 2×.

Options: per-family factor (jax-heavy vs not, e.g. by `jax` in the nodeid or a marker); or skip normalisation when the factor's spread across the slowest-25 is wide; or leave as is. Human ruling needed (scoring change).

<!-- filed 2026-11-15 by the health-review session (claude.ai/code/session_016nhQ8RkwYK9RzapmsQRGCj) -->
