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
