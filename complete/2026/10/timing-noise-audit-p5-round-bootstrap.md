Timing-noise audit phase 5 (fix phase 4 of the inventory): the A/B intervals resample paired whole rounds instead of individual calls iid and unpaired. Issue autolens_profiling#362 stays open for phase 3b and fix phases (5)–(6).

**Shipped:** autolens_profiling#407 (merged 2026-10-08, 8be806cc, head 93a9321d). It adds one shared module, `scripts/misc/likelihood_breakdown/round_bootstrap.py`, which provides `round_median_ratio` and `round_median_saving`. They resample whole rounds with the same indices for both arms and record `resampling: "paired whole rounds"` and `effective_n = n_rounds`. Medians, the 90 % percentile, 2000 draws and the cells' seeds are unchanged.

Seven cells wrap it: C6 `backward_pass_ab`, C7 `pytree_input_ab`, C8 `gradient_mode_crossover`, C9 / C10 `solver_config_sweep` (including the vmap ratios), `gradient_mode_library_ab`, `static_lattice_ab` and `vertex_dedup_ab`. `ab_verdict.tie_set` gains `n` / `min_n`: below 5 rounds nothing is excluded and no `best` is named.

**Re-judgement** (recorded as facts in the audit note; no JSON rewritten):
- No deciding call changed: C7 NO_GO, C6 RAL CPU / A100 10 GO / 6 NO_GO, the C8 crossovers and the C10 RAL CPU 5-member tie set.
- The laptop C6 solved `rev_analytic` row moves GO → INCONCLUSIVE ([0.805, 0.854] straddles 0.85). It never decided anything.
- The 3-round laptop C10 sweep names every candidate (3 < 5 rounds).

**Ledger and verdict counts:** the audit note moves to 33 rows, 20 SOUND, 8 FRAGILE and 5 UNSAFE-SILENT. `gpu_bottleneck_map` (C12) is a recorded remainder.

**Witness:** `scripts/misc/test/test_round_bootstrap.py` (25 tests). The full suite gave 1234 passed and 6 skipped. The independent Opus review returned FINDINGS (one stale `effective_n` label, two low); the fix commit 63642d52 was re-reviewed by the main session before merge. Heart was YELLOW, an 8× manifest drift plus no rehearsal, which the human acknowledged on 2026-10-08.

## Original prompt

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
Depends-on: complete/2026/10/timing-noise-audit-p4-ab-rule-semantics.md (fix phase 3, PR #406, merged 94861700)
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
