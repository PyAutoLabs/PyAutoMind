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
