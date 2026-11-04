# Batch records

One file per dispatched batch: `<YYYY-MM-DD>-<am|pm>.md`. Written at dispatch,
appended at collection. This is the ledger of what was sent into one shift and
what came back — the same genre as `complete/`, and the evidence base the budget
and the review-minute estimate are calibrated from.

It auto-merges (`scripts/ledger_merge.py` — `batches/` is a ledger dir), because
an unattended system that cannot record its own history unattended will not
record it.

**Collected once, reviewed once.** A dev batch is dispatched as one shift and
reviewed as one sitting: one `- review:` line, one review file. The dashboard's
batch status box is the live view of the open slot — every member with what it
is doing — and it offers the button to the review packet once `collected:` is
stamped, because there is nothing to review before that. A science batch is a
rolling board instead, ruled on more than once and closing only when nothing is
left on the board (`PyAutoCortex/batches/AGENTS.md`, "A rolling board, not a
dispatch"); that difference is the Cortex's, not a change here.

## Schema

```markdown
# Batch 2026-09-03 pm
- dispatched: 2026-09-03T17:40Z
- review-at: 2026-09-04T08:00Z     # stated by the human AT DISPATCH
- shift: night                     # free-text label the human gives it
- lane: any
- integration: yes            # optional, at dispatch: build the review's integration worktree at collect
- review-minutes-planned: 42
- usage-window-at-dispatch: <5h %, weekly %, opus %>
- heart-ack:                  # the reason set acknowledged FOR THIS SHIFT
  - <reason line>
- expected-effects:           # human-written at dispatch, one line per member with reach
  - <member>: <what it may legitimately change, e.g. "merges into PyAutoArray and may stale release validation">
- members:
  - <slug>: <prompt path> — <tier> — <review-minutes> — <outcome>
- outcomes:                   # filled at collect, from the ledger only
  - <slug>: merged | rejected-at-review | carried | unreviewed
- merge-order:                # filled at collect — advice for /prm, not an action
  - 1. <slug> — library (PyAutoFit) — before its workspace dependants
- collected: 2026-09-04T08:30Z
- reviewed-at: 2026-09-04T08:30Z   # when they actually sat down
- usage-window-at-collect: <5h %, weekly %, opus %>
- delivered: <n>/<n>
- packet: batches/packets/<YYYY-MM-DD>-<slot>.html
- integration-root: ~/Code/PyAutoLabs-wt/integration-<YYYY-MM-DD>-<slot> — integration/<slot>; 3 clean, 1 conflicted
- integration-remote: PyAutoFit:integration/<slot>, PyAutoArray:integration/<slot>-2   # only after --push
- sweep-after: 2026-09-11        # when the branch sweep may delete those refs
- review: batches/reviews/<YYYY-MM-DD>-<slot>.md
- review-minutes-actual: <n>
- notes: |
    What actually happened. Anything that stalled, and why.
```

## The four fields that are easy to get wrong

**`delivered:` is not "green".** A cloud session's green status means the session
started and exited without an infrastructure error; it does **not** mean the task
succeeded. A member counts as delivered only with a PR that has a non-empty diff
and checks that actually ran. A member that ends green with no PR is reported as
**not delivered**, loudly, at the top of the packet.

**`heart-ack:` is the shift's grant, written verbatim.** `AUTONOMY.md` ("Leg 4
under a batch launch") scopes a YELLOW acknowledgement to one shift and to the
reason set named here. Recording it loosely is how a scoped grant becomes a
standing one, which doctrine voids.

**`outcomes:` is the accounting; the member line is the evidence.** The member
line's last column says what was *observed* ("PyAutoFit#1554, 4/4 checks
green"); `outcomes:` says what *became of it*, in one of four words. `batch
collect` fills it from the ledger and from nothing else — a `complete/` record
naming the member (its `- batch:` line cites the slot and the member slug, or
the record is filed under the member's own name) is `merged`; a review `decision:` that rejected it is
`rejected-at-review`; a row still in `active.md` is `carried`; anything else is
`unreviewed`. In that order, because a rejected member is still in `active.md`.
No `gh` call is made to fill it, and none should be: the organism's own files
are what a record is allowed to claim. This exists because all nine members of
the 2026-08-31-pm slot merged and every one of them is recorded
`decision: UNREVIEWED` — the completion records knew, and nothing read them.
The next `batch plan` reads the `carried` members first: they are already
costing the human review-minutes in the slot being planned.

**`merge-order:` is advice, and it is the only order the record can give.**
`members:` is the dispatch order and the packet sorts by health, so neither is a
merge sequence. This block is one: dispatch order, with library repos first (the
library-first gate) and same-repo members serialised, because the first `/prm`
moves `main` and stales its siblings' evidence. Nothing is filtered out of it —
a member with no PR is listed in its place with what it is waiting on. It is
never enacted: `/prm` is the human's, one PR at a time.

**`review-minutes-actual:` is the only calibration there is.** The planned figure
is a seed from the sizing faculty; this is what the slot really cost. Without it
the estimate never improves, and the whole batch size rests on it.

`lifecycle.py check` reads these records: a member whose prompt path resolves in
no state folder and has never been in the repo is **drift** (the record is wrong
about what it dispatched, and the member's question and witness cannot be read),
and a closed record with no `review-minutes-actual:` is a **warning**. Member
lines that are not the grammar — a hand submission, a science wave with a
sentence where the path goes — are left alone.

**`packet:` is the page the human actually reviewed, archived.** One
self-contained HTML file per slot under `batches/packets/` (see that folder's
`AGENTS.md`), written at dispatch with PENDING members and refreshed at
collect. It is the historical record of what the human was shown; a batch
whose packet was never archived cannot be audited against what they ruled on.

**`integration:` is opt-in, and it is local.** `yes` asks the collect to build
one throwaway worktree root for the slot merging every member's head branch per
repo, so the reviewer can run the whole batch together. It costs git time, not
tokens, and it is off by default because most slots do not need it. Nothing is
pushed, nothing is resolved: a member whose merge conflicts is left out of that
repo's branch and named with the conflicting paths — that report is the point,
not a failure. `collect --integration` turns it on for one run without editing
the record, and what happened comes back as `integration-root:`, a key of its
own so the `yes` you wrote here survives.

**`integration-remote:` is what was published; `sweep-after:` is when it
dies.** Neither appears unless someone typed `collect --integration --push` —
the record cannot ask for a push, only for the local preview. `integration-remote:`
lists one `<Repo>:<branch>` per repo that got a ref, under the repo name the
branch sweep matches on, and it is **rewritten on every push**: the current
publication is the truth, and a stale entry would send the sweep after a ref
that no longer exists. A `-N` suffix (`integration/<slot>-2`) means that
refresh was not a fast-forward of what was already on origin — nothing was
forced, the earlier ref is untouched, and the new state went out under a new
name. `sweep-after:` is `review-at:` plus a week, **written once and yours to
change**: `bin/branch_sweep.sh` protects an `integration/*` ref until that date
and may delete it on or after the following day, and with no date — or no
record naming the branch — it is protected outright. Edit the date, do not
delete the key: without it the ref lives forever, because a merge preview can
never be proven contained in `main`.

**`review:` is what the human said, verbatim.** The markdown their packet-page
submission produced (or the orchestrator transcribed), one file per slot under
`batches/reviews/`. The orchestrator parses it at close-out — merges, rulings,
queued follow-ups all trace back to a line in this file, not to a memory of a
conversation.

**`review-at:` is the shift, and it is the human's to declare.** There is no
schedule: a slot is whenever they come in, so at dispatch they state when they
expect to be back and **the shift is dispatch → `review-at:`**. The batch's
grant expires there (`AUTONOMY.md`, "What a batch launch is"), and a member not
dispatched inside it returns to the queue. `reviewed-at:` is the same number
measured rather than promised — the pair is what the human's own estimates are
calibrated against, exactly as `review-minutes-actual:` calibrates the cost. A
`review-at:` that passes with nobody there dispatches nothing; the grant just
expires.

**`expected-effects:` is the only licence for "generated by an earlier member".**
Leg 4 lets a new YELLOW reason pass as *generated by an earlier member of this
batch* — but only where it matches an `expected-effects:` line the **human**
wrote here at dispatch. A run classifying a new reason as its sibling's doing on
its own authority is an autonomous acknowledgement, which the hard invariants
forbid (`AUTONOMY.md`, "Leg 4 under a batch launch", 2026-08-31 amendment). No
line, no match, the run parks.

## Shift brief (2026-11-03)

A **shift brief** is a batch record with a `brief:` block. It is the same file in
the same folder, under the same ledger-merge rules; every key above keeps its
meaning, `heart-ack:` and `expected-effects:` included. What changes is who
picks the work: the human writes the brief, and **writing it with `review-at:` is
the dispatch** (`PyAutoBrain/AUTONOMY.md`, "Shift briefs and unattended
`glance`" — 2026-11-03). The grant covers the named tasks plus the brief's
backlog policy, until `review-at:`. The deterministic watcher that starts
sessions under it is the one exemption to `policy/end_at_deliverable.md`, and
only while a brief is open (`policy/shift_watcher.md`).

```markdown
# Batch 2026-11-04 am
- dispatched: 2026-11-04T08:30Z
- review-at: 2026-11-04T11:30Z      # stated by the human; the grant expires here
- shift: morning
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/<n>   # the digest is posted here once
- packet: yes                       # optional; the HTML packet is opt-in under a brief
- heart-ack:
  - <reason line>
- expected-effects:
  - <member>: <what it may legitimately change>
- brief:
  - goals:                          # in order; the first outranks the rest
    - 1. land the next cluster-strong-lensing slice
    - 2. clear review-ready glance PRs on PyAutoArray
  - tasks:                          # named prompt paths, done first, in this order
    - draft/feature/autolens/<name>.md
    - draft/bug/autoarray/<name>.md
  - backlog: scoped                 # none | fill-idle | scoped
  - scoped:                         # only with backlog: scoped
    - epics: cluster-strong-lensing, autonomous-orchestrators
    - tags: jax-gradient
    - tiers: notify, glance
  - exclude:
    - draft/feature/autofit/<name>.md
    - epics: euclid-dr1
  - review-minutes: 45
  - lanes: any local-dev ral         # any subset of: any local-dev ral gpu wsl-data
  - merge-cap: 3                     # unattended glance merges this shift, at most
  - token-budget: <n>                # tokens the shift may spend, all sessions
  - max-workers: 2                   # optional: concurrent workers (default 2)
  - max-sessions: 6                  # optional: sessions this shift, all told (default 6)
  - worker-mode: auto                # optional: auto (default) | dontAsk | acceptEdits — never bypassPermissions
  - sandbox: no                      # optional: yes marks a test shift
  - shadow: no                       # optional: yes plans and digests, spawns nothing
  - ral-allowance:                   # only when lanes includes ral; phase 5 consumes it
    - packets: 2
    - partition: ral
    - cpu-hours: 64
```

`backlog:` decides what happens once the named tasks are done or blocked:
`none` — nothing more; `fill-idle` — the planner's own ranking, under every
batch constraint; `scoped` — only prompts matching the `scoped:` epics, tags or
tiers. `exclude:` removes prompt paths or epics from either dip. Backlog the
brief does not cover is **never** dipped.

`shadow: yes` (phase 4a) makes the shift a **shadow shift**: the watcher plans
inside the brief exactly as a live shift would and records each proposal —
prompt, tier, pick reason — but takes no lease and starts no worker, up to
`max-sessions:` proposals. Its digest lists them as `proposed (shadow)`. The
pilot opens with two shadow shifts as its baseline. At `review-at:` every shift,
shadow or live, appends one row to `batches/pilot/pilot.md` (the pilot ledger;
its own header says which cells are the human's to fill at check-in).

**`merge-cap:` in practice (phase 4b).** A `glance` worker ends at PR-open; once
its CI is green the watcher starts one independent close-out session (same
model, fresh context — `PyAutoBrain/AUTONOMY.md` "Stage-2 adversary amendment —
2026-11-04") that runs the witness, checks the label and Heart, and merges or
refuses. Merges plus close-outs in flight never exceed `merge-cap:`; a PR past
the cap, with red CI, or refused by its close-out waits for the human's `/prm`
and the digest says why. Each unattended merge adds one row to
`autonomy_log.md` "Unattended `glance` sub-window (stage 2)".

`max-workers:` and `max-sessions:` are the watcher's usage caps (phase 3a,
`PyAutoBrain/agents/conductors/batch/_orchestrator.py`): at a cap it stops
spawning and records the refusal. Omitted, they default to 2 and 6; a value that
is not a whole number refuses the brief.

`worker-mode:` is the permission mode real workers run in (phase 3b). `auto` is
the default the human chose on 2026-11-03: a worker that still needs a person
shows `blocked` in `claude agents --json`, and after 15 minutes the watcher
parks it for the digest instead of leaving it waiting. `bypassPermissions` is
refused. `sandbox: yes` marks a test shift. (Until phase 3c it was the only
brief a real worker could run under; the one-Mind-writer path lifted that — the
workers' Mind changes now reach `main` only through the orchestrator.)

**Calibration rule.** A new brief is not accepted while the previous record
lacks `review-minutes-actual:`. The planned figure is a seed; the 2026-08-31
record never closed it, and an estimate nobody measures never improves.

`batches/examples/` (phase 2) holds validator fixtures. It is **not** a record:
nothing in it was dispatched, and `lifecycle.py` does not read it as one.

### Digest

Appended to the record at collect, under a `## Digest` heading, and **posted
once** as a comment on the shift's `issue:`. The record plus that comment is
the review surface; the HTML packet is written only when `packet: yes`.

```markdown
## Digest

### Brief work
- <slug> — PyAutoLens#<n> — HEALTHY — glance, auto-merged (1/3)
- <slug> — parked: awaiting-input (question on the issue)

### Backlog picks
- <slug> — PyAutoArray#<n> — HEALTHY — why: scoped epic cluster-strong-lensing, next phase, notify
- <slug> — draft filed — why: decomposed from goal 2; needs bulk approval

### Proof packets
<one proof packet per task, in the order above>

### Counters
- merges: 2
- glance-auto-merges: 1
- reverts: 0
- pushes: 0
- drafts-filed: 1
- packets-sent: 0
- workers-crashed: 0
- tokens: <n> of <token-budget>
- review-minutes-planned: 45
```

Brief work and backlog picks stay separate, and **every backlog pick carries a
one-line reason** — the brief's rule it was picked under. A pick the human
cannot trace to the brief is a finding.

**Where each part comes from (phase 3d).** The watcher writes the digest at the
first tick after `review-at:` (`PyAutoBrain/agents/conductors/batch/_digest.py`)
from what it recorded itself: the reason for each pick, stored at dispatch
(`named task` · `scoped epic|tag|tier <x>` · `backlog: fill-idle`); each
worker's `<task>.done` (one URL per line, `merged <url>` for a PR it merged
in-turn under its tier); each worker's `<task>.proof.md`, quoted verbatim — a
task that wrote none gets a stub saying so, never an invented packet; one
read-only `gh pr checks` per PR for its health; and its own counters.
`glance-auto-merges`, `reverts`, `pushes`, `drafts-filed` and `packets-sent`
stay 0 until phases 4–5 count them (human, 2026-11-04). The comment is posted
**once**: a local marker is created before the post, so a crash leaves no
comment rather than two, and a failed post is not retried.
`batch digest --record <file>` prints it early; `batch brief --check` refuses a
digest missing a section, a counter, a pick's `why:` or a started task's
packet.

### Proof packet

One screen per task — if it does not fit, the task was too big:

```markdown
#### <slug> — <PR url>
- claim: <one sentence — what is now true>
- before/after: <numbers, or a figure path>
- witness: `<the Witness: command>`
    <its output, trimmed to the lines that decide it>
- not checked: <what this packet does not show>
- revert: `<one command>`
```
