Redesign PyAuto development workflow skills for the PyAutoBrain era.

Context

The PyAuto ecosystem is evolving into a software organism.

Current architecture:

PyAutoMind
Stores intent, prompts, tasks, priorities and workflow state.
PyAutoBrain
Performs reasoning through specialist agents.
PyAutoHeart
Performs health checks and readiness validation.
PyAutoBuild
Executes build, release and development operations.
This may later become PyAutoHands.

The existing workflow skills include:

start_dev
start_library
start_workspace
ship_library
ship_workspace
pyauto-status
handoff

These skills were created before PyAutoBrain became the central reasoning layer.

They now need to be reviewed and redesigned so that all development reasoning happens at the PyAutoBrain level.

Goal

Modernise the PyAuto development workflow skills so they align with the organism architecture and with PyAutoBrain specialist agents.

The core rule is:

PyAutoBrain reasons.

PyAutoBuild executes.

PyAutoHeart checks health.

PyAutoMind stores intent and workflow state.

Scope

Review and improve:

start_dev
start_library
start_workspace
ship_library
ship_workspace
pyauto-status
handoff
any closely related workflow skills or commands
Required architectural changes
1. Make PyAutoBrain the development reasoning layer

Development work should now be coordinated by PyAutoBrain agents.

Existing skills should no longer act as standalone reasoning systems.

They should either:

become PyAutoBrain agent entry points,
call PyAutoBrain agents,
or become thin execution wrappers around PyAutoBuild / PyAutoHeart / PyAutoMind.

For example:

start_dev
    should route through Feature Agent / Bug Agent / Refactor Agent as appropriate.

ship_library / ship_workspace
    should route through Build Agent and Health Agent before execution.

'd add a new section after the PyAutoBrain section:

1.5 Integrate PyAutoMemory throughout the workflow

The redesigned workflow should treat PyAutoMemory as the organism's long-term knowledge.

Workflow skills should consult PyAutoMemory whenever historical, scientific or architectural context would improve decisions.

Examples include:

previous architectural decisions,
scientific background,
literature summaries,
prior implementations,
previous failed approaches,
coding conventions,
project history,
design rationale.

The workflow should encourage PyAutoBrain agents to consult PyAutoMemory before making substantial planning decisions.

Typical interactions include:

Feature Agent
retrieves scientific and architectural context before planning a feature.
Build Agent
retrieves previous release history or deployment guidance when needed.
Health Agent
retrieves historical health trends, previous failures or recurring issues where useful.

The workflow should make it easy for future Brain agents to use PyAutoMemory without tightly coupling to its internal implementation.

Document PyAutoMemory as the organism's accumulated knowledge, distinct from PyAutoMind:

PyAutoMind stores what the organism intends to do.
PyAutoMemory stores what the organism has learned.

I'd also modify the architecture block at the top of Prompt 2 to include:

Current architecture:

- PyAutoMind
    Stores intent, prompts, priorities and workflow state.

- PyAutoMemory
    Stores long-term scientific, architectural and project knowledge.

- PyAutoBrain
    Performs reasoning through specialist agents.

- PyAutoHeart
    Performs health checks and readiness validation.

- PyAutoBuild
    Executes build, release and development operations.

One thought that occurred to me while we've been designing this: the architecture is starting to mirror a real cognitive system.

Mind
    What do I want?

Memory
    What do I know?

Brain
    What should I do?

Heart
    Am I healthy enough?

Build/Hands
    Do it.

That's a surprisingly complete model. More importantly, it gives every repository a single, unambiguous responsibility. That's usually a sign you've found a strong software architecture, not just a nice metaphor.

2. Preserve existing command names

Do not break existing user workflows.

Commands such as:

/start_dev
/ship_library
/ship_workspace

should continue to work.

But internally, they should delegate to the new organism architecture.

3. Remove Remote / mobile mode as a major workflow concept

The old skills may contain a "remote mode" or "mobile mode" subsection.

This should be removed or demoted.

Mobile / web-only work is no longer a special mode.

PyAutoBrain can operate in:

Claude web,
Codex web,
GitHub-only environments,
local Claude Code,
local development environments.

Therefore, replace "remote/mobile mode" with a more general environment model.

Suggested terminology:

Execution environment:
- local-dev
- web-github
- ci-only
- analysis-only

Make clear that PyAutoBrain may be used in Claude or Codex web-only development via GitHub.

Do not treat mobile as a lesser or exceptional workflow.

4. Shorten Claude skill files

Some existing skill .md files are longer than Claude guidelines allow.

Refactor them so that:

every primary skill .md file is under 200 lines,
operational instructions are concise,
long background explanations move into supporting docs,
examples move into examples files,
shared rules move into reusable common docs.

Do not remove important behaviour.

Make the skills shorter by factoring, not by deleting substance.

5. Clarify skill boundaries

Update each skill to state which organ owns each responsibility.

Examples:

PyAutoMind:
- prompt registry
- active/planned/complete task state

PyAutoBrain:
- task classification
- planning
- agent selection
- phasing decisions
- risk judgement

PyAutoHeart:
- tests
- validation
- readiness
- GREEN/YELLOW/RED gates

PyAutoBuild:
- worktrees
- branches
- commits
- PRs
- releases
- deployment
6. Integrate Health Agent and Build Agent

Shipping workflows should consult:

Health Agent for readiness,
Build Agent for execution planning.

The expected flow should become:

ship_library / ship_workspace
    ↓
Build Agent
    ↓
Health Agent
    ↓
PyAutoHeart
    ↓
GREEN / YELLOW / RED
    ↓
Build Agent
    ↓
PyAutoBuild execution
7. Integrate Feature Agent

Starting workflows should consult the appropriate PyAutoBrain agent.

For feature work:

start_dev
    ↓
Feature Agent
    ↓
PyAutoMind task
    ↓
PyAutoMemory context
    ↓
development plan
    ↓
PyAutoBuild execution wrapper

If the task is not a feature, route to the appropriate future agent or classify the missing agent as a follow-up.

8. Pair with PyAutoMind taxonomy

Ensure the workflow skills understand the new PyAutoMind structure:

feature/<target>/<task>.md
bug/<target>/<task>.md
refactor/<target>/<task>.md
docs/<target>/<task>.md
test/<target>/<task>.md
release/<target>/<task>.md
maintenance/<target>/<task>.md
research/<target>/<task>.md
experiment/<target>/<task>.md

Do not assume the first folder is the target repository.

The first folder is the work type.

The second folder is the target repo / domain.

9. Preserve start/ship lifecycle

The existing lifecycle remains valuable.

Preserve the concepts:

start_dev
start_library
start_workspace
ship_library
ship_workspace

but clarify that these are now workflow entry points used by PyAutoBrain.

They are not independent agents.

10. Documentation

Update documentation to explain:

old workflow,
new organism workflow,
how commands map to agents,
how local and web-only development work,
how health gates control shipping,
how PyAutoMind stores state,
how PyAutoBrain coordinates development.
11. Validation

Run:

skill install checks,
command resolution checks,
prompt status / inventory checks,
any existing workflow smoke tests,
grep for stale mobile/remote-mode terminology,
grep for stale old path assumptions,
line-count checks on skill .md files.

Add or update a simple script that reports any skill .md file over 200 lines.

12. PR

Create one PR titled:

Modernise PyAuto workflow skills for PyAutoBrain