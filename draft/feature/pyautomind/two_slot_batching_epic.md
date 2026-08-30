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

Parent tracker for the move from **one task per chat, babysat** to **a bounded
human slot and everything else unattended**. Never routed to `/start_dev`
directly — each phase is its own prompt, issued ONE AT A TIME.

The slug says "two slots" because that was the opening goal. The sizing decision
taken 2026-08-30 is **one slot a day as the baseline, plus a fill-only floor** —
a second slot is welcome and the planner will compose for it, but nothing is
sized on the assumption it happens. The slug stays; nine prompt headers and
`epics.md` point at it.

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

1. **Price review honestly and compose against it.** A batch's review-bearing
   half is planned against ~45 review-minutes — **one slot a day is the
   baseline**, a second is opportunistic — and everything above that is *fill*:
   work that costs zero review-minutes.
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
that reduces total attention rather than re-timing it**. The human decided on
2026-08-30 to **shadow it for four weeks** before granting or refusing it; phase
4 holds the protocol and the pre-registered decision rule, and the window is
already open.

**How much of the flow it can ever cover.** Bucketing all 332 August records by
the repos their PRs name: organ repos only **56 (17%)** — the `notify` candidate
pool; workspace/assistant/profiling only 52 (16%); touches a core library 99
(30%); **names no PR at all — research, decisions, written verdicts — 125
(38%)**. So the window will be well powered at roughly fifty candidates, and the
tier's ceiling is about a sixth of throughput. Worth the doctrine change, and
not the whole answer: the largest single bucket is judgement-shaped by nature,
and nothing here makes a written verdict cheaper to read. Say so rather than
letting the plan imply otherwise.

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

- **SLOT** — a human hour, **once a day as the baseline**, budgeted in
  review-minutes. A second slot is a bonus, never an assumption.
- **SHIFT** — the unattended interval between slots.
- **BATCH** — what is dispatched into one shift: a *review-bearing half* sized by
  the slot, plus a *fill* sized by the remaining allowance.
- **FILL** — work that costs zero review-minutes: tier-`notify` work, the
  adversarial review leg, slicing, witness authoring, re-grading, deeper
  verification. Never research — a verdict is the most expensive review there is.
- **FLOOR** — the fill-only batch that dispatches whether or not the human turns
  up. Fill-only is what makes it safe: a floor of review-bearing work just digs
  the hole deeper while they are away.
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
4. **The tier-A merge tier** — **decided 2026-08-30: shadow for four weeks**
   (window closes 2026-09-27), then grant, narrow or refuse against a
   pre-registered rule. Stage 1 rows are already being appended to
   `autonomy_log.md`, so the window is running and is not on the critical path.
   `draft/feature/pyautobrain/`
5. **Dispatch** — paced waves, concurrency cap, one member per library repo,
   degrade paths. `draft/feature/pyautobrain/`
6. **The batch board** — built before the slot starts. `draft/feature/pyautobrain/`
7. **Spend the whole allowance** — **decided 2026-08-30: target 100% of the
   weekly limit**, so the failure mode is *underspend*. Human review capacity
   caps the review-bearing half; the surplus goes to fill. Controlled by a weekly
   burn-up read once per slot. `draft/feature/pyautomind/`
8. **The laptop lane** — **decided 2026-08-30: science stays on the laptop**, and
   the lane is made first-class rather than engineered away.
   `draft/research/euclid/`

## The laptop lane, separately

**Decided 2026-08-30: science projects stay on the laptop.** Mobile sessions
cannot easily reach RAL, and an HPC outage would block everything — a canonical
home on RAL trades a dependency the human controls for one they do not. So the
laptop lane is *accepted* and made first-class rather than engineered away.

Closed by that decision, and recorded so nobody re-derives them: RAL as canonical
home; a git-courier cron on the login node (its value collapses once the laptop
must be on to hold the data anyway); a Globus Compute endpoint or a self-hosted
GitHub runner there (same, plus both are persistent login-node processes needing
an operator conversation). Already closed on other grounds: SSH from a Claude
container in any variant, Open OnDemand, Cirun — and the fact that
`euclid-dr1-prep` phases 4, 6a and 6b say in their *own prompts* that they are
human-driven and supervised with a judged verdict as the deliverable, so no
transport was ever going to make them unattended.

What survives, and matters more now:

- **The prepare / execute recut** — now the main lever, because it is the only
  thing that moves science work into the lane that can run unattended.
  Submission scripts, analysis code, plotting, catalogue tooling and library
  audits (phase 6c is already flagged as the one phase that could land as a fast
  standalone fix) are ordinary cloud work. Only the run itself is bound.
- **Manifest-first results**, for a changed reason: not to reach RAL, but to let
  a *cloud* session reason about outcomes while the laptop is off. The laptop
  pushes small result JSONs, catalogue CSVs and downsized PNGs when it is on; a
  cloud session reads those and plans the next submission without ever opening a
  FITS file.

The lane uses the vocabulary `PyAutoBrain/skills/WORKFLOW.md` already defines
rather than a parallel one: `Lane: any | local-dev`. **A session detects its own
lane and refuses to plan the other**, reporting rather than silently dropping —
*"4 local-dev tasks are ready, run this from the laptop"* — and a `local-dev`
batch is dispatched by the human, from the laptop, in a slot drained
opportunistically when they are doing science anyway. One queue holds both lanes;
the planner filters.

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
