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
