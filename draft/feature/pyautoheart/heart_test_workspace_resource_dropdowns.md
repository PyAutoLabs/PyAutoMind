# Heart test workspace resource dropdowns

Type: feature
Epic: scientist-adoption-pilot
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoScientist
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready

Give each registered `_workspace_test` repository its own discoverable expandable row on @PyAutoHeart's dashboard, grouped sensibly by project. Explain what that test workspace checks and why it belongs on Heart. The current Scientist-to-Heart link does not make this relationship clear.

## Useful content to select from existing evidence

Keep the collapsed row concise: repository name, project/purpose and current evidence state. Expanded content should show the latest relevant validation run, source revision, timestamp/freshness, pass/fail/skip counts and coverage, outstanding failures/skips with log or issue links, repository/suite links, and the next useful check-in or action. Only show dimensions Heart can substantiate; label unavailable fields honestly. Distinguish CI, smoke/regression/parity evidence and full release validation where relevant rather than inventing one combined verdict. Summaries remain subordinate to Heart's authoritative readiness logic; this navigation task must not change release gates or expand execution scope.

## Acceptance

- Each registered test workspace has its own native accessible dropdown, clearly linked to its project and source.
- Representative healthy, failing, stale and unavailable evidence renders honestly with useful destinations.
- A resource-specific anchor/deep link makes the Scientist relationship understandable and opens the right row.
- Desktop/phone, keyboard, no-JavaScript fallback and refresh preservation are verified.
- No new test campaign, generated fake evidence or readiness-policy change.

Existing `howto_real_settings_nightly.md` concerns a separate execution campaign: do not absorb or dispatch it here.

## Shared context and constraints

Scientist PR #58 added organ-linked project resource rows. Those links currently lead to broad boards without an obvious resource-specific destination. Reuse Mind's canonical repository identities and Scientist's explicit resource relationships. Keep names and paths configurable; do not infer identity from suffixes. Reuse shared board disclosures, navigation and responsive components. Resource sources stay in their existing repositories; link evidence instead of copying a competing ledger. Opening a dropdown must not run tests, models, tutorials, publication or paid work.

At start-dev inspect current board capabilities and existing work before implementing. Preserve unknown/stale/absent distinctions and scope. Missing evidence is not a passing result. Use stable resource anchors so a Scientist link can eventually open the relevant expanded row; include the minimal Scientist follow-up if required, with its own claimed branch/PR. This intake does not start implementation.

## Original request (verbatim)

intake a prompt to have _test workspaces have their own drop down on Heart with whatever information makes ene, I dont think that link is clear yet. Same for Broca and all the stuff listed including HowTo

<!-- formalised by the Intake (Conception) Agent on 2026-10-11 from file:organs/PyAutoMind/tmp/resource-dropdown-intake/heart.md -->

## Sizing and scope note

Medium assumes a bounded owner-board presentation change using available evidence, with minimal Scientist deep-link integration if needed. No edits to HowTo/tutorial/test workspace sources are planned. Broader evidence ingestion or schema migration must remain in the existing roadmap or be sliced at start-dev.
