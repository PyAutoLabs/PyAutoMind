M3.7c of the autonomous-orchestrators epic. Ruling S7 added to `AUTONOMY.md` under "Shift speed — 2026-11-19", with the human's plan decisions 1 to 3. The watcher timer ticks every 60 seconds and a new `pyauto-orchestrator.path` unit starts a tick when the kick file `%S/pyauto/orchestrator.kick` changes; workers, close-outs and branch-update sessions write it after their marker (decision 1). A `decision-taken` PR is refused for `/prm` at PR-open from the label alone (read in the watcher's existing `gh pr view`, once per PR per shift; an unreadable label is refused only after 3 misses over 15 minutes), with no session, slot or CI read; it stays an earlier PR in the M3.6j merge order. The shift closes early when nothing is live or startable and no input is unreadable; a paused shift never does (decision 2), and a park on a question does not hold it open (decision 3). The digest gains an early-close line and a "Waited behind your /prm" section. 32 new tests in `tests/test_watcher_latency.py`.

## Merge receipts

- PyAutoBrain#691: 1f51de13e (merged by the human's /prm, 2026-11-19)

Feature head b76fb79 is an ancestor of origin/main. Organ repo: no release obligation. Deploy (human, no shift live): pull the canonical Brain checkout, copy the service, timer and path units to `~/.config/systemd/user/`, daemon-reload, restart the timer, enable the path unit.

## Validation and review

Tests first; full Brain suite 2484 passed, 1 skipped; skill line budget, tenant firewall and discovery OK; `systemd-analyze --user verify` clean apart from two `TriggerLimit*` keys systemd 249 ignores; Heart scoped verdict green; PR CI GREEN on 3.12 and 3.13. Independent review (Opus 5.5): round 1 FINDINGS (failed steering or Mind reads let the shift close early; systemd start limit; unbounded label reads; carried merged PR misreported; missing guard tests), fixed; round 2 FINDINGS (3 label misses in 2 minutes refused PRs), fixed as suggested. Tier: judge (no shadow row).

Known effects: with the early close, the M3.6j in-shift path runs only while other work keeps the shift open; a `/add` after an early close is not read, as after review-at.

## Original prompt

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
