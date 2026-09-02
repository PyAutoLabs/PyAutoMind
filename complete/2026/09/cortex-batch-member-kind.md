- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/334 (closed completed 2026-09-02)
- completed: 2026-09-02
- library-pr: PyAutoBrain https://github.com/PyAutoLabs/PyAutoBrain/pull/335 (`6f3ece4`, merge `e917269`) →
  PyAutoCortex https://github.com/PyAutoLabs/PyAutoCortex/pull/5 (`a6d362d`, merge `88b17fc`), merged in
  that order (renderer before the organ, per the epic ledger).
- classification: feature (pyautobrain) — epic `cortex-birth`, phase 5 of 7 (0–6). Gates: phase 2 (SHIPPED
  #380) and the two-slot-batching `collect` verb (SHIPPED PyAutoBrain#332, this morning). Gates phase 6.
  Supersedes two-slot-batching phase 8 (`batch_science_lane.md`), retires `queue.md` #9, absorbs #2's
  science side.
- heart: YELLOW 65 at ship, acknowledged under the human's standing authorisation for the epic and recorded
  on the `active.md` entry — `manifest drift: local checkout origins — 1 mismatch(es)` and `CI status
  unavailable for all 6 libraries and 11 workspaces` (web container: no `gh`, measurement blindness).
- gate: tests 797 ✓ (776 → 797, 21 new) · smoke n/a (organ repos) · review CLEAN — leg 5 independent
  adversary run by Sonnet (implementer Opus, architect Fable), witness run on a scratch board, one
  disposition per claim (PR #335 comment) · Heart YELLOW acked · tenant firewall OK.

- summary: **the second batch member kind.** `pyauto-brain batch` gains `--kind dev|cortex|both`, defaulting
  from the lane (`local-dev` offers both; a cloud session `dev` only and reports the Cortex ready count).
  The phase-2 cortex conductor is **folded in, not rebuilt**: `_cortex.py` is imported lazily by file
  location and is unchanged, so it stays Mind-free for the Cortex's own `dashboard_refresh.yml`.

  `plan --kind cortex` = `_cortex.census` + `_cortex.plan` (ready + witness + budget + lane — no autonomy
  cap, no library-repo clash in either direction: a science run claims no library worktree); launch lines
  printed, never executed. `--apply --review-at <ISO> [--slot] [--shift] [--stamp]` opens
  `PyAutoCortex/batches/<slot>.md` in the Cortex schema — refused without `--review-at` (the human's),
  refused on an existing slot, rehearsed with the Cortex's own `check` on a copy; run stems, integer
  minutes, current state. `collect --kind cortex` is the **rolling board**: `score_cortex`/`cortex_blocks`
  registered as `KINDS["cortex"]` over `score_phase`/`member_block`, the Cortex health words (HEALTHY ·
  SUSPECT · FAILED · RUNNING), the four ruling verbs, `###` follow-ups and `(none)` default; a RUNNING
  member renders a live strip with **no review control** and is excluded from the progress count; phase
  moves and `refreshed:` lines go through the Cortex's `_apply_checked`, the record gets collect keys
  only (the state column is never touched), the packet is spliced in place through the shared renderer
  parametrised per organ, and the board is re-scored after the moves so a member the apply just
  delivered gets its controls in the same packet. Carry-forward: `- carried: <slug> — still <state> at
  review` at close; the next `plan --kind cortex --apply` includes still-live members at their current
  state with `- carried-from:` — the human never re-specifies them.

  Doctrine: `AUTONOMY.md` leg 4 ("Which record — 2026-09-02": a member reads its own organ's record;
  "no record → solo `--auto`" unchanged for dev, inapplicable to cortex), batch `AGENTS.md` ("Two kinds,
  two records"), `skills/batch/batch.md` (the Cortex recipe); PyAutoCortex `batches/AGENTS.md`
  (`carried:`/`carried-from:`, the record opened by the conductor), `packets/AGENTS.md` (the renderer
  exists; RUNNING members carry no control; `###`), `AGENTS.md` (the `--kind cortex` doors); Mind:
  `batch_science_lane.md` superseded, `two_slot_batching_epic.md` phase 8 marked, `queue.md` #9 retired,
  `batch_carry_forward.md` pointer (the dev side stays there).

- decisions: **61** no `heart-ack:`/`expected-effects:` on a Cortex record — the organ's own
  `batches/AGENTS.md` drops them (the Heart gates releases, not runs; no autonomy leg to license) and a
  science member is never `--auto`, so nothing reads them; the prompt's `heart-ack: n/a (cortex)` wording
  is overridden by the organ's schema and AUTONOMY.md says their absence is never an unacknowledged RED.
  **62** a RUNNING member has no review control at all and defaults to `(none)`; carry-forward, not an
  unclickable leave-to-finish, moves it to the next board. **63** the board is re-scored after the apply
  moves (a design deviation, kept): otherwise the member this refresh delivered would render RUNNING in
  the very packet that delivered it, and the human would collect twice to rule once. **64** the packet's
  permanent-home stamp line stays repo-relative (`batches/packets/<slot>.html`) so archived dev packets
  stay byte-comparable; the JS `PACKET_PATH` is organ-prefixed as designed.

- deviations from the plan (each in the code with its reason): a degraded member (phase not in this
  Cortex) is unreviewable as well as chip-less; `review-minutes-planned:` on a new record includes the
  carried members' minutes (the slot has to cover the carried board too); `--stamp` is accepted on
  `plan --kind cortex` as the record's `dispatched:`.

- witness: `pytest -n auto tests` → 797 passed. Cloud session, real trees read-only: `plan --kind cortex`
  reports the ready count (0 today) and plans nothing; dev `plan` proposes no `phases/` path; both trees
  untouched. Scratch Cortex: the record written passes `cortex check`; `collect --kind cortex --apply` on
  the four awaiting-ruling phases renders a 60 KB standalone packet; a second apply changes only the
  stamp, record byte-identical. Closed record `2026-08-31-pm`: nothing written, archived packet
  byte-identical. CI green on #335 and Cortex #5.

- lane notes: web-github session (no worktree, no `gh`; GitHub through the MCP tools; PyAutoHeart cloned
  read-only for vitals). No real Cortex batch has been planned through the new door yet — the first
  calibration point (`review-minutes-actual:` on a conductor-opened record) is phase 6's retrospective
  evidence and is still to come, at the laptop.

- follow-ups NOT filed (findable here, none blocking): the adversary's note that a phase in `State:
  pulled` whose run line still reads `running` is moved to awaiting-ruling on the state alone — the
  phase-2 `apply_ops` rule (state is authoritative), untouched here; a cross-check belongs in
  `cortex.py`/`_cortex.py` if a real pull ever trips it. The dev side of `batch_carry_forward.md`
  (queue #2) remains its own prompt.

- next: **cortex-birth phase 6** (`draft/feature/pyautocortex/cortex_public_surfaces.md`) — public
  surfaces and the retrospective; with no Cortex batch reviewed through the new door yet, the
  retrospective lands as a stub naming what it waits for.

## Original prompt

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
