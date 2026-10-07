# Shared dashboard freshness footer

Issued: 2026-10-07
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/486
Type: feature
Target: @PyAutoBrain
Difficulty: large

## Original request

Should all dashboards have a last updated text? Feels like they should and thtat this should be homogenized
and common amongst all. I would put it to the right of the "> Read the prompt" thing on each copyable button under the copy button,
with its text the same across all and it being in green if its within a certain time threshold (under 1 hour?) yellow for another and red for another, with it clickable or an update button next to it, but it should be smaller font that the other stuff in the button

## Approved design

User approved with “go”. Shared footer beside Read the prompt, under controls: Last updated <relative age> and Update. Green under 1 hour; yellow 1–24 hours; red at least 24 hours; grey unavailable. Smaller font, mobile wrapping, exact timestamp accessible on click, browser age advances without resetting source time. Timestamp represents successful displayed-information refresh, separate from scientific evidence age and health. Owner supplies real refresh destination; no fake reload-as-update behavior.

## Scope and validation

Extend Brain shared orchestration_panel/CSS/JS and standard; adopt across the thirteen organ boards (Brain, Mind, Cortex, Ears, Heart, Hands, Memory, Pulse, Insight, Nerves, Gut, Eyes, Scientist). Survey owner timestamps, refresh mechanisms and claims. Preserve domain meanings and actions. Validate boundary and missing timestamps, multiple panels, accessibility, prompt copying and responsive rendering. No merge authorization.

## Implementation checkpoint — 2026-10-07

Approved work implemented and validated. Brain issue #486 contains progress. Worktree: `/home/jammy/Code/PyAutoLabs/.worktrees/dashboard-freshness`; every claimed source repo on `feature/dashboard-freshness`. Eleven prepared diffs/PR bodies under `tmp/pr-drafts/`; full validation in `tmp/validation.md`. 3,945 Python tests verified across full/targeted reruns; 120 browser layouts and 14 clipboard checks pass. No unresolved test failure. Pulse/Insight use explicit successful-refresh receipt, preserving unchanged capture/evidence dates and offline replay. All thirteen board owners wired; standard/adoption matrix updated.

No source commit/push/PR yet: canonical Heart YELLOW acknowledgement required for `manifest drift: shared-standards blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml`. Release validation is stale due to source movement in PyAutoNerves/PyAutoFit/PyAutoArray/PyAutoGalaxy/PyAutoLens; no RED reasons. Resume commit/push/open eleven PRs after acknowledgement; merge remains human, Brain before owner consumers; then verify publication. Preserve approved design, no new planning gate.

## Ship and partial merge checkpoint — 2026-10-07

User invoked `$prm` directly after the disclosed Heart warning, authorizing ship and green-CI merge. Canonical YELLOW reason was unchanged and recorded in active.md. Eleven PRs opened; Brain #487 merged after docs plus Python 3.12/3.13 passed. Remaining PRs: Ears18, Heart289, Hands305, Memory120, Pulse22, Insight10, Nerves190, Gut26, Eyes22, Scientist47. Pulse incorporated fresh upstream snapshot and passed192 tests again.

Stopped as required by prm on Ears browser CI failure: `tests/board_browser.py:50` still asserts exactly two panel links; Update adds a third. This owner browser assertion was missed in development. Failed log preserved under task tmp/ci-failure-PyAutoEars-112691117119.log; run37590669940/job112691117119. Eight other consumer PRs green, Eyes lint pending at last audit. No other merges, reruns or code edits after failure. Source commits and open PRs retained. Resume development fix of that exact assertion, run Ears tests/board_browser.py, ship fix; then /prm and publication verification/closeout. Original approval and remaining scope persist.
