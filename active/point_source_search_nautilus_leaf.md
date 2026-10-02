# First point-source search leaf: Nautilus on the source-plane solved likelihood (admission bar)

Type: feature
Target: autolens_inference
Repos:
- autolens_inference
Themes:
- point-source
- inference
- profiling
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: active
Consequence: judge
Review-minutes: 20
Epic: point-source-cpu-speed
Lane: any
Filed: 2026-09-28
Issued: 2026-09-28

## Why

The source-plane χ² speed campaign (autolens_profiling, `draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md`)
has one remaining candidate — blackjax NUTS/SMC forward-mode `value_and_grad`. Per the 2026-09-27
profiling philosophy, a phase needs an admission bar from autolens_inference: the likelihood's share
of a real fit and the evaluation count for the use case. `autolens_inference/scripts/point_source/searches/`
is empty, so no bar exists. This task builds the first point-source search leaf (Nautilus, the
production sampler) and records that bar; a blackjax NUTS leaf follows as the next slice on the
same runner.

## Approved plan (human, 2026-09-28)

1. Run `scripts/misc/simulators/point_source.py` for the `simple` preset (dataset never simulated).
2. Small shared runner `scripts/misc/searches/_point_runner.py`, reusing `scripts/misc/slam/_runner.py`
   / `_inference_cli.py` CLI, row, truth and device helpers (no duplication where importable).
3. Leaf `scripts/point_source/searches/nautilus/simple_source_plane.py` (`--instrument simple`):
   source-plane solved likelihood (`FitPositionsSourceSolved`), the 5-parameter model of the
   autolens_profiling phase-2c L5 rung.
4. Result row: `wall_s`, `likelihood_evals`, `log_evidence`, truth Δσ, plus admission-bar fields —
   `per_call_s` (steady-state jitted call, timed after warm-up), `likelihood_share` =
   per_call_s × likelihood_evals ÷ wall_s, `compile_s`.
5. One-seed probe, then a 5-seed spread on RAL CPU (gpu partition, no --gres, euclid-ral-gpu-2);
   WALL-BASIS row; smoke line in lint.yml; README regen.
6. Record admission-bar numbers in the autolens_inference wiki and on the autolens_profiling
   campaign page (`wiki/campaigns/point_source_source_plane.md`, separate small PR or note).

## User request (verbatim, 2026-09-28)

"Prm and continue" → chose "Point-source search leaf (Recommended)" → "Approve as planned".

## Approved CI repair, 2026-10-02

Human approved the focused Student-t uncertainty fix and audit filing. This repairs the ledger companion PR #361 on the existing task branch; it is not a new campaign phase.

# Fix uncertainty handling in the ABBA instrumentation overhead test

Type: bug
Target: workspaces
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready

# Fix uncertainty handling in the ABBA instrumentation overhead test

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: high
Consequence: judge

## Goal
Unblock the existing point-source phase's ledger PR #361 by correcting its unrelated timing test's noise decision. Keep the 1.031 practical overhead threshold, correctness/coverage assertions and an unconditional 1.5 gross-regression guard. Use the one-sided 95% Student-t lower confidence bound on the three ABBA ratios to fail only a resolved exceedance; report overlapping measurements as inconclusive. Add deterministic cases for pass, failure, overlap and gross regression. Limit this patch to the test module; broader production/test gate audit is filed separately.

## Evidence
Failed ratios: [1.0218478812434695, 1.0243047139025747, 1.0470684004725312], mean 1.0310736652061918. Coverage 99.95%; likelihood equality passed. The existing block-range guard does not resolve whether the mean exceeds 1.031. Five local repeats showed large scatter. Do not increase the budget or rerun until green.

## Original user request
fix the noise cutoff, intake na issue to fix this long term (e.g. check all trests but also make sure the whole mechanism accounts ofr noise) and then prm and continue this task

<!-- formalised by the Intake (Conception) Agent on 2026-10-02 from file:tmp/noise-cutoff.md -->
