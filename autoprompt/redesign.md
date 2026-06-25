Yes — we did. The key idea was:

PyAutoMind stores intent. PyAutoBrain reasons over that intent.

So PyAutoMind should not just be a loose pile of prompts. It should structure intentions clearly enough that PyAutoBrain can route them to the right specialist agents.

A strong first-folder structure would be something like:

feature/
bug/
refactor/
docs/
test/
release/
research/
maintenance/
experiment/

Then PyAutoBrain can map these naturally to agents:

feature/      → feature-planning agent
bug/          → debugging agent
refactor/     → architecture/refactor agent
docs/         → documentation agent
test/         → testing agent
release/      → release-readiness agent
research/     → literature/design agent
maintenance/  → hygiene/dependency agent
experiment/   → prototype agent

Here’s the Codex prompt.

Improve PyAutoMind prompt structure and routing taxonomy.

Context

This repository was previously PyAutoPrompt and is being renamed to PyAutoMind.

PyAutoMind is the source of intent for the PyAuto software organism. It stores ideas, goals, tasks, priorities and future work.

PyAutoBrain will consume these intentions and route them to specialist agents.

Therefore, PyAutoMind needs a clearer prompt taxonomy so that prompts are easier for both humans and agents to understand, prioritise and route.

Goal

Restructure the prompt repository so that the first folder level describes the type of work, rather than primarily the target repository.

For example:

feature/
bug/
refactor/
docs/
test/
release/
research/
maintenance/
experiment/

Within each work-type folder, prompts can then be grouped by target package or topic:

feature/autolens/
feature/autofit/
feature/autoarray/
feature/workspaces/

bug/autolens/
bug/autofit/
bug/autoarray/

refactor/autofit/
refactor/autoarray/

docs/autolens_workspace/
docs/howtolens/

This makes PyAutoMind easier for PyAutoBrain to reason over.

The first folder answers:

What kind of thinking or agent is needed?

The second folder answers:

What domain or repository is affected?

Requirements
Design a clear top-level taxonomy.

Suggested first-level folders:

feature/ — new user-facing or scientific capabilities.
bug/ — incorrect behaviour, crashes, regressions.
refactor/ — internal restructuring without intended behaviour change.
docs/ — documentation, tutorials, notebooks, examples.
test/ — test coverage, smoke tests, validation scripts.
release/ — packaging, versions, deployment, release readiness.
maintenance/ — dependency updates, hygiene, cleanup, small technical debt.
research/ — exploratory scientific or algorithmic investigation before implementation.
experiment/ — prototypes, spikes, proof-of-concept work.

Review these names and adjust only if there is a clearly better alternative.

Preserve existing prompts.

Do not delete existing prompt files.

Move existing prompt files into the new taxonomy where their purpose is clear.

If classification is ambiguous, place them under:

triage/

and add a short note explaining that they need manual review.

Update registry files.

Update references in:

active.md
planned.md
queue.md
complete.md
parked.md
priority.md
any feature trackers
any issued prompt references

so that paths continue to resolve after the move.

Update skills and scripts.

Search for hard-coded assumptions that top-level folders correspond to repositories.

Update scripts and skills so they understand the new structure:

<work-type>/<target>/<prompt>.md

rather than:

<target>/<prompt>.md

This likely affects routing, status reporting, issue creation, queue processing and handoff logic.

Update routing logic for PyAutoBrain.

Add or update documentation that maps prompt categories to future PyAutoBrain agents.

For example:

feature/      -> feature planner
bug/          -> debugger
refactor/     -> refactor architect
docs/         -> documentation agent
test/         -> test engineer
release/      -> release engineer
maintenance/  -> hygiene agent
research/     -> research analyst
experiment/   -> prototype agent

Do not implement PyAutoBrain agents in this repository.

Only define the taxonomy and the metadata / documentation needed for PyAutoBrain to consume it.

Add prompt metadata conventions.

Each prompt should remain plain markdown, but introduce a lightweight optional header convention near the top of each file, for example:

# Short task title

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_workspace

Status: draft

Do not require YAML frontmatter unless already used elsewhere.

Keep prompts human-writable.

The goal is light structure, not bureaucracy.

Update documentation.

Update the README to explain:

PyAutoMind is the organism's source of intent.
The first folder level is the work type.
The second folder level is the target repo or domain.
PyAutoBrain will use this structure for routing.
Humans can still write natural-language prompts freely.

Include examples of good prompt paths:

feature/autolens/potential_corrections.md
bug/autoarray/mask_edge_case.md
refactor/autofit/result_object_cleanup.md
docs/workspaces/pixelization_tutorial.md
research/autofit/sbi_design.md
experiment/autoarray/jax_sparse_mapping.md
Backwards compatibility.

If existing commands such as /start_dev path/to/prompt.md assume the old folder structure, update them to handle both old and new paths during transition.

If compatibility is impossible, document the breaking change clearly.

Validation.

Run all available tests or smoke checks.

At minimum:

run any existing status script
run any prompt inventory script
check that moved prompt paths are referenced correctly
grep for stale old paths
verify /pyauto-status documentation remains accurate
PR

Create one PR titled:

Restructure PyAutoMind prompts by work type

The PR description should include:

summary of the new taxonomy
examples of moved prompts
compatibility notes
validation run
follow-up tasks for PyAutoBrain agent routing

This is the key architectural sentence I’d keep in the README:

PyAutoMind organises intent by the kind of thinking required; PyAutoBrain uses that structure to choose the right reasoning agent.