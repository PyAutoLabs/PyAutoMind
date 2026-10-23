Shipped the cluster-scale (multi-source) point-source figures from the approved v4 prototypes. There is one visual language for one or many sources. Each source's critical curves are drawn at its own redshift. Every figure is in `plots.yaml` and is written during a real `search.fit`, including the all-sources figures of a factor-graph (cluster) fit.

**Figures**
- `dataset_point.png` "Dataset Positions": source 0 is a black ●; further sources get colour + marker shape (colour by redshift with a colourbar beyond 8); `i` / `k·i` labels; no curves.
- `fit.png` "Fit Positions":
  - red ✕ at the true model positions, with true-length residual lines (solid hard / dashed soft pairing);
  - per-source own-redshift curves; σ on the legend entries for 2–8 sources;
  - `−2 ln L` for PairAll;
  - legend in the emptiest corner (one source) or outside the panel (several).
  - The source-plane panel moved to `fit_per_image.png`.
- `fit_per_image.png` (new): one row per source, "Residuals / IP / SP (point_k, z = …)":
  - square panels and no legends;
  - a shared linear ranking range with off-scale ▸ values;
  - one file per source beyond 8.
- `image_with_points.png` / `fit_image_with_points.png`: every source in the same symbols, with `k·i` labels.
- Critical curves and caustics are darker and thicker everywhere.

**Code**
- New `autolens.point.plot.point_sources` and `multi_source_plots`.
- `curves_for_planes` evaluates the FULL tracer's deflection field once and contours λt/λr = 0. This replaces the ~2 min/dataset LensCalc path on the 15-galaxy cluster.
- `PlotterPoint` / `VisualizerPoint` gain the combined figures.
- New `plots.yaml` keys, all on by default.
- Tests: test_autolens 925 passed (14 new). Real `search.fit` test-mode runs on point_source and on a 2-source cluster FactorGraph wrote every configured PNG.

Absorbs `draft/bug/autolens/point_fit_critical_curves_ignore_source_redshift.md` (record `complete/2026/10/point-fit-critical-curves-ignore-source-redshift.md`).

Merged 2026-10-22 via a human /prm (judge tier), in library-first order: PyAutoLens#794 → autolens_visualization#14 (lint green on rerun against the merged library main) / autolens_workspace#594 / autolens_workspace_test#347. Issue PyAutoLens#793 closed. PyAutoEyes `dashboard_refresh.yml` dispatched (run 39752061558).


**Not shipped (re-filed)**
- Cluster `point_solver.png` refinement-panel readability, and labelling for >10 images on the solver figure: `draft/feature/autolens/cluster_point_solver_refinement_readability.md`.
- HowToLens and autolens_assistant `plots.yaml` point keys are still stale: `draft/docs/autolens/point_plots_yaml_keys_howtolens_assistant.md`.

## Original prompt

# Cluster-scale point-source figures: dedicated pass

