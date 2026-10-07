# Complete Pulse profiling browser navigation

Type: feature
Target: PyAutoPulse
Repos: PyAutoPulse
Consequence: judge
Autonomy: human-required
Filed: 2026-10-07

Primary: @PyAutoPulse. Standalone organ/workspace change.
Parent: draft/feature/autolens_profiling/profiling_redesign_completion.md
Approval: Three-phase plan approved with "ok go"; after A/B merged, user said "ok continue". User explicitly authorized "Coordinate in parallel" with dashboard-freshness (Brain #486).

## Overview
Bring the Pulse captured-evidence setup browser into parity with Phase A: show available axes/devices/runs, choose useful runtime evidence by default, open populated panels, and expose explicitly qualified related hazards.

## Plan
- Port measurement availability and useful selection behavior from the project browser.
- Preserve per-instance URL state and immutable captured-commit shard validation.
- Display model-related and shared findings with explicit applicability qualifications.
- Validate real-data and multi-instance browser journeys, contracts, responsiveness and generated board.

Tier: judge — merge mode: human /prm.

## Detailed implementation plan

Edit pulse/setup_browser.js and .css (and .py only if required). Adapt project's overview, axis/device/run selectors, compatible filter persistence, exact-link error/recovery and populated-panel behavior. Preserve Pulse's per-instance URL prefix, root-scoped DOM, capture.commit links and remote_shards guard. Older indexes without axis_devices must still work without inventing device/axis associations. Read optional hazard_discovery independently of exact setup hazards, retaining unknown applicability.

Extend tests/browser_fixture.py and tests/browser_setup.cjs with imaging MGE/rectangular real evidence plus hermetic multi-instance captures: no-reference defaults, axis navigation and visible exact values, device persistence, back/forward, exact breakdown-only links, qualified hazards, unknown metadata, bad hash/retry, async race, keyboard and responsive widths. Keep Python capture/security contract tests. Run all pytest tests, Ruff and offline board checks. Regenerate via bin/pyauto-pulse board --offline over existing captured snapshots; no campaign execution, no pins or scientific data edits.

Branch: feature/profiling-browser-completion. Canonical Pulse main clean at 4f84d5f, one remote generated refresh cbb53ba ahead. Existing freshness worktree has uncommitted board/ingest source edits. Human approved parallel isolated branches: this task owns setup_browser.* and browser tests; freshness retains board/ingest/workflow edits. Both may regenerate dashboard.html; reconcile by rendering from merged sources, never overwriting another branch's board changes.

## Original requests (verbatim)


We rrecently did a lot of work restructing autolens_profiling in order to improve its dashboard. First, I think there are aspects of the refacotr which are incomplete, for example there is still a "hazards" folder with mge / pixelization stuff in, but all hazards stuff should be specific to each likleihod function. Same for imaging/likelihood_runtime and imaging_likelihood_breakdown and similar packages, It feels like the refactor only got half way through?

ok yeah then lets continue, and before we start review the process, previous work and remaining work with Fable. Also, the dashboard does not contain any of the expected output and information att he moment, so maybe it never fully finished and got ot that?

Review-routing answer: Prepare a review handoff for Fable


Continuation: ok continue
Coordination answer: Coordinate in parallel
