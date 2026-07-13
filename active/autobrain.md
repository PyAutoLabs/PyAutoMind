Rename the repository from **PyAutoAgent** to **PyAutoBrain**.

## Context

The PyAuto ecosystem is evolving into a software organism.

Current architecture:

* PyAutoMind — intent and goals.
* PyAutoBrain — reasoning, planning and orchestration.
* PyAutoHands — execution.
* PyAutoHeart — health monitoring.
* PyAutoMemory — long-term knowledge.

This repository is responsible for reasoning.

It performs:

* planning
* decomposition
* orchestration
* agent coordination
* decision making

It does **not** directly perform software execution.

Execution belongs to PyAutoHands.

The Brain determines how work should be performed.

The Hands perform the work.

## Task

Perform a repository-wide rename from PyAutoAgent to PyAutoBrain.

Update:

* documentation
* README
* scripts
* workflows
* references
* package names (if present)
* architecture documents

Throughout the documentation, replace descriptions centred around "agents" with descriptions centred around reasoning and planning where appropriate.

Clarify the architectural boundary:

Mind
→ decides what should be done.

Brain
→ figures out how.

Hands
→ performs the work.

Heart
→ determines whether the organism is healthy.

Maintain backwards compatibility wherever practical.

Run all available validation.

Create a single PR titled:

Rename PyAutoAgent to PyAutoBrain
