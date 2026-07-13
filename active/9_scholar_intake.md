# Scholar intake — science analysis and machine sources feed the Mind

Type: feature
Target: autonomy
Repos:
- PyAutoBrain
- PyAutoMind
- autolens_assistant
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft

## Why

The missing pairing: scientific analysis (autolens_assistant sessions,
PyAutoMemory reading, profiling results) currently produces insight that dies
in the session unless the human hand-carries it into `ideas.md`. The organism
should conceive tasks from its own scientific work — with the human as
*editor* of a proposed batch, not *author* of every prompt.

## What

1. **Scholar mode for `/research`**: a research run over autolens_assistant /
   PyAutoMemory (via the memory faculty) ends by emitting candidate task
   bullets into `PyAutoMind/ideas.md`, each with provenance — "motivated by
   <wiki page / paper / profiling result / session>". Bullets only: the
   existing `intake ideas` sweep then formalises them into headed prompts,
   and the human reviews the IntakeDecisions before `--apply`.
2. **Extend the intake sweep to machine sources**: beyond `ideas.md`, let
   `intake` propose prompts from accumulating machine output — Heart-filed
   issues, profiling result summaries, review-faculty findings that outgrew
   their PR — same dry-run-first, human-approves-batch contract.

## Boundaries (adversarial findings)

- **Never write prompts or planned.md directly** from scholar mode — ideas.md
  is the staging area precisely so intake's existing conception discipline
  (classify, size, human review, `--apply`) is reused, not bypassed. Noise
  tasks die cheaply at the bullet stage.
- **Provenance stays private**: PyAutoMemory citations live in Mind (private
  organism repo). They must never leak into public workspace/docs output that
  a formalised task later produces.
- Intake's own rules hold: it files, it never starts dev; low-confidence
  classifications land in `triage/`; raw bullets are marked
  `[formalised -> …]`, never deleted.

Blocked-by: 8_memory_faculty.md (the read surface), 1_autonomy_contract.md.
Independent of the 4–7 execution track.
