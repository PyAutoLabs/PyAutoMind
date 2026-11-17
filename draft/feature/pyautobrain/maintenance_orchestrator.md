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
Blocked-by: PyAutoBrain#574

## Why

Blocked by the M3 gate: PyAutoBrain#574 (phase 4c) closes there, with the unattended `glance` grant.

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
