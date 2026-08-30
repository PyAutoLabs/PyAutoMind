# Batch phase 0a — the review-cost grader (sizing faculty)

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
Themes:
- mind-workflow
Difficulty: medium
Autonomy: safe
Priority: high
Status: draft
Epic: two-slot-batching
Phase: 0
Parent: draft/feature/pyautomind/two_slot_batching_epic.md
Filed: 2026-08-30
Witness: the grade for a fixed set of sample prompts, pinned as a golden file; plus a case proving no-witness ⇒ judge, and a case proving declared beats derived.

Read the epic's "Three consequence tiers" and "The finding that reorganises
everything else" first — the *why* lives there and is not repeated here.

Read-only judgement only. This phase adds four outputs to
`agents/faculties/sizing/` and surfaces them on the `SizingSurface`. It writes
no prompt headers (0b) and re-grades no backlog (0c).

## The four outputs

**`consequence` → `notify | glance | judge`.** By rules over repo class and
surface, never by an agent's reading of its own work. Derive repo class from
`PyAutoMind/repos.yaml`, which already carries a category for every repo — do
not hand-maintain a second list.

- `notify`: docs, notebooks, profiling scripts, organ-repo tooling, test-only,
  pure refactor with a byte-equality witness.
- `glance`: library-internal change carrying a machine-checkable witness;
  workspace scripts.
- `judge`: public API, defaults, error contracts, science policy, an external
  reporter's issue — **and anything with no witness**. That default is
  load-bearing; it is what makes the witness requirement bite.

**`witness` → present/absent, plus the declared text.** Parsed from a `Witness:`
header. The faculty judges presence, not quality — quality is the human's call
in the slot, and a faculty that graded prose would be inventing certainty.

**`review_minutes` → an integer.** Seeded from the tier, not invented: `notify`
0, `glance` 2-5, `judge` 15-25. Calibrate the seed against real records —
`complete/2026/08/cmap-magma-default.md` (filed *small-medium, safe*) is 15-25;
an `autoarray-adapt-images-precondition`-shaped API fork is 15-20. Phase 7's
batch records carry the *actual* minutes and are what will correct this; say so
in the docstring so nobody mistakes the seed for a measurement.

**`unattended` → `ready | needs-slicing | never`.** Distinct from `difficulty`,
which is static blast radius. This answers "can it finish without me?". The rule
for `needs-slicing`: **a task that would need context compaction to finish is
too big to run unattended** (`anthropics/claude-code#54393` — compaction
destroys plan fidelity and nothing downstream catches it). `never` covers
science runs, releases, and anything whose deliverable is a judged verdict.

## Constraints

- Stdlib-only and offline, like the rest of the faculty.
- `effective_difficulty`'s precedence rule applies to every new field: a
  **declared** header wins, and the derived value is returned alongside so
  disagreement is reported rather than silently resolved.
- The faculty **opines and stops**. No writes, no dispatch — `ORGANISM.md` makes
  faculties sinks in the consult graph.

## Done when

- `pyauto-brain sizing <prompt>` prints tier, witness presence, review-minutes
  and readiness beside difficulty.
- The golden file in `tests/` pins the grade for the sample set, and the two
  named edge cases have their own tests.
- `AGENTS.md` for the faculty documents the four outputs and states plainly that
  `review_minutes` is a seed awaiting calibration.
