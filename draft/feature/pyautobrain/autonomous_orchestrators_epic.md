# Autonomous orchestrators epic: a Dev and a Science orchestrator, a human review cadence

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoCortex
- PyAutoHeart
Themes:
- autonomy
- orchestration
Difficulty: large
Autonomy: human-required
Priority: high
Status: campaign map — phases route through /start_dev one at a time; this file is never issued itself
Epic: autonomous-orchestrators
Filed: 2026-11-03
Consequence: judge
Review-minutes: 25
Unattended: never
Lane: local-dev

## Why

With Opus 5.5 a token allocation does far more work. The `/batch` door (review-minute
budgets, `review-at:`, Consequence tiers, `Witness:`) was built for exactly this, but only one
batch record exists (`batches/2026-08-31-pm.md`). Instead the human drives 4–5 chats at once
and mostly approves steps Claude already knows how to take, hits `/prm`, or watches long
test runs. **The constraint is now the human's attention, not tokens.** The target metric is
**verified useful work per minute of human review**. Token spend is a ceiling, not a target.

Target experience: two human-facing conversations, a **Dev orchestrator** (the
PyAutoScientist ecosystem through Mind + Brain) and a **Science orchestrator** (Cortex +
Insight). Each spawns full worker sessions the human can open, read and redirect. The human
checks in every 2–3 hours, reads one digest, gives a few judgements and revises priorities.

## Why the batch door went unused (read the 2026-08-31-pm record), and what this design does about it

