# Family-wise policy, paired round bootstrap and drift

Completed: 2026-10-13
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
PR: https://github.com/PyAutoLabs/autolens_profiling/pull/411
Merge commit: 3cf6b2ce44ff1172ab077bd428016e80926acc58
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/timing_noise_audit.md

Human explicitly authorized merging all four reviewed PRs when green on 2026-10-13.
Merged unchanged in order #410 → #411 → #412; each exact-head Actions run and
job completed successfully. Each branch head has zero commits outside origin/main.
Existing independent shipping review CLEAN; 1376 passed / 6 skipped (shipping evidence).
This close-out did not repeat the scientific measurements or claim a new independent
code review. The #412 Heart-RED development grant was supplemented by the separate
live merge authorization; no release clearance is implied.

C11 four-round evidence remains INCONCLUSIVE; no minimum relaxed. GPU memo MDI reinterpretation remains recorded, not a new measurement.

Issue #362 closed after all three implementation phases merged. The project audit
note records 38 rows: 35 SOUND including caveats, 3 FRAGILE descriptive rows,
0 UNSAFE-SILENT. No source or measurement edits in this close-out. No compute,
default/baseline change or scientific acceptance. Remaining domain work stays in
Pulse; Brain compile-drift remains its existing bounded Mind draft.

## Original prompt

# Timing-noise audit phase 9: family-wise policy (C6, C10, C11), C12 round bootstrap, P2 between-row drift

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
Depends-on: active/timing_noise_audit_phase8_phase3b_intervals.md (phase 3b, PR #410, stacked)
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/timing_noise_audit.md

## Original request (chat 2026-10-09)

"prm and then do 3b and leftovers fully wrap up --auto"; "do all work until complete --auto".

## Scope — "Phase 9" of the plan comment

One documented family-wise policy (Holm via `ab_verdict.holm_family_verdict`, family = one verdict) applied to C6 (routes × lanes), C10 (configurations; tie sets) and C11 (kernels × cells; ratio > 1.3 gets an interval); C12 `gpu_bottleneck_map` onto the paired round bootstrap where its layout allows; P2 between-row drift recorded, promotion INCONCLUSIVE when rows drift. Synthetic witnesses; no compute; committed rows re-judged as facts.
