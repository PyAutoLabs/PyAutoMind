# PyAutoMemory canonical-key TODO sweep

Type: maintenance
Target: PyAutoMemory
Repos:
- PyAutoMemory
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

PyAutoMemory canonical-key TODO sweep.

345 source-page sections across the wikis still carry "Canonical BibTeX key: TODO — no
unique match found in bibliography/pyautomemory.bib" markers (count from the 2026-07-16
structure-cleanup audit, PyAutoMemory#24). The restructure proved canonical coverage is
better than the TODOs suggest: the legacy-bib audit showed every unique legacy key already
exists in canonical, and the Hall 1952 TODO was resolved by identifying the paper
(PhysRev.87.387), adding the canonical entry, and filling the section — the proof of
pattern for this sweep.

Task: pair a matching script with a human verification loop to burn down the TODO count.

- Script: for each TODO section, extract the section heading (Author Year — tag) and any
  partial reference text; match against bibliography/pyautomemory.bib by author+year key
  stem, DOI, arXiv ID, then normalized title. Emit a ranked candidates report
  (section -> candidate keys + confidence), never auto-writing keys.
- Human loop: verify each proposed match against the public paper record before filling
  the section (per bibliography/README.md: never fabricate; uncertain stays TODO). Where
  no canonical entry exists, add verified metadata first.
- Batch by wiki (cti and galaxies have the densest TODO clusters); run
  make validate after each batch.
- Success: TODO count meaningfully down with zero fabricated keys; report the residual
  genuinely-unidentifiable sections.

Context: PyAutoMemory#24 design-note follow-up #1
(https://github.com/PyAutoLabs/PyAutoMemory/issues/24). The 856 canonical entries not yet
cited by any wiki page are explicitly OUT of scope — those fill paper-by-paper via the
reading queue.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/bccad7d5-61a2-4177-b2e0-0dafc0feed05/scratchpad/intake_todo_sweep.md -->
