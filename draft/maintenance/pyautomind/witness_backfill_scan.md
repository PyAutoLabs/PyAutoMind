# Witness backfill: scan Mind drafts with no Witness: and propose one each for the human to declare

Type: maintenance
Target: PyAutoMind
Repos:
- PyAutoMind
Themes:
- dashboard
- autonomy
Difficulty: medium
Autonomy: supervised
Priority: normal
Consequence: judge
Witness: a review page in Science/scratch/witness_backfill_<date>/ lists every `draft/**/*.md` (outside epic `*_reviews/` and `*_surveys/` folders) whose headers carry no `Witness:` line — 115 on origin/main e9c34daa4 — each with a proposed mechanical witness or a "cannot be witnessed mechanically" note; no draft gains a `Witness:` line until the human has ticked it on that page, and after the accepted ones are written `grep -L '^Witness:'` over the same set drops by exactly the number ticked
Review-minutes: 30
Unattended: never
Lane: local-dev
Filed: 2026-11-16

## Why

The 2026-11-16-pm shift brief had to exclude backlog picks because they carried
no `Witness:` and would be reviewed as `judge` (`ai_options_page_autolens_leg`,
`positions_source_jacobian_default_rerun_note`; the 2026-11-14-pm3 brief did the
same). The human, 2026-11-16: "maybe we intake a prompt scan mind and fix all
these?". 115 drafts lack the line (bug 26, docs 16, feature 34, maintenance 9,
research 15, refactor 4, test 4, human_review 3, release 2, triage 2).

## Constraint

Witnesses are **human-declared** (the 2026-09 witness campaign,
`complete/2026/09/witness-campaign.md`). An agent proposes; the human declares.
So this task never writes a `Witness:` line the human has not ticked.

## Steps

1. List the drafts with no `Witness:` header (skip epic campaign maps, which
   carry their own phase witnesses, and `*_reviews/` / `*_surveys/` files).
2. For each, read the body and propose one mechanical check that fails today and
   passes when the work is done (a command, a grep, a test name), or mark it
   "not mechanically witnessable" with one line why (most `research` drafts).
3. Put them on one review page in `Science/scratch/witness_backfill_<date>/`,
   grouped by work type, cheapest-to-review first, each with tick / edit / skip.
4. After the human's review, write the accepted witnesses into the drafts in one
   Mind commit through a temp worktree on origin/main (never the shared checkout).
