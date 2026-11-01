# Likelihood lifecycle phase 6a: gradient harness, catalogue ingestion and the imaging/mge pilot

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- jax-gradient
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Consequence: judge
Witness: scripts/imaging/mge/gradient_breakdown.py runs on CPU in CI and writes results/imaging/mge/<instrument>/jax_cpu_dense_fp64/<host>/gradient.json with forward and value_and_grad per call (single and vmap), grad compile time, grad_over_forward and the pre-registered FD check; build_catalogue turns a gradient.json into a measurement: gradient record (Pulse-valid) carrying the FD status and a hazard flag when grad/forward > 4 or FD fails; tests cover the harness, the FD rule and ingestion
Review-minutes: 30
Unattended: never
Epic: likelihood-lifecycle
Phase: 6
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-01

## Request (human, 2026-11-01, verbatim)

"start phase 6 and research it"

## Human rulings (AskUserQuestion, 2026-11-01)

- Heart RED: "Override + create issue" (development only; merge via /prm).
- Cells (all of phase 6): the 46 JAX Optimal cells plus, for the 25 numba-optimal CPU cells, their JAX CPU secondary (what a gradient sampler would run), plus the held datacube A100 provisional cells — about 74 cells.
- Depth: whole-likelihood — forward vs value_and_grad (single call and vmap), grad compile time, grad/forward, FD check; a per-step backward breakdown only for hazard cells, filed separately.
- FD rule (pre-registered): central differences in fp64 along 3 seeded random unit directions, steps h and h/2 with Richardson extrapolation; pass when |FD − grad·v| / max(|grad·v|, tiny) ≤ 1e-4 in every direction; the relative error is always reported.

## Phasing (one /start_dev task each)

- 6a (this): shared harness + gradient.json convention + catalogue ingestion + imaging/mge pilot, CI smoke; no compute.
- 6b: gradient_breakdown.py for the other 19 likelihoods + `gradient_p6.py` campaign generator (batch 0 walls, batch 1).
- 6c: compute, human go per batch, run from a RAL-capable session (this cloud session cannot reach RAL).
- 6d: ingest; coverage and day-zero pages; hazards (>4x or FD fail) filed through intake.

## Research (2026-11-01)

No gradient.json exists; Pulse already accepts measurement: gradient (seconds); the only precedent is point_source_source/source_plane/likelihood_breakdown.py (grad_over_forward). Each likelihood's runtime script builds its own fused jit-able likelihood; shared builders exist only for imaging/mge and galaxy_group.
