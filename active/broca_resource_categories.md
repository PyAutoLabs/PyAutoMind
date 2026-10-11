# Broca resource categories and Heart publication visibility

Type: bug
Epic: scientist-adoption-pilot
Consequence: judge
Difficulty: easy
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoBroca/issues/8

## Original request

I dont see _Test workspaces on heart board? For Broca, "communication resources" should remove Documentation, tutorials, user workspaces and assistants. Project repositories own the source; Broca presents communication context and available upkeep evidence. and have separate sub drop downs per category (e.g. workspace, How To, RRD) it should also not list aassistants whcih are their own.  also remove this: "Committed-file inventory; these checks do not establish response quality or scientific correctness." and "Assistant evaluation evidence · collection age and evaluation age are separate."

## Plan

Confirm Heart publication lag and route publication of the merged board through Build. In @PyAutoBroca, nest resource rows under Workspaces, How To and Documentation category disclosures; remove assistants from that inventory while preserving their resource-ID deep links on the existing assistant section. Remove the three exact requested prose passages. Keep canonical catalogue, project context, evidence records and shared styling unchanged. Interpret RRD as documentation/Read the Docs, without making a new resource kind.

Detailed: broca/resources.py groups non-assistant resource rows by explicit relationship, deduplicating stable IDs. broca/board.py places canonical resource anchors on existing assistant cards by exact canonical repo+remote match, and removes maintenance intro/footer text. Regenerate dashboard.html. Run Broca suite/check/render and browser nested hash/keyboard/no-JS checks. No new Heart source change unless investigation finds a render defect. Heart live currently lacks resource-lens-tests and latest publication run38134638064 predates merge295.

Tier: judge — merge mode: human /prm. Existing user authorization covers requested corrections; publication is a board deployment, not a software release.

## Additional requested polish

For Hands, I thinkt h is is unecesary as the check in prompt covrs it: Heart

release 📋 rehearse 📋 validate 📋 build 📋

Remove only the redundant action-shortcut row in @PyAutoHands autohands/board.py; retain the check-in prompt and footer navigation. Add Hands to the same presentation task, validate its board tests.
