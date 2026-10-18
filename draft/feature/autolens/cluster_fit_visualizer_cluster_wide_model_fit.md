# Cluster fit visualizer: cluster-wide model-fit figures at cluster scale

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_profiling
- autolens_workspace
- autolens_workspace_test
- PyAutoEyes
Difficulty: large
Autonomy: supervised
Priority: high
Memory: reading-queue.md; wiki/lensing/sources/dark-matter-substructure.md; wiki/lensing/sources/lens-modeling-methods.md
Status: formalised
Consequence: glance
Witness: autolens_workspace_test cluster fixture fit writes image/cluster_fit_overlay.png and one zoom per system (pytest asserts the files exist and are non-empty)
Review-minutes: 3
Unattended: needs-slicing

# Cluster fit visualizer: cluster-wide model-fit figures at cluster scale

Type: feature
Target: PyAutoLens
Epic: cluster-strong-lensing
Parent: draft/feature/autolens/source_cluster_arc.md
Priority: high
Difficulty: large
Autonomy: supervised
Witness: autolens_workspace_test cluster fixture fit writes image/cluster_fit_overlay.png and one zoom per system (pytest asserts the files exist and are non-empty)

## Original user request (verbatim, Pulse cluster-pointsolver chat, 2026-10-18)

> Do we have appropriate visualization on cluster scales for this pilot or is that a task we should do next to it, e.g to see that it works? Feels like we maybe should intake PyAutoEyes cluster visualization and pair it to this as the modeling result visualisation

> This is a good plan, but remember that most visualization defaults and inputs was designed for galaxy scale and will look awful on cluster scales so we need the campaign to also factor in the fact that some degree of bespoke visualization or update existing tools. Cross reference the Cluster epic in case this is also part of that?

## Problem

A cluster model-fit (`autolens_workspace/scripts/cluster/start_here.py`) runs one `AnalysisPoint`
per lensed system combined into a factor graph. Visualization during the fit is therefore the
galaxy-scale `VisualizerPoint` (`autolens/point/model/visualizer.py`) run once per system: N
separate galaxy-scale `FitPoint` figures with galaxy-scale extents, marker sizes and colour
defaults, and no cluster-wide figure of model versus observed positions. The bespoke cluster
plotting package (`autolens/cluster/plot/cluster_plots.py`, shipped 2026-07-09 under
PyAutoLens#577: `plot_positions_overlay`, `plot_image_group_zooms`, `plot_critical_curves`,
`plot_caustics`, `subplot_cluster_dataset`; per-source-plane curves, log normalisation, halo and
member centre markers, kpc scale bar) is re-exported in `aplt` but is not wired into any
visualizer, so model-fit output never uses it.

## Scope

- A cluster-aware visualizer (or a cluster mode of `VisualizerPoint`) that emits, at the usual
  on-the-fly and end-of-fit points: one cluster-wide fit figure — every system's model and observed
  positions on the cluster image, each system its own colour, per-source-plane critical curves —
  plus per-system zooms with cluster-scale extents and defaults; reuse `cluster_plots.py`, do not
  write a second cluster plotting layer.
- Audit the galaxy-scale defaults that leak through (extents, marker sizes, zoom half-widths,
  colour maps, `Include2D` critical-curve engines) and give cluster figures sensible defaults;
  update existing tools rather than adding bespoke copies where a parameter suffices.
- Absorb the two unfiled PyAutoLens#577 follow-ups: caustic × source-position overlay and
  `Include2D`-level integration.
- `config/visualize/plots.yaml` entries for the new figures; `autolens_workspace/scripts/cluster/plot.py`
  Visualizer section updated; integration test in `autolens_workspace_test` on a two-source-plane
  cluster fixture asserting the cluster-wide figure is written.
- Depends only on arc phase 3 (critical-curve engine dispatch, shipped 3a/3b 2026-10-02/04). It is
  a new child of the arc, NOT phase 8 (phase 8 is magnification maps only).

## Out of scope

- The oracle-verification figure of Pulse campaign `cluster-pointsolver` phase 1
  (autolens_profiling#436) — that is a measurement artefact and stays in autolens_profiling.
- Magnification maps (arc phase 8). Rendering/registration on the Eyes board (separate prompt:
  Eyes cluster visualization group).

## Acceptance

- A cluster fit on `dataset/cluster/simple` and the A2744 example writes the cluster-wide fit
  figure and per-system zooms; figures reviewed by the human (then via the Eyes loop) as legible
  at cluster scale.

<!-- formalised by the Intake (Conception) Agent on 2026-10-18 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/9383279d-b99b-40f7-90a8-9bab7d97d964/scratchpad/intake_cluster_fit_visualizer.md -->
