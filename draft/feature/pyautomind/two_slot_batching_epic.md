# Two slots a day — the batch workflow

Type: feature
Target: pyautomind
Repos:
- PyAutoMind
- PyAutoBrain
Themes:
- mind-workflow
- dashboard
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: draft
Epic: two-slot-batching
Filed: 2026-08-30

Parent tracker for the move from **one task per chat, babysat** to **two human
hours a day and everything else unattended**. Never routed to `/start_dev`
directly — each phase is its own prompt, issued ONE AT A TIME.

## The goal, in the human's words

> "Two chunks of time (ideally 1 hour each) per day where I review all completed
> tasks, merge them or write tweaks, and then submit the next batch. These tasks
> run end to end autonomously without input from me. The key goal is to minimise
> the amount of time I need to look at AI development and review, and enable a
> clear split between when my brain is doing this sort of work and when it can
> focus on other tasks like reading papers, science admin or meetings."

Two named problems: waiting on chats fragments attention; and tasks finish at
scattered times, so review never happens as a block and a human-review backlog
has begun to accumulate.

## The finding that reorganises everything else

**The bottleneck is not dispatch. It is the human's judgement, and the obvious
version of this design increases demand for it.**

August 2026 shipped **332 completion records, about eleven a day**, with the
human in-session. There is no throughput problem. What an honest reading of
those records shows is what "review" actually costs:

| Record | Filed as | What reviewing it really is |
|---|---|---|
| `cmap-magma-default.md` | small-medium, safe | a reach audit across three libraries, a user-visible behaviour change (silently-ignored config now raises), 2 PRs, 11 tests — **15-25 min** |
| `autoarray-adapt-images-precondition.md` | medium bug | an API-philosophy fork decided on behalf of an external reporter — **15-20 min**, and un-delegatable |
| `harvest-0827-gate-b-pt2.md` | medium | "factor ≤1e5 licensed, 1e8 rejected, six caveats" — the review *is* a PI's scientific ruling |
| `mge-lane-death.md` | medium research | survival-integral reasoning, a three-arm experiment, a "not citable" caveat, six spawned follow-ups — **30-60 min** |

94 of 332 August records name two or more PRs, so "one task, one quick PR
glance" is wrong in shape as well as size. At honest cost a one-hour slot holds
**about three of these, not eight**. Any design that dispatches sixteen tasks a
day into a review capacity of six makes the human do *more* AI-development
hours than today, at 6am, from a phone.

So the epic's real subject is **reducing human judgement per merged unit**, not
scheduling more of it. Three levers do that, and everything else is tuning:

1. **Price review honestly and compose against it.** A batch is planned against
   a 60-minute review budget, not a task count.
2. **Make work reviewable by construction.** The records that *are* reviewable
   in minutes are the ones carrying machine-checkable witnesses — "ids
   bit-identical, 62→9.7 ms", "31-rule byte-equality", control-tested spy
   sentinels. Reviewability is a property of how work was scoped and witnessed,
   not of how the report was written. So require the witness **at conception**.
3. **Spend tokens instead of minutes where it is safe to.** An independent-model
   adversarial review is the mechanism that actually caught the real errors in
   this organism's history — not the four-leg gate.

## The diagnosis — the backlog is not batch-ready

Measured on `draft/` at filing (137 headed prompts):

| Header | Distribution |
|---|---|
| `Autonomy:` | **supervised 120** · safe 10 · human-required 7 |
| `Difficulty:` | medium 49 · **too-large 31** · **large 27** · small 26 |
| `Themes:` | present on 140/141 · `Epic:` 34 · `Blocked-by:` 5 |

`AUTONOMY.md` defines `supervised` at the ship checkpoint as "park
(`awaiting-input`), question to the issue, continue elsewhere". A batch of six
supervised tasks returns six questions, not six PRs.

The cause is one rule measuring the wrong thing —
`PyAutoBrain/agents/conductors/intake/_intake.py:276` returns `supervised`
whenever `repo_count > 1`, and nearly every real task names a library plus its
workspace. Repo count is blast radius; the level is supposed to encode judgement
required.

**But the evidence usually cited for relaxing it does not survive scrutiny, and
this epic must not pretend otherwise.** `autonomy_log.md` shows 238 rows and zero
`rejected`, against a graduation rule of "≥10 clean rows with zero rejected".
Four things are wrong with using that here:

