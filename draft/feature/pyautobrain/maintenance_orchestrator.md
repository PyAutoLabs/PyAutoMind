# Phase 14 Maintenance orchestrator: shifts that do the organism's upkeep from what the boards report

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoHeart
Difficulty: large
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-17
Epic: autonomous-orchestrators
Phase: 14
Consequence: judge
Witness: one shadow maintenance shift (`shadow: yes`) whose brief names no task: its plan lists at least five prompts generated from Heart reasons, the `/hygiene` ledger, CI timing records and the no-run census, each with a `Witness:` and a tier, none written by a human; then one live maintenance shift whose digest reports board deltas (CI minutes saved, Heart reasons cleared, debris removed) that agree with the Heart and Brain boards read after it
Lane: local-dev
Unattended: needs-slicing

## Why

Sliced 2026-11-27 (below). Only the live maintenance shifts (14.3 live, 14.4) wait for the M3 gate, PyAutoBrain#574; 14.0–14.2, 14.5 and 14.6 may be built before it (human decision 1).

The Dev orchestrator works a queue the human writes. Much of the organism's important work
is already reported by its boards and never queued: Heart reasons, hygiene findings, slow
tests and CI legs. Today the `_green.py` lane only files drafts for Heart reasons, at most
three per brief, and someone still has to queue them. Most of this work is a bounded change
with a mechanical witness, which is exactly the work a shift can verify and merge
unattended once the M3 gate grants `glance`.

## What

Shifts that do the organism's important maintenance work from what the boards already
report.

- **Keep Heart green.** The `_green.py` lane grows from filing drafts to owning the work.
- **Work Brain's hygiene findings:** slow tests, scripts and imports, CLI noise,
  dependency-cap drift, stale API docs, workspace doc blocks, git and packaging debris.
- **Speed up tests and CI:** unit tests, integration and smoke tests, and CI legs
  (`/ci_speedup`).
- **Other code speed and quality upkeep** whose fix is a bounded change with a mechanical
  witness.
- **Phase 7a runs here:** golden-number invariance and numpy/JAX/numba parity gates. They are
  bounded changes with mechanical witnesses, and they turn refactors into `notify` work.

**Reuses** the Dev orchestrator's watcher, briefs, digest and gates, with a
maintenance-scoped backlog and its own goals line. No second watcher.

**The plan this task writes before any build:**

1. Where the work comes from: Heart reasons, the `/hygiene` ledger, CI timing records, the
   no-run census.
2. How a finding becomes a sized prompt with a `Witness:` and a tier, with no human writing
   it (the sizing faculty and intake's classify, fed by the board's own record).
3. Which tiers it may merge unattended, under the M3 gate's grant.
4. What its digest reports: board deltas (minutes saved, reasons cleared, debris removed).

Then slice it, one prompt per slice, each with its own witness.

## Out of scope

- Experiment and new-capability work: profiling campaigns, sampler trials, speed-up
  experiments and new speed-driven functionality (phase 15).
- Phase 7b (gradient checks, simulate-fit-recover, metamorphic tests).
- Releases. The release path stays the human's.

## Plan and slices (approved 2026-11-27)

The plan, with survey data, is in `Science/scratch/phase14_maintenance_plan_2026-11-27/PLAN.md`.

**Human decisions, 2026-11-27:**
1. Build 14.0, 14.1 and 14.2 before the M3 gate. They are read-only, or file drafts only. The gate applies from 14.3's live run onwards.
2. Tier floors: `glance` for census marker removals, hygiene fixes and organ-CI reds; `judge` for public names, workflow files and dependency caps.
3. `_green.py` folds into 14.1/14.2 as the Heart release-verdict adapter, so there is one filing path.
4. `worktree_drift` findings stay out; they belong to Gut and `/repo_cleanup`.

**Sources, in order of readiness:**
1. the no-run census;
2. the Heart monitoring inventory (keys without `run_id`);
3. hygiene, once it has a ledger;
4. CI timings, using only Heart-flagged rows.

**Slices:** 14.1 → 14.2 → 14.0 (in parallel) → 14.3 shadow → M3 gate → 14.3 live → 14.4 → 14.5; 14.6 any time.

| slice | prompt |
|---|---|
| 14.0 | **merged 2026-11-27** (PyAutoBrain#736; record `complete/2026/11/hygiene-ledger.md`) |
| 14.1 | **merged 2026-11-27** (PyAutoBrain#732; record `complete/2026/11/maintenance-finding-adapters.md`) |
| 14.2 | **merged 2026-11-27** (PyAutoBrain#734; record `complete/2026/11/maintenance-prompt-writer.md`) |
| 14.3 | **code merged 2026-11-27** (PyAutoBrain#738; record `complete/2026/11/maintenance-brief.md`). The shadow run on origin is pending the human's go-ahead; the live run waits for the M3 gate. |
| 14.4 | `draft/feature/pyautobrain/maintenance_p14_4_board_delta_digest.md` |
| 14.5 | **merged 2026-11-27** (PyAutoBrain#740; record `complete/2026/11/maintenance-hygiene-timing-sources.md`) |
| 14.6 | `draft/research/pyautobrain/phase_7a_invariance_and_parity_gates_plan.md` (planning only) |
