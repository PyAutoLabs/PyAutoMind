Rename the repository from **PyAutoPaper** to **PyAutoMemory**.

## Context

This rename is part of a broader architectural evolution of the PyAuto ecosystem into a software organism.

Current organism architecture:

* PyAutoMind — ideas, intent, goals and future work.
* PyAutoBrain — planning, reasoning and orchestration.
* PyAutoHands — execution.
* PyAutoHeart — health, testing and readiness.
* PyAutoMemory — long-term knowledge.

PyAutoPaper has evolved beyond a repository of papers.

It now stores and organises:

* literature summaries
* LLM-generated wikis
* reading queues
* accumulated scientific knowledge
* project knowledge
* architecture notes
* information the organism has learned

The repository is therefore functioning as the organism's long-term memory, not simply as a collection of papers.

## Task

Perform a repository-wide rename from PyAutoPaper to PyAutoMemory.

Update:

* README
* documentation
* repository metadata
* package names (if applicable)
* references in scripts
* GitHub workflows
* badges
* URLs
* internal documentation

Where documentation currently refers to "papers", consider whether "knowledge", "memory", "literature", or "learned information" better reflects the repository's new role.

Do not change functionality.

Maintain backwards compatibility wherever practical.

Add a README section explaining that PyAutoMemory stores what the organism has learned, including literature summaries, scientific knowledge and project knowledge.

Run all available validation.

Create a single PR titled:

Rename PyAutoPaper to PyAutoMemory
