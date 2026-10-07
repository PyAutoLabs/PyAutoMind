# Profiling browser completion

Completed: 2026-10-07

Phase C merged in [PyAutoPulse#23](https://github.com/PyAutoLabs/PyAutoPulse/pull/23), merge `da2aee38cbdc85d747050cad18ce55579748c4d2`; issue #21 closed. The human authorized parallel coordination with dashboard-freshness and the final reconciliation/merge.

Delivered useful runtime defaults, axis/device availability and selection, exact-link recovery, optional old-capture metadata support, and qualified related/shared hazard discovery. Preserved immutable capture provenance, verified shard loading, scoped instance routing and separate measurement-method/batch semantics. Reconciled generated dashboard with merged freshness changes in `549eb5d`.

Validation: 193 Python tests, expanded real-data Chromium interaction suite, Ruff and offline receipt/contract checks passed. Every CI job passed on exact head `549eb5d42d1abf29f49ba3840afea794b9b54213`; conditional publishing step correctly skipped on PR. Independent Sol review CLEAN. The unchanged Heart yellow/stale reasons had explicit human acknowledgement in this session. No scientific campaign or baseline acceptance was part of this task.

Published Pulse verification passed after deployment: MGE/HST has three visible runtime values, rectangular/HST one, both have four axis choices and expected qualified hazard sections; no browser errors.

Parent completion: complete/2026/10/profiling-redesign-completion.md.

## Original prompt

# Complete Pulse profiling browser navigation

Type: feature
Target: PyAutoPulse
Repos: PyAutoPulse
Consequence: judge
Autonomy: human-required
Filed: 2026-10-07
Issued: 2026-10-07
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/21

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

## PR-open checkpoint — 2026-10-07

PR: https://github.com/PyAutoLabs/PyAutoPulse/pull/23
Head: 3cfb95b (feature/profiling-browser-completion)

Implemented measurement availability overview, runtime defaults, axis/device/run selection, compatible filter persistence, populated exact-run panels and honest missing/unknown coverage. Related/shared/uncategorized findings retain applicability qualifications. Immutable capture URLs, same-commit hash validation, multi-instance navigation, inline v2 and older optional metadata are preserved. Independent review caught and verified correction of a porting regression in legacy batch/method grouping; the original grouping is retained and has new Chromium coverage.

Validation: 192 Python tests; expanded real Chromium journeys over seven hash-preserved MGE/rectangular shards, missing memory, device filters, numeric identity, hazard scope, exact-link recovery, older metadata, inline v2, separate batch/method scales, corrupted shards/retry, async races, multi-project history, keyboard, responsive and dark-mode checks. Ruff (19 files), offline owner board regeneration and check pass. Independent Sol review CLEAN. No snapshots/receipts/campaign data or scientific evidence changes. Review surface/verdict/logs live in the task bundle.

Heart YELLOW/stale reason set unchanged from the explicit human acknowledgement earlier in this session. Human explicitly authorized parallel coordination with dashboard-freshness (#486); this branch edits setup-browser assets/tests. Dashboard freshness has since merged and released its claim; see `complete/2026/10/dashboard-freshness.md`. Preserve its merged board/ingest/workflow contract. Regenerate dashboard from merged sources if generated HTML conflicts. Await human /prm after CI; published-site verification follows merge/deployment.
