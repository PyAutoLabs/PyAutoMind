# Assistant evaluation and upkeep organ

Type: feature
Target: pyautobrain
Consequence: judge
Autonomy: human-required
Priority: normal
Status: draft

## Original requests (verbatim)

> I am considering if we need a dediciated PyAuto organ for assistant management. I now have 4 assistants, but I rarely check in on them, I put benchmarking in but dont run it and dont think benchmarks should be saved and stored results over time in the assistant (which is a public facing repo) anyway. I can imagine there are more things I would benefit from having an assistant dashboard. Thoughts?

> yeah lets do that, make sure the dashboard follows the format of others, thoughts on name?

## Intent and scope

Create a small dedicated organ owning assistant evaluation history, collection
receipts and a shared dashboard. Working name: PyAutoMentor, pending human choice.
@PyAutoBrain owns interpretation and development routing; @PyAutoMind retains task
lifecycle and repository identity. Four public domain assistants are the initial
coverage: autocti_assistant, autofit_assistant, autogalaxy_assistant,
autolens_assistant. Keep private euclid_assistant out of initial publication.

Public assistants retain benchmark definitions and reproducible tooling. Routine
run summaries and artifact references belong to the new organ; bulky/raw/private
outputs stay outside public assistant Git histories. No deletion or migration of
existing published results in the initial phase. Assistants remain independently
usable and unaware of the organ. Cortex retains scientific project records;
Heart retains release readiness. Reuse Mind repo identities rather than create
another body map.

## Proposed delivery

1. Foundation: versioned evaluation result contract; append-only run records;
   assistant coverage configuration referencing Mind identities; validation and
   idempotent ingestion. Record assistant commit, benchmark revision, model,
   harness, library versions, run date, outcomes, cost/interventions when known,
   and artifact references. Separate failed runs, collection failures, no runs,
   outdated evidence and incomparable baselines.
2. Board: current evidence per assistant, history, attention items and next useful
   action. Reuse Brain board/_theme.py css, hero, navigation_cards,
   orchestration_panel, section_layout and JS; follow docs/standards.md. Standard
   banner, check-in panel, navigation cards and collapsible sections; successful
   collection timestamp distinct from evaluation age. Copying a prompt runs
   nothing. No fake scores or fresh timestamps from cached rerenders.
3. Integrate: register organ and board through Mind repos.yaml and Brain policy;
   document ownership and check-in procedure. Private operational storage by
   default; public board publication requires a deliberately sanitized surface.
   Prepare a local reviewable dashboard before any hosting decision.
4. Pilot: inspect existing assistant runners, select one inexpensive representative
   evaluation per assistant and demonstrate ingestion and display of real results
   where execution is available. Record execution requirements/costs before
   external model campaigns. Broader evaluations and project-feedback ingestion
   are follow-on work, not requirements for the first board.

## Validation / witness

Reject malformed and conflicting duplicate records; preserve provenance and
receipts; never call absent evidence green. Test matching versus incomparable
baselines. Render empty, stale, failed and populated states. Check desktop/tablet/
phone light/dark layouts, keyboard navigation, links, disclosures, exact prompt
copy/preview and private-field exclusion. Validate body-map generation and board
registration. No changes to modeling libraries or scientific APIs expected.

Tier: judge — merge mode: human /prm.
