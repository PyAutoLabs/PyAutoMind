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
