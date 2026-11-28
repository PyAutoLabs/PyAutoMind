Merged PyAutoBrain#740 (human /prm, 2026-11-27). Phase 14.5 of the maintenance orchestrator.

`batch maintain` gains two sources, both on by default.

**Hygiene** (from the 14.0 ledger, live on Pages):
- **Keys:** the ledger's own keys.
- **Gating:** per mode (`hygiene:<mode>`). A partial, unkeyed, not_scanned, absent-repo or missing mode is never filed or cleared.
- **Unread ledger:** unpublished, unreadable or over 48 h gives exit 3.
- **Tiers:** glance for refs, docstrings and escapes, with a file-surface rule (escapes stay glance only for docstrings and comments); judge for optdeps and extras.

**Timing** (Heart-flagged rows only):
- **Keys:** `timing:gate|script|unit:…`, always judge, with "investigate, speed up or re-baseline" text.
- **Failures:** a failing or timed-out smoke script becomes a separate judge `smoke:<repo>:<entry>` key; failing gates are dropped (`ci_status` files them).
- **Dedupe:** release timing lines are deduped into the timing keys.

Live dry-run, twice, with identical keys: 41 findings (census 20 judge; hygiene 13 glance; monitoring 2 glance and 3 judge; timing 3 judge). Full suite 2803 passed. Independent Opus review over 2 rounds: one major (failures filed as slowdowns) fixed; the last round CLEAN. Heart dev-ship GREEN.

**Follow-ups** (minor, from the review):
- `smoke:`/`no_run:` duplicate prompts for a script that is both parked and failing.
- A failing gate seen only in timing events is dropped without trace.
- An escapes scanner flag for docstring-only files.

## Original prompt

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