Consequence: judge
Autonomy: human-required
Issued: 2026-10-21
builds-on: complete/2026/10/point-solver-refinement-figure.md (PyAutoLens#788 / autolens_visualization#12) and complete/2026/10/point-dataset-positions-panel.md

@PyAutoLens @autolens_visualization

## Request (human, 2026-10-21)

> we will follow up with more dediciated work on cluster images next.

## Known issues to start from (2026-10-21)

- **Unreadable refinement panels.** The cluster `point_solver.png` panels for steps 1, 2 and final are only ▲ markers at the ~±40″ extent, and step 0 is a grey shade (369,937 triangles).
- **Label layout.** Image numbering and rejected-candidate labels at cluster scale needed a placement fix before #788 merged. The labelling has no plan for many images (>10 images → no numbers).
- **Multi-plane critical curves.** The curves ignore each point's source redshift: see `draft/bug/autolens/point_fit_critical_curves_ignore_source_redshift.md`.
- **Render cost.** The cluster producer takes about 4.5 min since the curves are computed (#786).

## Intent

Survey every cluster point-source figure (`dataset.png`, `fit.png`, `point_solver.png`, and the cluster-wide figures) with the human via /eyes. Decide the cluster-specific conventions: per-image zoom insets, labelling of many images, per-plane curves, and extent. Then run /start_dev for the agreed changes.

## Also fold in (2026-10-21)

The Fit Positions legend auto-placement for FitPositionsImagePairAll lands mid-panel over the mass centre, because of the longer "Residual (nearest, soft pairing)" label. Place it in the emptiest corner, like the source-plane panel. See `complete/2026/10/point-fit-source-plane-panel.md`.

## Human direction (2026-10-21, verbatim)

> For point osurces:
> - I think the currently plot files (dataset.png, fit.png) should show all points in one image, this wont be clutttered if the figsize of the image is chosen carefully. Each point should be labeled a different color, I wouldnt include this in th elegend unless its concise as for clusters we may have hundreds of multiple image groups, seeing them all in one place is good.
> - However, the above images will make it hard to judge how good the fit to each image is, as they will be cluttered and spotting the pairs with the larger sepration would take a lot of eye balling. I think we need a new subplot (fit_per_image.png?) which for each row corresponds to a given source (e.g. point_0) and then for each panel shows the dataset point of one image (not all multiple images from one source but literally one image), its corresponding paired model image with the dashed line, and probably the residual distance in the title or on te plot. This would then be shown for all images, so a reader can almost "read off" where the biggest mismatches are and trace that bck to the original image. However, think hard if there is a better way to get this detailed information across, I think we want two images the global "everything" image and detailed image by image visual. This image by image will also need to protray unpaired predicted images and what happens tot hem/
>
> I think that for the above, for clusters where all sorce planes are at different redshifts just further illustrates how important it is, and also means we need to factor in different caustics at redshifts correctly if we are not already.

## Proposed design (session, 2026-10-21; prototyping before approval)

- **Global `dataset.png` / `fit.png`:**
  - all point datasets in one panel, one colour per source;
  - each source's critical curve drawn in its colour, at its own source redshift (absorbs `draft/bug/autolens/point_fit_critical_curves_ignore_source_redshift.md`);
  - the legend shows symbols only; source colours enter it only when there are ≤ ~8 sources.
- **`fit_per_image.png`:** one row per source.
  - Column 1 is that source's source-plane panel (fit-class-paired, as #790).
  - Then one fixed-physical-scale zoom panel per observed image: observed dot + σ circle, paired model ✕, residual line (dashed for soft pairing).
  - Title `point_k · i  Δ = X mas (Yσ)`, numbered as in the global figure.
  - End of row: "unmatched model image" panels (hollow grey ✕, μ) and "no model image" panels.
- **Residual ranking strip:** a sorted dot plot of Δ/σ for every image, coloured by source and labelled `point_k · i`. It goes at the top of `fit_per_image.png` when there are few sources, or in `fit_residual_ranking.png` for clusters.
- **Cluster scaling:** above ~10 sources, `fit_per_image/` becomes one file per source; the ranking strip is the index.
- **Also:** PairAll legend placement in the emptiest corner (from #790).

## Human decisions (2026-10-21, after per-image prototype round 1)

- **`dataset.png`:** ONE function/concept, evolved from the left panel of the current point_source `fit.png`: black filled dots, σ in legend, arcsec ticks, solver extent. Never any critical curves on a dataset figure. Multiple sources get colour + marker shape, with `k·i` labels.
- **Global `fit.png`:** residual arrows (quiver), one shared exaggeration factor with a scale key, per-source own-redshift curves in the source's colour. More than 8 sources: colour by redshift with a colourbar and label identity. Solver-grid extent. The synthetic many-source formatting needs tidying.
- **`fit_per_image.png`:** the per-image zoom panels are DROPPED, because without image-plane context they carry too little information. One row per source, three panels:
  1. that source's residual ranking;
  2. an image-plane panel zoomed to that source's images, with residual arrows sharing one factor across rows;
  3. the source-plane panel.
  The ranking axis is linear Δ/σ (per-image χ for source-plane fits), with ONE shared range across rows, clipped at a robust max and off-scale values printed. Panels 1 and 2 are linked by image numbers. Many sources → one file per source.
- **Source-plane fits:** the per-image presentation uses that fit's own source-plane χ (fit-class pairing).

**Findings from round 1, for the build:**
- Per-plane curves via a single deflection-field evaluation plus contouring of λt=0 / λr=0 take 0.2 s (2 planes) and 1.8 s (24 planes), versus ~17 s per plane per curve type with LensCalc. They agree to within 0.05″ median.
- Curves, μ and solves must use the FULL multi-source tracer, because deflections are normalised to the last plane.

Round-2 prototypes: `per_image_prototype/*/{dataset_v2,fit_v2,fit_per_image_v2}.png`.

## Human feedback round 2 → round 3 (2026-10-21)

- **`fit_per_image`:** liked. All 3 panels square and the same aspect. Ticks styled like other PyAutoLens figures. Redshift in the row titles. (Session addition: source-plane dots use the same per-image colours as panels 1–2.)
- **Global `fit`:** still hard to see the data, the pairing and the model. Make the observed position, the model position and the pairing clearly readable; the 200 mas key arrow is barely visible. Variants are in round 3.
- **NEW:** a cluster image-with-points analogue (imaging data plus all sources' positions) and a fit version.
- **Unify symbols** between single-source `dataset.png` and multi-source `dataset_v2`: one function and one visual language. Single source stays the black-dot look.
- **Agreed answers from round 2:**
  - The shared ranking range is computed where all sources are visible (the same place as the global fit); a lone source uses its own range.
  - Accept per-panel arrow keys.
  - Colours mean image within rows and source globally.
  - "Residual / σ" label is OK.
  - The merged dataset figure is titled "Dataset Positions".

## Human feedback round 3 → round 4 (2026-10-21)

- **Curves:** critical curves and caustics are too faint everywhere; draw them darker and/or thicker.
- **`fit_per_image` titles:** too long with the redshift. Use "IP (point_k, z = …)" and "SP (point_k, z = …)".
- **Global fit:** REMOVE the exaggerated residual arrows and the ×F / "200 mas offset" key. Keep the red ✕ at the true model positions with true-length residual lines to the data; judge the fit by eye. The same applies to the `fit_per_image` IP panel.
- **Global fit `_with_points` variant** over the imaging, with identical symbols.
- **Session-agreed:**
  - variant (a) base;
  - smaller ✕ beyond 8 sources;
  - add a cluster imaging simulator plus a tracked FITS to autolens_visualization;
  - accept per-panel scales;
  - source 0 black on white panels and white on images;
  - library title/tick font sizes for the many-source case;
  - σ on per-source legend entries (no generic grey entry).

## FINAL design approval (human, 2026-10-21, after round 4)

"Images are good so I'm happy to start dev and do the task."

**Reference.** The v4 prototypes in `/mnt/c/Users/Jammy/Science/scratch/eyes/autolens/per_image_prototype/` are the approved look. The producer is `producer/figures_v4.py` and `run_v4.py`, with helpers from earlier rounds. Main files use the true model; `*_v4_perturbed.png` are demos only.

**Decisions:**
- `dataset.png` is one unified function: black ● for source 0, then colour + shape; `k·i` labels; no curves.
- Global `fit.png`:
  - red ✕ at the true model positions, with true-length residual lines (solid hard / dashed soft);
  - NO exaggerated arrows or keys;
  - per-source own-z curves, darker and thicker;
  - σ on the per-source legend entries (2–8 sources);
  - colour-by-z with a colourbar beyond 8 sources;
  - a smaller ✕ beyond 8 sources;
  - the solver extent.
- `fit_per_image.png`:
  - one row per source: "Residuals / IP / SP (point_k, z = …)";
  - square, equal-size panels with library ticks and fonts;
  - NO legends;
  - the ranking has σ values printed right of the dots, no x axis, unlabelled 1σ/3σ lines, a linear shared range clipped at a robust max, and off-scale ▸ values;
  - per-image colours shared across all three panels.
  - The shared range is computed where all sources are visible; a lone source uses its own range. Many sources → one file per source.
- `image_with_points.png` and `fit_image_with_points.png`: every source, the same symbols, `k·i` labels kept, NO legends.
- Mixture fits (PairAll classes): the legend shows `−2 ln L = …` instead of `χ² = …`.
- Source-plane fits rank by the fit's OWN per-image χ (not jacobian). The weighting default changed to jacobian in PyAutoLens#792 (record `complete/2026/10/positions-source-jacobian-default.md`, pending release).
- Darker and thicker critical curves and caustics everywhere, including the library SP panel and its inset.

**Also in scope:**
- Per-source critical curves at their own redshift (absorbs `draft/bug/autolens/point_fit_critical_curves_ignore_source_redshift.md`), via the fast single-deflection-field contour method.
- Curves, μ and solves must use the FULL tracer.
- The PairAll legend-placement fix.
- A cluster imaging simulator plus a tracked FITS in autolens_visualization.

## Human addition (2026-10-21): config + modelling output + Eyes

> make sure all this visualization work is also sorted in terms of config files so theyoutput in lens model fits and it all updates the PyAutoEyes dashboard

Scope:
1. **PyAutoLens `autolens/config/visualize/plots.yaml`.** Add an entry (with a comment, matching the existing style) for every figure this task adds or changes:
   - unified `dataset.png`;
   - global `fit.png`;
   - `fit_per_image.png`;
   - multi-source `image_with_points.png` / `fit_image_with_points.png`.
   Decide the defaults, e.g. `fit_per_image` on and cheap ones on. Wire each one through `PlotterPoint` / `VisualizerPoint` so the files are written during a real `search.fit`, including the cross-dataset (all sources) figures at the level where every source is visible.
2. **Verify in a real modelling run** (test mode / a short search on the point_source and cluster examples) that every configured PNG lands in the output folder. Don't rely on the viz producers alone.
3. **autolens_workspace `config/visualize/plots.yaml`** is already stale: `fit_point_dataset: {}` lacks `image_with_points`, `fit_image_with_points` and `subplot_point_solver` (#786/#788/#790). Mirror the library keys plus this task's.
   - NOTE: positions-source-jacobian-default closed 2026-10-21 (autolens_workspace#593 merged); autolens_workspace is free.
   - Also check autolens_workspace_test, HowToLens and autolens_assistant configs for point keys.
4. **autolens_visualization `config/visualize/plots.yaml`:** turn on every figure, and make sure the producers' outputs go into `gallery/viz_manifest.yaml` (PNG only; GIFs are tracked alongside).
5. **After the viz PR merges,** dispatch PyAutoEyes `dashboard_refresh.yml` and confirm the new figures appear on the dashboard.
   - Done 2026-10-21 for #786/#788/#790: run 39666522545 green; the point_solver and source-plane figures are listed.
