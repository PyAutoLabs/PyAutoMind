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

## Additional requests (verbatim)

For Inishgtm autofit_inference
Integrity: ok · Freshness: freshness policy unspecified · evidence 2026-10-08T18:53:07Z · Scientific qualification: 35/223 accepted by producer; remaining assessments shown below

Captured source branch: main. Revision: 900648b5c66514167dd79a4859aed400fcc9551e. Capture time: 2026-10-08T19:54:10Z. Latest attempt: 2026-10-08T19:54:10Z.

Scope: inference. Producer revision: 0c87bf1add74ebec24c0dda6cd6684d1c8005f95. Generated: 2026-10-08T19:27:05Z. Source commit timestamp; not a measurement or check-in time

Project dashboard · Ingest receipt

Coverage and limitations is a weird one off tab and presumbly ws meant to be in Inference Results -> PyAutoFit, but its contents are also just information overkill

This is overkill for DNA: remove t, 2 / 7 environments observed; 5 declaration mismatches. Observed versions describe an installation; support requires matching validation evidence.

RAL shared environment (login observation): jax 0.10.2 is outside declared compatibility; RAL shared environment (login observation): jaxlib 0.10.2 is outside declared compatibility; RAL shared environment (login observation): anesthetic 2.8.14 is outside declared compatibility; Local development: jax 0.10.2 is outside declared compatibility; Local development: jaxlib 0.10.2 is outside declared compatibility.

## Extended implementation plan

@PyAutoInsight insight/board.py: v1 results nested in project disclosure under Inference Results, using existing project label; remove raw coverage/limitations dump and verbose capture/revision boilerplate, retain concise status, warnings, result evidence and receipt links. @PyAutoDNA dna/board.py: remove only HTML headline/mismatch paragraphs, preserving state feed and records. Validate Insight full tests/ruff/offline contract, Hands board tests, DNA unittest suite, and browser structure. All source changes are dashboard presentation only.

Heart publication investigation: live page predates merge295. Build --mode deploy --dry-run aborts on STALE ('Could not obtain a readiness verdict'); no gate bypass or workflow dispatch. Overnight review move separately filed under scientist_overnight_review_entry.md; Brain claim blocks it pending #518.
