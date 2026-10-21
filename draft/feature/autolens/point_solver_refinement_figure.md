# Point-source phase 2: PointSolver refinement figure

Consequence: judge
Autonomy: human-required
blocked-by: active/point_dataset_positions_panel.md (phase 1; shares styling and the solver threading)

@PyAutoLens @autolens_visualization

## Request (human, 2026-10-21)

> I think we should also plan a "point solver" image which basically shows how for a given model the point solver gets to its solution, which is guess is a load of triangles being iteratively refined and displayed by each panel? We have an image of this in the workspace already, but maybe we lost the code to produce it? This is both a great diagnostic for users running lens modeling and also a great way to illustrate how the lens solver works to a user. Add this as another phase to this work, and also include a follow up which scans the workspace for places to slot it in and describe it (e.g. HowToLens's section of position solviung, which is either in chapter 1 or has a placeholder).

## What exists (checked 2026-10-21)

- `autolens/point/solver/shape_solver.py:469` `steps(...)` yields `Step` objects (`autolens/point/solver/step.py`) with `initial_triangles`, `up_sampled`, `neighbourhood` and `filtered_triangles`. There is a second `steps` at line 664, for the other solver class.
- `autolens/point/visualise.py` (last touched 2025-06) has debug-only helpers: `visualise(step)`, `plot_triangles` and `plot_triangles_compare`. They are raw matplotlib with `plt.show()` and `X`/`Y` labels, are not in the plot API or visualizers, and nothing calls them.
- The image the human remembers was not found in autolens_workspace, HowToLens or the PyAutoLens docs (search by filename and "triangle"). Ask the human where it lived, in case the old producer survives.

## Intent

A proper `point_solver.png` subplot: one panel per refinement step (or a chosen subset; first, middle and last when there are many). Each panel shows:
- the image-plane triangles kept at that step, coloured by role (initial, up-sampled, neighbourhood, filtered)
- the observed positions (phase 1 marker style)
- the final solved images
- the critical curves for context

It serves two purposes:
- a modelling diagnostic: did the grid cover every image, and how many triangles survive?
- teaching material for how the solver works.

## Design questions (settle in /start_dev)

- **Panel count and selection.** The number of steps depends on `pixel_scale_precision`. Options are every step, a log-spaced subset, or zoomed insets for the late steps (the triangles become sub-pixel at the full extent).
- **Optional source-plane row.** A second row could show the ray-traced triangles containing the source centre; this connects to the source-plane follow-up.
- **API placement.** Something like `aplt.plot_point_solver(solver, tracer, source_plane_coordinate)`, plus a config-toggled visualizer output during modelling (off by default, since it is costly). Retire or wrap `point/visualise.py`.
- **JAX path.** Decide whether the JAX solver path exposes the same steps, or the figure is numpy-only.
- **Re-render.** Producers in autolens_visualization for point_source_image_chi_squared and cluster.

## Research findings (2026-10-21, read-only prototype)

Prototypes are in `/mnt/c/Users/Jammy/Science/scratch/eyes/autolens/point_solver_prototype/variant_{a,b,c}.png`. The scripts are in the session scratchpad; they are not tracked, so re-derive them from this section.

**Lost image.** It was never committed anywhere. There are two display-only ancestors:
- autolens_workspace `scripts/guides/mappings.py:309-338` `__Solver Refinement Steps__` (#525, 2026-09-03), which plots only the kept-triangle means.
- PyAutoLens `point/visualise.py` (2024). Its only caller was removed in e8db9e276. It has a bug: it plots `triangle[:,0]` as x, so every plot is transposed.

**API.** `solver.steps(tracer=..., shape=Point(*beta))` works today with no library change. Each `Step` holds:
- `initial_triangles`
- `plane_triangles` (undocumented; the source-plane copy)
- `filtered_triangles`
- `neighbourhood`
- `up_sampled`

`n_steps = ceil(log2(scale/pixel_scale_precision))`. That gives 6 steps for the 0.05″ grid at 0.001. The counts are 23,283 tested at step 0, then 80 per step, with 5 kept: four images plus the lens-centre triangle that `magnification_threshold` rejects.

**Cost.** Collecting the steps with NumPy takes 0.15 s; rendering takes about 3 s, mostly the critical curves.

**JAX.** Steps work eagerly but come back NaN-padded (`MAX_CONTAINING_SIZE=20`). Inside jit they are hidden behind `implicit_diff`. So the figure is NumPy-only, re-solving with `xp=np` at the instance being visualised.

**Latent bug.** `Step.tree_flatten` returns 5 children for 6 fields (it omits `plane_triangles`), so `tree_unflatten` raises TypeError. It is harmless today.

**Variants.**
- A: all steps zoomed on one image. Steps 1-5 look identical (the refinement is self-similar), so drop it.
- B: steps 0/1/3/5 for one image, with a source-plane row of the traced triangles and the source star at the cusp. The research worker and the session judged it the teaching form.
- C: a step-0 overview with numbered images and the rejected centre annotated, plus zoom panels per image at steps 1, middle and last. Recommended as the default diagnostic `point_solver.png`.
