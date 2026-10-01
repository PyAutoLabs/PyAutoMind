# Adopt ecosystem responsibility roles and reconcile Brain documentation

Type: docs
Target: @PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Consequence: judge
Filed: 2026-10-01
Status: issued
Issued: 2026-10-01
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/442

## Original user request (verbatim)

continue

## User's selected continuation (verbatim)

Adopt the terminology and reconcile existing documentation (recommended)

## Context and accepted direction

Follow the research merged in PyAutoBrain#441 (issue #440), documented in
`docs/research/ecosystem_levels.md`; Mind completion record
`complete/2026/10/ecosystem-layers.md`. The human selected adopting the terminology
and reconciling existing documentation. This accepts library/project/organ as
responsibility roles; repository remains packaging. Existing repository categories
and their validation/release contracts remain authoritative and unchanged.

## Scope

1. Update `ORGANISM.md` first: define the roles and relationships, account for
   Nerves as both organ and library package, and correct Eyes' row and growth
   example to the current project-manifest/dashboard split. Project repos own
   render harnesses and figure artifacts; Eyes owns registry/read contract and
   dashboard; the Brain conductor judges.
2. Reconcile `docs/concepts/organism.md` with that canonical definition, including
   the stale Eyes table and framework/instance prose about rendered figures.
   Link to the canonical owner rather than inventing parallel policy.
3. Add a concise distinction in `docs/satellites.md`: responsibility role is not
   a body-map category, not a category: project filter, and not a change to
   workspace release gates. Link the role definition.
4. Check `docs/organs/eyes.md` and relevant Brain docs for contradictions; change
   only text needed to reconcile these boundaries. Keep the dated research note
   as the historical proposal rather than rewriting its pinned observations.
5. Build Sphinx with no warning regression and check links/source-of-truth
   consistency. Review the adoption wording independently before shipping.

## Boundaries and related work

No code/schema/registry changes, repository renames, new agents, new organs or
new dashboards. Agent routing trials and profiling/inference organ specifications
remain later tasks. Existing generated map rows already describe the correct Eyes
split; use the generator if a generated surface actually needs changing, and report
any expansion in affected repos before proceeding.

`draft/docs/pyautobrain/rtd_organism_currency.md` covers a Nerves page, count drift
and the build/hands URL decision; leave those unrelated changes and its prompt intact.
Stale Cortex references in inference are a separate follow-up:
`draft/docs/autolens_inference/reconcile_cortex_ledger_references.md`.
That repo is currently claimed by `point-source-search-nautilus-leaf`; do not edit it
or take its claim for this Brain-only task.

## Acceptance

The canonical definition and public docs agree on the three roles, explicitly
preserve categories/release semantics, and describe Eyes consistently with its
current read contract. Sphinx warning baseline remains zero. No implication that
profiling/inference organs already exist or that the routing trial has been adopted.
