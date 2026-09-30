- issue: https://github.com/PyAutoLabs/pyautolabs.github.io/issues/18 (closed)
- completed: 2026-09-30
- workspace-pr: https://github.com/PyAutoLabs/pyautolabs.github.io/pull/19 (MERGED)
- commit: e30b69df173668fec987dfcafa486e5ad2bd4723
- merge-commit: 54d97ec21ef05af106d892690a027ecae44f134a
- deployment: https://github.com/PyAutoLabs/pyautolabs.github.io/actions/runs/36760609419
- live: https://pyautolabs.github.io/cockpit/
- summary: Persistent icon/label navigation embeds nine independently published boards in one mobile-friendly cockpit. Overview preserves feed cards. Hash URLs, Back/Forward, accessible focus/status, touch targets, landscape layout, reload/new-tab recovery and updated offline shell implemented.
- review: Independent Fable 5.1 plan review; addressed history, worker-boundary, dynamic-height and inter-board-navigation findings.
- validation: Chromium nine live board snapshots across five viewport sizes (45 combinations), history/reload/polling, overview and embedded clipboard, keyboard focus, failure recovery, external URL guarding; live HTTP preview + worker scope/cache/offline; JS/JSON syntax and diff checks all passed. Post-deploy touch-emulated 390px browser confirms ten navigation links, embedded Heart/Brain switching without new tabs, Back to Heart, no shell overflow, shell-v2 worker and no JS page errors.
- heart-red-override: User "Authorize shipping cockpit #18" after exact RED reason `release validation FAILED (stage integrate)` and other Heart reasons were shown. All applicable branch checks passed. User then separately authorized "merge and deploy". Heart RED remains unrelated to this static Pages publication; no library release performed.
- ci: No PR checks configured; explicitly disclosed before acting on the user's merge command. Pages build, deploy and report-build-status jobs passed on the merge commit.
- limitations: Physical iOS/Android and installed-app launch untested. Existing Eyes child board requires horizontal scrolling below approximately 797px; shell contains overflow. Owning-repo follow-up remains outside this task.
- evidence: Local browser scripts, JSON results and screenshots preserved under PyAutoMind/tmp/cockpit-integrated-navigation-evidence/ before worktree removal (not versioned).

## Original prompt

# Integrated cockpit navigation with mobile-friendly organ icons

Type: feature
Target: pyautolabs.github.io
Repos:
- pyautolabs.github.io
Difficulty: medium
Status: active
Issued: 2026-09-30
Issue: https://github.com/PyAutoLabs/pyautolabs.github.io/issues/18

## Original user requests

> I want to improve and change the pyautolabs cockpit, which is nice but has a long way to go. My first question is at the moment I have it open in a web brwoser, and to open a new board I click the board and it opens a new tab. Is there anyway to make this more "integrated" into a single window, with the boards at the top as icons I can click but not opening new web browser tabs? Or does that require developing something way more complex than what it is currently?

> this sounds good, having icons will also help add character, be sure it'll be mobile friendly too

## Accepted direction

Keep the static cockpit and independently published boards. Add persistent organ icon navigation and embed the selected board below it. Keep the current cards as Overview. Give icons labels and live status dots. Mobile friendliness is a requirement.

## Implementation plan / proposed issue body

Title: feat: integrate cockpit boards with mobile-friendly navigation
Branch: feature/cockpit-integrated-navigation
Classification: website, routed through start_workspace and ship_workspace.

### High-level plan

- Add a persistent Overview/organ navigation bar with distinctive icons, labels, and status indicators.
- Display the selected board within the cockpit; route cockpit board links to that view.
- Make navigation touch-friendly and horizontally scrollable on narrow screens while preserving room for the board.
- Support selected-board URLs, reload, Back/Forward, accessible focus, and explicit standalone-board links.
- Check published board embedding, mobile layouts, copy actions, and existing overview/feed behavior.

### Detailed plan

