# Rename Broca communication section

Type: bug
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoBroca/issues/12
Epic: scientist-adoption-pilot
Consequence: judge

## Original request

yes, update

Accepted label: Guides & Workspaces, replacing Communication resources.

## Plan

Change @PyAutoBroca section heading and navigation label, retain existing anchors and behavior. Regenerate dashboard.html; run existing tests and inspect escaped HTML label. No shared theme or data changes. Tier: judge — human /prm.

## Heart refinement requested

For Heart, remove Project-owned test suites and their recorded CI evidence. Inventory is not a passing result. CI without matching repository run provenance is unavailable. Evidence older than 24 hours is labelled outdated here; release gates retain their own policy., I think we need a regneral rule not to put these long text descriptions of what it does everywhere they cluutter a worksghop and users will learn as they go. Also, make the textr under each drop down indentee and less wordy, I think just a summary of the tests, their number would be fine and if any fail is fine. Mkae it more structured and easy to read in

Plan: @PyAutoHeart heart/resources.py removes section prose and verbose per-resource boilerplate. Use indented structured suite/CI summary, available workflow counts and failures, brief test-count unavailable label (current CI contract has no individual test totals), run/source links and useful stale warning. Preserve exact provenance checks and readiness. Add local CSS in heart/dashboard.py; update affected test assertions and browser validation. Mind policy records user-directed terse dashboard copy convention; canonical Brain standards rollout remains pending its existing claim.

## Insight alignment requested

in Insight Inference Results
PyAutoLens
PyAutoFit is still weird, PyAutoFit should have same indepdent and block as PyAutoLens

Use the existing setup-navigation project wrapper around legacy Fit details in @PyAutoInsight insight/board.py. Match Lens project card border, padding, and nesting; keep the Fit anchor and result rows. Regenerate tracked HTML, run tests/ruff/offline checks and compare actual bounding boxes/styles in browser.

## Nerves utility links requested

remove board.json
·
GitHub from Nerves

Remove the utility-row board.json and GitHub links from @PyAutoNerves scripts/board.py; retain exported data and ordinary navigation. Full suite verifies no library behavior changes.
