# Communication indentation and Nerves summary removal

- issue: https://github.com/PyAutoLabs/PyAutoBroca/issues/10
- completed: 2026-10-11
- library-pr: https://github.com/PyAutoLabs/PyAutoBroca/pull/11
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/198
- summary: Broca resource rows visibly indented beneath categories, with a subtle guide. Nerves HTML GREEN/count summary removed; data feeds unchanged.

Validation: Broca22 and Nerves241 tests pass; six phone/tablet/desktop light/dark browser checks measure indentation and verify hash reveal, keyboard and no overflow. All6 CI test/build jobs passed across4 runs. Broca deploy intentionally skipped on PRs. Nerves freeze clear. Both source heads proven ancestors of origin/main. No package release needed: Nerves edits only the unshipped board script.

Heart and Hands owner dashboard refreshes succeeded (Heart38163976587, Hands38163979000); live Heart had all4 test resource anchors, Hands standalone Heart link absent. Generic Build generate was the wrong route for these existing owner refresh workflows, not a publication blocker. Remaining live rollouts are tracked in the publication follow-up. Evidence archived locally at tmp/broca-indent-evidence/.

## Original prompt

# Indent communication resource dropdowns

Type: bug
Epic: scientist-adoption-pilot
Consequence: judge
Difficulty: easy
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoBroca/issues/10

## Original request

for Communication resources, the drop downs under "Workspacees" and others are not indedneter whcih makes it hard to read

## Plan

In @PyAutoBroca, give each category a resource-list wrapper with modest logical-start indentation and a subtle shared-theme border. Keep category summaries aligned and resource IDs/native details intact. Change broca/resources.py markup and board.py local layout CSS, regenerate dashboard.html. Verify actual child/category offsets and no overflow at phone/desktop widths, keyboard and fragment reveal; run existing Broca tests. No shared Brain edits, data changes or deployment. Tier: judge — human /prm.

## Additional request

Remove GREEN
330 config files across 9 sources · 171 workspace overrides · 76 possibly unused library keys from Nerves

Change @PyAutoNerves scripts/board.py HTML renderer only: remove the status/count banner while preserving state/badge and inspection data. Run targeted board tests and render checks. No autonerves library API changes.

Heart and Hands board publication: user repeated missing test-workspace and standalone Heart-link reports. Existing owner workflows dispatched as dashboard refreshes: Heart38163976587, Hands38163979000. The previous generic Build generate route was inapplicable, not a board publication gate.
