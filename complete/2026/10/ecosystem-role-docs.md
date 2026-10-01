# ecosystem-role-docs

- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/442
- completed: 2026-10-01
- workspace-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/443
- commit: 6a124d948a715bf26134e6ffba09e06750f19921
- merge-commit: 0f7831b8a73641bb0add82ac3ed02d2edf565153

## Shipped

Adopted library/project/organ responsibility vocabulary in Brain's canonical
ORGANISM.md, distinguished it from repository packaging and body-map categories,
and reconciled Eyes ownership across public docs and its skill boundary.

Changed ORGANISM.md, docs/concepts/organism.md, docs/satellites.md,
docs/organs/eyes.md and skills/eyes/eyes.md. Project repos render and retain figures
and manifests; Eyes owns registry/read contract/dashboard; Brain conducts judgment.
Existing categories/release rules, skill commands, schemas and runtime behavior
remain unchanged. The research note from #441 remains a pinned historical proposal.
No routing trial or profiling/inference organ was implemented.

## Validation and authority

- Sphinx build: zero warnings (baseline 0); links/anchors and whitespace checked.
- Independent Claude Fable 5.1 final working-tree review CLEAN. All five committed
  files match the reviewed hashes; no claim that Fable reviewed a committed head.
- CI at feature head 6a124d9: Docs run 36914488774 (docs/docs-build) and Brain Tests
  run 36914487669 (pytest 3.12 and 3.13), all completed successfully.
- PR state MERGED confirmed; feature branch is an ancestor of origin/main with
  zero commits ahead. Scientific smoke not applicable to Markdown-only changes.
- Heart GREEN at shipping, score 100, no reasons (2026-10-01T19:24:04.745228+00:00).
  Earlier YELLOW checkpoint cleared before shipping; no override was used.
- Human approved the plan ("contiue and i approve") and separately invoked `$prm`
  to authorize merge and full close-out. No release/rehearsal or CI bypass.

## Follow-ups retained

`draft/docs/autolens_inference/reconcile_cortex_ledger_references.md` remains
separate, waiting for the existing inference repo claim to clear. Its link to
this adoption prompt is repointed to this completion record at close-out.
`draft/docs/pyautobrain/rtd_organism_currency.md` has separate Nerves-page/count/URL
scope and is not retired by this merge. Routing trials and new organ designs
remain future work, not uncompleted scope of this task.

## Evidence

Final independent review preserved below. Full review JSONs, source snapshots,
working-tree diff, hashes, CI inventory and build logs retained locally under
`PyAutoMind/tmp/ecosystem-role-docs-review/` before worktree removal. Generated HTML
and Python caches are reproducible and were not retained.

## Independent final review

**Verdict: CLEAN**

Reviewed on Fable 5.1 in-session, read-only. Scope is the five-file uncommitted working-tree diff in `../proposed.diff` against base 9e4c806, checked line for line against the live files. No committed diff is ahead of base, so no committed-head claim is made.

## Prior finding: resolved

The one must-fix from the prior review is closed. `skills/eyes/eyes.md:91-94` now assigns rendering, figure storage and manifests to the `<lib>_visualization` project repos, and registry, read contract and dashboard to PyAutoEyes. This matches `ORGANISM.md:19`, the Eyes contract layering table (`../review-sources/eyes-contract.md` lines 12-14), and the Eyes conductor's own AGENTS.md lines 7-10 and 95-97. A grep across the Brain repo finds no remaining text saying the organ renders or holds figures. The only hit is the research note's pinned historical observation, which the task says to keep. The clause is boundary prose only. Commands, steps, dashboard routes and the paper pass are byte-unchanged, so this stays inside scope item 4 and introduces no routing trial.

## Clarity changes: consistent

- **howto.** `ORGANISM.md:57` and `docs/satellites.md:11` now name the same three category groups in the same order. The rendered `satellites.html` line 277 carries the new wording, so the build reflects the current tree.
- **role / public_role.** `ORGANISM.md:64-65` now says the body-map strings are descriptive text, not a classification. This matches `../review-sources/body-map.md` usage and does not touch the generator, which hard-codes its invariants.
- **Eyes page.** `docs/organs/eyes.md:3` replaces the undefined "perception lifecycle" with "cross-project visualization view". The phrase has no remaining definition anywhere in the repo, and the rendered `eyes.html` line 270 shows the new text. The "perception mirror of the Heart" sentence on lines 9-11 survives and is consistent with the Eyes conductor doc.

## Regression check

- **Links.** `ORGANISM.md#responsibility-roles` is referenced from `docs/concepts/organism.md:29` and `docs/satellites.md:10` and appears in both rendered pages. The in-repo relative link at `ORGANISM.md:61` resolves. Both `{doc}` references in the concepts page resolved in the prior build and that file is unchanged since.
- **Single source.** Only ORGANISM.md defines the roles. The concepts page, satellites page and Eyes page link and summarise without adding policy. The generated AGENTS.md Eyes row already matched the split, so no regeneration is needed.
- **Categories.** The satellites category table and release expectations are unchanged. Growth-rule text at `ORGANISM.md:112-113` restates the existing rule and implies no new organ.
- **Scope.** Git status lists only the five markdown files. The research note is untouched.

## Claim dispositions

- claim: "must-fix Eyes skill contradiction resolved" → basis-cited: `skills/eyes/eyes.md:91-94` against `ORGANISM.md:19` and the contract table; repo-wide grep shows no residual contradiction.
- claim: "commands and workflow unchanged" → basis-cited: the skill hunk touches only the Boundary bullet; lines 1-88 and 95-96 are identical to the base copy.
- claim: "Sphinx HTML PASS, zero warnings" → basis-cited: empty warnings log and "build succeeded" at `sphinx-build.log:34`. The log shows an incremental build re-reading only organs/eyes and satellites. Other sources were last built clean in the earlier full run and have not changed since, so this is adequate but not a clean full rebuild.
- claim: "category table/release contracts unchanged; no executable/schema/registry/inference changes; research note unchanged" → basis-cited: git status and the diff file list; satellites.md hunk inserts above the table only.
- claim: "whitespace PASS" → idle; not load-bearing.
- Prior dispositions on Eyes ownership, Nerves overlap and category text are reused unchanged. The three files they rest on were either untouched since or changed only in the hunks inspected above.

## Verification and limits

I read the review contract, all five working-tree files, the base skill copy, the Eyes contract, the task prompt, validation.txt, both Sphinx logs and the rendered HTML for the three affected pages. I did not recompute the hashes in `review-final-hashes.json`, did not re-run Sphinx, did not run the review script, and did not test live GitHub anchors. No release-readiness opinion is offered.

## Optional preferences (not blocking)

- `ORGANISM.md:58-59` has no blank line between "them." and "The category in", so the workspace sentence and the category sentence render as one paragraph. A blank line would separate the two ideas.
- `ORGANISM.md:63` wraps past the file's usual line width. Cosmetic.
- The pre-existing "domains" registry claim at `docs/organs/eyes.md:38` remains out of scope, as the caller stated.

## Original prompt

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
