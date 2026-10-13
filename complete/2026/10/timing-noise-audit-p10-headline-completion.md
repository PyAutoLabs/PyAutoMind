# Median headlines, repeat summaries and wall basis

Completed: 2026-10-13
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
PR: https://github.com/PyAutoLabs/autolens_profiling/pull/412
Merge commit: 6108d0291a0b5b23dde1f1eaa4f05a11aed7736e
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/timing_noise_audit.md

Human explicitly authorized merging all four reviewed PRs when green on 2026-10-13.
Merged unchanged in order #410 → #411 → #412; each exact-head Actions run and
job completed successfully. Each branch head has zero commits outside origin/main.
Existing independent shipping review CLEAN; 1405 passed / 6 skipped (shipping evidence).
This close-out did not repeat the scientific measurements or claim a new independent
code review. The #412 Heart-RED development grant was supplemented by the separate
live merge authorization; no release clearance is implied.

Reference-host qualification and measured repeat endpoints remain separate baseline/compute decisions. Added median estimator stays separate from legacy block means.

Issue #362 closed after all three implementation phases merged. The project audit
note records 38 rows: 35 SOUND including caveats, 3 FRAGILE descriptive rows,
0 UNSAFE-SILENT. No source or measurement edits in this close-out. No compute,
default/baseline change or scientific acceptance. Remaining domain work stays in
Pulse; Brain compile-drift remains its existing bounded Mind draft.

## Original prompt

# Timing-noise audit phase 10: headline completion (README, remaining cells, wall basis, repeats support)

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
Depends-on: active/timing_noise_audit_phase9_familywise_policy.md (phase 9, PR #411, stacked)
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/timing_noise_audit.md

## Original request (chat 2026-10-09)

"prm and then do 3b and leftovers fully wrap up --auto"; "do all work until complete --auto".

## Scope — "Phase 10" of the plan comment

README runtime table reads the median headline where present; breakdown, datacube and `mge_mass` cells opt into `headline_steady_median` (mge_mass keys reconciled); `wall/rates.py` includes the median's extra calls; aggregator/dashboard support for `single_jit_repeats` (≥ 2 independent runs) so `flat` becomes reachable once repeats are measured. No compute; no committed JSON rewritten. Final audit-note wrap-up: every row's end state, what is deliberately left (v2 qualification on the setup-baseline decision; Brain compile-drift draft; human decisions flagged in #410/#411).
