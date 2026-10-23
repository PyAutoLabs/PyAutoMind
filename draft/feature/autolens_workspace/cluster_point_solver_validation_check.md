# `@autolens_workspace` cluster example: validate the best-fit PointSolver images against the observed positions

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Epic: cluster-pointsolver-speed
Related: autolens_profiling#439 (PR #440), `results/notes/cluster_pointsolver_campaign.md` "Starting grid vs close member image"
Filed: 2026-10-23

## Why

autolens_profiling#439 measured the workspace cluster example's `PointSolver` grid (100×100 @ 1.0″, `scripts/cluster/modeling.py` ~lines 241–247, used at ~582 for best-fit validation and visualization) on the autolens_visualization cluster model: image 3 of `point_0` (μ −0.89, 0.39″ from `main_1`'s core) is lost at 1.0″ and at every finer scale down to 0.3″; only 0.2″ finds it, and even 0.2″ misses other roots near `r_core = 0` member cores. Finer is not monotonically safer and no separation rule holds. Recommendation from the ledger: keep 1.0″ (the search uses `FitPositionsSourceSolved`, so the solver is not in the likelihood) and add a validation check instead of a fixed finer grid.

## Deliverables

1. Keep the 100×100 @ 1.0″ solver. After the best-fit solve, match each observed image to a solved image within a few σ of the positional noise.
2. For every unmatched observed image, re-solve on a small fine grid around it (e.g. `PointSolver.for_limits_and_scale`, ±1″ at 0.05″) and report what was recovered. (Candidates with a source-plane residual above 10 × precision are already dropped by the solver default, `residual_threshold`, from PyAutoLens#800.)
3. Print/record the per-source match table in the example's output; mirror in the `cluster/` notebook via the usual generation.

## Out of scope

Library changes (the spurious-core candidates are SHIPPED, on by default: PyAutoLens#800, record `complete/2026/10/point-solver-spurious-core.md`; this check no longer needs its own residual drop); changing the modelling grid default.