| What happened on 2026-08-31 | Design answer |
|---|---|
| The cloud wave was spawned bare (no repos, no skills) and all nine members died; ~13 min lost | Workers are spawned from a **session template** the orchestrator owns (phase 3), tested by a dry spawn whose first turn proves `pyauto-brain` and `gh` answer |
| Five members self-armed check-ins and drained usage overnight | Unchanged: sessions end at their deliverable; the only clock is a non-LLM watcher (phase 1 policy, phase 3 code) plus a usage-rate guard |
| The review was never submitted from the packet page; everything merged through `/prm` in chat and all nine rows read `decision: UNREVIEWED`; `review-minutes-actual` was never given | The **digest is text in the ledger and on a shift issue**, read where the human already reads; `/prm` close-outs are the review of record; the orchestrator asks for review-minutes-actual **once**, at the next brief, and refuses to open a new shift without the last one's number |
| Composition was human-pasted and the planner's proposal unused ("I'm very in the loop") | The brief is the human's composition act: named tasks first, then a backlog-dip policy the planner fills under; the planner never composes alone |
| Long-running laptop members were "carried" and blurred the collected-once model | Runs are not members: RAL work is a **packet** with its own lifecycle (phase 5) and science runs live on the Cortex board (phase 6); a dev member is only ever a PR or a draft |
| Dispatch needed a `review-at:`, a YELLOW ack with `expected-effects:` per member, and an HTML packet before anything started | The brief carries `review-at:` and the Heart ack in ten lines; the packet HTML becomes optional (`integration:`-style opt-in) |
| `Unattended: never` / `human-required` prompts (27 + 25 in today's backlog) and unwitnessed `judge` prompts (124 of 294 lack a `Witness:`) are rejected or priced at full cost | Goal decomposition files **drafts with proposed witnesses** for the human to approve in bulk; the verification campaigns (phase 7) convert whole classes of work to `notify`/`glance` |

## Human decisions (2026-11-03)

These are rulings. Later phases sharpen the wording; they do not reopen the decision.

- **Merging `glance` between check-ins is allowed**, extending "Merge authority follows
  Consequence" (AUTONOMY.md, 2026-10-02) from the shipping session's in-turn wait to a
  merge the watcher-started close-out performs after CI lands. Guards, all mandatory:
  - the `Witness:` is run by an **independent session** (not the author; a different model
    where one is available, as leg 5 already requires for the adversary);
  - merging **pauses on Heart RED, or on a YELLOW reason not matched by the brief's
    `expected-effects:`** (the existing leg-4 batch rule, applied per shift);
  - a **per-shift merge cap**, written in the brief;
  - the `glance` **Shadow window keeps appending rows**; a `reverted` row demotes the tier
    exactly as the 2026-10-02 section says;
  - **never `judge`-tier work, never a `decision-taken` PR, never a release.**
- **Push notifications only when absolutely necessary.** The test: *does waiting until
  `review-at` cause harm or waste the shift?* Qualifying classes: data loss or destructive
  risk; a breach of the RAL rules or runaway usage; the whole shift blocked on one human
  decision; a credential or security problem. Everything else goes in the digest.
  Budget ≈ 1 push per shift; a second push in a shift is itself a digest finding.
- **Lanes are routed by what a task needs, not its work type.** Ruled as a `Needs:` field;
  **implemented as values of the existing `Lane:` header** (see "Lane, not Needs" below —
  the planner, sizing faculty, intake and census already parse `Lane:`). Cloud sessions
  have no RAL, no laptop GPU and no `/mnt/c` (`policy/remote_sessions.md`). Dev tasks often
  need RAL test runs, so the **Science orchestrator is the single RAL gateway**: a dev
  worker hands it a **RAL test packet** (what to run, at which commit, the pass/fail rule)
  and parks as `awaiting-ral-witness` without holding a session open.
- **The human writes a shift brief.** It holds: primary goals in order; named tasks, done
  first; the backlog-dip policy (`none` / `fill-idle` / scoped to named epics, tags or
  tiers, plus exclusions); the review-minutes budget, `review-at:`, the allowed lanes and
  the merge cap. It **extends the `PyAutoMind/batches/` record schema** (one file per shift,
  same folder, same ledger-merge rules) and **the brief is the launch act**: writing it with
  `review-at:` is the human performing the dispatch that AUTONOMY.md "What a batch launch
  is" requires. The digest separates brief work from backlog picks and gives a one-line
  reason per pick.
- **Goals the orchestrator decomposes become DRAFTS only**, filed with proposed `Witness:`,
  `Consequence:` and `Lane:`, approved in bulk at check-in. Only already-formalised prompts
  run. Loosen this only after the Shadow window and the pilot's overrule rate say so.

## Lane, not Needs (decision taken in this review, 2026-11-03 — flagged as Q1)

`Lane:` already exists (`any` | `local-dev`; 41 backlog prompts carry it, 30 of them
`local-dev`), the batch planner rejects on it (`_lane_ok`), the sizing faculty parses it
(`LANE_VALUES`), and WORKFLOW.md fixes its meaning as "an intrinsic scheduling requirement".
A second routing field would have to agree with it on every prompt. So the ruling's
`Needs: ral | gpu | wsl-data | none` lands as:

```
Lane: any | local-dev | ral | gpu | wsl-data
```

`ral`, `gpu` and `wsl-data` each **imply `local-dev`** (they are refinements of it, never
alternatives), so every existing consumer keeps working: `_lane_ok` treats anything but `any`
as laptop-only; the new values add the RAL-gateway route (`ral` → packet to the Science
orchestrator), the GPU slot count (`gpu` → at most one at a time on the laptop) and the
`/mnt/c` guard (`wsl-data` → never a cloud session, outputs to a Linux scratch then copied).
`none` is spelled `any`. WORKFLOW.md's rule that `Lane:` never grows a product name
(`claude`, `codex`) is kept: these are resources, not products. (The spelling
`Lane: any | local-dev` appears only in two archived `complete/` records, never in the
backlog; the parser reads it as `any`, and phase 2 rejects it explicitly.)

## Design principles

- **Two rhythms.** AI execution is event-driven: CI finishes, a SLURM job completes, a
  dependency unblocks, a worker ends. The human review cadence (a 2–3 h digest, capped at
  the brief's review-minute budget) is separate and never drives execution.
- **A deterministic watcher with no LLM in it** polls `gh pr checks`, `squeue` (through the
  project's `hpc/sync jobs`, never raw) and Mind state, and starts a Claude session only when
  there is work to do. No tokens are spent watching. Claude sessions still never hold timers:
  the watcher is the one narrow exemption to `policy/end_at_deliverable.md`, written as a
  script that is not a session, and the hook keeps blocking every session as before.
- **One Mind writer per shift.** The shared Mind checkout has lost work to concurrent
  sessions repeatedly (reset --hard 09-30, `pull --rebase --autostash` conflict markers
  10-07, `prompt_sync_push` sweeping another session's files). Under a shift, **only the
  orchestrator commits to Mind**, from its own temporary worktree with cherry-pick; workers
  hand it ledger lines (their `active.md` claim, their close-out) as files in the lease
  directory, and never touch the canonical checkout. The dashboard self-heal bot is the only
  other mover of `main`, and the orchestrator rebases over it.
- **Spend spare tokens on cheaper review, not on more PRs:** independent witnesses; an
  adversarial second session; a one-screen **proof packet** per task (before/after numbers
  or a figure, the witness command and its output, what was *not* checked); bigger tasks,
  fewer PRs.
- **Background campaigns are bounded:** a hypothesis, a token budget, a stop condition and a
  measurable outcome. No refactoring to fill tokens.
- **The Science orchestrator is conservative.** It may produce diagnostics, compare seeds,
  and flag parameters at their bounds. It never gives a scientific verdict: Cortex records
  observed facts and the human's conclusions. It launches nothing the brief did not allow.
- **No new organ.** The orchestrator is the Brain's **batch conductor grown up** (`batch
  brief` / `dispatch` / `digest` verbs plus the watcher script), not a new conductor; Mind
  stays the task queue, Cortex the run record, Insight the campaign intent, Heart the gate.
- **A blocked decision sets that line of work aside** (decide-and-flag, or park with a
  question in the digest) and the orchestrator moves on. It never stalls the shift.
- **Every phase ships a machine-checkable `Witness:`** so its own review is minutes.

## External facts (verified 2026-11-03 against code.claude.com docs; recheck at phase 3)

- **Projects** (claude.ai/code and the desktop Code tab, under More): public beta on Pro,
  Max and Ultra, rolling out gradually; not on Team/Enterprise. Threads are cloud sessions by
  default, each on its own branch, sharing repos, instructions and memory; a thread can run
  **on this machine through Remote Control** (Claude Code ≥ 2.1.280, machine awake). Whether
  this account has it is a UI check, not a plan check.
- **Cloud scheduled tasks** (formerly routines): minimum interval **1 hour**; triggers are
  cron, an HTTP POST, and GitHub **pull request / release / issue** events only — no
  `check_run`, `check_suite` or `workflow_run`. Runs are fresh clones with no local files, no
  RAL and no `/mnt/c`. So the cloud lane cannot react to CI finishing on its own; a
  GitHub Action that labels a PR on green would be the only event bridge.
- **Desktop scheduled tasks** run only while the app is open and the machine is awake (one
  catch-up run after a sleep). `/loop` and CronCreate run only while that session is open.
  Nothing local survives a reboot.
- **Script-started sessions:** `claude --bg` starts a background session that survives
  sleep (not reboot) and is steerable with `claude attach <id>`; `claude -p` sessions are
  hidden from the picker but resumable by `--resume <id>` (a `--session-id` can be chosen
  up front). Whether either appears in the desktop app's session list is **not documented**
  and is phase 4's first witness.

Consequence for the launch mechanism: the watcher is **local** (a WSL systemd user timer or
cron, independent of the desktop app), workers are `claude --bg` sessions in per-task
worktrees, and the laptop stays awake for the shift (it must anyway for RAL SSH and `/mnt/c`).
A cloud scheduled task is at most an hourly fallback collector and is not in scope before
the pilot.

## Phases (each its own prompt via /start_dev, in order unless noted)

Phase numbers are integers (the dashboard's `Phase:` parser is `int()`); the original phase 1
split into 1 and 2 on size, so later phases moved up by one.

1. **Policy and formats (prose only).** Amend `end_at_deliverable.md` (watcher exemption),
   `AUTONOMY.md` (shift brief = launch; unattended `glance` guards; drafts-only decomposition;
   the push test; one-Mind-writer rule), `batch.md` + batch `AGENTS.md` (backlog dip under the
   brief), `batches/AGENTS.md` (brief and digest schemas, proof packet, `Lane:` doc in
   REFERENCE.md). *Witness:* hook still blocks timers (sample payloads exit 2); every new
   section carries a dated heading and a revert condition; `lifecycle.py check`,
   `repos_sync.py --check` and the Brain tests stay green. *Consequence:* judge. *Lane:* any.
2. **Lane values, brief schema and census (code).** `LANE_VALUES` grows `ral | gpu |
   wsl-data`; `_lane_ok` keeps them laptop-only; intake proposes a lane from the text and
   passes declared headers through; census counts lanes; `batch brief --check` validates a
   brief file against the schema. *Witness:* unit tests for each rule, a sample brief
   accepted and one lacking `review-at:` refused, a `Lane: any | local-dev` rejected.
   *Consequence:* glance. *Lane:* any.
3. **Orchestrator runtime: watcher, dispatch safety, digest.** The non-LLM watcher
   (systemd user timer), the session template, leases and claims, no duplicate dispatch,
   crash recovery, the kill switch, the usage-rate guard, the one-Mind-writer path, `batch
   dispatch` and `batch digest`, and the digest's delivery to the shift issue. *Witness:* a
   dry shift with fake workers (`PYAUTO_ORCHESTRATOR_FAKE=1`): two watcher ticks overlapping
   dispatch exactly one worker per lease; a killed worker's lease expires and is re-dispatched
   once; the kill-switch file stops the next tick; the usage cap refuses the N+1th spawn; the
   digest file validates and the issue comment is posted on a sandbox issue. *Consequence:*
   judge. *Lane:* local-dev.
4. **Dev orchestrator pilot.** Two shadow shifts first (the orchestrator proposes and
   digests, the human works as today, minutes are logged) to set the baseline; then 2–3
   workers, 2 h shifts, `glance` merges under the guards, only `notify`/`glance` work plus
   invariance or refactor tasks. Check Projects in the UI; if present, trial it for the
   cloud lane only, with Mind and auto-memory kept as the sources of truth. *Witness:* a
   `batches/pilot.md` table with one row per shift (planned vs actual review-minutes,
   merges, reverts, overrules, pushes, drafts filed, tokens) for ≥ 6 shifts, the baseline
   rows included; `claude --bg` workers confirmed attachable (and whether they show in the
   desktop app, recorded either way). *Consequence:* judge. *Lane:* local-dev.
5. **RAL handoff.** The RAL test packet format (commit, script, partition, resources, the
   pass/fail rule, the dev task it witnesses); the Science orchestrator submitting under
   `policy/hpc_ral.md` and AUTONOMY.md "Scheduler actions" **only against a packet
   allowance the brief names** (count, partition, CPU-hours; never bulk CPU on `gpu`; never
   `HPCPullPyAuto` on the shared mirror; private checkouts for A/B runs); the result
   returning as the dev task's `Witness:` and un-parking it. *Witness:* a packet submitted
   with `hpc/sync act submit --dry-run` leaves one `actions.log` line; a finished packet
   flips the dev row from `awaiting-ral-witness` to its ship step; an over-allowance packet
   is refused and digested. *Consequence:* judge. *Lane:* ral.
6. **Science orchestrator.** Bounded campaigns with explicit protocols, collect-on-completion
   via the watcher plus `cortex checkin`, automatic diagnostics (seed comparison,
   bound-hitting parameters, convergence flags), and human scientific checkpoints. Start with
   an analysis whose correctness can be checked independently. *Witness:* one campaign from
   brief to `awaiting-ruling` with zero human messages between; the ledger carries only
   `run` and `note` lines written by the machine and `result` lines written by the human.
   *Consequence:* judge. *Lane:* ral.
7. **Verification campaigns** (alongside phases 4–6), each with a hypothesis, budget and
   stop condition: golden-number invariance gates (so refactors become `notify`),
   numpy/JAX/numba parity, finite-difference vs autodiff gradients, simulate → fit →
   recover, metamorphic tests (equivalent lens descriptions, symmetries). *Witness:* each
   campaign lands as a CI leg or a `pyauto-brain` check with a stop condition in its prompt,
   and the sizing faculty regrades the affected backlog prompts to a cheaper tier.
   *Consequence:* glance per campaign. *Lane:* any.

## Cross-cutting requirements (owned by the phases named)

- **Crash recovery and duplicate dispatch (phase 3).** A lease is a file in the watcher's
  state directory (`~/Code/PyAutoLabs-wt/.orchestrator/<slot>/leases/<task>.json`: task,
  worktree, session id, started, heartbeat, expires). A tick dispatches only against a
  free task with no live lease; a worker with a stale heartbeat past its expiry is declared
  dead once, its worktree inspected, and the task re-dispatched **at most once per shift**
  with the crash noted in the digest. The repo/worktree claim guard (`worktree_check_conflict`)
  still runs inside the worker; the lease is the orchestrator-side mirror of it.
- **Usage-rate guard (phase 3).** No usage API exists locally, so the guard is counted:
  a cap on concurrent workers, a cap on sessions per shift, and a token budget in the brief
  consumed from each session's final usage report (`claude -p --output-format json`
  carries it; `--bg` sessions write theirs at exit). At the cap the watcher stops spawning
  and the digest says why. The kill switch is a file (`STOP` in the slot directory) and the
  watcher's first check.
- **Mind write contention (phases 1 and 3).** See "One Mind writer per shift".
- **How the digest reaches the human (phases 1 and 3).** The digest is written to the
  shift's `batches/<slot>.md` (ledger, auto-merged) and posted **once** as a comment on a
  per-shift GitHub issue in PyAutoMind; the orchestrator chat shows the same text when
  opened. A push notification is the one tool call reserved for the push test. The HTML
  packet is opt-in.
- **What the pilot measures (phase 4).** Per shift: `review-minutes-planned` vs `-actual`,
  verified merges, `glance` auto-merges, reverts, human overrules of orchestrator picks,
  pushes sent, drafts filed and approved, tokens, workers crashed. The target metric is
  verified merges (plus accepted drafts and packets) per `review-minutes-actual`; the
  baseline is the two shadow shifts.

## Success measures (pilot)

Fewer routine interruptions. Zero critical decisions taken without the human. More
independent evidence per task. Planned review minutes within 25 % of actual by the sixth
shift. Corrective-PR and revert rates no worse than the current calibration log. Verified
work per human review-minute above the shadow-shift baseline.

## Open decisions for the human (from the 2026-11-03 review)

1. `Needs:` → `Lane:` values (recommended yes; see "Lane, not Needs").
2. Phase 1 split into prose (1) and code (2), later phases renumbered (recommended yes).
3. Digest delivery via a per-shift PyAutoMind issue comment plus the ledger (recommended).
4. The shift brief's RAL packet allowance counts as "the human asked for that run" under
   AUTONOMY.md "Scheduler actions" (recommended yes, bounded; lands in phase 5).
5. Launch mechanism: local watcher + `claude --bg` workers; Projects only for the cloud lane
   after a UI check (recommended).
6. Shadow shifts first in the pilot (recommended, two shifts).

<!-- formalised by the Intake (Conception) Agent on 2026-11-03 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b15ff817-f0d9-4ab3-b23f-735fcbb990f5/scratchpad/autonomous_orchestrators_epic.md; reviewed and restructured 2026-11-03 (design review session) -->

## Programme: from the review to autonomous runs (adopted 2026-11-12)

Adopted by the human on 2026-11-12 (kickoff session) from the roadmap written after the ecosystem
review of 2026-11-10: `Science/scratch/ecosystem_review_2026-11/PROGRAMME.md` (now history; this
section is the source of truth) and the report, private Artifact
https://claude.ai/artifact/4A94P1cevvkESoM22QoMWm. Each session starts from the programme prompt in
PROGRAMME.md, reads the state table below and carries on from the first unfinished row.

**End state.** Scheduled cloud shifts that pick work from a ranked, premise-checked backlog,
dispatch 5–20 workers, and verify and merge `notify`/`glance` work unattended under gates GitHub
enforces; the human reads one digest per shift and rules only on judge-tier items.

**Numbering.** Milestones M1–M6 are epic phases 8–13 (the dashboard's `Phase:` parser is `int()`);
a task's prompt carries its milestone's phase number and names its task id (e.g. M1.1) in its
first line.

**Changes made at adoption (human-approved 2026-11-12):**
1. **Phase 4c folds into M3.** No further live shifts run on the watcher before M1 closes its
   confirmed state-machine gaps. 4c's existing rows (2 shadow, 2 live) stay as the baseline; its
   remaining live shifts are M3.1/M3.2; 4c closes at the M3 exit with its write-up.
2. **Phases 5–7 are parked behind M3**, unchanged. Phase 7 campaigns (glance per campaign) are
   candidate M3.2 shift workload.
3. **M1.3's draft is `Consequence: judge`.** Slices 1–2 are re-graded when sliced; if they stay
   judge, the merge is the human's.
4. **M1.4 runs before M1.3**, so every later merge records its actor.

**Human gates.** M1: none (all glance). M2: five rulings in one sitting (decision sheets prepared
during M1). M3: the unattended `glance` grant (after ten stage-2 rows). M4: the worker definition.
M5: the design, then each step up in workers. M6: each widening of a grant. Always the human's:
off-schedule release approval, manual release version, forcing YELLOW / accepting a named RED, the
kill switch, quarantine doctrine, judge-tier merges, the timing of any live shift.

**Exit tests.**
- **M1:** every task merged with its witness (command + observed result); the batch conductor's
  suite passes; one shadow shift whose digest and ledger row agree with GitHub and with what the
  workers did.
- **M2:** each ruling recorded in doctrine with its date; the builds merged; for M2.1 the 228 logged
  ships replayed through the new scope, with the share still needing an override.
- **M3:** ten stage-2 rows in `autonomy_log.md`; every path in M3.1 exercised at least once with
  evidence; in every shift the merge count equals GitHub's and every PR is recorded. Then the
  human rules on the unattended `glance` grant.
- **M4:** a cloud session holding only the declared bundle takes a glance task from start to an
  open PR, fixed load measured; Mind `main` receives no generated-file commits and its drift check
  is green.
- **M5:** at the target worker count, a run of consecutive shifts (count: human) reviewed by digest
  alone, no failure needing hand recovery.
- **M6:** scheduled cloud shifts; digest and shift numbers on the Brain board; the nightly kept
  green by a shift; grants widened only on evidence; the laptop watcher retired.

"Re-check first" = the review did not verify the finding: the task starts by re-checking it at
source and is dropped or reshaped if it does not hold. Side-lane rows are off the critical path.

### Programme state table

| milestone | task | state | evidence |
|---|---|---|---|
| M1 (ph 8) | M1.1 Close the four watcher state-machine gaps — record `complete/2026/11/shift-watcher-state-gaps.md` (CODE-1, CODE-2, ORCH-1, ORCH-3; confirmed) | **merged 2026-11-12** (PyAutoBrain#604, eecd2d505; Heart RED dev override by human) | `python -m pytest tests/test_orchestrator_*.py tests/test_batch_watch.py -q` → 134 passed, 1 skipped; 4 witness tests pass, all new tests fail on base; independent review CLEAN after fix 1898e11; CI pytest 3.12/3.13 green. Follow-ups: `draft/bug/pyautobrain/shift_watcher_followups_after_state_gaps.md` |
| M1 (ph 8) | M1.2 `prompt_sync_push` commits only the paths it is given — record `complete/2026/11/prompt-sync-explicit-paths.md` (FB-1, MIND-1; confirmed) | **merged 2026-11-12** (PyAutoMind#555 7ae138d5f + PyAutoBrain#605 3dfe3707d; Heart RED dev override by human) | `grep -n "add -A" scripts/prompt_sync.sh` → nothing; prompt_sync tests 21 passed (9 fail on old script); Mind suite 750 passed; independent review CLEAN after fix; close-out committed via the new helper with close's printed line. Follow-ups: `draft/maintenance/pyautomind/prompt_sync_explicit_paths_followups.md` |
| M1 (ph 8) | M1.4 Merge-actor column + random-sample audit — record `complete/2026/11/merge-actor-audit.md` (FLOW-2; confirmed) | **merged 2026-11-12** (PyAutoMind#558 dbc9affaf + PyAutoBrain#607 68e263a1f; human authorized the doctrine edit live; Heart RED dev override by human) | `lifecycle.py close … --actor in-turn-human-commanded` wrote the close row `in-turn-human-commanded (mergedBy Jammy2211)`; `lifecycle.py shadow-recount` → 69 ruling rows: human /prm 31, automatic/in-turn 10, not stated 28; `audit-sample --seed 20261112` → 19 of 93, same twice; Mind suite 772, Brain closeout 21; review CLEAN after fix. **Judge question for the human:** re-mark historical rows (38 counted would remain vs target 20) |
| M1 (ph 8) | M1.3 Premise check before dispatch + Lane backfill, slices 1–2 — record `complete/2026/11/premise-lane-checks.md` (MIND-2, MIND-3; confirmed) | **merged 2026-11-12** (PyAutoMind#559 + PyAutoBrain#609; block-gate RED override by human); backfill applied (e25156929) | `pyauto-brain batch premise --at 2026-11-06T11:20Z` → both 11-06 drafts `obsolete` with evidence; `lane_backfill.py` → 0 pool drafts without Lane after apply (119 written: 109 any/8 ral/2 wsl-data); Brain 1718, Mind 772; review CLEAN after fix. Follow-ups `draft/feature/pyautobrain/premise_check_followups.md` |
| M1 (ph 8) | M1.5 Shift numbers right and kept (tokens for live/parked/close-out; counters from worker exits; one row per shift) — CODE-4, ORCH-7, ORCH-8, FLOW-6, SIG-5; re-checked 2026-11-12 on Brain 68e263a: CODE-4/ORCH-7/ORCH-8 partly, FLOW-6/SIG-5 hold → draft `draft/bug/pyautobrain/shift_numbers_tokens_counters_row.md` | drafted; queued behind M1.3 (same repo) | |
| M1 (ph 8) | M1.6 A blocked worker reaches the human off the laptop — ORCH-13; re-check first; no draft; **channel ruled 2026-11-12: GitHub @mention on the shift digest issue** | not started | |
| M1 (ph 8) | side: nightly outcome record + same-night bug tasks — `draft/feature/pyautobrain/nightly_outcome_record_and_same_night_bug_tasks.md` (NIGHT-1, NIGHT-2) | not started | |
| M1 (ph 8) | side: unit-test trends + hygiene ledger on boards — record `complete/2026/11/dev-metrics-boards.md` (SIG-2, SIG-3 re-checked: both hold) | **SIG-2 merged 2026-11-12** (PyAutoHeart#339); SIG-3 split to `draft/feature/pyautobrain/brain_board_hygiene_ledger.md` | local cloud-style render: 12/12 suite cards 2 charts, 12/12 import cards 1 chart, total 9,777; Heart 1334; review CLEAN; live board to confirm after next daily run |
| M1 (ph 8) | prep: M2 decision sheets (M2.1–M2.5) | not started | |
| M1 (ph 8) | exit test (see above) | not started | |
| M2 (ph 9) | M2.1 Heart branch-scoped dev verdict + feed age / event triggers — `draft/feature/pyautoheart/dev_ship_reason_scope_and_feed_age.md` (REL-1, DASH-3); feed-age slice is glance, may build early | not started | |
| M2 (ph 9) | M2.2 Server-side merge gate + `gh pr merge --auto` — `draft/maintenance/ci/server_side_merge_gate.md` (PR-3); needs the human's admin credential | not started | |
| M2 (ph 9) | M2.3 Absent Lane fails closed; importance signal replaces `queue.md` — premise/lane draft slice 3 (MIND-3; MIND-4 re-check first) | not started | |
| M2 (ph 9) | M2.4 Release builds the rehearsed commits — `draft/feature/pyautohands/release_builds_rehearsed_shas.md` (REL-4) | not started | |
| M2 (ph 9) | M2.5 Where the always-apply rules live on the laptop (TOK-3) — human's home folder | not started | |
| M2 (ph 9) | side: script-level retry + expiring quarantine in Stage 3; shift-owned nightly lane (REL-2 plausible, REL-3 re-check first) | not started | |
| M2 (ph 9) | gate: five rulings + exit test | not started | |
| M3 (ph 10) | M3.1 One designed live shift ≥ 3 h exercising every unexercised path (absorbs 4c live shifts) | not started | |
| M3 (ph 10) | M3.2 Further shifts to ten stage-2 rows (stage-2 table: 0 rows on 2026-11-12) | not started | |
| M3 (ph 10) | M3.3 A fixed sheet per shift | not started | |
| M3 (ph 10) | gate: unattended `glance` grant; close 4c (PyAutoBrain#574) with write-up | not started | |
| M4 (ph 11) | M4.1 Cloud rehearsal (library, workspace, organ task + two `mobile_shift_operation.md` prompts) — BRAIN-4, ORCH-4; re-check first | not started | |
| M4 (ph 11) | M4.2 Cloud worker bundle, `doctor`, slim profile, travelling rules — `draft/feature/pyautobrain/cloud_worker_bundle_and_profile.md` (BRAIN-1, TOK-2, TOK-3) | not started | |
| M4 (ph 11) | M4.3 One network write path to Mind `main` (MIND-1; PR-1, PR-2 re-check first) | not started | |
| M4 (ph 11) | M4.4 Boards and indexes rendered in CI, not committed (PR-6; DASH-1, MIND-5, KNOW-2 re-check first) | not started | |
| M4 (ph 11) | M4.5 Lessons move from laptop memory into the repos (KNOW-1, FB-3; re-check first) | not started | |
| M4 (ph 11) | M4.6 Cross-repo effects in the gate: one CI-verdict script, dependants' tests after a library merge (FB-4, FB-5, REL-6, FLOW-3; re-check first) | not started | |
| M4 (ph 11) | M4.7 Machine-readable completion record (FLOW-4, FLOW-5; re-check first) | not started | |
| M4 (ph 11) | gate: worker definition + exit test | not started | |
| M5 (ph 12) | M5.1 Cloud watcher design vs the report's thirteen constraints — from `draft/feature/pyautobrain/shift_watcher_in_the_cloud.md` | not started | |
| M5 (ph 12) | M5.2 Build behind the tick's existing interfaces, state-store seam (CODE-3, CODE-6, ORCH-6; re-check first) | not started | |
| M5 (ph 12) | M5.3 Cloud shadow shifts → live 2–3 workers, merge cap 1 → 5 → 10 → 20 | not started | |
| M6 (ph 13) | Scheduled cloud shifts; laptop watcher retired | not started | |

## Progress

- 2026-11-03 — **phase 1 COMPLETE** (PyAutoMind#522, PyAutoBrain#552; record
  `complete/2026/11/autonomous-orchestrators-p1.md`). `policy/end_at_deliverable.md` left
  byte-identical; the watcher exemption is `policy/shift_watcher.md`, and its one-line pointer
  rides with the next stanza refresh. Next: phase 2.
- 2026-11-03 — **phase 2 COMPLETE** (PyAutoMind#523, PyAutoBrain#554; glance auto-merge; record
  `complete/2026/11/autonomous-orchestrators-p2.md`). `Lane: ral|gpu|wsl-data`, `batch brief --check`,
  `batch plan --brief`, intake header pass-through + lane inference, census lane histogram. The
  merge-cap rule is refined: refused only when every named task is `judge` **and** `backlog: none`.
  Next: phase 3 — prompt filed 2026-11-03 and sliced 3a (watcher core) → 3b (dispatch) → 3c (Mind writer) → 3d (digest), chained by Blocked-by; next 3a.
- 2026-11-03 — **phase 3a COMPLETE** (PyAutoMind#524, PyAutoBrain#556; record
  `complete/2026/11/autonomous-orchestrators-p3a.md`): STOP-first watcher tick, exclusive-create
  leases, crash re-dispatch once per shift, usage caps, fake workers; AUTONOMY "The watcher's network
  surface — 2026-11-03". The timer is not installed (human act). Next: 3b, unblocked.
- 2026-11-03 — **Shadow-window ruling (human):** grant `glance` narrowed after a spot audit
  (recorded `complete/2026/11/glance-tier-ruling.md`); **unattended `glance` merges
  get a separate stage-2 sub-window** (first 10 need the independent different-model adversary
  leg). Phase 4 must not auto-merge unattended before that sub-window exists.
- 2026-11-03 — **phase 3b COMPLETE** (PyAutoMind#525, PyAutoBrain#558; record
  `complete/2026/11/autonomous-orchestrators-p3b.md`): real `claude --bg` workers from one session
  template, `claude agents --json` liveness, blocked → parked after 15 min, transcript token budget;
  worker mode `auto` (human). Real dispatch is `sandbox: yes` only until 3c. CLI facts (2.1.316):
  `--bg` ignores `--session-id`, state word `working`, untrusted folders refused fast. Next: 3c.
- 2026-11-04 — **phase 3c COMPLETE** (PyAutoMind#526, PyAutoBrain#560; human /prm; record
  `complete/2026/11/autonomous-orchestrators-p3c.md`): one Mind writer — worker ledger ops in
  `<slot>/ledger/`, committed by the orchestrator from a temporary worktree on `origin/main`, worker
  pre-commit hook refuses direct Mind commits; the 3b sandbox fence is lifted. Next: 3d (digest), unblocked.
- 2026-11-04 — **Shadow-window ruling RECORDED** (PyAutoMind#529, PyAutoBrain#567; record
  `complete/2026/11/glance-tier-ruling.md`): audit 8/8 `ok`; `glance` granted, narrowed (non-PASS witness →
  human `/prm`); stage-2 sub-window table open in `autonomy_log.md`. Phase 4 unattended merges still
  need the shadow-row verb to write into that table.
- 2026-11-04 — **phase 3d COMPLETE — phase 3 COMPLETE** (PyAutoMind#531, PyAutoBrain#569; record
  `complete/2026/11/autonomous-orchestrators-p3d.md`): the shift digest, written into the record
  through the one Mind writer and posted once (marker before the post). Next: phase 4 Dev pilot —
  prompt not yet filed; it must route unattended merges into the stage-2 sub-window table.
- 2026-11-04 — **phase 4 SLICED** 4a (shadow shifts + `batches/pilot.md`) → 4b (unattended `glance`
  close-out + stage-2 Shadow rows) → 4c (the pilot run, ≥ 6 shifts), chained by Blocked-by; prompts
  `draft/feature/pyautobrain/autonomous_orchestrators_p4{a_shadow_shifts,b_unattended_closeout,c_pilot_run}.md`
  (agent proposal, human approved filing). Next: 4a.
- 2026-11-04 — **phase 4a COMPLETE** (PyAutoMind#532, PyAutoBrain#571; record
  `complete/2026/11/autonomous-orchestrators-p4a.md`): `shadow: yes` shifts propose without spawning;
  `batches/pilot/pilot.md` gains one row per shift. Next: 4b, unblocked.
- 2026-11-04 — **phase 4b COMPLETE** (PyAutoMind#533, PyAutoBrain#573; record
  `complete/2026/11/autonomous-orchestrators-p4b.md`): unattended `glance` close-out by one independent
  Opus close-out session; stage-2 rows via `table-append`; AUTONOMY "Stage-2 adversary amendment —
  2026-11-04" (same model allowed). Next: 4c, the pilot run.
- 2026-11-12 — **Programme ADOPTED** (human approval, kickoff session): the review-to-autonomy
  roadmap is filed above as phases 8–13 (M1–M6) with a state table; 4c folds into M3; phases 5–7
  parked behind M3. Next: M1.1 (watcher state-machine gaps).
- 2026-11-12 — **M1.1 MERGED** (PyAutoBrain#604; record `complete/2026/11/shift-watcher-state-gaps.md`). Next: M1.2 (`prompt_sync_push` explicit paths).
- 2026-11-12 — **M1.2 MERGED** (PyAutoMind#555, PyAutoBrain#605; record `complete/2026/11/prompt-sync-explicit-paths.md`). Next: M1.4 (merge-actor column + random audit).
- 2026-11-12 — **M1 side fix MERGED: prompt_sync detached-HEAD push** (PyAutoMind#557; record `complete/2026/11/prompt-sync-detached-push.md`): the temp-worktree Mind-write route now pushes via `PROMPT_SYNC_PUSH_TO=main`, publishing only the helper's own commit. Next: M1.4.
- 2026-11-12 — **M1.4 MERGED** (PyAutoMind#558, PyAutoBrain#607; record `complete/2026/11/merge-actor-audit.md`); AUTONOMY "Merge actor and random audit — 2026-11-12". Next: M1.3 (premise check + Lane backfill, slices 1–2).
- 2026-11-12 — **Block gate (human): M1.3 slices 1–2 + Heart side lane MERGED** (PyAutoMind#559, PyAutoBrain#609, PyAutoHeart#339); Lane backfill applied; 30 historical glance rows re-marked `human-/prm` (count 63; `fixed-model-json` stays counted). **M1.6 channel ruled: GitHub @mention on the shift digest issue.** Next: M1.5, then M1.6 (both PyAutoBrain batch).
