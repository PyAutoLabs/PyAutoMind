# Cortex phase 5 — the second batch member kind: separate records, separate review-at, rolling board

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoCortex
- PyAutoMind
Themes:
- mind-workflow
- dashboard
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: `pyauto-brain batch plan --kind cortex` in a laptop session proposes only `ready` Cortex phases against a Cortex review-minute budget and writes `PyAutoCortex/batches/<date>-<slot>.md`; `batch plan` (dev) in the same checkout proposes no Cortex phase and no science prompt; `batch collect --kind cortex` adds a newly `pulled` member to an open Cortex packet without touching the Mind record
Review-minutes: 25
Unattended: needs-slicing
Epic: cortex-birth
Phase: 5
Parent: draft/feature/pyautocortex/cortex_birth_epic.md
Filed: 2026-09-01
Issued: 2026-09-02

Phase 5 of 7 in the PyAutoCortex birth epic. **Gates: phase 2, AND the
two-slot-batching `collect` verb** (`draft/feature/pyautobrain/batch_conductor.md`,
`queue.md` #8 — "next verb = collect"). Build `collect` once with two member
kinds; do not let a dev-only `collect` ship and then reopen it here. If
`collect` is being built first, this prompt is its science half and should be
planned in the same session. Gates phase 6.

## Context

The batch layer stays in Brain (`two_slot_batching_epic.md`, "Placement — no
new organ" — that ruling is about the batch layer and stands; the Cortex is a
registry the batch layer reads, as the Mind is). Today `_batch.py` is
`plan`-only (`:317`), globs `PyAutoMind/draft/**` (`:134`), and rejects every
science run through the autonomy cap (`_sizing.py:934-937`, `_batch.py:190`).
Both 2026-08-31 batches held science members by hand, and the pm batch's two
laptop members were CARRIED across three refreshes and 14 h while nine dev
members sat reviewed — the out-of-sync problem this epic exists for.

The human's rule for science review (`/mnt/c/Users/Jammy/Science/prompt.md`):
dev batches are reviewed in one go when the whole batch is complete; science
review is **live whenever anything can be reviewed** — a task completes and is
added to the existing board; nothing mid-flight is reviewable; the board is the
live view of run progress.

## Task

1. **Two member kinds** in `agents/conductors/batch/_batch.py`: `dev` (Mind
   prompts, unchanged) and `cortex` (Cortex phases via the phase-2 conductor's
   `census`). `--kind dev | cortex`, default from the session's lane
   (`local-dev` → both are offered, cloud → `dev` only, reporting the Cortex
   ready count). A `cortex` member's admission is the phase-2 rule; the autonomy
   cap is never consulted for it. `LIBRARY_REPOS` clash detection applies to
   neither direction across kinds (a science run does not claim a library
   worktree) — say so in code.
2. **Separate batch records.** `cortex` batches write
   `PyAutoCortex/batches/<date>-<slot>.md` with their own `review-at:`,
   `review-minutes-planned:`, `heart-ack:` (n/a — Heart gates releases, not
   runs; record `heart-ack: n/a (cortex)` so the field's absence is never read
   as an unacked RED), `expected-effects:` (RAL queue/GPU usage, not repo
   effects), `members:` in the phase-1 line shape. A Mind batch record never
   lists a Cortex member and vice versa. `_dispatch_payload` (`_batch.py:247-255`)
   emits `/start_dev … --auto` for dev members only; a Cortex member's launch
   line is the project's submit command from `projects.yaml` (`sync_cli` +
   the phase's `Runs:` template), printed for the human, never executed.
3. **Rolling board.** `batch collect --kind cortex` may run any number of times
   per batch: each run reads the human's `hpc/sync pull` results (a `refreshed:`
   line per pull), scores (phase 2), and **appends** newly `pulled` members to
   the open packet; members still `submitted`/`running` render in a live strip
   with job ids and budget-vs-elapsed and hold no review control. The packet is
   only closed by the review submission. `review-at:` for a Cortex batch is
   therefore "when the human next sits at the laptop", declared at dispatch as
   today and re-declared at each refresh.
4. **Carry-forward, formalised Cortex-side.** A Cortex member never blocks a
   Cortex review: at review, members still running are recorded `carried` in
   the record and re-enter the next Cortex batch's packet automatically. This
   absorbs `queue.md` #2 (`draft/feature/pyautomind/batch_carry_forward.md`) for
   the science side — the dev side keeps whatever that prompt decides; leave a
   pointer in it.
5. **`AUTONOMY.md` leg 4** (`:386-394`): a member reads its own organ's batch
   record (`PyAutoMind/batches/…` for dev, `PyAutoCortex/batches/…` for
   cortex); the "no record → solo `--auto`" rule is unchanged for dev and
   inapplicable to cortex (never `--auto`). `skills/batch/batch.md` gains the
   Cortex collect recipe (pull → collect → packet refresh) and the two-record
   rule; `batch/AGENTS.md` the two-kind vocabulary.
6. **Supersede two-slot-batching phase 8** (`draft/research/euclid/batch_science_lane.md`):
   mark it superseded in `two_slot_batching_epic.md` ("Development through
   use") and in its own header (`Status: superseded by cortex-birth`), retire
   `queue.md` #9. Its closures were carried into the Cortex `AGENTS.md` at
   phase 1.
7. **Tests**: two-kind plan on a fixture holding both registries; collect
   appends without rewriting ruled members; a cloud session offers no cortex
   member; a dev record never gains a cortex line.

## Acceptance

- The witness above; Brain tests green; the first real Cortex batch after
  merge produces a record with `review-minutes-actual:` filled — the first
  calibration point the science side has ever had (both 2026-08-31 slots have
  none).
- PRs: PyAutoBrain (conductor + doctrine), PyAutoMind (queue/prompt
  retirements), PyAutoCortex (`batches/AGENTS.md` if the record schema moved).

## Out of scope

- A dispatcher of any kind (two-slot phase 5 remains deferred; the Cortex never
  dispatches — the human does).
- The batch board strip (`draft/feature/pyautobrain/batch_board.md`, `queue.md`
  #6) — it may later show both kinds; not here.
- Changing dev batch semantics.
