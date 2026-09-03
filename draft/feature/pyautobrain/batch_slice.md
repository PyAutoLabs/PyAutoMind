# `batch slice` — the decomposition pass for `needs-slicing` prompts

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
Filed: 2026-09-02

**A prompt too large to run unattended is not a scheduling problem, it is a
decomposition problem.** `AUTONOMY.md` and the sizing faculty have named
`Unattended: needs-slicing` since inception, and nothing has ever acted on it:
the human either splits the prompt by hand or the task runs too long and
compacts. This is the missing pass, and it is wanted whenever a prompt is
graded — from `/intake` the moment a new prompt sizes as `needs-slicing`, or
standalone against any prompt already carrying the grade.

It lives beside `plan` and `collect` on the conductor
(`agents/conductors/batch/_batch.py`, PyAutoBrain#332 shipped `collect`
2026-09-02; `plan` shipped 2026-08-30), which is where the prompt-writing
machinery already is; the *judgement* belongs to the sizing faculty
(`agents/faculties/sizing/`), and the conductor writes files only under
`--apply`.

## `batch slice <prompt>` — the decomposition pass

Input: a `needs-slicing` prompt. Output: two to four children with explicit
seams, plus an `epics.md` entry if the parent is not already an epic — phases
are ordered, so a sliced parent is an epic by construction.

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
  `plan` and `collect`, and `/intake` offers it when a freshly-filed prompt
  sizes as `needs-slicing`.
- Tests: a slice proposal rejected for having no witness; two-to-four children
  with seams; the parent untouched; `--apply` writes the files and the
  `epics.md` entry.
- `agents/conductors/batch/AGENTS.md` "Not built yet" is empty and removed.
