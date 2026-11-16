# Deep review: the orchestrator so far, and the whole PyAutoScientist ecosystem, ahead of fully autonomous dev runs

Type: research
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoHeart
- PyAutoHands
- PyAutoMemory
- PyAutoCortex
- PyAutoPulse
- PyAutoInsight
- PyAutoEyes
- PyAutoEars
- PyAutoBroca
- PyAutoGut
- PyAutoDNA
- PyAutoNerves
- PyAutoScientist
Difficulty: large
Autonomy: human-required
Priority: high
Status: draft
Filed: 2026-11-09
Epic: autonomous-orchestrators
Consequence: judge
Witness: a review report the human can read in one sitting (findings ranked by impact on autonomous runs, each with its evidence: file:line, record, run, PR or number) plus a short list of filed draft prompts; nothing built, merged or ruled
Review-minutes: 60
Unattended: never
Lane: local-dev

Model: Fable, extra-high effort. Run on the laptop (the organs are in `~/Code/PyAutoLabs/organs/`).

## Request (human, 2026-11-09, verbatim)

"give me a prompt which we will use fable extra toreview the work done so far on the orchestator, but also do a full review of the PyAutoScientist ecossytem with all organs to review previous work flows and assess how we can continue to improve it in general, as we move to these orchestrator fully autonomous development runs. I am happy with the work weve done so far, but I think using a lot of tokens (which we are behind on spending this week) to review the ecosystem in more detail and work out improvements is a good idea to inform the design going forward."

