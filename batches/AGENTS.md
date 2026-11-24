# Batch records

One file per dispatched batch: `<YYYY-MM-DD>-<am|pm>.md`. Written at dispatch
(today that is the shift brief), with the digest appended after `review-at:`. This is the ledger of what was sent into one shift and
what came back — the same genre as `complete/`, and the evidence base the budget
and the review-minute estimate are calibrated from.

It auto-merges (`scripts/ledger_merge.py` — `batches/` is a ledger dir), because
an unattended system that cannot record its own history unattended will not
record it.

**Reviewed once.** A dev batch is dispatched as one shift and reviewed as one
sitting: one `- review:` line, one review file. The dashboard's batch status box
is the live view of the open slot — every member with what it is doing. Its
button to the review packet keys on `collected:`, which only the retired collect
step stamped, so a record written since does not show it; the digest comment on
the shift's `issue:` is the review surface now. A science batch is a
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
- integration: yes            # legacy: read only by the retired collect step
- review-minutes-planned: 42
- usage-window-at-dispatch: <5h %, weekly %, opus %>
- heart-ack:                  # the reason set acknowledged FOR THIS SHIFT
  - <reason line>
- expected-effects:           # human-written at dispatch, one line per member with reach
  - <member>: <what it may legitimately change, e.g. "merges into PyAutoArray and may stale release validation">
- members:
  - <slug>: <prompt path> — <tier> — <review-minutes> — <outcome>
- outcomes:                   # legacy: filled by the retired collect step, from the ledger only
  - <slug>: merged | rejected-at-review | carried | unreviewed
- merge-order:                # legacy: filled by the retired collect step — advice for /prm, not an action
  - 1. <slug> — library (PyAutoFit) — before its workspace dependants
- collected: 2026-09-04T08:30Z     # legacy
- reviewed-at: 2026-09-04T08:30Z   # when they actually sat down
- usage-window-at-collect: <5h %, weekly %, opus %>   # legacy
- delivered: <n>/<n>
- packet: batches/packets/<YYYY-MM-DD>-<slot>.html
- integration-root: ~/Code/PyAutoLabs-wt/integration-<YYYY-MM-DD>-<slot> — integration/<slot>; 3 clean, 1 conflicted   # legacy
- integration-remote: PyAutoFit:integration/<slot>, PyAutoArray:integration/<slot>-2   # legacy
- sweep-after: 2026-09-11        # when the branch sweep may delete those refs
- review: batches/reviews/<YYYY-MM-DD>-<slot>.md
- review-minutes-actual: <n>
- notes: |
    What actually happened. Anything that stalled, and why.
```

Fields marked `legacy` were written by `pyauto-brain batch collect`, the manual
step that scored a dispatched batch into a review packet. `batch collect` was
retired in PyAutoBrain#701: a shift is now a brief the watcher runs, and its
digest is the report. Nothing writes those fields any more. Older records keep
them, and the readers that still use them (`batch plan` on `outcomes:`, the
branch sweep on `sweep-after:`) read them from those records.

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
collect` filled it, until it was retired, from the ledger and from nothing else — a `complete/` record
naming the member (its `- batch:` line cites the slot and the member slug, or
the record is filed under the member's own name) is `merged`; a review `decision:` that rejected it is
`rejected-at-review`; a row still in `active.md` is `carried`; anything else is
`unreviewed`. In that order, because a rejected member is still in `active.md`.
No `gh` call was made to fill it, and none should be: the organism's own files
are what a record is allowed to claim. This exists because all nine members of
the 2026-08-31-pm slot merged and every one of them is recorded
`decision: UNREVIEWED` — the completion records knew, and nothing read them.
`batch plan` still reads the `carried` members of the previous record first: they are already
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
`AGENTS.md`). The retired collect step wrote it at dispatch with PENDING members
and refreshed it at collect; under a shift brief the page is opt-in
(`packet: yes`) and the watcher writes it as `digest.html` with the digest. It is the historical record of what the human was shown; a batch
whose packet was never archived cannot be audited against what they ruled on.

**`integration:`, `integration-root:` and `integration-remote:` are history.**
The retired collect step could build one throwaway worktree root per slot that
merged every member's head branch per repo (`integration: yes`, or
`collect --integration` for one run), and could publish those merges as
`integration/<slot>` refs (`--push`), listed under `integration-remote:`.
Nothing builds or pushes an integration preview now, so no new record carries
these keys.

