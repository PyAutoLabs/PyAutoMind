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

Deferred feature — validate through real assistant usage before implementing:

- Add a **Scientific context and papers** step to science-project creation. Prompt the user for
  papers they already consider important (local PDFs, arXiv IDs/URLs, DOIs, or a bibliography),
  while always allowing them to skip the step and add papers later.
- Use the project description to inspect the assistant's existing literature wiki and identify
  what relevant work is already covered.
- Search the external literature for additional relevant papers, then present a reviewable
  shortlist separated into: user-supplied papers, existing wiki coverage, and newly discovered
  candidates. Do not silently ingest every search result.
- After user approval, ingest project-specific selections into the project-local bibliography;
  retain deliberate promotion as the only route into the shared literature wiki.
- Record enough provenance for each accepted reference to distinguish verified paper metadata
  from abstract-level or search-derived summaries. Keep local PDF paths and files out of the
  committed bibliography; persist public references such as arXiv IDs and DOIs instead.

This guided intake is intentionally a future enhancement. Use the assistant on real science
projects first to learn when users naturally supply papers, how much literature searching they
want during setup, and whether project creation is the right point for a potentially lengthy
review. The initial implementation should be shaped by that evidence rather than making the
creation workflow heavy by default.
