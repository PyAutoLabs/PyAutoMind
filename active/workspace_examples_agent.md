# Workspace Examples Agent — one Brain agent for workspace + HowTo example authorship

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

## Intent (original request, condensed)

PyAutoReduce will soon gain `autoreduce_workspace` / `autoreduce_workspace_test`,
mirroring the design, functionality and purpose of the existing workspaces
(autolens_workspace, autogalaxy_workspace). Workspace conventions: scripts follow
a specific contents + Python-docstring format used to generate their markdown and
Jupyter-notebook docs; they are the user-facing docs giving end-to-end scientific
examples for most high-level tasks; and they are the core scientific context that
trains the domain assistants (e.g. autolens_assistant). Working workspace examples
is becoming a common task in development workflows after source-library
extensions, so @PyAutoBrain needs a dedicated agent for it. Assess whether the
same agent can also cover the HowTo repos (HowToFit/HowToGalaxy/HowToLens — same
structure/format, but written at a lower level for first-time learners such as
undergrads and new PhD students), or whether a separate HowTo agent is needed.

## Assessment: one agent, two registers (decided at intake, revisit at start_dev)

One agent covering both, with an explicit `workspace` vs `howto` audience
register, is the right shape:

- ~90% of the machinery is identical: the contents+docstring format spec, the
  markdown/notebook generation conventions, the start_workspace → ship_workspace
  pipeline, API grounding against the installed stack, and the
  assistant-training role. Two agents would duplicate the format spec — a drift
  hazard the workspace's single-source-of-truth rule exists to prevent.
- PyAutoBrain doctrine agrees: "new agents are added on demonstrated need,
  never for symmetry"; there is no demonstrated HowTo-specific need yet, only a
  register difference. WORKFLOW.md already treats HowTo repos as workspace repos
  in the same pipeline, and its tutorial-prose split already places `howto*`
  prose in the judgment tier alongside workspace tutorials.
- Modes are the established pattern for one conductor with variant behaviour
  (build: build/deploy/release; profiling: campaign/ingest/triage).
- Split trigger (record in the agent's AGENTS.md): promote HowTo to its own
  agent only when it develops a decision surface the workspace register cannot
  share — e.g. curriculum/chapter-continuity planning, exercise design, or
  learner-feedback state. Until then it is a register, not an organism function.

## Design questions for start_dev

1. **Conductor vs faculty.** The authoring itself is dev work the existing
   `start_dev → start_workspace → ship_workspace` flow already executes; what is
   missing is specialist reasoning (where an example belongs, format/register
   checklists, coverage gaps after a library change). That is a read-only
   opinion → the Brain's tier rule suggests a **faculty** (an ExamplesSurface
   consulted by the `/docs` work-type entry and ship_workspace), not a new
   conductor. A conductor is only justified if it must decide-and-dispatch
   (e.g. select the next coverage gap and route it into start_dev, like the
   Feature Agent). Decide the tier explicitly before wiring.
2. What the decision object contains: target repo + package placement,
   format checklist, audience register, phasing, downstream-notebook impact.
3. How the format spec is grounded — point at the canonical spec/generator in
   the workspace repos / PyAutoBuild rather than restating it in prose.
4. autoreduce_workspace bootstrap: the new agent/faculty should serve the
   autoreduce workspace's creation as its first demonstrated-need case.

## Deliverables

- The one-vs-two assessment recorded (this file, refined if start_dev disagrees).
- The new Brain agent (conductor or faculty per question 1) under
  `PyAutoBrain/agents/`, with AGENTS.md, deterministic entrypoint, and the
  workspace/howto register distinction documented.
- Command-surface wiring only if a conductor: verb + skill body; a faculty
  stays consult-only behind `/docs`.

<!-- formalised via /intake on 2026-07-16 (intake classifier misrouted to
docs/autoreduce; header hand-fixed per feedback_intake_target_handfix) -->
