# Eyes cluster visualization group: render every cluster/point-source figure for PyAutoEyes

Type: feature
Target: autolens_visualization
Repos:
- PyAutoLens
- autolens_profiling
- autolens_visualization
- PyAutoEyes
Difficulty: large
Autonomy: supervised
Priority: high
Memory: reading-queue.md; wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/cosmos-survey.md
Status: formalised
Consequence: judge
Witness: gallery_run.sh renders the cluster group and gallery_build.py validates viz_manifest.yaml with at least one cluster/ row (CI green)
Review-minutes: 25
Unattended: needs-slicing

## Original user request (verbatim, Pulse cluster-pointsolver chat, 2026-10-18)

> Feels like we maybe should intake PyAutoEyes cluster visualization and pair it to this as the modeling result visualisation

> Ok do it ans then begin whatever work which gets us to the point we can check the oracle results visually, see that image on Eyes but the image of the oracle itself isnt on eyes but I guess just autolens profiling or wherever rsuits

## Problem

`autolens_visualization/gallery/viz_manifest.yaml` holds 40 figures, all under `imaging/`,
`interferometer/` and `misc/`. There are zero cluster or point-source rows, so PyAutoEyes cannot
show cluster modelling figures and the Eyes conductor has never judged the cluster plotting
package or the point-source fit figures. The human expects galaxy-scale defaults to look wrong at
cluster scale; the Eyes review loop is where that gets caught and routed back as critiques.

## Scope

- Add a `cluster/` group (and a `point_source/` group if the harness keeps dataset types apart)
  to `autolens_visualization`: producers + harness entries rendering every cluster/point-source
  visualizer output on `dataset/cluster/simple` (auto-simulated) and the workspace A2744 CSVs:
  per-system dataset positions, positions overlay, image-group zooms, cluster dataset subplot,
  per-source-plane critical curves and caustics, and the `FitPoint` figures from a short modelling
  run. Once the cluster fit visualizer prompt lands, add its cluster-wide fit figure and zooms.
- Register every PNG in `gallery/viz_manifest.yaml` under the existing read contract so PyAutoEyes
  ingests them with no Eyes-side change beyond a re-render; keep the re-render-each-release flow.
- Pairs with Pulse campaign `cluster-pointsolver` (autolens_profiling#436) as the modelling-result
  visualization surface. The campaign's oracle-verification figure is NOT part of Eyes; it stays
  in autolens_profiling.

## Out of scope

- Judging the figures (Eyes conductor), editing plot code (routes to a PyAutoLens prompt),
  PyAutoEyes registry/contract changes.

## Acceptance

- `gallery_run.sh` renders the group; `viz_manifest.yaml` validates; the Eyes board shows the
  cluster figures after its next render; the human reviews them through `/eyes`.

<!-- formalised by the Intake (Conception) Agent on 2026-10-18 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/9383279d-b99b-40f7-90a8-9bab7d97d964/scratchpad/intake_eyes_cluster_group.md -->
