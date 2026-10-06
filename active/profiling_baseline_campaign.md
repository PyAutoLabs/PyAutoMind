# Profiling baseline campaign

Type: feature
Target: pyautopulse
Repos: PyAutoPulse
Difficulty: medium
Consequence: judge
Autonomy: human-required
Priority: high
Filed: 2026-10-06

## Original request

ok do phase 6

Parent: draft/feature/pyautopulse/profiling_setup_browser.md (approved Phase 6).

## Scope

@PyAutoPulse: Record the dedicated setup baseline campaign and pending collection/acceptance task in Pulse. Link the project specification and its qualification limits. Render the board offline without restamping check-in, ingesting measurements, changing pins or authorizing jobs.

## Plan

1. Add a needs-decision baseline campaign in campaigns.yaml and a pending task under tasks/ describing missing revision/hardware/setup choices, compile capability, separate compute authorization and later scientific acceptance.
2. Link the project specification and Phase 6 implementation issue/PR; state archived rows are context only and CPU arrays use ral.
3. Regenerate board offline with current Brain renderer and check the committed snapshots without fetching. Preserve last_checkin, unrelated campaign rows and coordinated heading edits.
4. Run Ruff, full Pulse tests, offline check and independent review.

Tier: judge — merge mode: human /prm.

No profiling jobs, baseline pin changes, archive promotion or temporal charts. No Heart RED override or merge permission inherited from previous sessions.

Issued: 2026-10-06
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/17