- `cockpit/index.html`: add inline icon metadata to ORGANS; accessible navigation and selected-board heading; one titled iframe populated only when a board is selected. Keep overview cards and polling. Update status indicators without reloading the iframe. Validate embedded destinations against the expected Pages origin; external destinations use explicit external links.
- Add hash-based selection for Overview and organ routes, restoring from the URL across reload and browser history. Route card/Heart board links to local selection. Provide loading feedback, retry and a visible standalone link; do not claim iframe load proves successful HTTP content.
- CSS: use flexible viewport sizing, at least 44px touch targets, visible labels/focus/selection, horizontally scrollable mobile navigation with an overflow cue, and no shell-wide horizontal overflow. Test portrait/landscape and phone browser height changes.
- Verify all nine live board destinations permit framing. Check board content at narrow widths: wrapper responsiveness alone cannot fix fixed-width child content. Record any board-specific remediation required before extending scope into other repositories.
- `cockpit/sw.js`: bump shell cache version so deployed clients receive the new navigation; preserve feed network behavior.
- `README.md` / cockpit section of `AGENTS.md`: document navigation, direct board URLs and mobile behavior as needed.
- Validation: browser checks at 320/390px mobile, tablet, and desktop; board switching and history; dark/light themes; keyboard and touch navigation; board copy controls; existing polling; installed-window behavior where available. Check JS syntax and shell-cache upgrade. Record any unavailable browser/device coverage honestly.

## Approval / next step

The user accepted the integration approach and added mobile friendliness. Present the concrete issue body before issue creation, as required by start_dev. Complete branch/claim survey and worktree setup before source edits. No merge authorization.

## Fable review — 2026-09-30

Requested by the user: "review with fable, then go". Reviewed with local Claude CLI, actual model `claude-fable-5-1`; plan-only independent review, no source edits. Verdict FINDINGS; direction and scope sound. Incorporate all material findings before implementation:

- Keep shell history authoritative: replace iframe documents with `location.replace` rather than assigning `src` on each board switch; explicitly manage shell route history. Verify Back/Forward in a real browser engine.
- Audit board service-worker registration/scope and frame-busting scripts. Keep board requests out of cockpit shell caching; existing skipWaiting/clients.claim behavior remains.
- Use 100dvh with 100vh fallback, flex min-height:0, and shell overflow:hidden in board mode so the board owns vertical scrolling.
- Reconcile same-origin iframe navigation with the selected organ and shell URL; route inter-board link clicks through the shell when possible.
- Use a labelled nav with links, aria-current, decorative icons, textual statuses, board-heading focus, reduced-motion support, and scroll selected navigation into view.
- Keep touch targets >=44px, compact landscape layout, and contain navigation overscroll.
- Extract inline JS for syntax checking. Document HTTP preview. Distinguish browser emulation from real iOS/Android evidence.
- Fixed-width child-board defects remain reported follow-ups rather than widening this PR.

Live preflight: all nine canonical board URLs returned HTTP 200 and no X-Frame-Options or Content-Security-Policy header blocking framing.

Branch survey: website clean on main, recent branches main and docs/restore-organ-sentence. No active task claims website. Mind main has a separate untracked point-solver prompt; preserve unrelated work.
Approval: user approved plan and authorized implementation following Fable review. No merge authorization.

## Implementation handoff — 2026-09-30

- Worktree: `/home/jammy/Code/PyAutoLabs/.worktrees/cockpit-integrated-navigation/pyautolabs.github.io`; branch `feature/cockpit-integrated-navigation`; base `db14308`. Source changes committed and pushed as `e30b69d`.
- Changed: cockpit/index.html, cockpit/sw.js, README.md, AGENTS.md. Icon navigation, responsive single-board view, hash/history, clipboard, focus, recovery and external-link handling implemented; all Fable material plan findings addressed.
- Evidence in sibling `checks/`: browser-check.cjs, browser-results.json, layout.json, board-audit.json, pwa-check.cjs, edge-check.cjs, mobile/dark PNGs, pr-body.md. Playwright installed there only, no application dependencies added.
- Passed: nine live HTML board snapshots × five mobile/tablet/desktop sizes; history, route reload, inter-board links, polling preserving frame, two clipboard contexts, keyboard focus, failure recovery and external URL guard. Live cross-origin localhost preview, SW cockpit-only scope, shell-only cache and offline navigation passed. No JS page errors. Syntax/JSON/whitespace checks pass.
- Physical iOS/Android and installed-app launch not tested. Eyes child content overflows to roughly 797px; shell stays responsive and contains scrolling. Report owning-repo follow-up.
- Heart live refresh 2026-09-30T18:30:40.573510+00:00 RED: `release validation FAILED (stage integrate)`. YELLOW reasons: `workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py)`; `manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml`.
- Live authorization: “Authorize shipping cockpit #18”. Recorded on issue, PR body, active.md and autonomy_log.md. PR https://github.com/PyAutoLabs/pyautolabs.github.io/pull/19 is open with pending-release. Next: human review and separate prm/merge authorization; no merge or release authorization.
