# Broca communication resource dropdowns including HowTo

Type: feature
Epic: scientist-adoption-pilot
Target: PyAutoBroca
Repos:
- PyAutoBroca
- PyAutoScientist
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: in-progress
Consequence: judge
Review-minutes: 20
Unattended: claimed

Give the project communication resources listed on Scientist their own discoverable expandable rows on @PyAutoBroca's dashboard: assistants, user-facing workspaces, documentation and HowTo tutorials (including HowToFit, HowToGalaxy and HowToLens where registered). The current Scientist-to-Broca link does not make the individual resources or their relationship clear. Group by project and resource type without requiring an assistant.

## Useful content to select from existing evidence

A concise collapsed row names the resource, audience/purpose and observed upkeep state. Its dropdown links the source, published docs/tutorial entry where applicable, project/shared dependencies, relevant source revision and last collected evidence date, available upkeep/evaluation results, known gaps and a concrete next action/check-in prompt. Show inventory, technical validation, freshness and explanatory quality separately: a successful docs build or runnable tutorial is not proof of quality. Preserve immutable assistant history; use existing cheap evidence and show unknown when none exists. Explain What is this? / Where do I start? before technical detail.

## Acceptance

- Docs, HowTo tutorials, workspaces and assistants have first-class resource dropdowns and stable deep links, with no assistant prerequisite.
- Include a project with several resource types and one without an assistant; shared resources retain one identity.
- Scientist can link to the appropriate resource context rather than an unexplained generic board landing.
- Source ownership, private visibility, evidence freshness and missing-data handling are preserved; browser accessibility and responsive behavior are checked.
- No universal score, new evaluation campaign, external message or publication action on expansion/refresh.

## Relationship to existing Broca work

This is the bounded navigation/presentation slice of `broca_communication_pilot.md`, under the existing programme `broca_communication_documentation_and_workspaces.md`. Coordinate with `broca_communication_contract.md` before implementing expanded responsibility; reuse its inventory schema when available. Do not duplicate the broader inventory/evidence migration or require its entire roadmap for useful rows. Heart retains technical validation/readiness, Ears listening, Memory knowledge, Cortex science, Eyes figure evidence and Hands build/release execution. Broca can link Heart's execution evidence for a HowTo while owning its learning/communication view.

## Shared context and constraints

Scientist PR #58 added organ-linked project resource rows. Those links currently lead to broad boards without an obvious resource-specific destination. Reuse Mind's canonical repository identities and Scientist's explicit resource relationships. Keep names and paths configurable; do not infer identity from suffixes. Reuse shared board disclosures, navigation and responsive components. Resource sources stay in their existing repositories; link evidence instead of copying a competing ledger. Opening a dropdown must not run tests, models, tutorials, publication or paid work.

At start-dev inspect current board capabilities and existing work before implementing. Preserve unknown/stale/absent distinctions and scope. Missing evidence is not a passing result. Use stable resource anchors so a Scientist link can eventually open the relevant expanded row; include the minimal Scientist follow-up if required, with its own claimed branch/PR. This intake does not start implementation.

## Original request (verbatim)

intake a prompt to have _test workspaces have their own drop down on Heart with whatever information makes ene, I dont think that link is clear yet. Same for Broca and all the stuff listed including HowTo

<!-- formalised by the Intake (Conception) Agent on 2026-10-11 from file:organs/PyAutoMind/tmp/resource-dropdown-intake/broca.md -->

## Sizing and scope note

Medium assumes a bounded owner-board presentation change using available evidence, with minimal Scientist deep-link integration if needed. No edits to HowTo/tutorial/test workspace sources are planned. Broader evidence ingestion or schema migration must remain in the existing roadmap or be sliced at start-dev.

## Coordinated implementation

Tracked by `active/organ_resource_dropdowns.md` (Scientist issue #65). Do not start a duplicate task: Heart, Broca and Scientist share one coordinated branch set. Broader evidence ingestion remains separate.
