# Cluster point solver: adopt a default starting grid fine enough to find every observed image

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- cluster
- point-source
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: every `al.PointSolver.for_grid` call in `autolens_workspace/scripts/cluster/` uses the adopted starting grid, and a check run on the Simple, Pandora (Abell 2744) and MACS J0416 datasets (whichever are on disk) reports, per family, that every observed image has a predicted image within 3x its positional uncertainty at the fitted or true model; the PR states the per-solve cost at the old and the new grid
Review-minutes: 20
Unattended: ready
Lane: local-dev
Epic: cluster-usability
Phase: 3.2
Filed: 2026-11-26

## Why

autolens_profiling PR #537 (Simple cluster CPU profiling) found that the standard image-plane
solver grid, 1″ per pixel on 100 × 100 (`scripts/cluster/modeling.py`; `start_here.py` uses
120 × 120 at 1″), returns four predictions for the five `point_0` observations of Simple. The
second `point_0` observation at (y, x) = (10.362″, 8.143″) lies 2.764″ from its nearest
prediction. A 0.5″ grid also misses it; 0.25″ and 0.2″ recover it (separations 0.00745″ and
0.00672″) at the same field size and 0.001″ refinement precision. An image-plane fit that
silently drops an image is wrong, not merely slow.

## The human's decision (2026-11-26)

> adopt default with fine enough grid

## What to do

1. Plan first (start_dev): post the plan on the issue before any edit.
2. Find the coarsest starting pixel scale that recovers every observed image on each tier that
   is on disk (Simple; Pandora = Abell 2744; MACS J0416), at a field that covers every family.
   Try 0.5″, 0.25″ and 0.2″ at least; record per tier the images recovered and the per-solve
   wall time (JAX FP64, synchronised warm median) at each scale.
3. Adopt the coarsest scale that recovers all images on every tier as the default in every
   `al.PointSolver.for_grid` call under `scripts/cluster/` (field kept, `shape_native` scaled to
   match), with one sentence in the prose saying why the grid is that fine and what a coarser one
   misses.
4. Keep the check from step 2 as a short script or test so a future dataset can be re-checked.
5. Ship via ship_workspace to an open PR with the table from step 2 in its body.

## Rules

- Plan-first; workspace scripts only. A library default in @PyAutoLens is out of scope here;
  if the evidence says the library should own it, file that as a separate draft.
- Do not touch autolens_profiling: phase 3.5 re-times Simple on the adopted grid. (PR #537,
  Simple profiling, merged 2026-11-28; record complete/2026/11/simple-cluster-profiling.md.)
- No multi-hour runs on the laptop; no RAL submission. Merge and issue close stay human.
