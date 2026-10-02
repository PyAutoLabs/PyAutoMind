# Heart monitoring coverage — completed

- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/267
- pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/446
- pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/268
- merged: 2026-10-02
- pending-release: PyAutoBrain@https://github.com/PyAutoLabs/PyAutoBrain/pull/446
- pending-release: PyAutoHeart@https://github.com/PyAutoLabs/PyAutoHeart/pull/268

## Shipped

Headline monitoring score and systematic repair action share the complete inventory: all configured repositories, advisory and nested findings, missing evidence and unfinished baselines. A perfect monitoring score requires fresh green evidence across applicable checks. Release readiness remains separately labelled and its gate unchanged. Brain health gains explicit dashboard scope and cannot stop at release GREEN while monitoring is incomplete.

Collectors retain observation times; published local inventory keeps complete findings and privacy-safe placeholders. Older undated or incomplete evidence requires refresh and publication. Underlying advisory findings were not repaired by this task; they are covered by the expanded repair action. No scientific-library API migration or package release.

## Merge and validation evidence

Human /prm authorized merge and close-out. Brain merged first at cf13380a0ab02c354ca85d7560bdd0eeaede3a9e; Heart at aa358d3cfca29c8c7c33781945cbf000cb20d8bb. Both repository histories are non-shallow, and origin/main contains every claimed branch commit (zero unmerged).

Brain Actions run 36987274190 and Heart run 36987344066 each have passing Python 3.12 and 3.13 jobs. All runs for each head enumerated: one pull_request run per repo, every job completed successfully. Both PRs CLEAN/MERGEABLE before merge.

Local validation: Heart 1168 passed; Brain 1141 passed; collector timestamp tests 34 passed; tenant firewall and whitespace checks passed. Independent bounded review found no remaining blockers. End-to-end captured board: monitoring RED/42/incomplete, release GREEN/100; Brain adopts the distinct monitoring state correctly.

Logs and generated preview preserved under PyAutoMind/tmp/heart-monitoring-coverage/ (local scratch). Development worktrees contain only code/test caches, no scientific data products; remove after close-out. No remaining implementation scope.

## Backlog reconciliation

No sibling prompt is proven completed by these PRs. Six unrelated existing suspects remain filed under draft/bug/pyautoheart: reusable_smoke_workflow_relevance_gate_skips_custom_runner_tests; heart_smoke_runner_deletes_the_tracked_output; manifest_drift_parser_drops_suffixed_check_legs; ral_venv_dependency_floor_drift; release_integrate_analyze_path_filter_and_workspace_lint; smoke_install_flat_pip_chain_breaks_local_env_creation. Revisit with `pyauto-brain intake reconcile draft/bug/pyautoheart`; overlap/reference hints alone are not merge proof for this task.

## Original prompt

# Complete Heart monitoring score and repair coverage

Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/267
Issued: 2026-10-02
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

## Implementation plan approved 2026-10-02

1. Heart: audit all registered checks and all dashboard projections; build a complete structured findings/coverage inventory with stable identity, status, applicability, freshness, source and remedy. Include nested performance rows, skipped scripts, omitted observations and expected-but-missing checks.
2. Heart: calculate transparent monitoring penalties from that inventory; 100 iff all applicable checks are fresh green. Keep readiness.compute's release gate and its score available under explicit release labels; update HTML, JSON, terminal, Markdown, badge and state consumers consistently, preserving compatible fields where necessary.
3. Heart: drive build_fix_plan and the existing systematic repair button from the same inventory; retain clipboard budgets and complete machine-readable evidence. Diagnose grey families and provide supported refresh/publish routes or specific environment blockers.
4. Brain: extend the health conductor with an explicit complete-dashboard scope and completion condition; consume Heart-owned findings without recomputing health. Route each unresolved item to its owning workflow and report a complete reconciled checklist even when release GREEN.
5. Tests: green release plus adverse advisory checks; grey/missing/stale/nested findings; complete green inventory; explicit non-applicability; more findings than display/clipboard limits; repair inventory completeness; unchanged release gate; Brain completion and routing. Run affected suites and tenant checks, then normal ship workflow.

Proposed branch: feature/heart-monitoring-coverage
Primary repo: PyAutoHeart. Supporting repo: PyAutoBrain. Infrastructure development via start-library/ship-library.

## Implemented — awaiting merge

- Heart PR: https://github.com/PyAutoLabs/PyAutoHeart/pull/268 (draft pending Brain).
- Brain PR: https://github.com/PyAutoLabs/PyAutoBrain/pull/446 (merge first).
- Both branches: feature/heart-monitoring-coverage. Heart head 70e1177; Brain head cfe5c97.
- Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/heart-monitoring-coverage.
- Full tests: Heart 1168 passed; Brain 1141 passed. Collector timestamp tests 34 passed. Tenant firewall and whitespace checks pass. Independent bounded review: no remaining blockers.
- End-to-end captured board: monitoring RED/42/incomplete; release GREEN/100 unchanged. New health dashboard scope retains all findings and does not exit successfully at release GREEN.
- Authoritative vitals GREEN at shipping; no source-library API impact or scientific workspace smoke requirement.
- Full logs: task root logs/{heart-suite-final,brain-suite,heart-collectors,tenant-firewall}.log; local preview.html and board.json.
- Source observation timestamps added to collectors; older undated or partial published evidence stays unresolved until refreshed and republished. Underlying advisory repairs remain work for the expanded button.
- Next: /prm; merge Brain #446 first, mark Heart #268 ready and merge after its checks pass. No merge or release authority in this session. Published board changes only after merge/publish.
