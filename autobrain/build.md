I actually think the Build Agent should be the second canonical PyAutoBrain agent, because it demonstrates that Brain agents don't execute directly—they coordinate organs.

The flow becomes:

PyAutoMind
    ↓
Build Agent (PyAutoBrain)
    ↓
Health Agent (PyAutoBrain)
    ↓
PyAutoHeart
    ↓
GREEN / YELLOW / RED
    ↓
Build Agent
    ↓
PyAutoBuild (future PyAutoHands)

The Build Agent is therefore the executive function. It owns the build workflow, but delegates health decisions to the Health Agent.

I'd give Codex this prompt:

Implement the second specialist PyAutoBrain agent: Build Agent.

Context

The PyAuto ecosystem is evolving into a software organism.

Current architecture:

PyAutoMind
Stores intent, goals and future work.
PyAutoBrain
Contains specialist reasoning agents.
PyAutoHeart
Performs health monitoring, testing and readiness checks.
PyAutoBuild
Performs software execution, release tasks and repository actions.
(This may later be renamed PyAutoHands.)

The first PyAutoBrain specialist agent is the Health Agent.

The Build Agent should become the second.

Fundamental architectural principle

The Build Agent does not build software itself.

PyAutoBuild performs builds.

The Build Agent decides:

whether building should happen,
what should be built,
when it should be built,
which PyAutoBuild capabilities should be invoked,
whether execution should continue or stop.

The Build Agent is therefore an orchestration layer.

It reasons.

PyAutoBuild executes.

Responsibilities

The Build Agent should:

understand build requests from PyAutoMind
inspect repository state
determine the required build actions
request a health assessment from the Health Agent
interpret the GREEN/YELLOW/RED result
decide whether execution may proceed
invoke the appropriate PyAutoBuild capabilities
monitor execution
produce a structured execution summary

It must never duplicate PyAutoBuild functionality.

Existing capability audit

Before implementation:

Audit the existing PyAutoBuild repository.

Discover every existing capability including:

bash scripts
Python scripts
Claude skills
slash commands
GitHub workflows
deployment logic
release logic
packaging
version management
PR creation
repository management
automation scripts

The Build Agent should understand these capabilities.

It should call them.

Not replace them.

Boundary audit

Confirm that PyAutoBuild contains only execution behaviour.

If health-related logic is found:

identify it,
determine whether it belongs in PyAutoHeart,
document the finding,
avoid duplicating it inside the Build Agent.

Likewise, ensure reasoning remains inside PyAutoBrain.

The architecture should remain:

PyAutoMind

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

PyAutoBuild

Build lifecycle

The Build Agent should reason through a workflow similar to:




Receive build request.




Determine required execution steps.




Request health assessment.




Interpret Health Agent decision.

GREEN

Proceed automatically.

YELLOW

Proceed cautiously.

Include warnings.

RED

Abort execution.

Explain blockers.




Invoke appropriate PyAutoBuild capabilities.




Monitor execution.




Summarise results.

Interface

Design a simple interface similar to:

BuildDecision = BuildAgent().execute(...)

returning structured information including:

requested action
health status
execution plan
execution summary
warnings
blockers
follow-up recommendations
Claude skill guidance

If implementing as Claude skills:

keep every .md file below 200 lines,
split large skills into reusable components,
keep instructions concise,
place architecture documentation elsewhere.
Documentation

Update documentation describing the organism.

Explain:

PyAutoMind

Creates intent.

PyAutoBrain

Reasons.

Build Agent

Coordinates execution.

Health Agent

Assesses readiness.

PyAutoHeart

Measures health.

PyAutoBuild

Performs work.

The Build Agent should become the canonical example of how PyAutoBrain coordinates multiple organs.

Future Brain agents

Document how this pattern generalises to future agents such as:

Feature Agent
Bug Agent
Refactor Agent
Documentation Agent
Research Agent
Release Agent

The Build Agent should be designed as a reusable template for future specialist Brain agents.

Validation

Run all available validation.

Ensure every existing PyAutoBuild capability remains usable through the Build Agent.

No existing functionality should regress.

PR

Create one PR titled:

Implement initial PyAutoBrain Build Agent

One design suggestion that emerged while writing this: I wouldn't make the Build Agent simply "call the Health Agent." Instead, I'd introduce the idea that Brain agents can consult one another. That means in the future:

Feature Agent asks Health Agent if the codebase is in a good state for a refactor.
Release Agent asks Build Agent to package a release.
Research Agent asks Feature Agent to estimate implementation complexity.

You start to get a genuine society of reasoning agents within PyAutoBrain, while the organs (Heart, Hands, Memory, Nerves) provide capabilities and state. That's a richer and more extensible architecture than every agent talking directly to every organ.



But for the first implementation, let Build Agent include release workflows and document that release may later become its own agent.

Reason:

Build is broad: run packaging, create artifacts, invoke scripts, open PRs, deploy.
Release is higher-stakes: versioning, changelog, PyPI, tags, cross-repo compatibility, human approval.
Release should consult Health Agent more strictly than ordinary build work.

So the mature architecture is:

Release Agent
    ↓ consults
Health Agent
    ↓
PyAutoHeart

Release Agent
    ↓ requests execution from
Build Agent
    ↓
PyAutoBuild

Whereas day one can be:

Build Agent
    ├─ build mode
    ├─ deploy mode
    └─ release mode

I’d update the prompt with this paragraph:

Treat release as part of the initial Build Agent scope, because PyAutoBuild currently owns release/build/deployment execution. However, design the Build Agent so that release logic is clearly isolated as a “release mode” or “release workflow”. Do not mix release-specific reasoning into generic build execution.

Document that a future PyAutoBrain Release Agent may be split out. In that future architecture, the Release Agent will make release-specific decisions about versioning, changelogs, PyPI/tags and human approval, consult the Health Agent for readiness, and then request execution from the Build Agent / PyAutoBuild.

So: one agent now, clean seam for two later.