**The human has opted into a large token spend and multi-agent orchestration for this review** ("use a workflow", the Workflow tool's opt-in): fan out reviewer agents per area, then synthesise. Depth beats economy here, but every finding must still carry evidence.

## What this review is for

The next design step is fully autonomous development runs: shifts that pick work, dispatch workers, verify and merge, with the human reviewing a digest rather than each step. Likely they will run in the cloud, not on the laptop. The review should tell the human **what in today's ecosystem helps, what will break or waste effort at that scale, and what to change first**. It informs the design of `draft/feature/pyautobrain/shift_watcher_in_the_cloud.md` and phase 5+ of the epic.

## Part A: the orchestrator so far (epic `autonomous-orchestrators`)

Read: the epic `draft/feature/pyautobrain/autonomous_orchestrators_epic.md`; its `complete/2026/11/` records (p1–p4b, batch-watch-live-view, shift-digest-readable-picks, shift-opens-at-dispatched, watcher-workers-survive-systemd-tick, live-shift-worker-gaps, rectangular-parity-absolute-bound, gallery-runner-missing-tiers); `PyAutoBrain/AUTONOMY.md` (glance ruling, stage-2 amendment, shift-brief sections); `PyAutoBrain/agents/conductors/batch/` (`_orchestrator.py`, `_digest.py`, `_brief.py`, `_watch.py`, `_mind_writer.py`, templates, `AGENTS.md`); `PyAutoMind/batches/` (records 2026-11-05-am/pm, 2026-11-06-am/pm, `pilot/pilot.md`, `AGENTS.md`); `autonomy_log.md` (shadow window plus the stage-2 table); pilot issue PyAutoBrain#574 and digests PyAutoMind#534, #536, #542, #543; `draft/feature/pyautobrain/mobile_shift_operation.md`.

Assess honestly:
1. **What the pilot shows** (4 rows: 2 shadow, 2 live, one failed at spawn).
   - Shift 1, unguided: 6 of 6 picks overruled; picks ranked alphabetically because every `notify` prompt grades ~0 review-min.
   - 2 of 3 named live tasks were stale prompts.
   - One worker stalled 70 min on an EnterWorktree prompt.
   - systemd killed the workers at spawn.
   - Late finishers were stranded.
   - About 233k tokens bought one merged PR.

   Which of these are fixed, which are symptoms of a deeper design issue, and what has the pilot not yet tested at all (unattended close-out merges, re-dispatch on a real crash, the token cap, multiple concurrent repos, a long shift)?
2. **Design soundness.** One-Mind-writer, leases and the reaper, the digest as the review surface, tier and merge-cap gating, the calibration rule, `queue.md` as the only importance signal. Where is the state machine fragile? What assumes a laptop (local files, systemd, `claude --bg`, a shared canonical checkout) and must change for a cloud watcher?
3. **Code quality.** Tests that pin behaviour versus tests that pin wording. Duplication between `_digest`, `_watch` and `_orchestrator`. Error paths that fail silently.

## Part B: the whole ecosystem, all organs

Organs (`~/Code/PyAutoLabs/organs/`): PyAutoBrain (conductors: batch, bug, build, clone, community, cortex, docs, eyes, feature, health, hygiene, intake, profiling, refactor, release, workspace; faculties: memory, review, samplers, sizing, vitals; skills), PyAutoMind, PyAutoHeart, PyAutoHands, PyAutoMemory, PyAutoCortex, PyAutoPulse, PyAutoInsight, PyAutoEyes, PyAutoEars, PyAutoBroca, PyAutoGut, PyAutoDNA, PyAutoNerves, PyAutoScientist. Read `organs/AGENTS.md` first for the map.

Review previous **workflows as they actually ran**, not as documented. The evidence:
- `PyAutoMind/complete/2026/{09,10,11}/` (about 600 records);
- `autonomy_log.md` (calibration and Shadow-window rows: gate cells, Heart states at ship, witness forms);
- `active.md`, `planned.md` and `parked.md` churn;
- the draft queue: what is stale? The 2026-11-05 sweep closed 27 shipped drafts and re-scoped 24;
- Heart's readiness history (how often YELLOW, STALE or RED, and why);
- CI wall-clock;
- GitHub PR history: merge latency, reruns, reverts, corrective PRs;
- the auto-memory feedback files at `~/.claude/projects/-home-jammy-Code-PyAutoLabs/memory/` (100+ `feedback_*.md`, each a lesson a session learned the hard way; cluster them: which classes recur?).

Questions to answer, with numbers where possible:
1. **Where does human attention go?** Count interruptions by kind: Heart acks, plan approvals, `/prm`, permission prompts, "merge in the UI" API failures, questions. Which could autonomy remove safely, and which must stay?
2. **Where do tokens go?** Session context load: AGENTS.md chains, MEMORY.md and its sub-indexes, skill files. Repeated re-reads. Subagents that inherit ~20k tokens of AGENTS.md. There is an open draft, `draft/maintenance/organs/reduce_session_token_load.md`; assess it against what you measure.
3. **Recurring failure classes.** Shared-checkout races (the Mind "sweeps" memories), stale canonical checkouts, firewall reds, gh/API flakiness, venv/env traps, stale prompts. Which would multiply under parallel autonomous workers?
4. **Gates.** Is Heart a useful gate or mostly acked noise (how many ships went through on YELLOW, STALE or RED acks)? Do Witness lines get checked or rubber-stamped? Is the review faculty used? What did the 69-row glance window and the 8/8 audit really prove?
5. **Organ boundaries.** Overlap, dead weight, organs with no consumers, docs out of date against code, what a cloud worker (one repo clone, no laptop) can and cannot do in each.
6. **Backlog health.** How stale is the draft queue, how good are `Consequence:`/`Witness:`/`Review-minutes:` headers, and does sizing predict reality? (Compare `Review-minutes` to `review-minutes-actual` wherever both exist.)

7. **Dashboards and the information flow into them.** Added by the human, 2026-11-09: "I think they are good and its not that anything should be removed but I think we need to continue to improve the information flow from development work to dashboard updates. In particular, I feel like things like number of unit tests, integration tests, their run time, many of the things we do hygiene runs on are not being fed through to a dashboard so I can track and monitor it."
   - **Inventory every dashboard and board:** the Mind dashboard (`dashboard.md`/`.html`, `state.json`), Heart's health/readiness board and feed, the Brain board, the Hands release board, the Eyes dashboard, Insight, Pulse, the Cortex science board, the autolens_profiling dashboard, and any others. For each: what it shows, where its data comes from, what refreshes it and when (tick, CI dispatch, local render, manual), and how stale it typically is. Memories `tickNoTimings` and `heartFeedDispatch` show sidecars frozen for weeks.
   - **Map the signals that are produced but never reach a dashboard:** unit-test counts and runtimes per repo, integration/smoke/workspace-validation counts and runtimes, CI wall-clock per gate, slow tests, CLI noise, dependency-cap drift, stale API docs, packaging and git debris (everything the `hygiene`, `ci_speedup`, `cli_noise_clean`, `dep_audit`, `audit_docs` and `repo_cleanup` runs measure), coverage, flaky reruns, prompt and backlog staleness, and orchestrator pilot metrics (`batches/pilot/pilot.md`). For each: where it is computed today, whether it is persisted at all, and the cheapest path to a tracked time series on an existing board. Prefer feeding existing boards over new ones; removing a board is out of scope.
   - **Propose the flow:** how a development run (or a CI run) should publish its numbers so the boards update without a human re-render, and what the human should see trend over time (counts, runtimes, red/green history).
8. **The Heart + release loop.** Added by the human, 2026-11-09: "the heart plus release loop we repeat constantly can probably be set up more efficiently, currently I often 'pause' everything to do heart and hands work (see the history) and there must be a better way to do this. Part of the problem is nightly builds always fail."
   - **Reconstruct the loop from history:**
     - release-pass records and memories (10-07, 10-16, 10-23, 11-04);
     - `/review_release` runs;
     - freeze and thaw episodes;
     - `NIGHTLY_RELEASES` pauses;
     - Heart RED/YELLOW/STALE causes;
     - the nightly driver's run history on GitHub.

     How often does the human stop development to tend Heart and Hands, for how long, and what triggered each stop?
   - **Classify every nightly failure** over the available history: token expiry, tag or publish transients, real test regressions, smoke timeouts, environment drift (Colab, RAL, conda), infrastructure flake, wall-clock caps. Give the share per class and the fix that would remove each class. The question is why "nightly builds always fail", and what would make a green nightly the normal case.
   - **Propose a better loop:** for example, Heart as a background signal that only blocks on real regressions; quarantine of known-flaky legs; automatic retry or self-healing for transient classes; release decoupled from day-to-day development; and what parts an autonomous shift could own (a `notify`/`glance` "keep the nightly green" lane) versus what must stay the human's (version choice, release approval).

## Method

- Read-only on every repo. No branches, PRs, merges, releases, label changes or doctrine edits. Mind writes only for the deliverables below, always from a temporary worktree on `origin/main` (never the shared canonical checkout; other sessions dirty it).
- Fan out: one reviewer per area (orchestrator; Mind/lifecycle/records; Heart/Hands/release/CI and the nightly failure history; dashboards and signal flow; Memory/Insight/Pulse/Cortex knowledge organs; Eyes/Ears/Broca/Gut/DNA/Nerves/Scientist; workflows-as-run from records and autonomy_log; memory-feedback clustering; token/context load). Give each a brief naming its files and questions, then **verify** every high-impact finding independently before it goes in the report (an adversarial check, not a re-read by the same agent). Mark findings `CONFIRMED` or `PLAUSIBLE`.
- Measure where you can (counts, timings, token sizes of the context load) rather than estimate.

## Deliverables

1. **A review report** for the human. Publish it as a private Artifact page and also save it at `/mnt/c/Users/Jammy/Workspace/Science/scratch/ecosystem_review_2026-11/`. Open it with a one-screen summary: the top 10 changes, ranked by impact on autonomous runs, each one line, with the cost to do and the risk of not doing. Then the detail per part, with evidence, including a dashboard signal map (signal → where computed → where shown, or the gap) and a nightly-failure breakdown. End with "what the cloud orchestrator must be designed around".
2. **Draft prompts**, at most ~10, for the highest-value changes. File them in `PyAutoMind/draft/<type>/<target>/` with intake-style headers, honest `Consequence:` tiers and checkable `Witness:` lines. Doctrine changes are `judge` and say so. Do not start any of them.
3. **One comment** on PyAutoBrain#574 linking the report.

Stop at the deliverables. The human reads the report and decides what to start.

<!-- filed by hand 2026-11-09 at the human's request; headers mirror intake's -->
