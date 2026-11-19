# M3.7c Watcher latency: short tick, early shift close, `decision-taken` refused at PR-open

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-19
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Witness: (1) `bin/systemd/pyauto-orchestrator.timer` ticks every 60 seconds, and a systemd path unit in `bin/systemd/` starts the same service when a worker's `.done` file appears; (2) an orchestrator test: a PR opened with the `decision-taken` label is recorded as refused for `/prm` on the next tick with no close-out session spawned and no merge slot taken; (3) the same test: a later PR of the shift on that library still waits behind it until GitHub says MERGED or CLOSED (M3.6j ruling c); (4) the digest of that shift has one line per library naming the merges blocked behind a `/prm`-bound PR; (5) an orchestrator test: with no worker live, no close-out live, no PR waiting on CI or a branch update, and no startable task, the shift posts its digest on that tick rather than at `review-at:`; (6) the Brain suite passes
Lane: any
Unattended: ready

## Request (verbatim)

Human, 2026-11-19, in the chat prompt that opened this work: "Refusing decision-taken PRs at PR-open must keep them as "earlier" PRs in the M3.6j merge order." Then, on the plan: "approved, all rulings yes".

## Why

Measured in shifts 2026-11-18-pm, -pm2 and 2026-11-19-am:

- The timer is 2 minutes and ticks land about 3.1 minutes apart. From one worker's end to the next task's start took 10 minutes, about 5 of them waiting for ticks.
- Shifts 11-18-pm and -pm2 sat idle for 54 and 44 minutes before the digest.
- A `decision-taken` PR is refused in 20 to 40 seconds, but only after CI has landed and a close-out session has started (about 40k tokens each). 3 of 7 tasks were `decision-taken`.

## Rulings (human, 2026-11-19)

- **S7.** The watcher refuses a `decision-taken` PR at PR-open, from the label alone, with no close-out session. The PR keeps its place as an "earlier" PR in the M3.6j merge order (ruling c unchanged), so later unattended merges on that library wait for the human's `/prm`. The digest reports what waited.

## Shape

- `bin/systemd/`: timer to 60 seconds; a `.path` unit on the orchestrator home's `.done` files. Check `PyAutoMind/policy/shift_watcher.md` for the tick interval the exemption states and amend it in a Mind PR if it names 2 minutes.
- `_orchestrator.py`: the label read at PR-open (`gh pr view --json labels`, already in the network surface for shift PRs); the early close rule; the tick lock already makes overlapping ticks safe, confirm with a test.
- `_digest.py`: the "blocked behind `/prm`" lines.
- Installing the units on the laptop is a deploy step for the human or a chat session, when no shift is live.

## Not in this task

Two workers on one library on disjoint files. It is noted in the epic as a later step, to decide after M3.7a to M3.7e have run in a shift.

## Order

After M3.7b (same file).
