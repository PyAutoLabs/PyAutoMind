Shipped phase 2 of the point-source figures: the PointSolver refinement figure.

**Figures**
- **Still:** `aplt.plot_point_solver(solver, tracer, source_plane_coordinate, ...)` draws a 2×2 of steps 0, 1, 2 and final, in the approved `variant_f_coarse` style:
  - tested grey, kept blue, kept-then-rejected hatched, neighbours orange, up-sampled green
  - the step-0 image numbering and `magnification_threshold` note
  - a centroid ▲ for sub-pixel triangles
  - arc-second ticks and no axis-label text
- **Teaching GIF:** `animate=True` uses the same `draw_point_solver_panel` and writes a Pillow GIF (4 frames, final frame held).
- **Visualizer output:** `PlotterPoint.point_solver`, behind `fit_point_dataset: subplot_point_solver` (default false). It re-solves with NumPy for the best fit only and warns when a step keeps ≥16 of the JAX `MAX_CONTAINING_SIZE` of 20.

**Also in this PR**
- `Step.tree_flatten` fixed.
- `point/visualise.py` removed.
- Thinner model ✕ in the phase-1 Fit Positions panel.
- Cluster labels: each number is adjacent to its own image; several rejected candidates get one corner label with an arrow to each. Dense tilings are drawn as a shade.

**autolens_visualization**
- Real-solver `point_solver.png` for point_source_image_chi_squared and cluster.
- Teaching still and GIF in `point_source_image_chi_squared/images/visualization/teaching/`. The GIF is tracked but kept out of the PNG-only manifest.
- The Eyes mirror now copies GIFs too.

Merged 2026-10-21 via a human /prm (judge tier), library first. The full test_autolens suite passes (873).


**Follow-ups**
- `draft/docs/autolens/point_solver_figure_workspace_placement.md` (phase 3)
- `draft/feature/autolens/cluster_point_figures_dedicated_pass.md`
- `draft/feature/autolens/point_fit_source_plane_panel.md`
- `draft/bug/autolens/point_fit_critical_curves_ignore_source_redshift.md`

## Original prompt

# Point-source phase 2: PointSolver refinement figure

Consequence: judge
Autonomy: human-required
Issued: 2026-10-21
builds-on: complete/2026/10/point-dataset-positions-panel.md (phase 1 shipped 2026-10-21; shares styling and the solver threading)

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

## Human design direction (2026-10-21, after seeing A/B/C)

The human prefers the old `visualise(step)` style, a fixed-axes panel showing every image, because it shows the triangles shrinking. A/B/C lose that because their axes rescale.

Direction:
- **Panel 0** is the variant-C overview: numbered images, and the centre triangle annotated as rejected by `magnification_threshold`.
- **Later panels** show every image at a fixed extent.
- **Zooms** happen only when a zoom is unavoidable, and are explicit: a dashed box on the previous panel and "zoom ×k" in the title, held fixed across the steps that follow.
- **Colours.** Kept-then-rejected (μ < threshold) triangles get a colour paired with the kept colour on every panel.
- **Teaching mode** may use a coarse grid; the diagnostic uses the real solver.
- **Fixes.** Correct the (y,x) transposition; no axis labels.

Variant D (real grid and coarse grid) is being prototyped into the same scratch folder.

Still open with the human:
- cluster row/image capping
- visualizer output: config-toggled, off by default, best-fit only, with the JAX `MAX_CONTAINING_SIZE` warning
- retiring `point/visualise.py` and fixing `tree_flatten` in the same PR

## Human decision: figure layout (2026-10-21, after variants D/E)

- **Layout:** a 2×2 `point_solver.png` showing steps 0, 1, 2 and the **final** step; the steps in between are skipped.
- **Style:** exactly `variant_d_coarse.png`'s top-row panels (tested grey, kept blue, kept-then-rejected hatched muted blue, neighbours orange, up-sampled green, critical curve, observed circles, solved red ✕, plus the step-0 numbering and the `magnification_threshold` annotation).
- **Extent:** the same fixed full extent on all four panels, with no insets or zooms. Sub-pixel kept triangles on the final panel are drawn as a centroid ▲ marker.
- **Rejected alternatives:** the per-image inset rows were judged information overload, and the simplified-triangle variant E was not chosen.
- **Prototype:** `variant_f_coarse.png` (teaching) and `variant_f.png` (real solver), in the scratch prototype folder.

## Human addition: teaching animation (2026-10-21)

The teaching figure also gets an **animation in exactly the same style**: one panel at a time, playing steps 0 → 1 → 2 → final in sequence.

Implementation intent:
- One shared per-panel draw function used by both the 2×2 still and the animation, so the two cannot drift apart.
- Output via `matplotlib.animation` with `PillowWriter` as a looping GIF, so there is no ffmpeg dependency. The final frame is held longer.
- An API option alongside the still, e.g. `aplt.plot_point_solver(..., animate=True)`.

Phase 3 places the GIF next to the still in HowToLens tutorial 4 and the workspace `point_source/fit.py` placeholder.

The prototype is `variant_f_coarse.gif` in the scratch prototype folder.

## Prototype producer preserved (2026-10-21)

The scratch producer is at `/mnt/c/Users/Jammy/Science/scratch/eyes/autolens/point_solver_prototype/producer/`. Run `python variant_f.py coarse|real [gif]`.
- Its `draw_panel(ax, i, step)` is shared by the 2×2 PNG and the GIF.
- `common.py` loads the viz true model.
- Use it as the reference implementation for phase 2.

`variant_f_coarse.gif` is 0.14 MB: 4 frames at 1.25 s each, with the final frame held for 3.75 s.

On the real grid, steps 1, 2 and final look identical (sub-pixel triangles). The proposed diagnostic is therefore two panels (step 0 and final), pending the human's answer.

## Human decisions (2026-10-21, final design round)

- **Teaching figure:** `variant_f_coarse.png` is approved, along with the GIF in the same style.
- **Modelling output (option C):** the visualizer saves the same 2×2 (steps 0, 1, 2, final) using the model's real solver, accepting that on fine grids steps 1, 2 and final look alike. Config-toggled.
- **Axes:** show arc-second coordinate tick labels in the standard PyAutoLens style (e.g. `1.9"`, as in the phase-1 positions panels), produced with the library's own tick/extent machinery rather than raw matplotlib ticks. There are still no `x (")` / `y (")` axis-label text, consistent with phase 1. This applies to the still and to every GIF frame.

Still to confirm at /start_dev:
- cluster image capping
- default-off toggle, best-fit only, and the JAX `MAX_CONTAINING_SIZE` warning
- retiring `point/visualise.py` and fixing `Step.tree_flatten`

## Carry-over from phase 1 (approved in chat 2026-10-21)

Thin the model ✕ in the Fit Positions panel (`positions_panel.py`), using a thinner line and smaller marker, so the observed dot stays visible under it when the fit is exact. Re-render the point_source_* and cluster figures.
