# Standardize dashboard controls and remove redundant chrome

Type: maintenance
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/505
Difficulty: medium

Primary: @PyAutoBrain. Audit all thirteen organ dashboards and change affected owner renderers only, including @PyAutoHeart, @PyAutoHands, @PyAutoMemory, @PyAutoPulse, @PyAutoEars and @PyAutoScientist. Cortex and Mind renderer code belongs to Brain.

## Original request (verbatim)

The top right button in the box with the copy prompt has different text across dashboards, for example
PyAutoBrain is - Open work repositroy, PyAutoHeart is Open Heart repository. They should all just be the name
of the GitHub repository they link to, without the PyAutoLabs/. 

The copy prompt is nearly the same across all repos, I think it should be "Copy check-in prompt" for all
so a few need updating.

On PyAutoCortexc, remove the word "Open" before all the repos as this is just repetition and takes up space. 





- Remove this on any repos which have it which takes up space: GitHub Page

✗
Last check-in
2026-09-30T09:51Z
stale, paste the check-in

## Scope and acceptance

- Repository links in check-in panels show the actual destination repository name, without owner prefixes or Open/repository filler; preserve destinations and distinguish non-repository community links.
- All primary check-in copy buttons say Copy check-in prompt, preserving their existing payload and clipboard behavior.
- Remove Open before repository links across the Cortex dashboard.
- Remove redundant GitHub Page links and the old standalone last-check-in/stale block wherever present. Retain shared Last updated / Update controls and underlying evidence/check-in data.
- Update the shared orchestration contract and affected expectations, render representative boards, inspect output for consistency.
- Coordinate existing Brain board-one-click-update and Ears ears-followup-window claims before implementation. No source changes before approved plan and worktree setup.

## Proposed implementation plan (awaiting approval)

1. Standardize displayed repository labels using each GitHub destination's repository name in Brain's shared orchestration panel. Keep Community Hub as a non-repository companion link and preserve the copied prompt's existing metadata and domain instructions.
2. Use Copy check-in prompt on all primary panel buttons; remove Cortex, Heart, Pulse and Ears overrides. Remove Open from Cortex repository links outside the shared panel too.
3. Remove redundant GitHub Page links from Brain, Cortex, Heart, Hands, Memory and Scientist renderers. Remove Cortex's standalone old check-in widget, its unused freshness script/styles, and repair any navigation anchor targeting it. Audit other boards for the same redundant widget without removing domain evidence dates.
4. Update the shared presentation contract and existing affected tests, render the affected boards with fixture/cached data, and verify repository names, button text, working destinations, clipboard payloads and shared refresh controls.

Tier: undeclared — merge mode: human /prm.

### Detailed file scope

- PyAutoBrain/board/_theme.py: orchestration_panel visible repository link labels, excluding GitHub organization/discussion destinations; preserve URLs, escaping and prompt payload.
- PyAutoBrain/board/_board.py: redundant GitHub Page link.
- PyAutoBrain/agents/conductors/cortex/_cortex.py: copy label, repository label prefixes, obsolete standalone last-check-in markup/script/style and navigation target, redundant GitHub Page link.
- PyAutoBrain/agents/conductors/intake/_intake.py: verify Mind adoption through shared component; edit only if needed.
- PyAutoBrain/docs/board-orchestration.md: record uniform repository names and primary copy label; explicitly distinguish retained shared freshness footer from removed legacy widget.
- PyAutoHeart/heart/dashboard.py: primary copy override and redundant GitHub Page link.
- PyAutoPulse/pulse/campaigns.py: primary copy override.
- PyAutoEars/ears/board.py: primary copy override; retain Community Hub companion.
- PyAutoHands/autohands/board.py, PyAutoMemory/scripts/board.py, PyAutoScientist/scripts/organism_board.py: redundant GitHub Page links.
- Audit shared-component output across all thirteen organ boards, including Nerves, Gut, Insight and Eyes; avoid unnecessary consumer edits. Generated artifacts use their owning render commands after approval.
- Read each affected owner's AGENTS.md before implementation. Run existing focused shared-theme and owner-renderer tests; inspect rendered HTML and desktop/mobile appearance. No new test framework.

### Branch and coordination survey

Proposed branch: feature/dashboard-control-labels. Proposed isolated worktree bundle inside workspace: .worktrees/dashboard-control-labels.

Affected source repos Brain, Heart, Hands, Memory, Ears and Scientist are on main and clean; Memory's cached tracking state is behind by two commits. Pulse is clean on feature/pulse-linear-solver-p4a-merged-p5-issued. Fetch and recheck before setup; do not alter that branch.

Hard claims confirmed by worktree_check_conflict:
- Brain: board-one-click-update, feature/board-one-click-update; prototype and shared Update integration pending.
- Ears: ears-followup-window, feature/ears-followup-window.

Require explicit coordination authorization or wait for those tasks to ship. Preserve unrelated dirty Cortex data and Eyes artifacts. Helper also reports unregistered Brain/Heart/Hands pending-release-published-only worktrees; inspect relevant branch differences before setup, without cleanup.

Heart at planning: STALE (release STALE; monitoring RED), exit 1; planning permitted by start_dev. Re-read authoritative status at shipping.

No issue, source edits or worktree created yet; next action is human plan review and overlap decision.

## Approval
User approved plan and coordination with existing Brain/Ears claims: `go`. Source development uses start_library / ship_library; no merge authorized.
