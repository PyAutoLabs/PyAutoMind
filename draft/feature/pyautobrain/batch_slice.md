# Batch phase 2b — `batch slice`: the decomposition pass

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoMind
Themes:
- mind-workflow
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Witness: `pyauto-brain batch slice <needs-slicing prompt>` on a fixture parent proposes two to four children each carrying its own `Witness:`, refuses a child with none ("a smaller judge task, not a slice"), and under `--apply` writes the child prompts plus an `epics.md` entry without renaming or retiring the parent
Review-minutes: 15
Unattended: ready
Epic: two-slot-batching
Phase: 2
Parent: draft/feature/pyautomind/two_slot_batching_epic.md
Filed: 2026-09-02

Re-filed from `batch_conductor.md` (Batch phase 2 — plan, slice, collect) when
`collect` shipped on its own: PyAutoBrain#332, record
`complete/2026/09/batch-collect.md`. `plan` shipped 2026-08-30 and `collect`
2026-09-02; `slice` is the phase's remaining verb and is the only thing this
prompt covers. The conductor is `agents/conductors/batch/_batch.py`; the
judgement belongs to the sizing faculty (`agents/faculties/sizing/`), and the
conductor writes files only under `--apply`.

## `batch slice <prompt>` — the decomposition pass

The pass `AUTONOMY.md` and the sizing faculty have named since inception and
which has never been built. Input: a `needs-slicing` prompt. Output: two to four
children with explicit seams, plus an `epics.md` entry if the parent is not
already an epic. The judgement belongs to the faculty; the conductor writes the
files under `--apply`.

Seam rules, in priority order:

1. **A slice is one unattended run** — it finishes without context compaction.
2. **A slice is independently reviewable, and carries its own witness.** If a
   proposed slice has no witness, it is not a slice, it is a smaller `judge`
   task — say so rather than shipping the illusion.
3. **A slice is independently revertible.**
4. Prefer seams at repo boundaries, and library before workspace, because the
   merge gate already works that way.

Never rename or retire the parent without the human saying so.

## Done when

- `slice` runs offline and stdlib-only, like every Brain entrypoint, beside
  `plan` and `collect`.
- Tests: a slice proposal rejected for having no witness; two-to-four children
  with seams; the parent untouched; `--apply` writes the files and the
  `epics.md` entry.
- `agents/conductors/batch/AGENTS.md` "Not built yet" is empty and removed.
