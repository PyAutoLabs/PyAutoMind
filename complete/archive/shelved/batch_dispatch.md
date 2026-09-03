# Batch phase 5 — dispatch

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoMind
Themes:
- mind-workflow
Difficulty: large
Autonomy: supervised
Priority: normal
Status: SHELVED 2026-09-03 — the retired batch epic's own ledger calls the dispatcher "dead — do not resurrect"; the human dispatches by tapping the dashboard's chips and never needed it (ledger complete/archive/epics/two_slot_batching_epic.md)
Consequence: judge
Review-minutes: 25
Unattended: ready
Filed: 2026-08-30

The least important phase in the epic, deliberately scheduled late. Until it
exists the human dispatches by tapping the chips the dashboard already renders,
which costs a couple of minutes at the end of a slot and buys all of phases 0-4's
value. Build this only once the review economics are working.

## Shape

One **architect** session per shift, launched by the human at the end of the slot
(so the launch is a human act — see phase 3 on what a batch launch is). It reads
the approved `BatchDecision` and fans out one **implementer** run per member,
each carrying the member's prompt, its witness, and the shift's Heart reason set.

## Pacing, not fan-out

Dispatch in **waves of at most three**. Two reasons, both measured:

- Concurrent instances share one rate-limit window, and exhausting it stalls
  every member at once — the morning then shows nothing done.
  `anthropics/claude-code#62426` reports five to six concurrent instances on the
  top paid tier being blocked with "Server is temporarily limiting requests (not
  your usage limit)" — an infrastructure limit distinct from the plan quota.
- Effective parallelism is bounded by distinct hot repos anyway (phase 2), so
  wide fan-out buys nothing but contention.

Wall-clock is not scarce overnight. Throughput per window is.

## Substrate, and its degrade paths

Preferred: sibling cloud sessions spawned from the architect session. Observed
working today, but **undocumented and preview-shaped**, so the design must
degrade rather than depend:

1. sibling sessions, paced waves;
2. failing that, the architect runs members **sequentially** in its own session —
   slower, and it must then respect the compaction rule that made each member a
   single-run task in the first place;
3. failing that, one `workflow_dispatch` per member against
   `anthropics/claude-code-action@v1`, which runs in automation mode on any
   event. Note it bills the **same** subscription when authenticated with a
   `CLAUDE_CODE_OAUTH_TOKEN`, so this is a different execution surface, not a
   second budget. GitHub-hosted jobs cap at 6 h.

Scheduling primitive: a **Routine** (custom cron, one-hour minimum interval, or a
one-off timestamp). Keep routine use to two or three fires a day — the packet
build before each slot and a mid-shift watchdog — because there is a documented
per-account daily cap on routine runs. Do not spend one fire per task.

## The watchdog

A cloud session's VM is reclaimed after inactivity and **in-flight background
work is lost**, with no documented TTL and no warning. So a mid-shift check must
report, in the batch record: which members reached PR-open, which are still
running, which stopped without delivering, and which never started. A member that
vanished is a *finding*, not an absence.

## Done when

- `batch dispatch` refuses to launch a batch the human did not approve in a slot.
- Concurrency is capped and configurable; the cap is stated in the batch record.
- Each degrade path is exercised by a test or a documented manual run.
- The watchdog's output distinguishes "asked, nothing" from "could not ask" — the
  lesson already paid for once in `complete/2026/08/mobile-performance-review.md`.
