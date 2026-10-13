# HST/MGE CPU pilot preparation

Merged PyAutoPulse#54 after all CI jobs passed. Issue PyAutoPulse#53 closed.

Added the draft pilot contract, proposed separate compilation/runtime methods,
resource ceilings and unresolved freeze choices. Updated the campaign and parent
task, regenerated Pulse board; 206 tests, ruff and offline check passed.

Preparation only: no compute, freeze, baseline/default changes or scientific
acceptance. Producer implementation remains in the separate Mind draft
`draft/feature/autolens_profiling/hst_mge_pilot_observations.md` and the scientific
work remains in Pulse `tasks/hst_mge_cpu_pilot.md`.

## Original prompt

# Prepare the HST/MGE CPU pilot contract

Issued: 2026-10-13
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/53
Type: docs
Consequence: judge
Target: @PyAutoPulse

## Original request

> ok go

Approved context: prepare a small HST/MGE fp64 CPU pilot before expanding builder
coverage. Specify inputs, hardware, correctness, separate compile/runtime methods
and a capped resource budget; identify bounded instrumentation gaps in Mind.
Compute, freeze, baseline promotion and merge are not authorized.

## Plan

- Record a draft pilot contract in Pulse, linked to setup_baseline_campaign.
- Distinguish the merged manual HST builder from unavailable global dispatch.
- Specify measurement boundaries, repetitions, proposed resource ceiling,
  provenance and correctness decisions; retain missing facts explicitly.
- File a separate bounded implementation draft in Mind; no producer edits now.
- Regenerate and validate Pulse board, publish a reviewable PR.

Tier: judge — merge mode: human /prm.

Detailed changes: add tasks/hst_mge_cpu_pilot.md; add its task row and update only
setup-baseline campaign/parent next steps in campaigns.yaml; append a dated
receipt to tasks/setup_baseline_campaign.md. Preserve last_checkin (focused work),
measurement dates, original migrated text, existing manifest and all pins.
Validate ruff, existing Pulse tests, board --offline and check --offline.
