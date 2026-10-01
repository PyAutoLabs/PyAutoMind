# Bound dashboard assistant prompts

Type: bug
Issued: 2026-10-01
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/261
Primary: @PyAutoHeart
Related: @PyAutoBrain

## Original request

This is from the fix all systemstically thing on pyautoheart dashboard, I guess we need to put a limit on all claude copyable prompts in all dashboards? ■ Message exceeds the maximum length of 1048576 characters (1346509 provided).

## Intent

Keep every dashboard assistant copy action within a conservative size budget. Replace Heart's uncapped raw observations with bounded summaries and references to complete evidence. Preserve instructions, safety constraints, and task scope; never silently truncate. Protect clipboard dispatch centrally, including Heart's copy override and manual fallback.

## Authorization

2026-10-01: user said “i authorize, go” in response to proceeding with planning despite Heart RED: PyAutoGalaxy: CI failure, https://api.github.com/repos/PyAutoLabs/PyAutoGalaxy/actions/runs/24007765443. Development override only, no release or merge authority.

## Acceptance

- Proposed shared ceiling: 50,000 characters, measured on the final clipboard payload.
- Heart fix-all uses concise evidence summaries with discoverable full evidence.
- Oversized generic prompts use an explicit compact fallback with a complete-evidence reference or are blocked with truthful feedback when no recoverable reference exists.
- Small prompts and shell commands retain their meaning.
- Tests cover huge nested snapshot data, Unicode, exact boundaries, overrides and clipboard failure/manual fallback.

## Implementation plan (approved 2026-10-01: “ok go”)

1. Reproduce the overflow with a synthetic large snapshot using Heart's dashboard fixtures. Retain the full observations in their existing evidence artifacts; do not change readiness calculations.
2. In PyAutoHeart/heart/dashboard.py build_fix_plan, replace raw JSON embedding with a budgeted summary. Keep the workflow instructions and snapshot identity, summarize finding counts/categories, and provide actual accessible evidence locations. If the summary itself exceeds budget, emit a compact health-workflow prompt that explicitly instructs discovery and reading of the authoritative evidence.
3. In PyAutoBrain/board/_theme.py introduce the shared 50,000-character budget and guard clipboard dispatch before per-board copyCmd overrides. Preserve short payloads; use a declared complete-evidence fallback for oversized payloads, otherwise explain that copying is blocked. Never report success for a failed clipboard operation.
4. Survey all dashboard copy entry points from the shared theme's board registry and Mind's renderers. Wire any bypasses to the same policy; preserve terminal commands without truncation. Confirm manual selection paths and non-HTML prompt output have equivalent bounds or explicit evidence handoffs.
5. Extend tests/test_board_theme.py and Heart tests/test_dashboard.py with oversized payload, Unicode/boundary, full-evidence recovery, and clipboard-override cases. Run affected dashboard suites and validate rendered HTML behavior.

## Branch survey

2026-10-01: PyAutoBrain and PyAutoHeart main checkouts are clean and behind origin/main; implementation must start from fetched origin/main. Mind main is clean before this draft. No active.md task claims Brain or Heart. Existing Brain worktrees are present and must be preserved.
Suggested branch: feature/dashboard-prompt-budget.
Suggested task root: .worktrees/dashboard-prompt-budget inside PyAutoLabs.
Initial source targets: PyAutoBrain and PyAutoHeart; expand only if the dashboard entry-point inventory demonstrates a bypass.

## Reasoning record

Bug and Feature conductors run on this prompt; both found no matching Memory context. Bug heuristic reports medium severity, multi-repo, infrastructure owner Heart, investigate-first. Source inspection identifies unbounded serialization in build_fix_plan and an unguarded shared copy listener. No library/scientific API change is intended; the heuristic's public-API warning is not supported by the identified scope.
