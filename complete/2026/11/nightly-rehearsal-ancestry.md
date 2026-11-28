The scheduled-nightly release driver (`agents/conductors/release/nightly.sh`, step 4c) now runs PyAutoHeart's `heart.checks.rehearsal_ancestry` after the validation ingest and before `state.aggregate()`, non-fatal like `ci_status`. Before this, any library `main` that moved during the ~1h validation window read as "ancestry unproven" and the release-ci gate returned STALE, which blocked the nightly on 2026-11-23, 24 and 25 (anchor stuck at 2026-11-22T09:26:59Z) despite M2.4 (PyAutoHands#337).

Verified: `bash -n`; new `test_nightly_proves_rehearsal_ancestry_before_aggregate` passes on the branch and fails on old main; full Brain suite 2506 passed / 1 skipped; Heart's module run on a fixture `HEART_STATE_DIR` with the 2026-11-25 pattern proved PyAutoFit (ahead 3) and PyAutoLens (ahead 8) as ancestors. PR CI green (pytest 3.12, 3.13).

Not yet proven live: the first scheduled nightly with mid-window merges should report `ahead_by` instead of "ancestry unproven".

## Original prompt

# Nightly release driver never runs Heart's rehearsal-ancestry check

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Consequence: judge
Priority: high
Status: draft
Filed: 2026-11-25
Issued: 2026-11-25
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/721
Lane: any

Bug fix in PyAutoBrain: the scheduled-nightly release driver
(`agents/conductors/release/nightly.sh`, step 4c "ingest + assemble the CI readiness
snapshot", lines ~403-420) never runs PyAutoHeart's `heart.checks.rehearsal_ancestry`
check before `state.aggregate()`. So whenever a library `main` moves during the ~1h
validation window, Heart's release-ci gate reports STALE "release validation stale:
source moved since rehearsal (...; ancestry unproven)" and the nightly stops, even though
M2.4 (PyAutoHands#337) says a forward-moved `main` stays fresh when ancestry is proven.

Evidence: nightly runs 45155720996 (11-23), 45390127904 (11-24), 45599731441 (11-25) on
PyAutoLabs/PyAutoBrain all stopped STALE this way; `NIGHTLY_LAST_WINDOW_END` stuck at
2026-11-22T09:26:59Z. `heart/tick.sh:59` already runs
`python3 -m heart.checks.rehearsal_ancestry`.

Fix: run the ancestry check in step 4c after ci_status/ingest and before aggregate
(non-fatal on failure, like ci_status), plus a test. Human approved routing this through
start_dev on 2026-11-25.
