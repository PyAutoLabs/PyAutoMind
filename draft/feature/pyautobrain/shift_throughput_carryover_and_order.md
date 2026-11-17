# M3.6c Shift throughput: carry-over, in-shift restart, `first: glance`, a session cap from the budget

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-17
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Witness: `python -m pytest tests/test_orchestrator_*.py -q` passes with new fake-clock tests that fail on today's main: (1) the first tick of a shift starts a close-out for the previous shift's late `glance` PR (fixture: the 2026-11-16-pm late arrival) and restarts a task whose inbox question is answered; (2) a question answered with 31 minutes left restarts its task, with 29 minutes left it does not; (3) with `first: glance` a ready `glance` task spawns before the named `judge` tasks, and without it the order is unchanged; (4) a brief with no `max-sessions:` gets a cap derived from `token-budget:` and `max-workers:`, shown in the snapshot, and the 2026-11-16-pm brief replayed under it never refuses on sessions while under half the token budget
Lane: any
Unattended: never

## Why

Shift 2026-11-16-pm produced no stage-2 rows, by construction, and idled twice.

- Named tasks go first and the backlog dip last. The two `glance` tasks started at 18:33Z and
  18:41Z, with 45 and 37 minutes left. One parked on PyAutoFit#1777, the other missed the end:
  its PR, PyAutoGalaxy#720, opened at 19:24:59Z, after the digest. Nobody has looked at it.
- PyAutoFit#1777 was answered at 18:42Z, three minutes after the question, and the task still
  lost the shift: an answer releases a task to the next shift only.
- `max-workers 2` held six tasks for the first 22 minutes. After the raise, `max-sessions 8`
  stopped all new starts from 18:44Z: one worker ran for the last 34 minutes with 2.3M tokens
  unspent and two tasks waiting. Tokens used: 2.66M of 5M.

A task that does not start rolls to the next shift, so this is not about the long queue. It
is about the late PR, which no later shift picks up, and the answered question.

## What

1. **Carry-over at the first tick.** The first tick closes out the previous shift's late
   `glance` PRs (the same close-out path as in-shift) and restarts tasks whose questions were
   answered.
2. **In-shift restart.** An answered question restarts its task if more than 30 minutes
   remain before `review-at:`.
3. **`first: glance`.** A brief line that starts ready `glance` work before the named judge
   tasks, or holds one worker for it. Without it the order stays as now.
4. **Session cap from the budget.** Drop `max-sessions` as a separate default; derive it from
   `token-budget:` and `max-workers:`. An explicit `max-sessions:` still wins.

## Out of scope

- The decisions sheet that lists late arrivals (M3.3 slice 2).
- The cockpit staying attached for late arrivals (M3.6g).
- Sessions idling after their deliverable (infrastructure review).