- The rows run densely 2026-07-08 → 08-01 and then stop: **about 7 rows for all
  of August, against 332 August completions.** The calibration base is July,
  human-in-session work — the one regime that is *not* what this epic proposes.
- The human was in the loop for nearly every row ("human-directed merge
  in-session", "park released same-session by human"). Failures were corrected
  before they could become rows.
- `rejected` is structurally unreachable. A human rejecting a run's
  recommendation was logged `amended`; an entire shipped mechanism withdrawn —
  five PRs closed, branches deleted — was logged `reverted`. Two rows say
  verbatim "NOT a clean row for graduation purposes".
- Most damning: the 2026-07-09 calibration review raised the work-type caps
  **because** `infer_autonomy` was conservative about multi-repo work. Every
  clean row was generated with that guard on. Citing them to remove the guard is
  using evidence collected under a safety device to justify deleting it.

The raise may still be right. The argument is not. So phase 3 runs it as a
**dated experiment** with a human-stamped `rejected-at-review` outcome, not as a
graduation.

## Three consequence tiers — the spine

Decided **at conception, by rules over repo class and surface**, never by the
agent's own assessment of its work:

| Tier | What it is | Review | Gate |
|---|---|---|---|
| **A — notify** | docs, notebooks, profiling scripts, organ-repo tooling, test-only, pure refactor with a byte-equality witness | none; the human is told, and can revert | four legs **plus a mandatory independent-model adversarial review** |
| **B — glance** | library-internal change carrying a machine-checkable witness; workspace scripts | 2-5 min — the human reads the **witness**, not the diff | four legs + witness verified |
| **C — judge** | public API, defaults, error contracts, science policy, anything with an external reporter, anything with no witness | 15-25 min; the human is PI | four legs; human merges |

**No witness declared ⇒ tier C.** That single default is what makes the witness
requirement bite at conception rather than being aspirational.

Tier A is a genuine doctrine change — `AUTONOMY.md` today says merge and
issue-close are "human, always" — and it is **the only mechanism in this epic
that reduces total attention rather than re-timing it**. It is the human's
decision to make, explicitly and dated, and phase 4 exists to put it to them
with the evidence rather than to assume it.

## What already exists and must be reused

`skills/start_bundle` (architect + implementer, one issue and PR per member).
The auto-bundler's theme-affinity packing. The Mind dashboard and the Brain
board as published-surface precedents. The four-leg gate ending at PR-open.
`active.md` as cross-environment state, already carrying `status:`, `location:`,
`question:`. `mind_ledger_merge.yml`. `morning_status.yml` as the
Claude-on-a-cron precedent. And
`draft/feature/pyautomind/bundle_nightly_claude_pass.md`, parked 2026-08-27 for
want of a driver — this epic is the driver.

## What does not exist

No queue (`board/_board.py:644` already reads a `queue.md` defensively and always
gets `None`). No batch record. No budget. No consequence tier, no witness, no
review-cost estimate. No decomposition pass, though doctrine has named one since
inception. No machine-readable epic phase state. No dispatcher. No review surface.

## Vocabulary

- **SLOT** — a human hour, twice a day, budgeted in **review-minutes**.
- **SHIFT** — the unattended interval between slots.
- **BATCH** — what is dispatched into one shift.
- **QUEUE** (`queue.md`) — the human's ordered wishlist; they never compose a
  batch by hand.
- **WITNESS** — the machine-checkable claim that makes a task reviewable.

## Placement — no new organ

`PyAutoBrain/AGENTS.md`: "New capability grows as a faculty, not a new organ,
unless it owns state or effects no existing organ can."

| Part | Home |
|---|---|
| Queue, batch records, new headers | **PyAutoMind** ledger — workflow state it already owns, and it auto-merges |
| Consequence tier, witness check, review-minutes, slicing | **PyAutoBrain** `agents/faculties/sizing/` — these are *opinions*, and `ORGANISM.md` forbids a conductor consulting a conductor |
| `batch` conductor (plan / dispatch / collect) | **PyAutoBrain** `agents/conductors/batch/` — thin, because the judgement lives in the faculty |
| The batch board | A second published surface, exactly as pictured: the Mind dashboard is *what could be done*, this is *what is in flight and what it produced* |
| The shift scheduler | A workflow or Routine. Precedent: `nightly-release.yml`, "a scheduler, nothing more" |

**Graduation trigger** to a real organ (the circadian layer, `PyAutoRhythm`):
only when the batch layer owns effects no organ can — its own dispatch
credentials, its own budget ledger, its own runners — *and* the conductor exceeds
a conductor's worth of machinery. Not before, never for symmetry.

## Roles, not model names

| Role | Does | Claude | Codex |
|---|---|---|---|
| Architect | plans the batch, judges members, never implements | Fable | *(no orchestrator — run the lane sequentially)* |
| Implementer | one task, end to end, to PR-open | Opus | Codex |
| Adversary | the independent review leg | **a different model from the implementer** | ditto |

Invariants: the adversary is never the implementer, and **a run never writes its
own approval** — a measured failure mode, not a hypothetical (agents forging
"user-approved" ratification files is one of twelve primitives in
`anthropics/claude-code#54393`, a postmortem of five consecutive failed
autonomous overnight runs).

## Phases

Ordered by value, not by build dependency. **The dispatcher is the least
important part** — phases 0-4 can all be driven by hand in the slot, tapping the
chips the dashboard already renders.

0. **The review-cost model** — consequence tier, witness requirement,
   review-minutes, readiness grade; fix `infer_autonomy`; re-grade all 137
   prompts. `draft/feature/pyautobrain/`
1. **The queue and the batch record** — `queue.md`, `batches/`, `Lane:`, the
   `ledger_merge.py` allowlist. `draft/feature/pyautomind/`
2. **The `batch` conductor: plan, slice, collect** — reasoning only, no
   dispatch. `draft/feature/pyautobrain/`
3. **The gate under unattended conditions** — the adversarial fifth leg;
   batch-aware Heart semantics; what a batch "launch" means; decide-and-flag,
   capped; the `rejected-at-review` outcome and the dated autonomy experiment.
   `draft/feature/pyautobrain/`
4. **The tier-A merge tier** — the doctrine decision that buys back throughput.
   `draft/feature/pyautobrain/`
5. **Dispatch** — paced waves, concurrency cap, one member per library repo,
   degrade paths. `draft/feature/pyautobrain/`
6. **The batch board** — built before the slot starts. `draft/feature/pyautobrain/`
7. **Budget and backpressure** — window readings, soft ramp, bucket reservation.
   `draft/feature/pyautomind/`
8. **The science lane** — prepare/execute recut, manifest-first results, the HPC
   bridge assessment. `draft/research/euclid/`

## Standing risks every phase must respect

- **Heart is the most park-productive gate in the system and nobody can ack it
  at 3am.** The log shows a YELLOW reason set growing 2→4→6 *across one day*, and
  a run's own sibling merge manufacturing a new reason that would park later
  waves. It has already produced a doctrine violation under pressure (a
  *standing* RED ack, which `AUTONOMY.md` explicitly voids). Phase 3 owns this.
- **Ambient activation.** `AUTONOMY.md`: levels bind "only when the human
  launches with an explicit `--auto` … never ambient: no config flag, no
  environment variable, no 'remembered' mode." A wave firing at 4am under a slot
  approval is a stored grant unless doctrine says what a batch launch *is*.
- **Effective parallelism is about two or three, not six.** August records name
  PyAutoFit 118/332, PyAutoArray 98, PyAutoGalaxy 82, PyAutoLens 78. Concurrent
  members don't collide at dispatch (separate worktrees) — they collide at
  *merge*, because the first `/prm` moves `main` and invalidates the others'
  test and smoke evidence.
- **A missed slot is the common case, not the exception.** An academic with
  papers and meetings will miss slots and disappear for conference weeks.
  Backpressure must ramp down, never deadlock to zero.
- **Green is not done** — officially: a cloud session's green status "means the
  session started and exited without an infrastructure error. It does not mean
  the task in your prompt succeeded." Delivery must be asserted, never inferred.
- **20% of August records carry a CORRECTION or a retraction** (68/332). That is
  the base rate against which any "the agent judged this safe" mechanism must be
  sized.

## Notes

- Issue phases ONE at a time. No bulk issue queues.
- Phase 4 is a decision, not an implementation task. Do not start it as code.
