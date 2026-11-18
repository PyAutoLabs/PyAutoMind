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
Witness: replaying the 2026-11-16-pm record through `batch digest --record` ends in one numbered decisions block that lists autolens_inference#70, euclid#133 and PyAutoBrain#654 awaiting /prm, the `decision-taken` flags, the set-aside writes and the late PyAutoGalaxy#720, and a test shows a worker-filed untested risk as an inbox entry in that block
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
