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

## Why

With Opus 5.5, a token allocation does far more work. The `/batch` door (review-minute
budgets, `review-at:`, Consequence tiers, `Witness:`) was built for this, but only one batch
record exists (`batches/2026-08-31-pm.md`). Instead the human drives 4–5 chats at once and
mostly approves steps Claude already knows how to take, hits `/prm`, or watches long test
runs. **The constraint is now the human's attention, not tokens.** The target metric is
verified useful work per minute of human review. Token spend is a ceiling, not a target.

Target experience: two human-facing conversations, one Dev orchestrator (the PyAutoScientist
ecosystem through Mind + Brain) and one Science orchestrator (Cortex + Insight). They spawn
full worker sessions the human can open, read and redirect. The human checks in every
2–3 hours, gives a few judgements and revises priorities.

## Human decisions (2026-11-03)

- **Merging `glance` between check-ins is allowed.** Guards:
  - an independent session (not the author) runs the `Witness:`;
  - merging pauses on Heart RED, or on a YELLOW not matched by `expected-effects:`;
  - a per-shift merge cap;
  - the `glance` shadow window keeps appending rows, and a revert demotes the tier;
  - never `judge`-tier work, never a release.
- **Push notifications only when absolutely necessary.** The test: does waiting until
  `review-at` cause harm or waste the shift? That covers data loss or destructive risk, a
  breach of the RAL rules or runaway usage, the whole shift blocked on a human decision, and
  credential or security problems. Everything else goes in the shift digest.
  Budget ≈ 1 push per shift.
- **Lanes are routed by what a task needs, not its work type.** A new prompt field
  `Needs: ral | gpu | wsl-data | none`. Cloud sessions have no RAL, laptop GPU or `/mnt/c`
  (see `policy/remote_sessions.md`). Dev tasks often need RAL test runs, so the **Science
  orchestrator is the single RAL gateway**. A dev worker hands it a "RAL test packet" (what
  to run, at which commit, the pass/fail rule) and parks as "awaiting RAL witness" without
  holding a session open.
- **The human writes a shift brief.** It holds:
  - primary goals, in order;
  - named tasks, done first;
  - the backlog-dip policy (none / fill idle capacity / named epics or tags or tiers, plus
    exclusions);
  - the review-minutes budget, `review-at` and the allowed lanes.

  It extends the `PyAutoMind/batches/` record schema, and the brief *is* the launch act.
  The digest separates brief work from backlog picks and gives a one-line reason for each
  pick.
- **Goals the orchestrator decomposes become near-formalised DRAFTS only.** They are filed
  with proposed `Witness:`, `Consequence:` and `Needs:`, and the human approves them in bulk
  at check-in. Only already-formalised prompts are run. Loosen this once the shadow window
  builds trust.

## Design principles

- **Two rhythms.** AI execution is event-driven: CI finishes, a SLURM job completes, a
  dependency unblocks. The human review cadence (2–3 h digest, capped at the review-minute
  budget) is separate.
- **A deterministic watcher with no LLM in it** polls `squeue`, `gh` checks and Mind state,
  and starts a Claude session only when there is work to do. No tokens are spent watching.
  Claude sessions still never hold timers. This needs only a narrow amendment to
  `policy/end_at_deliverable.md`, which exists because of the 08-31 and 09-03 usage drains.
- **Spend spare tokens on cheaper review, not on more PRs:**
  - independent witnesses;
  - an adversarial second session;
  - a one-screen proof packet per task (before/after numbers, a figure, the witness output,
    what was not checked);
  - bigger tasks, fewer PRs.
- **Background campaigns are bounded:** a hypothesis, a token budget, a stop condition and a
  measurable outcome. No refactoring just to fill tokens.
- **The Science orchestrator is conservative.** It may produce diagnostics, compare seeds and
  flag parameters hitting their bounds. It never gives a scientific verdict: Cortex records
  observed facts and the human's conclusions. It does not launch unbounded follow-ups.
- **No new organ.** The supervisor is a PyAutoBrain conductor. Mind stays the task queue,
  Cortex the run record, Insight the campaign intent.
- **A blocked decision sets that line of work aside** (decide-and-flag) and the orchestrator
  moves on. It never stalls the whole shift.

## Phases (each its own prompt via /start_dev, in order unless noted)

1. **Policy and formats.** Amend:
   - `end_at_deliverable.md`: the watcher is the only timer;
   - `AUTONOMY.md`: shift brief = launch, unattended `glance` with the guards above;
   - `batch.md`: backlog dip under the brief replaces "never substitute your own picks".

   Define the shift-brief schema, digest format, proof-packet format, the push-notification
   test, and the `Needs:` header (intake + census aware).
2. **Deterministic watcher plus dispatch safety:**
   - work leases and repo/worktree claims;
   - no duplicate dispatch, and recovery when a worker crashes;
   - a kill switch;
   - a usage-rate guard.

   Decide the launch mechanism: Desktop scheduled task, local systemd/cron in WSL, or a cloud
   Routine with GitHub `check_run`/`workflow_run` triggers for the cloud lane.
3. **Dev orchestrator pilot.** 2–3 workers, `glance` merges under the guards, 2 h shifts,
   only `notify`/`glance` work plus invariance or refactor tasks. Measure planned vs actual
   review minutes, overrules, reverts, pushes and tokens. Check whether the account has
   Claude Code Projects (beta, cloud threads, Pro/Max). It fits the dev lane only (no RAL),
   and its shared memory must not compete with Mind or auto-memory as the source of truth.
   Otherwise use local worktree sessions.
4. **RAL handoff.** The RAL test packet format, the Science orchestrator submitting under
   `policy/hpc_ral.md` (never bulk CPU on `gpu`, never HPCPullPyAuto the shared mirror,
   private checkouts for A/B runs), and the result returning as the dev task's witness.
5. **Science orchestrator.** Bounded campaigns with explicit protocols, collect-on-completion
   via the watcher plus Cortex pull, automatic diagnostics, and human scientific checkpoints.
   Start with an analysis whose correctness can be checked independently.
6. **Verification campaigns** (can run alongside phases 3–5), each with a hypothesis, budget
   and stop condition:
   - golden-number invariance gates, so refactors become `notify`-tier;
   - numpy/JAX/numba parity;
   - finite-difference vs autodiff gradients;
   - simulate → fit → recover the truth;
   - metamorphic tests (equivalent lens descriptions → equivalent observables, symmetries).

## Success measures (pilot)

Fewer routine interruptions. Zero critical decisions taken without the human. More
independent evidence per task. Planned review minutes close to actual. Corrective-PR and
revert rates. Verified work per human review-minute.

<!-- formalised by the Intake (Conception) Agent on 2026-11-03 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b15ff817-f0d9-4ab3-b23f-735fcbb990f5/scratchpad/autonomous_orchestrators_epic.md -->
