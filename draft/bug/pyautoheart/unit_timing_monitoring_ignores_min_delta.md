# Heart: the unit-test timing monitoring summary flags noise its own row policy calls ok

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-15
Consequence: judge
Witness: with the 2026-11-15 board's unit-timing rows, the monitoring `unit_test_timing:*` findings agree with each row's own `state` (both-gates rule from `config/repos.yaml thresholds.unit_timings`), and a test that is 3× slower by >= `min_delta_s` still reads red
Review-minutes: 15
Unattended: never
Lane: any

## Finding (2026-11-15 health review)

Monitoring carried `unit_test_timing:coverage` RED ("1 test regressions (>3× baseline), 14 slow (>1.5×)") plus one red and eleven yellow per-test findings. Measured: **none is a code regression.**

- **PyAutoNerves `test_decorator.py::test_config`** (red, 0.015 s → 0.043 s, ratio 3.01): measured locally CI-style (full suite, `--cov`, junit `time`), 5 runs per commit: 15 ms at d3b577a (pre-#212), **5 ms** at 9b204c9 (#212 config-yaml-parse-cache) and 5 ms at main 0850c6c. The code got faster; the 43 ms CI row is one runner sample. `test_board::test_panel_routes…` (27–31 ms) and `test_fitsable::test__fits_readers…` (24–31 ms) are flat across the same commits.
- **PyAutoArray `test_coordinate_jax.py::test__step0_route…` and the other JAX yellows**: raw CI seconds in `timings/unit/PyAutoArray.jsonl` are bimodal by runner (step0 nopad: 7.5–9.2 s or 11.1–15.4 s across 2026-10-29 → 11-15); the flagged 11.94 s is inside that range. They were flagged only after normalisation by the run's median speed ratio (0.753): most of the slowest-25 ran ~25% faster that run while these compile-bound JAX tests did not, so `seconds / run_speed_factor` inflated them to 1.5–1.8×.

## Cause

`heart/checks/unit_timings.py`:
1. `legacy_summaries()` sorts rows into red/yellow by `LEGACY_RED_FACTOR` (3.0) / `LEGACY_YELLOW_FACTOR` (1.5) on `ratio` **alone**. The configured policy (`thresholds.unit_timings`: `slow_factor: 2.0`, `min_delta_s: 2`) — which each row's own `state` already applies through `classify_test_drift` — is ignored, so a 28 ms change on a 15 ms test is a "3× regression" and RED. Every one of the 2026-11-15 rows has row `state` ok.
2. The single `run_speed_factor` (median over the slowest-25 shared tests) assumes all tests scale together; compile-bound JAX tests and numba/numpy tests do not, so a fast runner manufactures JAX "slowdowns".

## Options (human ruling — this changes what monitoring scores; not done in the review)

A. Monitoring adopts each row's own `state` (both gates); the legacy 3×/1.5× tiers apply only to rows the policy already calls `warn`. Clears all 2026-11-15 findings.
B. Keep 3×/1.5× tiers but require `delta_s >= min_delta_s`. 2026-11-15: the red clears; 3 PyAutoArray step0 rows stay yellow (normalised deltas 5.6 s / 2.6 s / 2.5 s), which point (2) says are still runner artefacts.
C. B plus a per-family speed factor (or raw seconds for jax-cached legs).

Recommendation: A (one policy, already in config), then reconsider (2) separately. Do not raise factors or drop tests.

<!-- filed 2026-11-15 by the health-review session (claude.ai/code/session_016nhQ8RkwYK9RzapmsQRGCj) -->
