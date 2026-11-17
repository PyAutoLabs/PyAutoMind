# M3.3 Readiness pass and decisions sheet: one sheet before a shift, one after

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-17
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Witness: slice 1: `python -m pytest tests/test_batch_ready.py -q` passes, including a fixture queue.md with one epic whose next phase has no prompt and one task on a claimed repo, where `pyauto-brain batch ready` queues exactly two `question-add` ops and a replayed digest ends "The next shift needs 2 rulings from you"; slice 2: replaying the 2026-11-16-pm record through `batch digest --record` ends in one numbered decisions block that lists autolens_inference#70, euclid#133 and PyAutoBrain#654 awaiting /prm, the `decision-taken` flags, the set-aside writes and the late PyAutoGalaxy#720, and a test shows a worker-filed untested risk as an inbox entry in that block
Lane: any
Unattended: never

## Why

Shift 2026-11-16-pm cost the human more time at its two ends than the 45 review-minutes it
was planned around.

- **Before:** none of the three queued epics could run as queued. The kick-off chat asked
  four questions at 17:18Z and a second round at 17:46Z. likelihood-lifecycle 5A needed
  three rulings, hpc-campaign 5d needed a DR1 ruling and a tier change, and results-library
  5c needed a human `sbatch`. The chat spent 10 minutes and four subagents finding each
  epic's next unit.
- **After:** decisions arrived one at a time in the cockpit chat from 19:54Z to 21:19Z: the
  defaults plan (asked 20:00Z, answered 20:24Z), the five risks on euclid#133 (20:39Z), a RAL
  test, a notes update and the last `/prm` (21:17Z). The euclid#133 worker listed five
  operational risks in the PR but filed no follow-up and asked no question; one needed a
  code change (euclid#135).

Human ruling R4 (2026-11-17): M3.3 is these two sheets.

## What

Two slices, each its own PR.

**Slice 1: the readiness pass (before).**

1. `pyauto-brain batch ready` walks `queue.md` and resolves each entry to its next startable
   unit: the epic's next phase, with its prompt filed.
2. It runs the premise check and the claim check on each unit, and files every gate it finds
   (a missing prompt, a ruling, a tier change, a human-only step) as a ruling in the
   questions inbox through the one Mind writer.
3. It runs at the end of every shift (from the digest step) and on request.
4. The digest ends with "The next shift needs N rulings from you". The human clears them with
   `/questions` when it suits. Launching is then `brief --new`, read, go.

**Slice 2: the decisions sheet (after).**

1. The digest ends with one numbered decisions block: every PR waiting for `/prm`, every
   `decision-taken` flag, every risk a worker listed, every set-aside write and every late
   arrival. The human answers in one message.
2. A worker that lists a risk it cannot test files it as an inbox entry (worker contract in
   `worker_template.md`), so it is in the block when the human sits down.

Slice 2 may follow the M3.2 shift; slice 1 is built before it.

## Out of scope

- Answering the rulings: that stays the human's, through `/questions`.
- Changing what the planner dispatches (M3.6b) or the carry-over step (M3.6c).
- The HTML packet.
