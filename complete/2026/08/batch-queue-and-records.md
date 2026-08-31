- shipped: 2026-08-30 — branch `claude/autonomous-task-batching-k8lw9t`.
- classification: feature (PyAutoMind) — epic `two-slot-batching`, phase 1.
- summary: the ledger side of the batch workflow — two new files and one new header, no
  reasoning and no dispatch. `queue.md` is the human's ordered wishlist, the one thing they
  maintain by hand between slots, where file order *is* priority and an entry is a `prompt`,
  an `epic-slice` or a `theme-sweep` (with an optional `lane:`), leaving the queue only when
  its work reaches `complete/`, not when it is dispatched. `batches/<YYYY-MM-DD>-<am|pm>.md`
  is the batch record, written at dispatch and appended at collection, carrying the members,
  the planned and actual review-minutes, the usage window at each end, the shift's Heart
  acknowledgement and a `delivered:` count deliberately not defined as "green" — a member
  counts only with a PR carrying a non-empty diff and checks that actually ran. The `Lane:`
  header (`any | local-dev`) reuses `WORKFLOW.md`'s existing environment vocabulary rather
  than inventing a parallel one, and stays distinct from `active.md`'s live `location:`.
  Both new paths were added to `ledger_merge.py` (`LEDGER_DIRS` gains `batches/`,
  `LEDGER_FILES` gains `queue.md`) so batch history auto-merges instead of waiting on a
  human, and `lifecycle.py check` was taught not to read a batch record as an unclaimed
  active prompt.
- lifecycle: Shipped 2026-08-30 from draft/ without a lifecycle advance (cloud branch
  claude/autonomous-task-batching-k8lw9t); record backfilled 2026-08-31 by the ghost-draft
  reconciliation sweep.

## Original prompt

# Batch phase 1 — the queue and the batch record

Type: feature
Target: pyautomind
Repos:
- PyAutoMind
Themes:
- mind-workflow
- dashboard
Difficulty: small
Autonomy: safe
Priority: high
Status: shipped 2026-08-30 — branch claude/autonomous-task-batching-k8lw9t
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: two-slot-batching
Phase: 1
Parent: draft/feature/pyautomind/two_slot_batching_epic.md
Filed: 2026-08-30

The ledger side of the batch workflow. Two new files and one new header; no
reasoning, no dispatch.

## `queue.md` — the human's ordered wishlist

The one thing the human maintains by hand, and the only thing they have to think
about between slots. Coarse order, not a batch: "roughly what I want done next".
`batch plan` (phase 2) composes the actual batch from it.

An entry is one of three kinds, so that "line up a big epic and take slices of
it" is expressible directly:

```markdown
## <n>. <label>
- kind: prompt | epic-slice | theme-sweep
- ref: draft/<work-type>/<target>/<name>.md    # kind: prompt
- ref: euclid-dr1-prep                          # kind: epic-slice — take the next phase
- ref: numba-cpu                                # kind: theme-sweep — any ready prompt on this theme
- lane: any | local-dev                         # optional; default any
- note: <one line, optional>
```

Order in the file *is* the priority. Entries leave the queue when their work
reaches `complete/`, not when it is dispatched — a task in flight is still the
thing the human wants.

## `batches/<YYYY-MM-DD>-<am|pm>.md` — the batch record

One file per dispatched batch. Written at dispatch, appended at collection.
It is the calibration evidence for phase 6's budget loop, so the observations
matter more than the prose:

```markdown
# Batch 2026-09-03 pm
- dispatched: 2026-09-03T17:40Z
- shift: night
- lane: any
- review-minutes-planned: 42
- usage-window-at-dispatch: <5h %, weekly %, opus %>   # read from /usage
- members:
  - <slug>: <prompt path> — <tier> — <review-minutes> — <outcome>
- collected: 2026-09-04T08:30Z
- usage-window-at-collect: <5h %, weekly %, opus %>
- delivered: <n>/<n>          # reached PR-open with a real diff and checks run
- review-minutes-actual: <n>  # what the slot really cost — the only calibration
- heart-ack:                  # the reason set acknowledged for this shift
  - <reason line>
- notes: |
    What actually happened. Anything that stalled, and why.
```

`- delivered:` is deliberately not "green". A cloud session's green status
"means the session started and exited without an infrastructure error. It does
not mean the task in your prompt succeeded" (Claude Code routines
documentation). A member counts as delivered only with a PR that has a non-empty
diff and checks that actually ran.

## The `Lane:` header

```
Lane: any | local-dev
```

Reuse the environment vocabulary `PyAutoBrain/skills/WORKFLOW.md` already
defines (`local-dev` / `web-github` / `ci-only` / `analysis-only`) rather than
inventing a parallel cloud/laptop one. `local-dev` means the work needs the local
dataset and output trees, an SSH endpoint, or the human at the machine.

A session **detects its own lane and refuses to plan the other**, reporting
rather than silently dropping: *"4 local-dev tasks are ready — run this from the
laptop."* One queue holds both lanes; the planner filters, the human does not
maintain two backlogs. See phase 8.

Note `active.md` already carries `location:` for the `/handoff` flow — `Lane:` is
the prompt-side static fact, `location:` stays the live per-task one. Do not
merge them.

## The `ledger_merge.py` entries

`scripts/ledger_merge.py` is default-deny with a closed exact list, so both new
paths must be added or every batch push waits on a human:

- `LEDGER_DIRS` gains `batches/`.
- `LEDGER_FILES` gains `queue.md`.

That edit is itself code and lands as a normal reviewed PR — once.

## Done when

- `lifecycle.py check` knows about `batches/` (it must not read a batch record as
  an unclaimed active prompt).
- `python3 scripts/ledger_merge.py classify --base origin/main` returns ledger for
  a diff touching only `queue.md` and `batches/`.
- The schemas are documented in `REFERENCE.md` beside the `active.md` schema.
- `queue.md` ships with its own header prose explaining that order is priority.
