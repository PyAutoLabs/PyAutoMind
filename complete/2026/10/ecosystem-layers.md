# ecosystem-layers

- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/440
- completed: 2026-10-01
- workspace-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/441
- commit: 9ae0db90518cedf4de558e79ad291d5af587e435
- merge-commit: 9e4c8064d4f56bb34b0a73f45416126f4d15c616

## Shipped scope

One non-normative research note, `PyAutoBrain/docs/research/ecosystem_levels.md`:
https://github.com/PyAutoLabs/PyAutoBrain/blob/9ae0db90518cedf4de558e79ad291d5af587e435/docs/research/ecosystem_levels.md

Recommends library/project/organ as responsibility roles rather than a strict
containment hierarchy, distinguishes those roles from repository categories and
release contracts, and maps visualization, profiling and inference ownership.
Includes an ownership diagram/table, three agent-routing examples, minimal
contract recommendations, staged follow-ups and a no-new-organ alternative.
Research complete; architecture adoption and organ implementation remain future
human decisions, not uncompleted scope of this task. No implementation prompts
were filed, no organs created, and no scientific campaigns run.

## Verification and review

- Local Sphinx HTML build: zero warnings (baseline 0).
- 32 citations to 17 commit-pinned source files verified; whitespace clean.
- Independent Claude Fable 5.1 final draft review CLEAN, after fixing gallery/
  dashboard routing, recording the Memory consultation, and clarifying role versus
  category semantics. The final reviewer report is preserved below.
- Committed artifact SHA256 matches the reviewed draft:
  `3345cd00f3354c428426ef87d9092ef7683ca570e5c3bb8941d1abc860ef9d0b`.
- GitHub CI: both runs and all three jobs completed successfully at the exact
  feature head: Docs 36900902139 (docs/docs-build); Brain Tests 36900900503
  (pytest 3.12 and 3.13). PR state MERGED confirmed; branch ancestry proven,
  zero commits ahead of origin/main. Scientific smoke N/A for prose-only change.

## Authorizations and boundaries

User approved the research plan, requested the independent Fable review, then
replied "yes do it" and "I authorize" to the task-specific development-only
Heart RED override. Exact RED reason: `release validation FAILED (stage integrate)`.
Shipping override was recorded on the issue, PR, active entry and autonomy log.
The user subsequently invoked `$prm`, separately authorizing merge and close-out.
No release, rehearsal, protection bypass or assertion that Heart became healthy.

## Evidence retention

The final review is included in this tracked record. Full reviewer JSONs,
intermediate reports, pinned-source snapshots, CI inventory and validation logs
are retained locally in `PyAutoMind/tmp/ecosystem-layers-review/` before worktree
cleanup. Generated HTML and Python caches are reproducible and need no retention.

## Independent final review

**Verdict: CLEAN.** The remaining must-fix from the previous review is resolved, the two accepted suggestions are correctly applied, and no regression was introduced. One optional wording note below is a preference, not a defect.

| Item | Value |
|---|---|
| Artifact | `PyAutoBrain/docs/research/ecosystem_levels.md`, untracked on `feature/ecosystem-layers`, base `c7bfd68` |
| SHA256 (caller-supplied, not recomputed) | `3345cd00f3354c428426ef87d9092ef7683ca570e5c3bb8941d1abc860ef9d0b` |
| Reviewer | Claude Fable 5.1, independent of the GPT-6 author, in-session, no delegation |

This is a local draft review, not a committed-head gate. No release-readiness opinion is given.

**Disposition of the remaining finding (category/role collision).** Resolved. The Project row at `docs/research/ecosystem_levels.md:75` now links the category contract, calls the role a superset rather than a rename, and states that the "no release mechanics" expectation does not transfer and that workspace release gates are unchanged. I verified each clause against the pinned snapshot, which is byte-identical to the worktree copy of `docs/satellites.md` at the base commit. Line 19 of that page gives the `project` category its "polled for state; no release mechanics" contract, and line 13 gives `workspace` its run_workspace, version-pin and required-CI gates. The new sentence "not every `category: project` entry is a measurement project" is true in the pinned body map, where PyAutoScientist and the Pages docs hub also carry that category. Routing step 1 at lines 140-143 preserves the registered category and workflow and forbids reading the role as a category filter, which closes the earlier failure scenario of an agent searching for a `category: project` repo to fix a workspace defect. The Workspace row and line 48 remain consistent with this.

**Other changes verified.**
- "Emits the wrong link" at line 169 no longer collides with the registry header and contract layering table, both of which say the organ renders nothing. The phrase appears in the rendered HTML.
- Lines 218-219 now keep plural agreement for future registries. Rendered.
- Citation mapping: 17 labels defined, all 17 used, 32 inline uses. The rendered page carries 32 pinned hrefs plus the issue link, and every URL matches its `research_sources.json` entry on repo, path and commit, including the new satellites entry. This agrees with the validation text. The build log reports success and the warnings log is empty.

**Optional, not a defect.** "A superset of the existing satellite categories" at line 75 reads literally as including the `library`, `organ` and `admin` categories too. The surrounding sentence and the separate Library and Organ rows make the intended referent obvious, so no routing error follows. Tightening it to "of the workspace-family and `project` categories" would be marginally more precise.

