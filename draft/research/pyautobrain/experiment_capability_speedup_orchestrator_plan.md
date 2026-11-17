# Phase 15 Plan the experiment and capability-speedup orchestrator (planning only)

Type: research
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoPulse
- PyAutoInsight
- PyAutoCortex
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-17
Epic: autonomous-orchestrators
Phase: 15
Consequence: judge
Witness: a plan document, linked from this epic's Progress, that answers each of the four questions under "What to settle" with a named mechanism and the file or organ that owns it, and lists the prompts for any later build, each with a `Witness:` line; no code changes
Lane: any
Unattended: never
Blocked-by: PyAutoBrain#574

## Why

Blocked by the M3 gate: PyAutoBrain#574 (phase 4c) closes there, with the unattended `glance` grant.

Some of the organism's work runs experiments with verdicts or builds new capability whose
purpose is speed. That is not maintenance (phase 14), and the Dev orchestrator's
merge-a-witnessed-PR shape does not fit it: a profiling campaign or a sampler trial ends in a
verdict, often after RAL or GPU runs, not in a PR. The likelihood-lifecycle epic's later
phases already run this way by hand. This phase plans how they should run; it builds nothing.

## What it covers

PyAutoPulse and PyAutoInsight work, and anything shaped like it:

- profiling campaigns;
- sampler trials (`/sampler_pipeline`);
- "make this likelihood faster" experiments;
- new functionality whose purpose is speed (a new operator, route or search).

These will likely need their own orchestrator or way of running.

## What to settle

1. How a campaign is briefed.
2. Who judges a verdict.
3. How RAL and GPU compute is allowed for.
4. How results reach Pulse, Insight and the Cortex.

## What it relates to

- Phase 5 (RAL hand-off packets) follows this phase, because this phase settles how compute
  is allowed for.
- Phase 6 (Science orchestrator over Cortex and Insight).
- Phase 7b (gradient checks, simulate-fit-recover, metamorphic tests), which runs with this
  phase and phase 6.
- The likelihood-lifecycle epic's later phases.

## Out of scope

- Any build, including a watcher change.
- Maintenance work (phase 14).
- Submitting any RAL or GPU job.
