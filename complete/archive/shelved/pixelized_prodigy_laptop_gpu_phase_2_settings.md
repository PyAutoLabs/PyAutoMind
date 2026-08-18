# Optimize pixelized Prodigy settings on the laptop GPU

Type: research
Target: autolens_workspace_developer
Repos:
- @autolens_workspace_developer
Difficulty: medium
Autonomy: human-required
Priority: high
Status: retired (2026-08-18 — delivered inside the phase-1 PR + superseded by the 2026-08-17 inference programme; human-confirmed)
Parent: `pixelized_prodigy_laptop_gpu.md` (retired the same day, same reasons)

## Retirement (2026-08-18 — do NOT start dev on this prompt)

This phase was never issued separately: the phase-1 session delivered the
phase-2 characterisation in the same PR (autolens_workspace_developer#126,
merged 2026-08-13; record `complete/2026/08/pix-prodigy-gpu-compat.md`) —
DelaunayNN starts curve, the 6 GB VRAM ceiling (batch 8 OOMs family-wide),
batch-size comparison, free-vs-fixed regularization, and the four-mesh
recommendation table this prompt asked for. Residual settings questions
(optimal n_starts via basin-hit probability, mesh searches with wrong-mass
basins fenced) are owned by the 2026-08-17 inference programme
(autolens_profiling#134, `results/notes/inference/PROGRAMME.md`, Phases 3
and 5), which redesigns them around PositionsLH — a lever this prompt
predates.

Consume the phase-1 four-mesh compatibility results and determine the
`af.MultiStartProdigy` settings that reach the best supported likelihood in
the fewest optimizer steps and shortest wall time on the laptop RTX 2060
Max-Q. Cover rectangular, KNN, Delaunay, and DelaunayNN without repeating
settled CPU arms unnecessarily.

Compare useful `n_starts` values (starting at 4 and escalating through 8/16
only when they add basin coverage), memory-tiling `batch_size` values that fit
6 GB VRAM, and fixed/inherited versus free Matérn and free AdaptSplit
regularization where scientifically relevant. Keep the validated broad start
band unless evidence demands otherwise. Use full FoM histories to report
steps-to-bar rather than launching redundant step-ceiling runs.

Produce a four-mesh recommendation table with maximum likelihood, recovered
mass parameters, steps-to-bar, wall-to-bar, per-step time, resurrection rate,
and VRAM/overflow constraints. Clearly distinguish highest-likelihood,
fewest-step, and shortest-wall winners when they differ, and document every
configuration that fails within its tested budget.

## Original request

> Then work out what settings infer the max Lh modle I fewest steps e.g.
> perform best.
