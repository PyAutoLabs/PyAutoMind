# Batch phase 7 — budget and backpressure

Type: feature
Target: pyautomind
Repos:
- PyAutoMind
- PyAutoBrain
Themes:
- mind-workflow
Difficulty: medium
Autonomy: safe
Priority: normal
Status: draft
Epic: two-slot-batching
Phase: 7
Parent: draft/feature/pyautomind/two_slot_batching_epic.md
Filed: 2026-08-30

Target: about ten batches a week at roughly a tenth of the plan allowance each.
Two budgets, and they are not the same thing:

- the **human budget** — review-minutes per slot, which phase 2's planner spends;
- the **token budget** — the plan allowance, which this phase governs.

The human budget is the binding one. Read this phase as protecting the token
budget from the batch, and protecting the human's own interactive sessions from
both.

## The constraint that decides the design

**Per-batch token attribution for cloud sessions is not measurable.** The
`/usage` plan breakdown is computed from local session history on the machine it
runs on and does not include claude.ai or cloud usage; `ccusage` is likewise
local-only; the Admin and Analytics APIs are Team/Enterprise. The only meter
covering cloud sessions is the account-level **percent-consumed gauge** for the
5-hour and weekly windows, plus the separate Opus bucket.

So do not build a per-task cost model, and do not fake one. Record window
readings at slot boundaries in the batch record; the delta is the batch's cost,
in the only unit that exists, account-wide and including anything else the human
did in the same window.

## Do not build a controller yet

The obvious design — a ±1 step on a points cap, adjusted each slot — is a random
walk here. It gets two samples a day of a signal whose within-class variance
exceeds the whole control range: `mge-lane-death` was filed `medium` and consumed
a multi-session three-arm investigation that spawned six follow-ups;
`cmap-magma-default` was filed `small-medium` and audited three libraries. And
`BUNDLE_SIZE_POINTS` — the points scheme it would control — was a context-window
packing heuristic for a single session, never a measure of compute.

Instead: a **static cap, revisited weekly by the human**, until at least thirty
batch records exist. Then look at the distribution before choosing a control law,
if one is still wanted.

## Reserve the human's own window

The 5-hour rate-limit bucket is shared with the human's interactive sessions. A
day-shift batch that drains it locks the human out of the slot they are about to
run. So pin the day shift to a fraction of the bucket and reserve the remainder;
prefer the night shift for anything large.

Two related facts worth checking before calibrating anything: weekly Claude Code
limits have been running about 50% above the published standard since 2026-05-13
as a repeatedly-extended temporary boost, most recently through **2026-08-31** —
a lapse moves the target by a third. And with usage credits enabled the
prompt-cache TTL drops from one hour to five minutes, which *inflates* burn on
slow-cadence sessions; a batch that spills into credits costs more per unit of
work than one that does not, which is a further argument for staying under the
cap rather than over it.

## Backpressure

Owned by phase 2's planner; this phase supplies its shape and its evidence.
Count **tasks awaiting review**, not PRs. Ramp: above half the cap, halve the next
batch; at the cap, plan a batch of one. **Never zero.** A missed slot is the
common case for an academic, not an exception, and a conference week must not
deadlock the thing whose whole purpose is to work while nobody is watching.

Also record what the *blocked* queue costs: pending workspace PRs rot behind the
library-first gate as `main` moves, and the first slot back is then spent
rebasing evidence rather than reviewing. If that shows up in the records, the
answer is smaller batches, not a bigger buffer.

## Done when

- Every batch record carries both window readings, the delivered count, the
  planned review-minutes and the **actual** minutes the human spent.
- `batch plan` reads the last three records and reports the trend, without acting
  on it, until thirty records exist.
- The day-shift reservation is enforced and stated in the record.
