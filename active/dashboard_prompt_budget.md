# Bound dashboard assistant prompts

Type: bug
Issued: 2026-10-01
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/261
Primary: @PyAutoHeart
Related: @PyAutoBrain @PyAutoEyes

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

## Validated implementation — 2026-10-01

- Implementation committed and pushed from `.worktrees/dashboard-prompt-budget/{PyAutoBrain,PyAutoHeart,PyAutoEyes}`, all on `feature/dashboard-prompt-budget`.
- Shared 50,000-character clipboard guard covers the theme family, Heart's override and standalone batch packets. Oversized requests download intact for attachment; no silent truncation or false copy success.
- Eyes was the other standalone clipboard path discovered during the approved inventory. It enforces the same ceiling without adding a Brain checkout dependency; dashboard.html regenerated.
- Heart emits a prompt under 45,000 characters, explicitly marking omissions and referring to board.json. Complete source observations are retained in additive `fix_plan.evidence`; readiness calculations are unchanged.
- Synthetic reproduction: 1,351,774-character old prompt → 2,452-character new prompt; all 1,350,000 raw observation characters preserved.
- Validation: Heart 1,113 passed; Brain 1,131 passed; Eyes 79 passed (2,323 total). Eyes Ruff lint/format and live check of all 265 figure URLs plus state schema passed. All diffs pass whitespace checks.
- Brain's full test run needs `env -u PYAUTO_MIND -u PYAUTO_HEART` after activation: the grouped-layout fixture expects its temporary paths to override ambient worktree hints. Initial run was 1 failed/1,130 passed; the isolated fixture and then full suite passed with those hints removed, without modifying source for that failure.
- Full logs: task-root `logs/heart-tests.log`, `logs/brain-tests-clean-env.log`; PR drafts: `logs/{brain,heart,eyes}-pr.md`.
- Refreshed vitals RED: `release validation FAILED (stage integrate)`. Yellow reasons: `workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py)`; `manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml`; `manifest drift: tenant firewall (organ code) — 1 mismatch(es) vs PyAutoMind/repos.yaml`; `manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml`.
- Shipping authorization: user “I authorize you to conitnue” (2026-10-01), directly replying to the request to commit, push and open all three PRs despite `release validation FAILED (stage integrate)`, after all 2,323 tests passed. Development only; no release or merge authority.
- PRs: https://github.com/PyAutoLabs/PyAutoBrain/pull/439 (`862823a`); https://github.com/PyAutoLabs/PyAutoHeart/pull/262 (`58f25a0`, draft pending Brain); https://github.com/PyAutoLabs/PyAutoEyes/pull/11 (`afa48e5`). All labeled pending-release.
- Next: human merge command and green required CI; merge Brain before marking Heart ready so the shared browser guard is present. Eyes is independent. Stopped at PR-open; no background waiting or merge authority.

## CI repair — 2026-10-01

- `/prm` found Brain #439 and Eyes #11 green, but both Heart #262 legs failed the tenant firewall after all 1,113 tests passed. No PR was merged.
- Failure: `PyAutoHeart/tests/test_fix.py: new instance fact(s) in unlisted file — 'pyautolabs.github.io' (line 89)`. Logs saved in task-root `logs/heart-ci-110412983424.log` and `logs/heart-ci-110412983761.log`.
- User authorized the named repair: “can you perform the repair”. Changed the assertion to use `dashboard.PAGES_URL`, preserving its check of the evidence URL without hard-coding tenant identity.
- Validation: all 9 test_fix.py tests pass; tenant firewall passes against a CI-style layout containing Heart, Mind and Brain checkouts; git diff --check passes.
- Pushed Heart commit `66a717c` to existing PR #262. Replaces Heart's previously recorded head `58f25a0`. Next: re-run `/prm` to judge fresh CI; Brain remains the prerequisite for Heart.
