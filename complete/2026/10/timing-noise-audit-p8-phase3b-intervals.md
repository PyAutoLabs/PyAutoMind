# Intervals for memo-policy, scaling and logdet gates

Completed: 2026-10-13
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
PR: https://github.com/PyAutoLabs/autolens_profiling/pull/410
Merge commit: 4abe4226784556f15251e50176b872ad2a5fe90e
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/timing_noise_audit.md

Human explicitly authorized merging all four reviewed PRs when green on 2026-10-13.
Merged unchanged in order #410 → #411 → #412; each exact-head Actions run and
job completed successfully. Each branch head has zero commits outside origin/main.
Existing independent shipping review CLEAN; 1341 passed / 6 skipped (shipping evidence).
This close-out did not repeat the scientific measurements or claim a new independent
code review. The #412 Heart-RED development grant was supplemented by the separate
live merge authorization; no release clearance is implied.

C1 keeps its five-round minimum; four-repeat classifications remain INCONCLUSIVE. C5 keeps its both-estimators requirement.

Issue #362 closed after all three implementation phases merged. The project audit
note records 38 rows: 35 SOUND including caveats, 3 FRAGILE descriptive rows,
0 UNSAFE-SILENT. No source or measurement edits in this close-out. No compute,
default/baseline change or scientific acceptance. Remaining domain work stays in
Pulse; Brain compile-drift remains its existing bounded Mind draft.

## Original prompt

# Timing-noise audit phase 8: intervals for C1, C3, C4, C5 (inventory phase 3b)

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
Filed: 2026-10-09
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
Plan: https://github.com/PyAutoLabs/autolens_profiling/issues/362#issuecomment-6079746240
Depends-on: complete/2026/10/timing-noise-audit-p7-warmup-witness-band.md (fix phase 6, PR #409, merged 4db4d988)
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/timing_noise_audit.md

## Original request (chat 2026-10-09)

"prm and then do 3b and leftovers fully wrap up --auto"

## Scope — "Phase 8" of the plan comment

C1 `matched_counterfactual` paired-repeat interval (flags only when resolved; false_accepts/false_rejects relabelled, INCONCLUSIVE count); C3 six-target memo verdict with per-target intervals under Holm across the six (GO only if all resolve, NO_LEVER only if one resolves against, else INCONCLUSIVE); C4 `breakdown_reconciles` interval vs ±5 %; C5 logdet `clears_threshold` interval vs 0.5 ms on both estimators. All through `ab_rule_verdict`; synthetic witnesses; no compute; committed rows re-judged as facts.