**Reused dispositions.** The Eyes split, Cortex model, existing-metadata, existing-layering and body-map role dispositions from the previous report are reused unchanged, since the sections they cover did not change. The Memory disposition at lines 285-288 is also unchanged and was accepted previously as matching the captured digest. The author's decision not to cite the two extra Memory hits was an optional suggestion and stands as their call.

**Adversarial claim pass.** There are no commit messages, so the claims surface is the validation text. Build and citation claims are basis-cited by the logs and my href count. "Operational history read before drafting" remains unverifiable from a repeated capture and is treated as idle, as before.

**Limitations.** No shell, so the SHA256 was not recomputed and the pinned snapshots were trusted as extracted. The memory-consultation capture was not re-read this pass. Live GitHub state after the pinned commits was not checked.

## Original prompt

# Explore source, project/workspace, and organ levels in the agentic ecosystem

Type: research
Target: PyAutoBrain
Repos:
- autolens_inference
- autolens_profiling
- autolens_visualization
- PyAutoBrain
- PyAutoEyes
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: issued
Issued: 2026-10-01
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/440
Consequence: judge
Review-minutes: 20
Unattended: ready

## Original user request (verbatim)

In promoting autolens_visualization to PyAutoEyes, I used the term "workspace" level. I think this has important
contexts, we are now building up layers of the ecosystem where there is a source code level, workspace
level (which includes stuff like profiling) and the organ level. I think a prompt which explores this and
works out if it can be built into the agentic AI design may yield fruit.  workspace level could also be
repo level, separate from the source code level.

Note also that I soon want to add a dashboard (and thus organ) for profiling (which pairs to autolens_profiling
and other _profiling repos) and for inference (which pairs to autolens_inference) and other inference repos.
These also feel like they help define the organ level, as they will have many repos at the repo or workspace level
which link to an organ and dashboard.

## Research question

Investigate whether explicit ecosystem levels would improve agent context selection,
ownership, routing, and human oversight. Treat the proposed levels as a hypothesis
and recommend useful terminology and boundaries, including a simpler alternative
if a strict hierarchy does not fit. This is one bounded architecture investigation,
not implementation of new organs or dashboards.

## Cases and questions

- Distinguish reusable source/library capabilities; project/workspace repositories
  that exercise them, run campaigns and produce evidence; and organs that own
  cross-project responsibilities, registries, durable state and human dashboards.
  Compare "workspace", "project", and "repo" for the middle level. Repositories
  and source code also exist at the other levels: separate packaging from role.
- Ground the proposal in visualization: library plotting code, the per-library
  visualization producers and artifacts, and Eyes' registry/dashboard. Check what
  was actually promoted or aggregated rather than assuming the producer disappeared.
- Work through planned profiling and inference organs, each connected to multiple
  corresponding project repos across libraries. Separate per-project run dashboards
  from cross-project organ dashboards. Keep proposed organ names undecided.
- Identify where scripts, manifests, results, provenance, freshness, judgments,
  execution and state belong. Examine Brain conductor/faculty responsibilities,
  Cortex science ledgers, Heart readiness and Mind intent to avoid duplicate owners.
  Compare the proposal with the existing rule that new organs require distinct
  state or effects; investigate when a dashboard warrants an organ.
- Decide whether relationships form a strict hierarchy or a graph: multiple
  projects per organ, possible multiple organ consumers per project, and organs
  such as Nerves that also provide library code. Do not force every organ into
  an evidence-aggregation template.
- Show how an agent would use the distinction: selecting minimal context, locating
  the authoritative owner, reading evidence, deciding the correct action scope,
  and routing a finding back to library or project work with provenance. Preserve
  existing development and human decision gates; do not assume a level requires
  its own LLM agent or extra delegation.

## Evidence and related work

Start from Brain's ORGANISM.md and Mind's repos.yaml, then read only relevant
Eyes contracts and profiling/inference project instructions. Consult Memory for
prior architectural decisions before finalizing recommendations. Distinguish
verified current arrangements from planned capabilities.

Related existing task (Mind-relative):
`draft/feature/pyautobrain/register_profiling_dashboard_on_brain_board.md`.
That task registers a project profiling dashboard and explicitly excludes organ
birth. This research should complement it and identify dependencies, not repeat it.

## Deliverable and acceptance criteria

Produce one cited design note with:
1. A recommended vocabulary, comparison of plausible alternatives, and explicit
   reasons for adopting or rejecting levels in the agentic design.
2. An ownership/relationship diagram and responsibility table, exercised against
   visualization, profiling and inference, including counterexamples and overlaps.
3. Concrete agent-routing examples: a visualization defect, profiling drift, and
   an inference benchmark finding, from evidence to the responsible next action.
4. A minimal proposal for any registry metadata, read contracts, agent instructions
   or routing changes, identifying canonical owners and avoiding parallel registries.
5. A staged follow-up recommendation for profiling/inference organs and general
   wiring, with dependencies, open human decisions, and a no-change option.

Do not create organs, run campaigns, change code or registries, or implement the
proposed design as part of this research task. The result should support a human
architecture decision before separately scoped implementation work.

<!-- formalised by the Intake (Conception) Agent on 2026-10-01 from file:../PyAutoMind/tmp/ecosystem_layers_intake.md -->
