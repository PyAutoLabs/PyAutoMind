## pyautobroca-assistant-management
- issue: https://github.com/PyAutoLabs/PyAutoBroca/issues/1 (closed)
- completed: 2026-10-08
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/495 (merged e6d4ce43)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/511 (merged 3fd1d2c5)
- library-pr: https://github.com/PyAutoLabs/PyAutoBroca/pull/2 (merged 043f03ab)
- summary: PyAutoBroca owns immutable assistant evaluation records, collection receipts and a dashboard using Brain's shared components. Four public assistants covered; 14 historical AutoLens benchmarks plus four separately labelled maintenance inventories. No private assistant or raw transcripts ingested.
- visibility: PUBLIC at the user's explicit request; tracked records and source inspected before conversion. GitHub Pages remains unconfigured; dashboard.html is the standalone snapshot.
- validation: Broca 18 tests, Brain 1252 tests, Mind 696 tests; ten browser cases across five widths in light/dark, no page overflow, keyboard copy and exact preview verified. All final-head applicable CI jobs passed. Mind drift job intentionally skipped on PR events; privacy and firewall green. Brain Python 3.12/3.13 green. Broca push and PR test runs both green after Brain merged.
- approvals: user approved scope/name, coordinated Brain/Mind changes, exact ship-time Heart YELLOW manifest-drift acknowledgement, all merges via prm, and public visibility. No release action.
- boundaries: Brain interprets evidence; Mind owns implementation lifecycle; Cortex owns science; Heart owns readiness. Public assistants remain independent. No paid or recurring benchmark execution configured.
- known limits: historic incomplete scorer/harness provenance prevents comparison; AutoCTI inventory finds no committed benchmark prompts; new response-quality baselines, deeper drift audits, project feedback and hosted publication remain future extensions rather than claims of this implementation.
- reconciliation: no stale task references remain. Intake flagged unrelated batch_slice.md, board_without_gh_phase2_legs.md and brain_board_follow_ups.md on resemblance only; retained for /intake reconcile draft/feature/pyautobrain.
- lifecycle: global check reports pre-existing unclaimed active/timing_noise_audit_phase1_inventory.md and a historical batch review-minutes warning; Broca-scoped lifecycle check passes.
- cleanup: validation screenshots/logs preserved at .artifacts/pyautobroca-assistant-management; committed data and dashboard retained in canonical Broca. Worktree removal follows lifecycle close.

## Original prompt

# Assistant evaluation and upkeep organ

Type: feature
Target: pyautobrain
Consequence: judge
Autonomy: human-required
Priority: normal
Status: active
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoBroca/issues/1

## Original requests (verbatim)

> I am considering if we need a dediciated PyAuto organ for assistant management. I now have 4 assistants, but I rarely check in on them, I put benchmarking in but dont run it and dont think benchmarks should be saved and stored results over time in the assistant (which is a public facing repo) anyway. I can imagine there are more things I would benefit from having an assistant dashboard. Thoughts?

> yeah lets do that, make sure the dashboard follows the format of others, thoughts on name?

## Intent and scope

Create a small dedicated organ owning assistant evaluation history, collection
receipts and a shared dashboard. Approved name: PyAutoBroca.
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

## Approval

User chose Broca and authorized execution: "do it, go". User explicitly allowed coordinated Brain/Mind changes, preserving board-one-click-update and pyautodna-stack-management.
