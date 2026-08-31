# Batch phase 7 — spend the whole allowance

Type: feature
Target: pyautomind
Repos:
- PyAutoMind
- PyAutoBrain
Themes:
- mind-workflow
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: two-slot-batching
Phase: 7
Parent: draft/feature/pyautomind/two_slot_batching_epic.md
Filed: 2026-08-30

**Decided 2026-08-30: the target is 100% of the weekly Claude allowance.** That
inverts the usual budget problem. The failure mode to design against is not
overspend — it is **underspend**, and the shape of the work has to adapt to fill
the allowance without filling the review queue.

## The two caps, and why they force a mix

Two independent limits, and they bind on different things:

- **Human review capacity** caps *review-bearing* work. That is about **45
  review-minutes per slot** by default — roughly three library-touching tasks —
  and the human sets the number per slot (see below). No amount of token budget
  moves it.
- **The weekly allowance** caps *everything*, and the human wants it fully spent.

So the surplus — the allowance left after the review-bearing half — must go to
work that costs **zero review-minutes**. Call it **the fill**. This is the whole
design of this phase: a batch has a review-bearing half sized by the human's
hour, and a fill sized by whatever budget remains.

### What legitimately goes in the fill

- **tier-`notify` work**, once the shadow window grants it — the only fill that
  produces merged code. Roughly a sixth of historical throughput.
- **The adversarial review leg** (phase 3) on the review-bearing members. This is
  the purest fill there is: it spends tokens to buy review-minutes back.
- **Slicing and decomposition passes**, and **witness authoring** across the
  backlog — the fill that makes *future* review-bearing work cheaper.
- **Backlog re-grading** and other ledger work, which auto-merges.
- **Deeper verification of work that already passed**: re-running suites,
  cross-checking a run's claims, actively trying to falsify its witness.

### What must never go in the fill

**Research and experiments.** They produce verdicts, and a verdict is `judge`
load — the most expensive kind. 125 of August's 332 records named no PR at all,
which is exactly this class. Filling with research is precisely how the review
backlog gets rebuilt while looking productive. Research is review-bearing work
and is planned inside the 45 minutes, or not at all.

## The planner's dial

`batch plan` reads two numbers — the weekly burn-up and the review queue — and
picks from four cases:

|  | review queue clear | review queue backed up |
|---|---|---|
| **under budget for the week** | plan more review-bearing work | plan fill |
| **near the weekly cap** | hold, glide to reset | hold, and shrink tomorrow's review-bearing half |

A persistently large fill is itself a finding: it means the organism has spare
capacity it cannot turn into merged code, and the answer is to invest in
witnesses and in the `notify` tier rather than to burn tokens for their own sake.

## Measuring it

Per-batch token attribution for cloud sessions **is not measurable** — the
`/usage` plan breakdown is computed from local session history and excludes
claude.ai and cloud usage; `ccusage` is likewise local-only; the Admin and
Analytics APIs are Team/Enterprise. The only meter covering cloud sessions is the
account-level percent-consumed gauge for the 5-hour and weekly windows, plus the
separate Opus bucket.

The 100% target makes that sufficient, which it would not have been for a
per-batch budget. Read the **weekly bar once per slot** and compare it to how far
through the week you are: a burn-up curve, eyeballed, is entirely adequate
control for "use it all". Record the reading in the batch record. Do not build a
per-task cost model, and do not build a ±1 controller — two noisy samples a day
will not support one. A static per-slot cap, revisited weekly by the human, until
at least thirty batch records exist.

## Operational consequences of aiming at 100%

- **You will touch the ceiling regularly**, so decide in advance what happens
  there. Routine runs are rejected at the start when over cap. Keep a small
  reserve (~5%) so the *slot itself* always runs — being unable to review because
  the batch spent the window is the worst possible failure.
- **Reserve part of the 5-hour bucket for the human.** It is shared with their
  interactive sessions; a day batch that drains it locks them out of the slot
  they are about to run. Prefer the night shift for anything large.
- **Think about usage credits before enabling them.** With credits on, the
  prompt-cache TTL drops from one hour to five minutes, which *inflates* burn on
  slow-cadence sessions — you pay more per unit of work. At a 100% target the
  default should probably be credits off, gliding into the weekly reset rather
  than paying inflated rates past it.
- **Verify the headline number before calibrating.** Weekly Claude Code limits
  have been running about 50% above the published standard since 2026-05-13 as a
  repeatedly-extended temporary boost, most recently through **2026-08-31**. If it
  lapses, the target moves by a third.

## Backpressure, against a horizon the human declares

**Decided 2026-08-31 (superseding the 2026-08-30 "one slot a day plus a floor"
sizing):** a slot is whenever the human comes in, and at dispatch they state
`review-at:` — the shift is dispatch → `review-at:`, and the review budget is
theirs to set for that slot. Nothing is sized on a rhythm. This is the honest
promise: two hours a day indefinitely is 14 h/week, an academic will come back
late and vanish for conference weeks, and sizing on 14 h produces a queue that
saturates in two days and then square-waves.

- Count **tasks awaiting review**, not PRs (94 of 332 August records name two or
  more PRs, so a PR count trips on one healthy batch).
- Above half the cap, halve the next batch's review-bearing half. The fill is not
  halved — it does not touch the queue.
- **The floor is closed** (2026-08-31, never built): with the human carrying the
  timing, a missed `review-at:` dispatches nothing new and the outstanding grant
  simply expires. Revisit only if the queue is found starving during a long
  absence.
- At the cap the batch a human dispatches is **fill only** — adversarial reviews,
  slicing, witnesses, re-grading — which keeps the allowance spent and the
  backlog getting cheaper without deepening the review queue.
- Never plan zero *review-bearing* capacity out of backpressure alone: a batch
  that reaches the cap still composes fill, so a long gap ends with a
  *better-prepared* backlog rather than a stalled organism.

## Done when

- Every batch record carries the weekly and 5-hour readings, the delivered count,
  the planned review-minutes and the **actual** minutes the human spent.
- `batch plan` reports which of the four cases it is in and what it chose.
- A fill-only batch (at the backpressure cap) is proven to contain no
  review-bearing member.
