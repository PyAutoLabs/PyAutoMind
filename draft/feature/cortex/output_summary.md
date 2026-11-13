# Cortex output summaries — phase 2

Targets: @PyAutoBrain @PyAutoCortex
Type: feature
Filed: 2026-10-14
Lane: any

Parent request and verbatim user text: `complete/2026/11/cortex-projects-dashboard-parent.md` (parent closed 2026-11-05; phase 1 shipped in PyAutoBrain#526).

After the presentation phase, inspect supported project output metadata and define explicit read-only collection of structured summary receipts. Distinguish unique datasets with completed outputs from fit counts; report CPU core-hours and GPU device-hours independently, with timestamp, provenance, measured/estimated basis and coverage. Never equate resource requests with consumption or infer scientific acceptance. Rendering reads saved receipts without filesystem crawls or cluster calls. Validate duplicates/restarts, partial coverage, absent metadata, stale receipts and offline rendering. Final collector details depend on source inspection; await human plan approval before source changes.

Tier: undeclared — merge mode: human /prm

Approval: User approved the two-phase direction in session. Phase 1: https://github.com/PyAutoLabs/PyAutoBrain/issues/521. Preserve this approval when resuming.
