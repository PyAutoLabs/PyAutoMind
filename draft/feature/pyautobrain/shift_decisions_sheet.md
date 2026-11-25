# M3.3 slice 2: the decisions sheet, one numbered block after a shift

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-18
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Witness: a test shows a worker that lists a risk it cannot test filing it as an inbox entry, which then appears as a numbered row under "Answer" in the digest's review table (PyAutoBrain#718); and replaying a record with a set-aside write and a late arrival lists both as numbered rows in that table
Lane: any
Unattended: never

## Why

The remainder of M3.3 (`complete/2026/11/shift-readiness-pass.md` records slice 1, the
readiness pass, merged 2026-11-18 as PyAutoBrain#674 and PyAutoMind#585). Shift
2026-11-16-pm's decisions reached the human one at a time in the cockpit chat from 19:54Z
to 21:19Z: the defaults plan, the five risks on euclid#133, a RAL test, a notes update
and the last `/prm`. The euclid#133 worker listed five operational risks in the PR but filed
no follow-up and asked no question; one needed a code change (euclid#135).

Human ruling R4 (2026-11-17): M3.3 is two sheets. This is the one after a shift.

## What

**Scope changed 2026-11-24 (human-approved in chat).** Item 1's numbered block is built by
PyAutoBrain#718 (shipped 2026-11-25, PyAutoBrain#719; `complete/2026/11/digest-review-table.md`): a numbered review table at the top of the digest, grouped by the human's next
action (`/prm`, answer, fix, blocked, running, done), with `decision-taken` and refusal reasons
in its Note column. What remains here: item 2 (workers file untested risks as inbox entries),
and set-aside writes and late arrivals as rows in that table.


1. The digest ends with one numbered decisions block: every PR waiting for `/prm`, every
   `decision-taken` flag, every risk a worker listed, every set-aside write and every late
   arrival. The human answers in one message. It sits just above slice 1's closing line
   ("The next shift needs N rulings from you.").
2. A worker that lists a risk it cannot test files it as an inbox entry (worker contract in
   `worker_template.md`), so it is in the block when the human sits down.

## Out of scope

- Answering: that stays the human's, through `/questions` and `/prm`.
- The readiness pass (slice 1, shipped).
- The HTML packet.
