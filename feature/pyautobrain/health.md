Implement the first PyAutoBrain specialist agent: Health Agent.

Context

The PyAuto ecosystem is evolving into a software organism.

Current architecture:

PyAutoMind
Stores intent, goals and future work.
PyAutoBrain
Performs reasoning and coordinates specialist agents.
PyAutoHeart
Performs health monitoring, readiness checks, validation and testing.
PyAutoBuild
Executes software changes and releases.
(This may later become PyAutoHands.)

A key architectural principle is:

PyAutoHeart measures health.

PyAutoBrain reasons about health.

The Brain never performs health checks itself.

Instead, it asks PyAutoHeart to evaluate the organism and then interprets the results.

This separation should be maintained throughout the design.

Goal

Implement the first specialist PyAutoBrain agent:

Health Agent

Its responsibility is to decide whether the organism is healthy enough to proceed with work.

Responsibilities

The Health Agent should:

invoke PyAutoHeart
collect all health reports
reason about their significance
determine overall readiness
explain the decision
provide actionable recommendations

It should not implement testing or validation logic.

That remains owned entirely by PyAutoHeart.

Inputs

PyAutoHeart may provide information such as:

unit tests
integration tests
workspace validation
release readiness
dependency consistency
URL hygiene
documentation completeness
repository cleanliness
generated file classification
installation checks
future health checks

The Health Agent should treat PyAutoHeart as an abstract health provider.

Avoid coupling to specific individual checks.

Outputs

The agent should produce a structured report.

Example:

Overall Health

Status:
GREEN

Summary

All critical health checks passed.

Warnings

- Documentation coverage below target.

Recommendations

- Improve API documentation before next release.

Blocking Issues

None.

The important output is:

GREEN

or

YELLOW

or

RED
Gate semantics

GREEN

The organism is healthy.

PyAutoBuild may proceed automatically.

YELLOW

The organism is mostly healthy.

Work may proceed.

Human review is recommended.

RED


Additional requirements

Before implementing the Health Agent, audit the existing health infrastructure.

Inspect PyAutoHeart and identify every existing health-related asset, including:

bash scripts
Python scripts
Claude skills
slash commands
GitHub workflows
readiness gates
validation scripts
smoke-test scripts
documentation describing health checks

The Health Agent must know about these existing checks and treat them as PyAutoHeart capabilities.

Also inspect PyAutoBuild to ensure no health/readiness logic has drifted there.

If PyAutoBuild still contains health-related checks that should belong to PyAutoHeart, do not silently duplicate them. Instead:

document the drift,
propose whether the logic should move to PyAutoHeart,
ensure the Health Agent understands the current boundary,
add a follow-up task if migration is non-trivial.

Architectural rule:

PyAutoHeart owns health checks.
PyAutoBrain Health Agent reasons over PyAutoHeart outputs.
PyAutoBuild acts only after receiving a GREEN/YELLOW/RED decision.
Health Agent skill file constraints

If implementing the Health Agent as a Claude skill or markdown-based agent definition:

keep each .md file under 200 lines,
follow Cl