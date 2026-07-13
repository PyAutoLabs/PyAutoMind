# So I’d document it as

Type: feature
Target: PyAutoBrain
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

So I’d document it as:

Feature Agent, the growth function of PyAutoBrain.

Here’s the prompt.

Implement the PyAutoBrain Feature Agent.

Context

The PyAuto ecosystem is evolving into a software organism.

Current architecture:

PyAutoMind
Stores intent, goals, prompts, priorities and future work.
PyAutoBrain
Contains specialist reasoning agents.
PyAutoMemory
Stores accumulated scientific, software and project knowledge.
PyAutoHeart
Performs health checks and readiness validation.
PyAutoBuild
Executes build, development and release workflows.
This may later become PyAutoHands.

The Feature Agent is the PyAutoBrain agent responsible for deciding how the organism should grow.

It reasons over feature work.

It does not directly implement code unless explicitly delegated through the existing development workflow.

Goal

Implement the initial Feature Agent.

The Feature Agent should:

select suitable feature tasks from PyAutoMind,
accept an explicitly requested feature task,
select tasks by difficulty or available model capability,
decide whether a task is too large and must be phased,
use PyAutoMemory for scientific and architectural context,
integrate closely with the existing development lifecycle:
start_dev
ship_library
ship_workspace
coordinate with Health Agent and Build Agent where appropriate.
Core responsibilities

The Feature Agent should support three modes.

1. Specific task mode

The user provides a specific PyAutoMind prompt or issue.

The Feature Agent should:

read the task,
inspect relevant context,
consult PyAutoMemory,
classify target repositories,
decide whether it is ready for development,
produce a plan compatible with start_dev,
identify whether library work, workspace work, or both are required.
2. Task selection mode

The user asks the agent to choose what to work on.

The Feature Agent should:

inspect PyAutoMind priorities, queues and available prompts,
consider project priorities,
consider repository health,
consider recent work,
consider dependencies between tasks,
choose the best next feature task,
explain why it selected that task.

It should not simply pick the first prompt in a list.

3. Difficulty-constrained mode

The user specifies constraints such as:

choose an easy task,
choose a high-impact task,
choose something suitable for a weak model,
choose something suitable for a strong model,
choose something that can be done with limited tokens,
choose something ambitious for an overnight run.

The Feature Agent should estimate task difficulty and select accordingly.

Difficulty should consider:

number of repositories affected,
amount of code likely to change,
scientific complexity,
architectural risk,
test burden,
documentation burden,
whether PyAutoMemory context is required,
whether the task requires human judgement.
Task sizing and phasing

The Feature Agent must explicitly decide whether a task is:

small enough to implement directly,
medium and suitable for one PR,
large and should be split into phases,
too ambiguous and should become a research/design task first.

If a task is too large, it should produce phased feature prompts.

For example:

feature/autofit/sbi_phase_1_design.md
feature/autofit/sbi_phase_2_core_api.md
feature/autofit/sbi_phase_3_workspace_examples.md
feature/autofit/sbi_phase_4_docs.md

Each phase should be independently shippable.

Prefer multiple small PRs over one large fragile PR.

Relationship to PyAutoMind

PyAutoMind stores intent.

The Feature Agent reasons over that intent.

It should understand the PyAutoMind taxonomy, including paths such as:

feature/autolens/...
feature/autofit/...
feature/autoarray/...
research/autofit/...
experiment/autoarray/...

If the task belongs in another category, the Feature Agent should say so.

For example:

unclear science → research task
proof-of-concept → experiment task
behaviour fix → bug task
internal cleanup → refactor task
release/versioning → release/build task

The Feature Agent should help keep PyAutoMind organised.

Relationship to PyAutoMemory

Before planning substantial scientific or architectural feature work, the Feature Agent should consult PyAutoMemory.

Use PyAutoMemory to gather:

scientific background,
prior design decisions,
relevant papers or summaries,
known architectural constraints,
previous related work,
project-specific context.

The Feature Agent should cite or summarise which memory sources influenced the plan.

Do not invent scientific context if PyAutoMemory has relevant material.

Relationship to development workflow

The Feature Agent should pair closely with the current PyAuto development lifecycle.

It should know when to use or recommend:

start_dev
start_library
start_workspace
ship_library
ship_workspace
pyauto-status
handoff
active / planned / complete task tracking

The Feature Agent should not bypass this workflow.

It should produce outputs that can be consumed by existing commands and skills.

For library-only work:

start_dev -> start_library -> ship_library

For workspace-only work:

start_dev -> start_workspace -> ship_workspace

For combined work:

start_dev -> library branch/PR -> workspace branch/PR -> ship both in order

The agent should explicitly identify which path applies.

Relationship to Health Agent and Build Agent

Before recommending that work proceed, the Feature Agent should consult or request a health assessment where appropriate.

Use the Health Agent when:

repository health is unknown,
a task is risky,
a task affects multiple repositories,
a task is intended for release,
previous checks have failed.

Use the Build Agent / PyAutoBuild when:

development execution should begin,
PR creation is needed,
packaging or release steps are needed,
the task is ready to move from planning into action.

The Feature Agent reasons.

PyAutoBuild executes.

PyAutoHeart measures health.

Output format

The Feature Agent should produce a structured decision.

Include:

Selected task:
<path or description>

Mode:
specific | selection | difficulty-constrained

Why this task:
<reasoning>

Difficulty:
small | medium | large | too-large

Recommended workflow:
library | workspace | combined | research | experiment | refactor | bug

Relevant context:
<PyAutoMemory context used>

Phase decision:
direct | split-into-phases | research-first | defer

Execution plan:
<steps compatible with start_dev / ship_library / ship_workspace>

Health considerations:
<when Health Agent should be consulted>

Risks:
<main risks>

Next action:
<single concrete next step>
Claude skill constraints

If implemented as a Claude skill or markdown agent definition:

keep every .md file below 200 lines,
follow Claude skill guidelines,
keep the main instruction file concise,
move long examples and architecture notes into supporting docs,
avoid large essays inside the skill file.
Validation

Run available tests or smoke checks.

Validate that:

the Feature Agent can identify feature prompts in PyAutoMind,
it can select a task when none is specified,
it can respect difficulty constraints,
it can recommend phasing for large tasks,
it references PyAutoMemory where appropriate,
it outputs plans compatible with the current development workflow.
PR

Create one PR titled:

Implement initial PyAutoBrain Feature Agent

My only tweak would be: long term, I’d maybe have Growth Agent as the organism-facing name and Feature Agent as the engineering-facing name. But for Codex and repo clarity, Feature Agent is the safer first implementation.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
