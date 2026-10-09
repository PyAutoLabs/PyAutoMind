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