**`sweep-after:` still governs the refs already published.** It is
`review-at:` plus a week, written once and yours to change:
`bin/branch_sweep.sh` protects an `integration/*` ref until that date and may
delete it on or after the following day, and with no date — or no record
naming the branch — it is protected outright. Edit the date, do not delete the
key: without it the ref lives forever, because a merge preview can never be
proven contained in `main`.

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
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/<n>   # required for a live brief; `brief --new` creates it
- live: LIVE · 1 running … — status: <comment url>   # written by the watcher only (PyAutoBrain#622)
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
  - lanes: any local-dev ral         # the default; any subset of: any local-dev ral gpu wsl-data
  - merge-cap: 3                     # unattended glance merges this shift, at most
  - token-budget: <n>                # tokens the shift may spend, all sessions
  - max-workers: 4                   # optional: concurrent workers (default 4)
  - max-sessions: 8                  # optional: sessions this shift, all told (default 8)
  - worker-backend: claude           # optional: claude (default) | codex
  - worker-mode: auto                # optional: auto (default) | dontAsk | acceptEdits — never bypassPermissions
  - sandbox: no                      # optional: yes marks a test shift
  - shadow: no                       # optional: yes plans and digests, spawns nothing
  - ral-allowance:                   # required when lanes includes ral; these are the defaults
    - packets: 2
    - partition: ral
    - cpu-hours: 64
