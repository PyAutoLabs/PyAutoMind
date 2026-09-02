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
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: two-slot-batching
Filed: 2026-08-30

Parent tracker for the move from **one task per chat, babysat** to **a bounded
human slot and everything else unattended**. Never routed to `/start_dev`
directly — each phase is its own prompt, issued ONE AT A TIME.

The slug says "two slots" because that was the opening goal. The sizing decision
taken 2026-08-30 — one slot a day as the baseline, plus a fill-only floor — was
**superseded 2026-08-31** (see "Slot timing" below): there is no daily baseline
and no floor. A slot is whenever the human comes in, and at dispatch they
declare `review-at:`, the horizon the shift is sized against. The slug stays;
nine prompt headers and `epics.md` point at it.

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
   half is planned against the review-minutes the human declares for that slot
   (default 45), and everything above that is *fill*: work that costs zero
   review-minutes. The budget follows the nature of the work and the human's
   schedule, never a fixed rhythm.
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

**CORRECTION 2026-08-30, measured in phase 0b.** This epic was filed asserting
that one rule caused the 120 — `_intake.py:276` returned `supervised` whenever
`repo_count > 1`, and nearly every real task names a library plus its workspace.
Removing it and re-deriving every prompt says otherwise:

| | `safe` | `supervised` | `human-required` |
|---|---|---|---|
| with `repo_count > 1` | 30 | 117 | 6 |
| without it | **55** | 92 | 6 |

`repo_count > 1` is the *sole* supervised trigger for **25** prompts — the
largest single one, ahead of `large`-or-above (20) and architectural risk (17),
but nothing like 120. The triggers overlap heavily, and the 120 are *declared*
levels written by earlier intake runs, not one rule's output. Removing it is
right on its merits and frees 25 prompts; it is not the unblocking of the
backlog it was taken for. **Where that actually lives is phase 3's
ship-sign-off change** — 19 of the 46 parked rows are the contract park
`supervised` imposes at ship, and no grading change touches them.

Also measured and reverted, recorded so it is not re-proposed: replacing
`repo_count` with `human_judgement` as a supervised trigger made things *worse*
(`safe` fell to 24), because the ambiguity keywords fire on 63% of prompts. It
was the same mistake as the rule it replaced — a loose proxy standing in for a
judgement it does not measure.

The evidence usually cited for relaxing autonomy does not survive scrutiny
either, and this epic must not pretend otherwise. `autonomy_log.md` shows 238
rows and zero `rejected`, against a graduation rule of "≥10 clean rows with zero
rejected". Four things are wrong with using that here:

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

- **SLOT** — a human sitting down to review, **whenever they come in**. Not
  scheduled and not daily. Budgeted in review-minutes, which the human may set
  per slot (default 45).
- **SHIFT** — the unattended interval from dispatch to the `review-at:` the
  human declared at dispatch.
- **BATCH** — what is dispatched into one shift: a *review-bearing half* sized by
  the slot, plus a *fill* sized by the remaining allowance.
- **FILL** — work that costs zero review-minutes: tier-`notify` work, the
  adversarial review leg, slicing, witness authoring, re-grading, deeper
  verification. Never research — a verdict is the most expensive review there is.
- **FLOOR** — *closed 2026-08-31, never built.* It was the fill-only batch that
  would dispatch whether or not the human turned up; timing now lives with the
  human, so a missed `review-at:` dispatches nothing and the grant expires.
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

0. **The review-cost model**, split three ways on 2026-08-30 — the Feature
   Agent derived `too-large` (score 11) against a declared `large` and
   recommended phasing, which is this epic's own slicing rule firing on its own
   prompt. Each child is one unattended run with its own witness:
   - **0a** the grader — four read-only outputs on the sizing faculty.
     `complete/2026/08/batch-grade-faculty.md`
   - **0b** intake writes them, `infer_autonomy` is fixed, and the autonomy
     change ships as a dated experiment. The distribution is a **dry run** here,
     so the rule is reviewable on its numbers before it touches 137 files.
     `complete/2026/08/batch-grade-intake.md`
   - **0c** re-grade the backlog and give the dashboard a slot-shaped pick list.
     `complete/2026/08/batch-grade-backlog.md`
