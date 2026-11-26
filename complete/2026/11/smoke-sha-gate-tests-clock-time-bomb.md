## Outcome
Retired by /prm close-out of smoke-sha-gate-date-drift: same bug, filed in parallel by another session on 2026-11-26. PyAutoLabs/PyAutoHeart#375 (merged a8ac38b) makes the two `main()` tests use a full-sweep time one day before the real clock — the second option this prompt offered. Witness met: Heart Tests green on main at a8ac38b (run 45815158876). Record: complete/2026/11/smoke-sha-gate-date-drift.md.

## Original prompt

# Heart Tests red since 2026-11-25: smoke_sha_gate main() tests read the real clock

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: easy
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Filed: 2026-11-26

## Finding

Heart Tests has failed on every run since 2026-11-25 (main 72df0d455 and 6db363450, and PR branch feature/arcticpy-27-git-source). The last green run was 2026-11-24. Two tests in `tests/test_smoke_sha_gate.py` fail:
- `test_main_writes_record_outputs_and_summary` (:163, `swept` is True)
- `test_main_reads_force_and_the_latest_run_from_the_environment` (:188, reason is "no main moved, but the last full sweep ... a full sweep runs at least every 7 days")

The `_previous()` fixture hardcodes `full_sweep_created_at="2026-11-18T03:00:00Z"`. The `decide()` tests pass a fixed `NOW`, but `gate.main()` uses the real clock. Since 2026-11-25T03:00Z the fixture is more than `FULL_SWEEP_MAX_AGE_DAYS = 7` old, so main() correctly chooses a full sweep. This is a test-only time bomb; the gate itself is fine.

## Ask

Pin the clock in the two `main()` tests (monkeypatch the gate's now source to the module's `NOW`, or make `_previous()` default `full_ts` relative to it). Do not change `FULL_SWEEP_MAX_AGE_DAYS`.

Witness: Heart Tests is green on main.
