Timing-noise audit phase 1 (audit only): inventory every timing assertion and profiling gate in autolens_profiling with its noise model and a PASS / FAIL / INCONCLUSIVE proposal. Issue autolens_profiling#362 stays open for the fix phases.

**Shipped:** autolens_profiling#402 (merged 2026-10-08; main had to be un-reddened first by the dashboard re-render #403, a PyAutoBrain theme drift unrelated to this task). `results/notes/timing_noise_audit_2026_10.md` (31 rows; per-class PASS/FAIL/INCONCLUSIVE semantics with the small-sample t-bound, outlier, drift and multiple-comparison limits; six ranked fix phases each with a synthetic witness; explicit "nothing changed" statement); `scripts/misc/tooling/list_timing_assertions.py` (AST/grep lister, ~3 s, 70 candidate sites, `--check` in lint.yml, tests in `scripts/misc/test/test_list_timing_assertions.py`); new `wiki/campaigns/measurement_tools.md` + `wiki/index.md` row; pointers in AGENTS.md (Testing) and `scripts/misc/tooling/README.md`.

**Result:** 11 SOUND, 10 FRAGILE, 10 UNSAFE-SILENT. UNSAFE-SILENT (a point estimate or no measurement can qualify a result): dashboard `qualify()` (laptop rows with provenance, rows without load average, HPC rows with `host: None` all qualify — confirmed on synthetic rows; Pulse `pulse/catalogue.py` requires that flag), the fixed-light numba ABBA overhead gate (12 ms point budget) and its promotion rule (noisy result published as measured NO_LEVER), the sweep timeout (one slow run writes a permanent GPU-only marker), memo-policy 3 % paired flags and GO/NO_LEVER verdict, numba-scaling PASS, logdet `clears_threshold`, pytree phase-2b go (CIs computed, never used), solver sweep `best_admissible` argmax over possibly tied configurations. The #361 trigger test is FRAGILE: near-zero false-fail rate but near-zero power (true overhead ~0.8–5.4 % → INCONCLUSIVE → pass), INCONCLUSIVE only printed (silent under `pytest -q`), passed on the laptop at a mean ratio 0.79 which instrumentation cannot produce, shares no code with the 12 ms production cell, budget already relaxed 1.03 → 1.031 (d5462d4). Cross-repo (read only): Brain profiling conductor `COMPILE_DRIFT_RATIO` 2.0 / 1 s compares one point to one point; Heart `script_timing` is not used here.

**Fix phases proposed (priority order):** (1) one shared overhead verdict for the #361 test and the cell, budget in the cell's unit, interval vs excess over budget, INCONCLUSIVE never raises or promotes and is a visible CI warning — witness: fixed block sets (clear pass/fail, the #361 blocks → INCONCLUSIVE, below-1 blocks → INCONCLUSIVE, too few blocks, gross failure, invalid samples, the three pinned RAL rows) + a same-function check; (2) dashboard qualification + drift wording (laptop / missing loadavg / missing host → unqualified; "flat" never reads as measured no-change — today a 1.9× regression publishes as `flat`) — profiling-summary contract change, Pulse coordination; (3) INCONCLUSIVE state for go / lever / NO_LEVER rules using their existing CIs, tie sets instead of argmax. Phases 4–6 in the note.

**Caveats:** the full local suite failed the #361 test once (verdict not captured, `-x`), passed on rerun; lychee not run locally; lister recall limited to numeric / UPPER_CASE-constant comparisons (two-variable comparisons, config-read caps, argmax selections and the sweep timeout were found by reading and are so marked). Commit c9d65a1 carries an Opus 5.5 co-author line beside the Fable line.

**Remainder:** phase 2 = fix phase (1), to be filed as a Mind prompt from the Pulse task `timing_noise_audit` (reuse #362). Related draft `draft/bug/autolens_profiling/call_accounting_ci_timing_threshold.md` is subsumed by fix phase (1) and should be retired when that phase is filed.

## Original prompt

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
