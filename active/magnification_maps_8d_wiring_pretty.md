# Magnification maps 8d: wire into fit subplots and make them pretty

Type: feature
Target: PyAutoLens
Repos:
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
Themes:
- visualization
- cluster
Epic: cluster-strong-lensing
Phase: 8d
Parent: draft/feature/autolens/magnification_maps_visualization.md
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: no
Filed: 2026-11-02
Issued: 2026-11-02
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/818

## Context

Slice of phase 8. Replace the linear 9th Magnification panel of fit_imaging / fit_interferometer `subplot_fit` with
the 8a style where it earns its place; then the human's "make them pretty" pass via /eyes over the 8a–8c figures.
Witness: /eyes review accepted by the human.

## Original request (human, 2026-11-02)

> prm and then do 8d
> go

## Approved plan (2026-11-02)

1. One colour convention: every magnification map uses a log colour scale on |mu| with colour-bar ticks in mu
   (1, 10, 100), matching the mesh map; the 8c uncertainty map stays linear (it is a fraction). PyAutoArray:
   `plot_array` auto-adds log-spaced contours for log plots with no way to turn them off — add one, so only the
   fixed-mu contours are drawn.
2. Replace the linear-scale Magnification panel of `subplot_tracer` (panel 8), imaging `subplot_fit` and
   interferometer `subplot_fit` (PyAutoLens) with the 8a map drawn into the panel's axes; check contour labels are
   legible at panel size.
3. "Make them pretty" pass: render every phase-8 figure on imaging, multi_galaxy and group examples to
   Science/scratch/arc_phase8d_figures/ and review with the human via /eyes (colour maps, contour styling and label
   size, critical-curve / caustic colours, titles); apply critiques in this branch.
4. autolens_visualization re-renders its gallery after the release — no PR now.
