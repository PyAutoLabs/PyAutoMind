# Autonomous orchestrators phase 3: orchestrator runtime — watcher, leases, dispatch safety, kill switch, usage guard, digest

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: large
Autonomy: human-required
Priority: high
Status: formalised
Filed: 2026-11-03
Epic: autonomous-orchestrators
Phase: 3
Consequence: judge
Witness: a dry shift with fake workers (`PYAUTO_ORCHESTRATOR_FAKE=1`, tmp state dir, tmp Mind): (a) two overlapping watcher ticks dispatch exactly one worker per lease; (b) a killed worker's lease expires and the task is re-dispatched exactly once per shift, the crash counted in the digest; (c) a `STOP` file in the slot directory makes the next tick a no-op before it reads anything else; (d) the concurrent-worker / sessions-per-shift / token-budget caps refuse the N+1th spawn and the digest says why; (e) no open brief, or a brief past `review-at:`, dispatches nothing; (f) `batch digest` output passes the phase-2 brief/digest schema and is posted once as a comment on a sandbox issue (a second run posts nothing); (g) only the orchestrator path commits to Mind, from a temporary worktree, with workers' ledger lines read from the lease directory; `pytest PyAutoBrain/tests -q` and PyAutoMind tests green
Review-minutes: 30
Unattended: never
Lane: local-dev

Parent: draft/feature/pyautobrain/autonomous_orchestrators_epic.md — read "Design principles",
"Cross-cutting requirements" (crash recovery, usage-rate guard, Mind write contention, digest
delivery) and "External facts" (recheck them: they were verified 2026-11-03 and say recheck at
phase 3). Doctrine is already merged: PyAutoBrain AUTONOMY.md "Shift briefs and unattended
`glance` — 2026-11-03" and PyAutoMind policy/shift_watcher.md (the watcher is the one exemption
to end_at_deliverable; no Claude tool, arms nothing inside a session, no dispatch without an open
brief, STOP checked first). Phase 2 shipped `batch brief --check` / `plan --brief`
(agents/conductors/batch/_brief.py) — build on it.

## Deliverables

1. **The watcher** — a stdlib, non-LLM script (e.g. `PyAutoBrain/bin/orchestrator_watch.py`)
   run by a systemd user timer under WSL. Each tick, in order: `STOP` in the slot directory →
   exit; no open brief (valid per `brief --check`, `review-at:` not passed) → exit; read leases,
   `gh pr checks`, Mind state; decide; spawn or collect. Ship the unit/timer files as templates
   plus an install note — **installing the timer on this machine is the human's act**, not the
   session's (the end_at_deliverable hook stays as is for every session).
2. **Leases** — `~/Code/PyAutoLabs-wt/.orchestrator/<slot>/leases/<task>.json` (task, worktree,
   session id, started, heartbeat, expires), written atomically with an exclusive create so two
   ticks cannot both claim a task; stale lease past expiry → declared dead once, worktree
   inspected, task re-dispatched at most once per shift. `worktree_check_conflict` still runs
   inside the worker.
3. **`batch dispatch`** — spawns a worker from the orchestrator's session template (sources,
   bootstrap, the brief path, `/start_dev <path> --auto`, the end-at-deliverable contract),
   as `claude --bg` (fake mode: a stub process). Never bare.
4. **Usage-rate guard** — caps on concurrent workers and sessions per shift, plus the brief's
   `token-budget:` consumed from each session's final usage report; at a cap the watcher stops
   spawning and the digest says why.
5. **One Mind writer** — workers write ledger lines (claim, close-out) as files in the lease
   directory; only the orchestrator commits to PyAutoMind, from a temporary worktree with
   cherry-pick onto origin/main (never the canonical checkout, never reset --hard).
6. **`batch digest`** — appends `## Digest` to the brief record per `batches/AGENTS.md` (brief
   work vs backlog picks with reasons, one proof packet per task, the counters), and posts it
   once as a comment on the record's `issue:`. Phase 2's validator gains a digest check.

## Out of scope

The pilot (phase 4), RAL packets (phase 5), the Science orchestrator (phase 6). No merge logic
beyond what AUTONOMY.md already grants; unattended `glance` close-outs reuse `/prm`.

## Notes for start_dev

Large and multi-surface: expect start_dev to slice this into ordered PRs (e.g. leases + fake
mode + kill switch first; dispatch + usage guard; Mind writer; digest + delivery), each
judge-tier.

<!-- formalised by the Intake (Conception) Agent on 2026-11-03 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/67475caf-6471-45ce-9711-84cb5f0c456f/scratchpad/p3_raw.md -->
