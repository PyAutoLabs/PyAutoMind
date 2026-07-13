# PyAutoBrain Clone Agent (Mitosis Agent) to generate new assistants

Type: feature
Target: PyAutoBrain
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Design (not yet implement) a future PyAutoBrain agent that can generate new
domain assistants modelled on autolens_assistant.

Naming: the engineering term is **Clone Agent** (CLI: `pyauto-brain clone`);
the organism-facing name is **Mitosis Agent** — the agent that lets the PyAuto
organism reproduce a mature assistant cell, copying its core machinery and
then differentiating it for a new organ/domain. `clone` is the better CLI
name; Mitosis Agent is the nicer architecture name for docs.

## Inputs

- a source library repo, e.g. PyAutoFit;
- a workspace repo, e.g. autofit_workspace;
- an optional HowTo repo, e.g. HowToFit;
- the reference assistant repo, initially autolens_assistant.

It produces a new domain assistant modelled on autolens_assistant (e.g.
autofit_assistant, autogalaxy_assistant, autoarray_assistant).

## Behaviour

The Clone / Mitosis Agent should:

- inspect the source library, workspace examples and optional HowTo tutorial
  material;
- identify the domain concepts, APIs, workflows and user audiences;
- copy the assistant architecture without blindly copying PyAutoLens-specific
  science;
- generate appropriate AGENTS.md, README, skills, wiki structure, source
  registry and project workflow;
- distinguish generic assistant infrastructure from domain-specific content;
- produce a **CloneDecision** before writing anything;
- ask whether this is an exact clone, a differentiated sibling, or a
  lightweight seed assistant;
- preserve the PyAuto organism boundary:
  - PyAutoMind stores the intent to create the assistant;
  - PyAutoBrain reasons and plans the clone;
  - PyAutoBuild/Hands executes repository creation and file generation;
  - PyAutoHeart validates the resulting assistant;
  - PyAutoMemory supplies reusable architectural knowledge.

## Prerequisite

The autolens_assistant audit prompt (filed separately) should land first: it
makes the reference assistant the clean canonical pattern this agent clones,
and leaves notes on which parts are PyAutoLens-specific vs generic assistant
infrastructure.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/3690563e-5959-43ff-b131-b00fe70bd60c/scratchpad/intake_2_mitosis_agent.md -->
