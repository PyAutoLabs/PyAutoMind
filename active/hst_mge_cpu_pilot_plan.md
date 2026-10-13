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
