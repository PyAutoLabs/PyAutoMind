# Complete Heart monitoring score and repair coverage

Type: bug
Priority: high
Difficulty: medium

Targets: @PyAutoHeart @PyAutoBrain

## Original request

PyAutoHeart is green and has a score of 100, but the individul dashboard still has yellows, reds and greys. I think that we should not acheive a full score if anything is not green, and I think we should ensure some of these dashboard entries are not grey and are fixable.We did the "Systematically fix alll in heart" thing but it seems ike that didnt cover everyhting that is monitored, therefore we should extend the scope of that button (or add another button) which covers everyhting

## Intended result

The headline monitoring score reaches 100 only when every applicable monitored check has fresh green evidence. Keep authoritative release readiness explicit and separately labelled. Unknown, missing and stale evidence cannot silently count as success; explicitly inapplicable checks need a reason and must be distinguished from missing evidence.

Extend the existing systematic repair action to enumerate all monitored findings and evidence gaps, including advisory repo findings, timing, hangs, skipped-script debt, and local observations. Use a shared complete inventory for scoring and repair coverage, including individual rows and full evidence beyond display limits. Give every unresolved item an evidence source, owner, supported remedy or explicit blocker. The full-dashboard health loop must not stop merely because release readiness is GREEN. Preserve approvals and task claims; never manufacture green, lower thresholds or discard user work.

## Observed evidence (2026-10-02)

Published board timestamp 2026-10-01T20:28:06.722401+00:00: release verdict green, score 100; six non-green sections: libraries, workspaces, worktree_drift, import_time, ci_timing, no_run_census. No grey top-level section in this fetched snapshot; audit individual rows and missing/expired evidence paths as well.

Current score is readiness.compute's weighted release penalties. dashboard.build_fix_plan already includes section summaries and full evidence references, but the health conductor's documented completion condition is release GREEN. Grey local rows use a generic tick/publish action; establish per-family refresh requirements rather than assuming this gathers every deep check.

## Implementation plan awaiting approval

1. Heart: audit all registered checks and all dashboard projections; build a complete structured findings/coverage inventory with stable identity, status, applicability, freshness, source and remedy. Include nested performance rows, skipped scripts, omitted observations and expected-but-missing checks.
2. Heart: calculate transparent monitoring penalties from that inventory; 100 iff all applicable checks are fresh green. Keep readiness.compute's release gate and its score available under explicit release labels; update HTML, JSON, terminal, Markdown, badge and state consumers consistently, preserving compatible fields where necessary.
3. Heart: drive build_fix_plan and the existing systematic repair button from the same inventory; retain clipboard budgets and complete machine-readable evidence. Diagnose grey families and provide supported refresh/publish routes or specific environment blockers.
4. Brain: extend the health conductor with an explicit complete-dashboard scope and completion condition; consume Heart-owned findings without recomputing health. Route each unresolved item to its owning workflow and report a complete reconciled checklist even when release GREEN.
5. Tests: green release plus adverse advisory checks; grey/missing/stale/nested findings; complete green inventory; explicit non-applicability; more findings than display/clipboard limits; repair inventory completeness; unchanged release gate; Brain completion and routing. Run affected suites and tenant checks, then normal ship workflow.

Proposed branch: feature/heart-monitoring-coverage
Primary repo: PyAutoHeart. Supporting repo: PyAutoBrain. Infrastructure development via start-library/ship-library.
