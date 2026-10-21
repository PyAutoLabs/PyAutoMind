# Cluster-scale point-source figures: dedicated pass

Consequence: judge
Autonomy: human-required
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
