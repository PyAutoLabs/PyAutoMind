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
