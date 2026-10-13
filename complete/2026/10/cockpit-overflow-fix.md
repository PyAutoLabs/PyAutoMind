# Cockpit icon overflow correction

Merged PyAutoScientist PR #82, commit 769ffdbd893b7637ffb4797f204e86be32263a78; issue #81 closed. Branch ancestry proven merged. Removed the 1160px width cap and forced scrollbar styling; full-width automatic overflow matches the original cockpit. All desktop icons fit without a horizontal scrollbar or hint; narrow screens preserve reference navigation access.

Validation: 26 focused Python tests, 30 browser cases, desktop screenshot review, and all source CI jobs passed. Published validated seven-file PyAutoEmbryo artifact candidate as 4812aed to https://pyautolabs.github.io/PyAutoEmbryo/. Publication receipt and evidence: tmp/cockpit-overflow-fix/. Live verification recorded separately in publication-candidate.json. No inference, production profiling, or scientific collection occurred. Existing static-publication approval and Heart STALE exception apply.

Human prm authorized merge and close-out. No pending library release. Only disposable Python caches existed in task worktree. Dashboard regeneration and worktree cleanup performed by prm.

## Original prompt

# Remove forced cockpit scrollbar
Issued: 2026-10-13
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/81
Difficulty: small
Consequence: judge

## Original request
The icon scrolling left right bar is still there, I dont want a scroll and the PyAuto one does not have it

## Correction to approved cockpit-matching work
@PyAutoScientist scripts/instance_navigation.py constrains .nav-scroll to 1160px and forces overflow-x:scroll, unlike the original pyautolabs.github.io cockpit. Remove the width cap, forced scrollbar and custom scrollbar rules; use the original full-width overflow-x:auto behavior. At desktop width all icons should fit with no scrollbar/hint; retain the reference cockpit narrow-screen accessibility. Existing header, toolbar and content are unchanged.

Update tests/navigation_browser.cjs to assert width-dependent overflow and auto behavior. Verify desktop shows all icons without horizontal scrolling and mobile retains access as in the reference. Prepare regenerated Embryo artifacts. Suggested branch feature/cockpit-overflow-fix. Single clean Scientist main checkout, no active claim; old DNA worktree untouched. This is an explicitly requested correction to the already approved cockpit parity scope. Tier judge; human /prm before merge/publication.

## Shipping handoff — 2026-10-13
Source PR: https://github.com/PyAutoLabs/PyAutoScientist/pull/82
Source commit: 67c4e1fea97085bc1b9ee323e780ae58faf62a75
Removed forced scrollbar/custom styling and width cap; matches original cockpit full-width automatic overflow. Desktop screenshot shows every icon without a scrollbar/hint; narrow screens retain original overflow access.

Validation: 26 focused Python tests and 30 browser cases passed; desktop screenshot visually inspected; git diff --check passed. CI Board tests in progress at handoff. Heart STALE solely missing release rehearsal. No inference or production profiling.

Evidence: tmp/cockpit-overflow-fix/{python-tests.log,browser.log,browser/validation.json,browser/overview-1440-light.png,heart-readiness.json}. Regenerated seven-file Pages candidate plus SHA256 receipt at tmp/cockpit-overflow-fix/publication-candidate.json. Source worktree committed and pushed. Human /prm required by judge tier; source merge and live publication have not happened. After merge publish candidate to existing PyAutoEmbryo-pages clone, verify Pages, close issue and lifecycle, clean source worktree. Existing static-publication approval applies.
