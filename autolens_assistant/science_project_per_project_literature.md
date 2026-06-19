`wiki/literature/` is the assistant's shared, self-contained base reference for strong-lensing
science (decoupled from any external paper repo; see @autolens_assistant/wiki/literature/AGENTS.md).
Spun-off science projects refer back to it rather than copying it. Open question: when a paper
is ingested **for a specific project**, where does it go?

Decision (lean: hybrid):

- **General concepts** (mass-sheet degeneracy, substructure, time-delay cosmography, …) — the
  project refers back to the shared `wiki/literature/`. One source of truth.
- **Papers specific to this analysis** — the project's own bibliography (they are part of the
  paper's reference list), kept **in the project**, NOT pushed into the shared wiki. This stops
  one project's niche references polluting the global source of truth.
- A paper that turns out to be **generally useful** can still be contributed upstream via
  `al_ingest_paper` run from the assistant clone — a deliberate promotion, not the default.

What to implement:

- Define the project-local literature location (e.g. the project's `wiki/project/` bibliography
  or a project `literature/` page) and its shape.
- Teach @autolens_assistant/skills/al_ingest_paper.md to choose its target: project-local by
  default when working inside a project, shared `wiki/literature/` only on explicit promotion.
- Have @autolens_assistant/skills/start-new-project.md scaffold the project-local bibliography
  home and explain the hybrid rule in the project's thin docs.
