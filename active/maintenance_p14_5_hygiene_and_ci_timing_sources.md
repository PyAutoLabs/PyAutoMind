# Phase 14.5 Maintenance sources: hygiene findings and slowed CI timings

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-27
Issued: 2026-11-27
Epic: autonomous-orchestrators
Phase: 14
Consequence: judge
Witness: `batch maintain --dry-run` lists hygiene findings (refs, escapes, docstrings) and Heart-flagged slow gates, scripts and unit tests with stable keys identical across two reads
Review-minutes: 10
Lane: local-dev
Unattended: never

Slice 14.5 of `draft/feature/pyautobrain/maintenance_orchestrator.md`. Depends on 14.1 and on 14.0 (`draft/feature/pyautobrain/brain_board_hygiene_ledger.md`, which gains per-finding keys and the scan-root fix).

## What

- **Hygiene adapter:** key `<mode>:<repo>:<file>:<reference>`. It does not use the line number, because lines drift.
- **CI-timing adapter:** only rows Heart already flags (`state: warn`, slowed), never `hygiene ci`'s raw ranking. Witness: post-merge runs below the flagged threshold, a slow witness so the tier is judge.
