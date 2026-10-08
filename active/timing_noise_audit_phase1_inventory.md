# Timing-noise audit phase 1: inventory every timing assertion and profiling gate, with a noise model and PASS / FAIL / INCONCLUSIVE semantics

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- measurement-tools
Difficulty: moderate
Autonomy: supervised
Priority: high
Consequence: judge
Status: active
Filed: 2026-10-08
Issued: 2026-10-02
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/timing_noise_audit.md

## Original request (Pulse task `timing_noise_audit`, issue #362, filed 2026-10-02)

"Audit all runtime-sensitive tests and the production profiling acceptance mechanisms for correct
treatment of measurement noise. Inventory absolute/relative cutoffs, warmup, repeated blocks,
pairing/order, sample count, clock/synchronization, host qualification, estimator uncertainty and
multiple comparisons. Follow dependencies into other repos only when the inventory identifies
them; split implementation into bounded phases after the audit."

Human direction 2026-10-08 (Pulse check-in): after the linear-solver programme closed, "move on
to the next Pulse task" — this is the highest-priority ready task.

## Scope of phase 1 (audit only — no gate, budget or tolerance changes)

1. **Inventory**: every timing assertion in `scripts/misc/test/`, every production acceptance /
   qualification gate (likelihood_breakdown call accounting, sweep drift policy, `qualified`
   flags, ABBA cutoffs, `check_submits` wall basis, the Heart unit-timing baseline only where
   the inventory shows a shared mechanism), each with: estimator, sample count, warm-up and
   repeated-block structure, pairing/order, clock, host qualification, the cutoff and its
   justification, the implied noise model, the false-positive and false-negative risk, and the
   owner (test vs production instrument).
2. **Semantics**: a proposed PASS / FAIL / INCONCLUSIVE definition per gate class, such that
   INCONCLUSIVE never qualifies a result silently and never reads as a measured pass; limits of
   small-sample Student-t bounds, non-normal/outlier timings, dependence/drift and multiple
   comparisons stated explicitly.
3. **Phase plan**: the bounded implementation phases the inventory implies (e.g. the #361
   call-accounting guard — compare uncertainty to the excess, not block range to the whole
   budget — and the related Mind draft `draft/bug/autolens_profiling/call_accounting_ci_timing_threshold.md`),
   each with its deterministic synthetic-data witness.
4. **Deliverable**: `results/notes/timing_noise_audit_2026_10.md` (the inventory table and
   semantics), linked from `wiki/campaigns/` (measurement-tools) and the Pulse task; no code
   change beyond what reading requires. Optional: a tiny read-only script that lists the
   assertions mechanically so the inventory cannot drift.

## Witness

The audit note exists, every timing assertion / gate found by `grep` over the repo appears in
its table, and `build_readme.py --check`, `check_wiki` and `ruff` stay green.
