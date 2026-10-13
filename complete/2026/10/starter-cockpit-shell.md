## starter-cockpit-shell
- issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/79
- completed: 2026-10-13
- workspace-pr: https://github.com/PyAutoLabs/PyAutoScientist/pull/80

Independent Scientist previews now use the cockpit three-row shell: instance-owned MyScientist / Cockpit identity, grey disabled IDLE placeholder (awaiting work), horizontally scrolling icon strip, and selected-board Reload / New tab toolbar. The shell stays fixed while board content scrolls. Existing onboarding text and inactive/paused feed isolation are preserved; JavaScript-disabled connected views retain their external link.

Source PR #80 merged as `ee06ba61568dde6696297a06a0454848de3df839` after every exact-head CI run/job/step passed for `08fdf425edcebb3bb0007760d9c2cbadbd3d7073` (one pull_request run and one tests job). Human /prm authorized the complete close-out.

Validation: 148 Python tests, 7 JavaScript checks, 30 browser cases at five widths/light-dark, plus final 26 renderer tests. Browser evidence covers actual new-tab destinations, reloads, native scrollbar, fixed toolbar/content scrolling, keyboard/history/clipboard, inactive network isolation and no-JavaScript fallback. No independent review claimed.

Prepared Pages files and tester ZIP published to PyAutoLabs/PyAutoEmbryo commit `47bc449856432214a60ac0bbed8613d08fd5188c`, under the existing human-approved static-only publication exception. Heart at shipping was STALE solely for missing current-source release rehearsal; no software/scientific release or organ activation.

Evidence and publication receipt: `organs/PyAutoMind/tmp/starter-cockpit-shell/`, outside the disposable task worktree. Independent collaborator acceptance remains a separate programme step.

Live verification passed at 390/1440px: identity/IDLE, native scrollbar, popup destination, reload, home navigation and clipboard; no browser errors. HTTP 200 and exact hashes verified for index, empty preview and ZIP. Live URL: https://pyautolabs.github.io/PyAutoEmbryo/. No remaining work for this shell change.

## Original prompt

# Match the independent starter to the cockpit shell

Issued: 2026-10-13
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/79
Difficulty: medium
Consequence: judge

## Original user request

Can we make it look the same as my cockpit, so it should have the PyAutoLabs / Cockpit link but say MyScientist / Cockpit, the icons should now have a scroll bar, it should have the same bar and format at the top but instead of YELLOW it should just be a greyed out button and say a word to imply its awaiting work   and also have the Scientist board Reload / New tablt thing.

## High-level plan

- Match the existing cockpit's three-row shell: identity/status, horizontally scrollable icons, selected-board toolbar.
- Show MyScientist / Cockpit for the demo, derived from instance-owned identity. Use a grey disabled IDLE status button for this starter shell, meaning awaiting work, not a health verdict.
- Keep a visible horizontal scrollbar/scroll affordance for organ navigation; preserve touch and keyboard access and the existing organ order.
- Add the selected board name plus Reload / New tab controls. Connected organs target their configured board; Scientist and inactive-organ views remain local. Keep descriptions and setup prompts unchanged.
- Preserve the familiar full-width shell and independent board-content scrolling, and verify desktop/mobile, light/dark, deep links/history, reload/new-tab destinations and clipboard behavior.
- Prepare regenerated PyAutoEmbryo pages and tester download. Tier: judge — merge mode: human /prm before publishing.

## Detailed implementation plan

@PyAutoScientist is the sole source repository. Use pyautolabs.github.io/cockpit/index.html as the read-only appearance/interaction reference; do not change the existing cockpit. Extend scripts/instance_navigation.py/.js and the instance-only wrapper in scripts/organism_board.py. Scope shell CSS to independent profiles and preserve unprofiled rendering. Keep configurable identity/destinations and inactive-feed isolation.

Add focused coverage in tests/test_instance_navigation.py and tests/navigation_browser.cjs for the three-row order, IDLE label, horizontal scrolling, selected-board toolbar, reload destination, new-tab destination, history, no unexpected external requests, and no overlap/whole-page overflow. Update STARTER.md only for the new shell/control behavior.

Survey: Scientist main is clean at 921d4ef; no active claim. Old unregistered DNA worktree remains untouched. Proposed branch feature/starter-cockpit-shell; proposed worktree .worktrees/starter-cockpit-shell. Live demo: https://pyautolabs.github.io/PyAutoEmbryo/ (publication clone in organs/PyAutoMind/tmp/pyautoembryo-tryout-2026-10-13/PyAutoEmbryo-pages).

Plan approved in this session; isolated worktree created.

## Implementation handoff — 2026-10-13

- Source PR https://github.com/PyAutoLabs/PyAutoScientist/pull/80, commit `08fdf425edcebb3bb0007760d9c2cbadbd3d7073`.
- Worktree `.worktrees/starter-cockpit-shell/PyAutoScientist`, branch `feature/starter-cockpit-shell`, clean.
- Instance shell now has configured repository identity / Cockpit, grey disabled IDLE, horizontal icon scrollbar, board toolbar with Reload / New tab, fixed shell and independently scrolling content. Existing prompts and inactive/paused isolation retained; ordinary Scientist rendering unchanged.
- 148 Python tests, 7 JavaScript checks, 30 browser cases passed; final focused renderer checks 26 passed. Browser covers five widths/light-dark, visible native scrollbars, real popup destinations, local/connected reload, history/focus/clipboard and no-JS external-link fallback.
- All logs, screenshots and generated artifacts: `organs/PyAutoMind/tmp/starter-cockpit-shell/`. No independent review claimed.
- Heart STALE solely `release validation incomplete: no rehearsal for current source`; development shipping allowed, no release-readiness claim.
- CI in progress when judged. Judge tier requires human /prm before merge.
- `pages-candidate/` contains updated index/connected/empty pages, README, tester ZIP. `publication-candidate.json` holds hashes/source pin/destination. Not yet published.
- Next: merge #80 when exact-head CI is green; publish prepared files to PyAutoLabs/PyAutoEmbryo using the existing user-authorized static-only exception, then verify live header, scrollbar, toolbar and ZIP. No science or activation.
