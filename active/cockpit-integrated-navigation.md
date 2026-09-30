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
