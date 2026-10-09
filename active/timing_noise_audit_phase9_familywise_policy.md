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