```

**Goals come from [`goals.md`](../goals.md)** (PyAutoMind#565). `pyauto-brain
batch brief --new <slot> --review-at <ISO>` writes a skeleton brief whose
`goals:` are that file's goals in order, with `backlog: scoped` to the union of
their `epics:`/`tags:` (or `tiers: notify, glance` when no goal names any) plus
the epics whose ledgers `queue.md` names, and defaults for the rest: `merge-cap:
0`, and `lanes: any local-dev ral` with the `ral-allowance:` above (2 packets,
partition `ral`, 64 cpu-hours; PyAutoBrain#696), so a queued RAL phase can run.
Edit any of them per shift. It prints to stdout unless `--out`
names a file, so writing the record — the dispatch — stays the human's act.
`goals.md` is written by the human alone, so every goal is copied as written.
`--new` also prints, on stderr, how the goals changed since the newest brief.
`brief --check` warns when goal 1 of `goals.md` is missing from a brief.

**The launch (2026-11-17, PyAutoBrain#659).**

- **`issue:` is required for a live brief** (not `shadow: yes`): the status
  comment, the steering commands and the digest all go there. With `--out`,
  `brief --new` creates it on PyAutoMind (one `gh issue create`) and writes
  it; a file that already names one keeps it, and `--issue <url>` names one by
  hand. `brief --check` refuses a live brief without it, and refuses the
  launch while the CLI login has expired or expires before `review-at:` (run
  `claude /login`).
- **Only a pushed brief opens.** The watcher finds the brief itself on Mind
  `origin/main`: the one whose `dispatched:` has passed and whose
  `review-at:` has not. A brief written but not pushed grants nothing.
- **Never two open briefs.** If two pushed briefs overlap, the watcher ticks
  neither and says `two open briefs on origin/main`.
- **The watcher stops at `review-at:` + 45 min.** It posts the digest at
  `review-at:`, sweeps late arrivals for 45 minutes, then stops ticking the
  slot and renews no lease. A worker still out by then is in the digest.

**The keep-Heart-green lane** (PyAutoBrain#625). `brief --new` first reads
Heart's release verdict and sorts every reason into `fixable-dev`,
`local-checkout`, `release-scope` or `human-only`, and appends a `## Heart`
section after the brief's bullets: the reasons by class, what it filed or
picked, and what needs the human. For `fixable-dev` reasons it files at most
3 new bug drafts (deduplicated against `draft/`, `active/`, `queue.md` and its
own state, by a `<!-- heart-key: … -->` mark), with no `Unattended:` header,
so sizing decides. **It writes only with `--out` and an explicit `--mind`
that is not the shared canonical checkout**: use a temp worktree on
`origin/main`, then commit and push the drafts with the record from there. A
stdout preview, or the shared checkout, writes nothing and says so. With
`--green pick` (the human's opt-in) it names the drafts whose `Lane:` the
brief allows under `tasks:`, with a last `heart-green` goal. It never
releases, dispatches a workflow, forces or quarantines. Details: `PyAutoBrain/agents/conductors/batch/AGENTS.md`.

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
shadow or live, writes one machine-readable line to `batches/pilot/pilot.jsonl`
(one line per slot: mode, tokens by component, merged PR URLs with `mergedBy`
and merge actor, per-worker exits, stall minutes, `amended`), and
`batches/pilot/pilot.md` is rendered from it (the pilot ledger; its own header
says which cells are the human's to fill at check-in; in a shadow row they
measure the human's own review time and merges in the window, the baseline).
Both go through the one Mind writer as upsert ops, so a late arrival amends the
slot's line (`amended`) and never adds a second (PyAutoBrain#610). Tokens a shift
could not measure are written `null` (`unmeasured` in the render), never 0.

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
spawning and records the refusal. Omitted, they default to 4 and 8; a value that
is not a whole number refuses the brief.

`worker-mode:` is the permission mode real workers run in (phase 3b). `auto` is
the default the human chose on 2026-11-03: a worker that still needs a person
shows `blocked` in `claude agents --json`, and after 15 minutes the watcher
parks it for the digest instead of leaving it waiting. `bypassPermissions` is
refused. `sandbox: yes` marks a test shift. (Until phase 3c it was the only
brief a real worker could run under; the one-Mind-writer path lifted that — the
workers' Mind changes now reach `main` only through the orchestrator.)

`worker-backend:` selects execution only: `claude` remains the default for
existing briefs; `codex` uses the local Codex CLI on Linux/WSL. Codex briefs
must also declare `codex-model: <model-id>`; `codex-effort:` accepts `low`,
`medium` (default), `high` or `xhigh`. Use a model/effort supported by the
installed CLI/account. Codex accepts `worker-mode: auto` (automatic approval
review) or `dontAsk` (never ask); both retain workspace-write sandboxing.
`acceptEdits` has no Codex equivalent and is refused. No API billing fallback
or automatic hook trust is enabled.

Codex workers use the same task, proof and question contracts. Their local
supervisor supplies liveness; unavailable/corrupt state holds the lease rather
than declaring a crash. `/kill` targets that supervisor; the existing retry
and `/drop` rules remain unchanged. Codex's pre-ship review runs in a fresh
Opus CLI session through the accounted review helper, and close-outs remain
Opus. Thus **both CLI logins are required even with `merge-cap: 0`**. Reviews
are included in the worker's token accounting; live/incomplete usage retains
its reservation. Backend identity is stored per lease, so old sessions are
observed using their own backend. Preparation and the explicit no-op smoke
check are in PyAutoBrain `docs/codex_orchestrator.md`.

**Calibration rule.** A new brief is not accepted while the previous record
lacks `review-minutes-actual:`. The planned figure is a seed; the 2026-08-31
record never closed it, and an estimate nobody measures never improves.

`batches/examples/` (phase 2) holds validator fixtures. It is **not** a record:
nothing in it was dispatched, and `lifecycle.py` does not read it as one.

### Digest

Appended to the record by the watcher's first tick after `review-at:`, under
a `## Digest` heading, and **posted once** as a comment on the shift's
`issue:`. The record plus that comment is
the review surface; the HTML packet is written only when `packet: yes`.

```markdown
## Digest

### Review table
2 to /prm (3 PRs) · 1 to answer · 1 blocked or not started

| # | Task | Tier | Work | Note |
|---|---|---|---|---|
| | **Merge: your /prm** | | | |
| 1 | [<prompt title>](<Mind prompt>) | judge | [PyAutoGalaxy#<n>](<url>) | tier judge |
| 2 | [<prompt title>](<Mind prompt>) | glance | [PyAutoGalaxy#<m>](<url>) after PyAutoGalaxy#<n><br>[PyAutoLens#<k>](<url>) | merge-cap 0 reached this shift |
| | **Answer: question on the issue** | | | |
| 3 | [<prompt title>](<Mind prompt>) | judge | [PyAutoLens#<i>](<url>) | question on PyAutoLens#<i> |
| | **Blocked or not started** | | | |
| 4 | <slug> | — | — | autogalaxy held by <task> |

### Brief work
- [<prompt title>](<link to the prompt>) (`<slug>`; small · PyAutoLens) — PyAutoLens#<n> — HEALTHY — glance
- [<prompt title>](<link>) (`<slug>`; medium · PyAutoArray) — parked: awaiting-input (blocked on a person)

### Backlog picks
- [<prompt title>](<link>) (`<slug>`; small · PyAutoArray) — PyAutoArray#<n> — HEALTHY — notify — why: scoped epic cluster-strong-lensing · not in queue.md · ~3 review-min · priority normal · epic cluster-strong-lensing phase 8
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
- tokens: <measured> of <token-budget> (cache-read <n>; <k> session(s) unmeasured)
- review-minutes-planned: 45

### Workers
- <label> (<worker key>): spawned/finished
- <label> (<worker key>): spawned/parked — blocked 40 min — mentioned (parked)

### Refusals
- <task> — token-budget 100: 55 committed + 60 reserved per worker — 2× from <at>
```

**The review table comes first** (PyAutoBrain#718): every named task and
backlog pick in one table, numbered straight through so a reply can say "prm
1–4, 6", under a count line. Each task sits in exactly one group, its most
urgent, in this order; an empty group is left out:

1. **Merge: your /prm** — awaiting /prm, CI green, running, unknown or absent,
   a branch updated from main with CI not red, waits behind another PR, held on
   an unknown workspace sweep, or merged in-turn with no merge slot. The late
   sweep closes nothing out, so a PR still in CI at review time is yours.
2. **Answer: question on the issue** — parked on an issue, or blocked on a person.
3. **Fix: CI failed or crashed** — CI failed (also after a branch update),
   crashed, abandoned, killed.
4. **Blocked or not started** — not started (with the skip reason), dropped
   (unless a PR of it still needs merging or fixing), obsolete, finished with
   no PR or issue named.
5. **Still running** — a worker still out at review time, or a close-out
   checking or updating a PR.
6. **Done** — merged, already merged, verdict posted.
7. **Proposed (shadow)** — a shadow shift's proposals.

`Work` lists each PR or issue as `repo#n` in merge order, with "after repo#m"
where it waits. A carried-over task whose PRs you already merged is left out of
the table, as it is of the entries below. The entries below are unchanged.

Brief work and backlog picks stay separate, and **every backlog pick carries a
one-line reason**: the brief's rule it was picked under, then the planner's
ranking (queue.md position, or review-minutes and priority, then the path).
Picks are named by their prompt's title, linked, with the slug in backticks. A
shadow digest prints its counters as one line, since every one is 0. A pick the human
cannot trace to the brief is a finding.

**Where each part comes from (phase 3d).** The watcher writes the digest at the
first tick after `review-at:` (`PyAutoBrain/agents/conductors/batch/_digest.py`)
from what it recorded itself: the reason for each pick, stored at dispatch
(`named task` · `scoped epic|tag|tier <x>` · `backlog: fill-idle`); each
worker's `<task>.done` (one URL per line, `merged <url>` for a PR it merged
in-turn under its tier); each worker's `<task>.proof.md`, quoted verbatim — a
task that wrote none gets a stub saying so, never an invented packet; one
read-only `gh pr checks` per PR for its health; and its own counters.
`glance-auto-merges`, `reverts`, `drafts-filed` and `packets-sent` stay 0
until phases 4–5 count them (human, 2026-11-04); `pushes` counts the
@mentions below (PyAutoBrain#611). The comment is posted
**once**: a local marker is created before the post, so a crash leaves no
comment rather than two; a post that fails outright is retried on later ticks,
at most 3 attempts in all, and never after a timeout (a timeout may have
posted). Counters come from one exit record per worker and from GitHub's merged
state for each PR in the window, read at review-at after a final reap
(PyAutoBrain#610). A late arrival amends the record and the pilot line and posts
**one** correction comment. A worker that parks, or parks on its issue with a
question (awaiting input), gets **one** comment on the digest issue
@-mentioning the human (`mention_login`), derived from durable
state and retried like the digest; the watcher posts with
`PYAUTO_SHIFT_GH_TOKEN` (a bot account, PyAutoMind `issues: write` only) so the
mention notifies, and the digest warns when the poster is the mentioned account
(PyAutoBrain#611; AUTONOMY.md watcher network surface, amended 2026-11-12).
**While the shift runs (PyAutoBrain#622)** the watcher keeps **one status
comment** on the same issue: created once, then only edited (on a change of
state, or every 10 minutes), never @-mentioning anyone. It shows each task's
state, tokens against the budget, blocks, parks, refusals, time to `review-at:`
and the steering commands. The human steers by commenting, the comment's first
line one of `/pause`, `/resume`, `/drop <task>` or `/stop`; only their
`mention_login` counts. Each command is acknowledged once, in that status
comment. `/pause` holds spawns, re-dispatches and new close-outs until
`/resume`; reaps and mentions continue. `/stop` writes the watcher's `STOP`
file. `/drop` takes only a task of this shift; a dropped worker already
running is not killed, and a merge that lands after a drop is never counted
as unattended. The record's `- live:` line is the dashboard's
one-line copy, rewritten through the one Mind writer when the state changes;
nobody else writes it. Doctrine: AUTONOMY.md watcher network surface,
amendment 2026-11-13.
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
