## Outcome
Heart Tests on main failed from 2026-11-26 because two `smoke_sha_gate` `main()` tests used a fixed previous full-sweep time (2026-11-18) while `main()` reads the real clock; past 7 days the gate (correctly) forced a sweep. The tests now use a full-sweep time one day before the real clock (`_recent_full_sweep_ts()` in `tests/test_smoke_sha_gate.py`). Test-only; the gate and `FULL_SWEEP_MAX_AGE_DAYS` are unchanged.

- PR: PyAutoLabs/PyAutoHeart#375 (merged a8ac38b, 2026-11-26), issue PyAutoHeart#374.
- Evidence: full Heart suite 1523 passed / 0 failed; sha-gate tests pass under +30 and +365-day shifted clocks (control: main's version fails the same 2 under +30).
- Shipped under AUTONOMY.md "Corrective-PR exception for Heart RED" for reason "PyAutoHeart: Heart Tests failure on main" (authorization: PyAutoHeart#374 comment 7191236646).
- Unblocks PyAutoLabs/PyAutoHeart#373 (arcticpy-27-git-source).

## Original prompt

# Heart: smoke_sha_gate main() tests fail as the real clock passes their fixed dates

Type: bug
Target: PyAutoHeart
Repos:
- @PyAutoHeart
Themes:
- ci
- tests
Difficulty: small
Autonomy: human-required
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 5
Unattended: never
Lane: any
Issued: 2026-11-26
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/374

## Request (human, 2026-11-26, verbatim)

> Do this task here: "Fix date drift in Heart smoke_sha_gate tests"

## Diagnosis (2026-11-26)

Heart Tests on main fail since 2026-11-26 (last green 2026-11-24, run 45364461481):
- `tests/test_smoke_sha_gate.py::test_main_writes_record_outputs_and_summary`
- `tests/test_smoke_sha_gate.py::test_main_reads_force_and_the_latest_run_from_the_environment[env2-no main moved since run 100]`

`.github/scripts/smoke_sha_gate.py` `main()` passes `datetime.now(utc)` to the gate, which forces a
full sweep when the last one is `>= FULL_SWEEP_MAX_AGE_DAYS` (7) days old. Both tests build the
previous record with `_previous()`'s default `full_ts="2026-11-18T03:00:00Z"`, which became 7 days
old on 2026-11-25, so `main()` now reports "...a full sweep runs at least every 7 days" instead of
"no main moved since run 100". The pure-function tests use a fixed `NOW` and are unaffected.

This is the Heart RED reason "PyAutoHeart: Heart Tests failure on main", which blocks merging
PyAutoLabs/PyAutoHeart#373 (arcticpy 2.7 stopgap, issue PyAutoHeart#372).

## Scope

Test-only: give the two `main()` tests a previous full-sweep timestamp relative to the real clock
(e.g. one day ago), so they keep exercising the "no main moved" path on any date. Do not change the
gate or loosen `FULL_SWEEP_MAX_AGE_DAYS`.
