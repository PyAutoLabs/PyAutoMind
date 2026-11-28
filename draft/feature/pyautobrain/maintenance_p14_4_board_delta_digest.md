# Phase 14.4 Board-delta digest for maintenance shifts

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-27
Epic: autonomous-orchestrators
Phase: 14
Consequence: judge
Witness: a live maintenance shift whose digest `## Board deltas` section (findings cleared or new, census entries removed, hygiene count change; CI minutes the next day from Heart `timings/gates.jsonl`) agrees with the Heart and Brain boards read after it
Review-minutes: 10
Lane: local-dev
Unattended: never
Blocked-by: PyAutoBrain#574

Slice 14.4 of `draft/feature/pyautobrain/maintenance_orchestrator.md`. Depends on 14.3. The witness needs a live maintenance shift, so it follows the M3 gate.

## What

- **Before:** at `brief --new`, a snapshot of the monitoring keys, census rows, hygiene counts and gate p50s goes into the slot.
- **After:** at `batch collect` and the late window, an after-read builds the deltas.
- **Constraint:** the tick never reads Heart.
- **CI minutes:** lag, because gates need runs. They are reported from the committed daily timings.
