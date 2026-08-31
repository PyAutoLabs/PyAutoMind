# Batch phase 0c — re-grade the backlog, and give the dashboard a slot-shaped pick list

Type: feature
Target: pyautomind
Repos:
- PyAutoMind
- PyAutoBrain
Themes:
- mind-workflow
- dashboard
Difficulty: medium
Autonomy: safe
Priority: high
Status: shipped 2026-08-30 — PyAutoMind main 1a70a6fb, merged via #374
Consequence: notify
Witness: the before/after distribution of `Autonomy:`, `Consequence:` and `Unattended:` across every draft prompt, plus `lifecycle.py check` clean and a dashboard regeneration whose only diff is the new pick list and the new facets.
Review-minutes: 0
Unattended: ready
Epic: two-slot-batching
Phase: 0
Parent: draft/feature/pyautomind/two_slot_batching_epic.md
Filed: 2026-08-30
Blocked-by: phase 0b (the rule and the headers must be settled before 137 files are touched)

Depends on 0b, whose dry run has already shown what this will do.

## 1. Apply the grades

Run the settled grader over every prompt under `draft/` and write
`Consequence:`, `Witness:` (where one can be honestly derived — otherwise leave
it absent, which correctly grades the prompt `judge`), `Review-minutes:` and
`Unattended:`.

Never overwrite a human-declared value. Report every disagreement between
declared and derived rather than resolving it — that list is itself useful,
because it is where the grader and the human's intuition part company.

**`Witness:` cannot be invented.** For most prompts there is no honest witness to
derive, and writing a plausible-sounding one would defeat the entire mechanism:
the whole value of the field is that its *absence* is informative. Leave it
absent and let the prompt grade `judge`. Filling those in is ordinary work for
future slots, one prompt at a time, by whoever picks it up.

## 2. The pick list

`_intake.py`'s Quick wins is `difficulty == small and autonomy == safe`
(`:1907`), which with ten `safe` prompts in the backlog is nearly empty — the
surface that exists to hand out unattended work has almost nothing to hand out.

Replace it with **"Fits a slot"**: `Unattended: ready`, ordered by
`Review-minutes:` ascending, with the tier shown on each row. Render tier and
review-minutes as facets alongside target/autonomy/priority.

## 3. Report what it means

The PR body carries the before/after distribution and, from it, the honest
answer to the question this whole epic turns on: **how many tasks can a slot
actually hold, and how much of the backlog is reachable without slicing?**

## Constraints

- This is a large ledger diff. Keep it to prompt headers, the renderer change and
  the regenerated dashboard, so `ledger_merge.py classify` puts the prompt half
  on the ledger side and only the renderer needs a human.
- Regenerate the dashboard in the same commit; never hand-edit it.

## Done when

- Every `draft/` prompt carries the new headers, or is listed as a deliberate
  exception.
- "Fits a slot" renders and is non-empty.
- `lifecycle.py check` and `index --check` clean.
