# Timing-noise audit phase 5: paired whole-round bootstrap for the A/B intervals (fix phase 4)

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
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
Depends-on: active/timing_noise_audit_phase4_ab_rule_semantics.md (fix phase 3, PR #406; this branch stacks on it)
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/timing_noise_audit.md

## Original request (chat 2026-10-08)

"do next phase auto and the one after" — fix phase (4) of `results/notes/timing_noise_audit_2026_10.md`,
launched with `--auto` (effective supervised: bug, Consequence judge); plan approved in chat 2026-10-08.

## What is wrong (audit rows C6, C8, C9 and the reported CIs)

Every point-source A/B cell bootstraps its median ratios by resampling individual calls iid and
unpaired, although calls are timed in interleaved round-robin rounds (calls within a round are
autocorrelated; routes are paired by round). The intervals are too narrow, and since fix phase 3
the C6 / C7 / C10 verdicts read them.

## Scope (fix phase 4; bounded PR, stacked on fix phase 3)

1. Shared `scripts/misc/likelihood_breakdown/round_bootstrap.py`: `round_median_ratio`,
   `round_median_saving` — resample whole rounds with the same indices for every route; record
   `resampling: paired whole rounds` and `effective_n = n_rounds`. Estimator otherwise unchanged
   (medians, 90 % percentile, 2000 draws, fixed seeds).
2. Replace the iid `_median_ratio` / `_median_saving_ms` / `_ratio_boots` in C6
   `backward_pass_ab`, C7 `pytree_input_ab`, C8 `gradient_mode_crossover`, C9/C10
   `solver_config_sweep` and the reported CIs of `gradient_mode_library_ab`, `static_lattice_ab`,
   `vertex_dedup_ab`, `gpu_bottleneck_map` (where the round layout is available). Phase 3's
   verdicts keep consuming the same keys.
3. Witness: synthetic rounds with injected within-round correlation — the iid 90 % CI visibly
   narrower than the round bootstrap's; under a fixed seed the round bootstrap covers the true ratio.
   Each cell imports the same function objects.
4. Re-judge the committed rows' CIs with the round bootstrap (per_call_ms in round order) and record
   the changed intervals / verdicts as facts in the note (no JSON rewritten, no decision reversed).

## Witness

`pytest scripts/misc/test` (new `test_round_bootstrap.py`), ruff, every lint.yml `--check`,
independent review.
