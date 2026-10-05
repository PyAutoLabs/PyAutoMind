# Minimal dashboard text and top Heart action

- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/467
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/468
- library-pr: https://github.com/PyAutoLabs/PyAutoEars/pull/13
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/284

All three PRs merged in dependency order. Shared hero ledes and orchestration descriptions are no longer displayed; Mind's tutorial paragraphs removed; Ears Last checked and usage paragraphs removed; Heart systematic-fix prompt is in the top shared panel with work-repo link, no lower duplicate, and evidence refresh displayed only when available. Prompt and data contracts preserved.

Validation: 2,493 local tests, strict docs, shared 10-case browser witness and Heart three-width exact-copy/layout checks. Every CI job passed: Brain three, Ears three, Heart two. Branch ancestry proven in each origin/main.

Shipping used the explicit development-only RED override recorded on issue comment 6000820253: `autolens_workspace_test: Smoke Tests failure on main`. Human separately invoked /prm; this merge does not clear Heart or authorize release.

Remaining broader orchestration rollout and cross-repo guidance are tracked in draft/feature/pyautobrain/standardize_dashboard_orchestration_prompt_panel.md. Unrelated batch_slice.md reconciliation suspect retained; /intake reconcile draft/feature/pyautobrain is its review door.

## Original prompt

# Remove dashboard tutorial prose and elevate Heart action

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoEars
- PyAutoHeart
Difficulty: medium
Consequence: judge
Autonomy: supervised
Issued: 2026-10-05
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/467

## Plan
User approved this refinement explicitly. Remove dashboard-purpose/tutorial prose from shared headers and panel descriptions; remove Ears Last checked; place Heart systematic fix action in the top shared panel, removing its bottom duplicate. Keep work links and exact prompts.

## Detailed plan
Brain board/_theme.py: preserve callable compatibility while omitting masthead ledes and panel description paragraphs without empty spacing. Update Brain-owned renderers' introductory copy and shared presentation docs. Ears ears/board.py: remove timestamp line and static instructional prose from check-in. Heart heart/dashboard.py: shared orchestration_panel immediately after hero, using existing build_fix_plan payload and configured work-repo link; retain separate stale-evidence action and legacy per-row copy fallbacks; remove usage paragraphs and footer. Existing tests plus browser witness, full affected suites, fresh Heart ship gate. No data contract or approval-policy changes.

Survey: Brain, Ears, Heart main clean; no conflicting claims. Branch feature/dashboard-minimal-text; worktrees under .worktrees/dashboard-minimal-text. Tier judge: human /prm.

## Original user request
Remove all explanatory text which says what a dashboard does and how to use it -- only I use this I dont need a reminder, on Mind this is "Every task the Mind is holding. Tap a task's 📋 and its start-dev skill prompt is on your clipboard — paste it into an AI assistant chat to route the assistant straight to that task. Recent is the same work by date — what has been happening rather than what to do next.", on Ears, just remove the "Last checked 05 Oct 2026, 17:30 UTC2 as its text whic breaks dashboard symmnetry, on heart remove the text "Is it safe to release? See what needs attention, then copy a prompt to work through it in your coding chat." and get the main button up there which basically will replace the "Fix Heart Systematically" button at the bottom.

## Implementation handoff

Implemented in the three claimed worktrees, uncommitted. Shared header ledes and panel descriptions omitted; Mind usage prose removed; Ears Last checked removed; Heart existing fix-plan prompt moved to top shared panel with repo link; duplicate lower action removed and evidence refresh conditional. Browser screenshots and draft PR bodies are in tmp/dashboard-minimal-text/.

Ship-time Heart RED (2026-10-05T18:37:22Z): `autolens_workspace_test: Smoke Tests failure on main`. Additional STALE reason: `release validation stale: source moved since rehearsal (PyAutoNerves)`. No shipping override granted. Awaiting explicit development-only override for issue #467; PR/commit/push of implementation held.

## Ship handoff

User subsequently authorized: “I authorize permission”. Recorded on issue #467 (comment 6000820253), each PR, active.md and autonomy_log.md. Heart remains RED with the same exact reason above.

PRs: Brain#468 (99b6aaf), Ears#13 (ff09eea), Heart#284 (795f306). Merge Brain first. Validation: Brain 1,195 tests, Heart 1,227, Ears 71; strict docs, shared browser witness, actual Heart three-width copy/layout check, tenant firewall and whitespace all pass. Ready for human /prm; no live rollout claimed.
