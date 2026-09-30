# Reuse organ icons in cockpit overview panel headings

Type: feature
Target: pyautolabs.github.io
Repos:
- pyautolabs.github.io
Difficulty: easy
Consequence: glance
Status: active
Issued: 2026-09-30
Issue: https://github.com/PyAutoLabs/pyautolabs.github.io/issues/20

## Original request

> Can we also put icons next to each cockpit panel when you scroll down

## Proposed issue body

Title: feat: add organ icons to cockpit panel headings
Branch: feature/cockpit-panel-icons

### Plan

- Reuse each organ's existing navigation icon beside its name on the nine Overview cards.
- Add the matching icon to the pinned Heart panel.
- Preserve status dots/text and responsive heading wrapping; decorative icons use aria-hidden.

### Implementation and validation

In `cockpit/index.html`, update `cardHtml()` and `renderHeart()` to render `o.icon` beside the heading text using a small shared heading-icon style. Keep icon data in ORGANS. Update `cockpit/sw.js` shell cache version for the new markup. No other board repositories change.

Check all ten panel headings at 320px and desktop width, light/dark appearance, heading wrapping, unchanged status labels and no horizontal overflow. Extract inline JavaScript for syntax validation and run diff checks.

Branch survey: website and Mind clean on main; no active website claim. Existing navigation work shipped in PR #19. Heart entry feed STALE (test run status unknown, install verification not run, no release validation for current source); fresh ship gate remains required.

Approval: user approved implementation with “go” on 2026-09-30. No merge or deploy authorization for this new task.

## Implementation handoff

Implemented in `/home/jammy/Code/PyAutoLabs/.worktrees/cockpit-panel-icons/pyautolabs.github.io`, branch `feature/cockpit-panel-icons`, base `54d97ec`. Committed and pushed as `59f2fdc`. Two files changed: cockpit/index.html and cockpit/sw.js. Reuses ORGANS icons, decorative aria-hidden markup, grouped icon/name headings, narrow-screen wrapping and shell cache v3.

Passed Chromium checks: all ten headings, navigation/icon consistency, status dots/text intact, no horizontal overflow at 320px and 1440px in light/dark. No JS errors. Mobile screenshot inspected. Inline and worker JS syntax plus diff checks pass. Evidence/PR body in sibling checks/ directory.

Heart RED: `release validation FAILED (stage integrate)`. Other current reasons: `workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py)`; `manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml`.

Live authorization: “Authorize shipping cockpit #20”, recorded in the issue, PR body, active.md and autonomy_log.md. PR https://github.com/PyAutoLabs/pyautolabs.github.io/pull/21 is open with pending-release. Next: await human merge/deploy request; no merge/deploy authorization yet.