1. **The queue and the batch record** — **SHIPPED 2026-08-30.** `queue.md`,
   `batches/` (both on the ledger side of `ledger_merge.py`, so batch history
   lands without a human), and the `Lane:` header.
   `complete/2026/08/batch-queue-and-records.md`
2. **The `batch` conductor** — **`plan` SHIPPED 2026-08-30**, **`collect`
   SHIPPED 2026-09-02** (`complete/2026/09/batch-collect.md`); `slice` remains,
   re-filed as `draft/feature/pyautobrain/batch_slice.md`. `plan` is useful alone: run it in a slot and dispatch by
   tapping the dashboard's existing chips. `draft/feature/pyautobrain/`
3. **The gate under unattended conditions** — **SHIPPED 2026-08-30.** All four
   doctrine changes are in `AUTONOMY.md`, dated, each with a revert condition:
   what a batch launch is (membership fixed at approval, grant expires with the
   shift, the human dispatches); leg 4's shift-scoped Heart acknowledgement;
   leg 5, the independent adversary (`review --witness … --adversary`); and
   decide-and-flag capped at one per PR. `rejected-at-review` landed in 0b.
   `complete/2026/08/batch-gate-unattended.md`
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
   `draft/research/euclid/` — **SUPERSEDED 2026-09-02** by cortex-birth phase 5
   (the Cortex is the science lane's home; `Lane: local-dev` is every Cortex
   phase's).

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
- **The human's return is declared, and estimates slip.** An academic with
  papers and meetings will come back late and disappear for conference weeks. A
  missed `review-at:` dispatches nothing new — the grant simply expires — so
  backpressure is about review-queue *depth*, not timing: it must ramp down,
  never deadlock to zero.
- **Green is not done** — officially: a cloud session's green status "means the
  session started and exited without an infrastructure error. It does not mean
  the task in your prompt succeeded." Delivery must be asserted, never inferred.
- **20% of August records carry a CORRECTION or a retraction** (68/332). That is
  the base rate against which any "the agent judged this safe" mechanism must be
  sized.

## Independent review — 2026-08-31 (claims re-run; plan amendments)

An independent adversarial session recomputed every load-bearing claim in this
epic and its shipped doctrine, and read the four AUTONOMY.md changes in full.
The grading claims all reproduce exactly (151/153 judge; 33/104/16 given a
witness; repo_count sole trigger for 25, safe 30→55; human_judgement variant
safe 24 on 63% keyword firing; 31 of 101 ready resolve safe). What did not:

- **"68 of 332 records carry a CORRECTION or retraction (20%)"** reproduces
  only as a case-insensitive grep for `correction|retract`; ~11–13 of the 68
  are false positives (the lensing *potential correction* feature name, and
  "correction" describing a task's own deliverable). Honest count **~55–57
  (17%)**, or 33 (10%) demanding an explicit marker. Every doctrinal use
  survives at 17%; stop re-citing 68/20%.
- **"94 of 332 name two or more PRs"** does not reproduce. Strict distinct
  PR-URL count: **48**. The 94 is only reachable via `Repo#N` shorthand, which
  cannot distinguish PRs from issues or a task's own PRs from cited prior art.
  Backpressure-in-tasks-not-PRs still stands at 48.
- "150 prompt files rewritten" — the regrade commit touched **153**; 150 is
  the count *left without a witness*.
- AUTONOMY.md's trigger ranking "large-or-above (20), architectural risk (17)"
  recomputes to **16 and 16** (25 remains the largest; the ranking holds).
- **The correction's own redirect is unshipped.** This file says the backlog
  "actually unblocks" at phase 3's ship-sign-off change — but phase 3 as
  shipped changes no supervised ship sign-off. Decide-and-flag excludes
  `judge`-tier, 151/153 of the backlog grades `judge`, so it currently applies
  to nothing, and the planner still rejects 72 prompts as "would park at
  ship". The real unblocking chain is witness adoption → glance/notify →
  bigger batches, and until the witness work happens, two-member batches are
  the steady state.

**Plan amendments**, in priority order:

1. **Before the first real batch: one doctrine edit to AUTONOMY.md "Leg 4
   under a batch launch", closing two holes.** (i) A new YELLOW reason may be
   classified "generated by an earlier member" only by matching an
   expected-effect line the *human* wrote into the batch record at dispatch
   ("member X merges into PyAutoArray and may stale release validation") —
   the run's own 4am attribution is an autonomous acknowledgement, which the
   page's hard invariants forbid, made by the party with the incentive to
   ship. (ii) State the mechanism by which a member session learns the
   shift's grant: it reads `batches/<date>-<am|pm>.md` at its leg-4 check,
   and a member finding no batch record treats itself as a solo `--auto`
   launch. Without (ii) the leg-4 change never operates — dispatch hands each
   member only `/start_dev <path> --auto`, nothing tells it a shift ack
   exists, and every batch returns parked questions.
2. **The witness campaign becomes owned work, not a fill remark.** It is the
   single highest-leverage item in the design — the whole distance from
   151-judge to 33/104/16 — and no phase owns it. Human-declared witnesses
   only; the no-invention rule stands.
3. **`collect` outranks `dispatch`.** The slot's real cost is assembling the
   review packet (adversary verdicts, delivered-vs-green, decision-taken
   ordering), not the two minutes of dispatch tapping. Build the review
   packet before the dispatcher (reorder effort within phases 5–6).
4. **Noted, small, none blocking batch 1:** `_sizing.py discover_prompts`'s
   legacy-flat fallback sweeps the Mind's real `docs/` folder in as 5 phantom
   prompts (158 ≠ 153) for any caller not restricted to `draft/`; no
   ingestion path exists from `review-minutes-actual:` back into the seeds;
   leg 4's "repo intersects the run's repos" test has no defined parse for
   reason strings naming no repo ("release validation FAILED (stage
   integrate)"); and `pyauto-brain vitals` is unreachable from a web
   container (no Heart checkout), so the dispatch procedure needs a "Heart
   unreadable from this lane" branch saying what the batch record records.
5. **Calibration prior:** a cold read of six August library records averaged
   ~41 review-minutes each (range 15–75). "An honest hour holds about three"
   is *generous* for unwitnessed work — plan on **two** judge-tier
   library-touching members per slot until `review-minutes-actual:` says
   otherwise.

## Development through use — 2026-08-31

The first review session was run for real (packet `batches/packets/2026-08-31-am.html`),
and use redrew the build order the plan guessed at. Recorded here so the ledger
tracks reality, not the plan-as-imagined.

**What use built that the plan never had:** the review surface itself — per-member
decisions and notes on the packet page, submit → `batches/reviews/<date>-<slot>.md`;
science-run members scored against pre-registered witnesses (health evidence ≠
sacct COMPLETED); retrospective members for merged phases the human skipped; the
laptop mirror (`Science/inference_programme/` + `autolens_profiling hpc/sync pull`)
so every pointer is a local path; the public packet archive on Pages; and
`review-at:` (see "Slot timing").

**Phase verdicts, measured against what shipped:**

- **0, 1, 3 — shipped** (0a `PyAutoBrain` main `e755ddd`, 0c `PyAutoMind` main
  `1a70a6fb`; status headers reconciled today).
- **2 — `plan` shipped; `collect` is now the top build item and is
  spec-complete from use**: the spec is `batches/packets/TEMPLATE.md` plus the
  2026-08-31 packet's "what a `batch collect` for science runs would need to
  automate" list (stamp the stack per task at import time; never trust State;
  preserve sampler state on reference runs; score against the pre-registered
  witness, never the sampler's flag; pull the witness file; diff A/B siblings).
  `slice` waits.
- **4 — shadow running**, window closes 2026-09-27. Untouched.
- **5 — dispatcher deferred.** The orchestrator-chat model (one chat plans and
  collects; cloud members get their own sessions; local-dev members are
  paste-lines, dispatched first in the evening while the laptop is on)
  supersedes it in spirit. Revisit only if dispatch tapping becomes the
  measured bottleneck.
- **6 — board re-scoped by the human 2026-08-31, and wanted soon:** not a
  second published surface — a "Batches" strip near the top of the Mind
  dashboard, ABOVE "Start here". Prompt re-cut accordingly
  (`draft/feature/pyautobrain/batch_board.md`, now `small`).
- **7 — slimmed**: the 100%-allowance decision stands; the burn-up read is
  unbuilt; the one-slot-a-day sizing went with the floor.
- **8 — half-shipped through use**: the mirror + routine pull is a stronger
  mechanism than the planned manifest-first transport (full outputs on the
  laptop, not manifests). Still owed: leg A, the `Lane:` recut of the remaining
  euclid phases. Leg B survives only for the laptop-off cloud-reasoning case.
  **Superseded 2026-09-02** by cortex-birth phase 5: the science lane's home is
  the Cortex, where every phase is `Lane: local-dev` by construction and the
  batch conductor's `--kind cortex` reads it, so the owed `Lane:` recut has no
  surface left to recut. `batch_science_lane.md` is marked superseded and
  `queue.md` #9 retired.

**Dead — do not resurrect:** the floor (closed, "Slot timing"); the dispatcher,
for now; the standalone board surface; manifest-first-as-transport.

**Still live from the independent review:** amendment 1's leg-4 holes (closed in
PyAutoBrain PR #323 alongside this edit: members read the batch record at leg 4;
"generated by an earlier member" must match a human-written `expected-effects:`
line) and amendment 2, the witness campaign — now owned work,
`draft/feature/pyautomind/witness_campaign.md`, queued.

## Slot timing — 2026-08-31

**Decided: the human declares the review horizon at dispatch; the floor is
closed.** A slot is whenever the human comes in — not a scheduled hour, not once
a day, no second-slot assumption. At dispatch they state `review-at:`, an ISO
timestamp for when they expect to be back, and **the shift is the interval
dispatch → `review-at:`**. It is written into the batch record, and the batch's
grant expires there (`AUTONOMY.md`, "What a batch launch is"). The budget is
still review-minutes and still defaults to 45, but the human sets it per slot —
they know whether the next one is a quick morning check or a long afternoon.
This is what makes the pattern bend to a work schedule and to the nature of the
work rather than to a rhythm nobody can keep.

**The FLOOR is closed, not deferred, and was never built.** It was the fill-only
batch that would dispatch whether or not the human turned up. With the human
carrying the timing there is nothing for it to do: if they do not show, nothing
new dispatches and the outstanding grant expires at `review-at:`. Recorded as
closed so nobody re-derives it — revisit **only** if the queue is found starving
during a long absence. Backpressure is untouched: it ramps on review-queue
depth, which is not a timing question.

Phase 7's "spend the whole allowance" decision is untouched; only the "one slot
a day" sizing assumption that rode along with it goes.

## Notes

- Issue phases ONE at a time. No bulk issue queues.
- Phase 4 is a decision, not an implementation task. Do not start it as code.
- 2026-08-31: independent review re-ran every claim; corrections and plan
  amendments in the dated section above. Amendment 1 (the leg-4 doctrine
  edit) precedes the first real batch.
- 2026-08-31: slot timing moved to the human — `review-at:` declared at
  dispatch, the shift is dispatch → `review-at:`, the per-slot budget is the
  human's, and the floor is closed. See "Slot timing — 2026-08-31".
- 2026-08-31: development through use redrew the build order — collect
  spec-complete and top of the queue, dispatcher deferred, board re-scoped to a
  dashboard strip, phase 8 half-shipped via the laptop mirror. See "Development
  through use — 2026-08-31".
