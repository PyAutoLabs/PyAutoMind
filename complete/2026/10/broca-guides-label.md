# Concise dashboard labels and detail blocks

- issue: https://github.com/PyAutoLabs/PyAutoBroca/issues/12
- completed: 2026-10-11
- library-pr: https://github.com/PyAutoLabs/PyAutoBroca/pull/13
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/296
- library-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/27
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/199
- summary: Broca Guides & Workspaces label; indented structured Heart test-workspace facts instead of boilerplate; matching Insight Fit/Lens project blocks; Nerves utility links removed. Concise dashboard-copy policy recorded in policy/dashboard_copy.md and linked from Mind AGENTS.md.

Validation: Broca22, Heart142, Insight183 and Nerves241 tests; Insight lint/format/offline contract; browser verifies Heart inset and equal Fit/Lens block geometry/styles at390/1440px. All10 test/build/lint jobs passed across7 exact-head CI runs. Broca PR deploy skipped by design. Nerves freeze clear. All4 heads proven merged into origin/main. Heart STALE only for missing release rehearsal; earlier local Nerves behind-origin reason cleared by clean fast-forward and fresh observation.

Test totals are not supplied by the current CI contract: Heart distinguishes unavailable test counts from available workflow totals and failures. No invented numbers or readiness changes. Nerves board scripts are not packaged; no PyPI release required. Evidence archived in tmp/broca-guides-label/evidence/.

Published via owner workflows: Heart38165564679, Nerves38165567495, Broca38165523332 and Insight38165558712. Live pages verified: Guides & Workspaces heading, Heart test-workspace-detail markup, Fit setup-navigation wrapper and no Nerves board.json utility link. Public HTML snapshots retained in tmp/broca-guides-label/.

## Original prompt

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
