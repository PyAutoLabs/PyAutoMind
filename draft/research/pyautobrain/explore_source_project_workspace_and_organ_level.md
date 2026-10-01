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
Status: formalised
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
