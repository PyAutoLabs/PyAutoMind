# Optimize MultiStartProdigy for pixelized meshes on the laptop GPU

Type: research
Target: autolens_workspace_developer
Repos:
- @autolens_workspace_developer
Difficulty: large
Autonomy: human-required
Priority: high
Status: retired (2026-08-18 — phases shipped + direction superseded by the 2026-08-17 inference programme; human-confirmed)

## Retirement (2026-08-18 — do NOT start dev on this prompt)

Two independent reasons, both verified:

1. **The phase work already shipped.** Phase 1 (compatibility) and phase 2
   (characterisation) were delivered together in a single PR —
   autolens_workspace_developer#126, merged 2026-08-13 (issue #125 closed).
   Record: `complete/2026/08/pix-prodigy-gpu-compat.md`; results write-up on
   wsdev main: `searches_minimal/pix_prodigy_laptop_gpu_findings.md` §1–6.
   All four meshes have truth bars, GPU feasibility, the batch-size headline
   (batch decides whether plain Delaunay finds truth; DelaunayNN is
   batch-insensitive), and revised recommendations.
2. **Forward direction is owned by the inference programme.** The 2026-08-17
   human-approved inference-methods programme (autolens_profiling#134, merged
   as `results/notes/inference/PROGRAMME.md` via PRs #136/#137) supersedes this
   prompt's remaining scope: its Phase 3 is the final MultiStartProdigy
   investigation (basin-hit probability, n_starts) and its Phase 5 is
   pixelized/mesh global searches — with **PositionsLH fencing**, which this
   prompt predates (pixelized profiling analyses explicitly disabled the
   positions guard). Re-running settings sweeps without positions would redo
   work the programme has redesigned.

This prompt is **not** the programme prompt itself — it is the older per-mesh
laptop-GPU scoping (phased 2026-08-11). Loose ends it left (DelaunayNN
free-AdaptSplit beyond 300 steps; high-coefficient truth-bar scan for lane
deaths) are recorded in the completion record and fall under programme Phase 5.

Continue the shipped CPU investigation of `af.MultiStartProdigy` on pixelized
source meshes using the laptop NVIDIA RTX 2060 Max-Q through the `PyAutoGPU`
environment. Produce comparable results for rectangular, KNN, Delaunay, and
the new `DelaunayNN` mesh whose natural-neighbour interpolation provides
smoother gradients across Delaunay topology flips.

First establish whether Prodigy recovers the correct maximum-likelihood mass
model for each mesh, reusing prior CPU findings where they remain valid and
running controlled laptop-GPU confirmations. Establish mesh-specific truth
likelihood bars and record failures precisely (non-finite wall, overflow,
VRAM limit, stalled basin, or insufficient tested budget).

Then determine settings that reach the highest likelihood in the fewest
optimizer steps and shortest wall time. Compare useful values of `n_starts`
and `batch_size`, and the fixed/inherited, free Matérn, and free AdaptSplit
regularization cases where relevant. Preserve broad start bounds unless new
evidence overturns the prior result that narrowing hurts. Persist full
figure-of-merit histories, recovered mass parameters, resurrection counts,
step throughput, steps-to-bar, hardware/library identity, and a concise
four-mesh recommendation table.

Keep the existing `autolens_profiling` DelaunayNN runtime task and its dirty
worktree separate. Mature winning configurations into profiling only after
the experiment-tier evidence is settled.

## Phases

1. `pixelized_prodigy_laptop_gpu_phase_1_compatibility.md` — establish
   four-mesh truth bars, GPU feasibility, and matched fixed/inherited-reg
   compatibility results.
2. `pixelized_prodigy_laptop_gpu_phase_2_settings.md` — use phase 1's valid
   configurations to optimize starts, batching, and regularization for
   likelihood quality, steps-to-bar, and wall time.

## Original request

> Using thr GPU on this laptop via PyAutoGPU continue work investigating
> MultiStartProdigy for the pixelized mesh use cases including the new
> DelaunayNN which has improved gradients. First confirm prodigy works for
> these meshes or document when it doesn't, then work out what settings infer
> the max Lh modle I fewest steps e.g. perform best

Follow-up:

> All sounds good but make aure we have results for rectangular and knn too
> which partly have already run?
