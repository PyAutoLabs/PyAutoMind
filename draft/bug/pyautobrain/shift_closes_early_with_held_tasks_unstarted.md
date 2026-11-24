# Shift closes early while tasks held behind a parked worker are still unstarted

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-24
Epic: autonomous-orchestrators
Consequence: judge
Witness: re-check first: from the 2026-11-24-am record, confirm the shift closed at 08:34Z (review-at 09:30Z) with `mge_deflections_reverse_mode_nan_at_grid_centre` and `jit_cache_not_hit_modeling_visualization` not started because their repos were held by `substructure_util_zero_padded_halo_slots_make`, whose worker had parked; if confirmed, a watcher test where the holding worker parks with more than 30 min left starts the held task (or records why not) instead of closing early, and fails on the base commit
Lane: local-dev
Unattended: never

Original note (filed from PyAutoBrain#718's prompt, "Related, not in scope", 2026-11-24):
"In shift 2026-11-24-am, `mge_deflections_reverse_mode_nan_at_grid_centre` and
`jit_cache_not_hit_modeling_visualization` were held behind
`substructure_util_zero_padded_halo_slots_make`'s worker. When that worker
parked, the shift closed early (08:34Z, review-at 09:30Z) instead of starting
them. That looks like an early-close gap in the watcher and should be filed as
its own bug if confirmed."

## Why

A parked worker frees its repo for the rest of the shift's time, but the early-close rule
(M3.7c, PyAutoBrain#691: "a park on a question does not hold the shift open") may close the shift
before the planner re-checks tasks it skipped for a held repo. The shift lost about an hour and
two ready tasks.

## What

Re-check at source (`_orchestrator.py` early-close and the planner's held-repo skip). If it
holds: at the tick where a holder parks, re-plan skipped tasks whose repo is now free before the
early-close check, under the in-shift restart rule (> 30 min left).

This changes the watcher, so it is never a shift task (organ rule): run it in chat.
