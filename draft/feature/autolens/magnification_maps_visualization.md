# Magnification maps: image-plane contour maps, source-plane mesh maps, uncertainty maps

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
- PyAutoArray
- PyAutoGalaxy
- autolens_workspace
Themes:
- visualization
- cluster
- pixelization
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Lane: any
Epic: cluster-strong-lensing
Phase: 8
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-08-19 (backfilled from git)

# Magnification maps: image-plane contour maps, source-plane mesh maps, uncertainty maps

Part of the Source & Cluster arc (phase 8 of 12), gated on phases 3-7. User request
(verbatim): "Image plane and source plane Magnification plots? This isn't just clusters.
make sure they are plotted follow up will be to make them pretty. The image plane image
is one where every square shows the magnification of that pixel in the image plane, the
source plane one would mirror a source reconstruction (e.g. delaunay mesh) with
magnification for each mesh pixel. I guess we could make a square pixel one for
something like an MGE source. Leggos figure 4 Magnification Maps we need that! Contour
plot." Plus the closing bullets: "Visualization to go with all of this. Make pretty
visualization for all this source science Magnification stuff."

Audit findings — everything is one call away but nothing is wired:
- Magnification appears ONLY as one panel in three subplots (tracer_plots.py:192/217,
  fit_imaging_plots.py:709/768, fit_interferometer_plots.py:528/595). No aplt export
  contains "magnification"; no standalone plot function exists.
- `aplt.plot_array` already supports `contours=` (autoarray/plot/array.py:45, applied
  :294-299) — the LEGGOS Fig-4-style contour map is one call, but no script/library
  function makes it; the manual pattern sits in guides/lens_calc.py:314-319.
- `plot_mapper(mapper, solution_vector=...)` colors a mesh by arbitrary per-pixel
  values — but no per-mesh-pixel magnification vector exists to pass (phase 4/6 build
  it).

Work:
1. `aplt.plot_magnification` (image-plane μ map, log-friendly color handling around the
   μ→∞ critical lines, optional constant-μ contours + critical-curve overlay from the
   phase-3 dispatcher). Works at galaxy, group, and cluster scale; multi-plane variant
   takes plane_redshift.
2. Source-plane magnification map: mesh reconstruction colored by per-mesh-pixel μ
   (delaunay et al. via plot_mapper), and a square-pixel interpolated variant for
   parametric/MGE sources.
3. LEGGOS Fig-4 twin: fractional-uncertainty map — per-pixel σ_μ/|μ_best| over the
   phase-7 posterior-draw ensemble, with best-fit constant-μ contours overlaid.
4. Wire into source_science.py examples (both tiers) and the standard fit subplots
   where it earns its place; "make them pretty" acceptance pass via /eyes at the end.

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/483da28c-8c96-4c83-ad87-a43448ca2164/scratchpad/source_cluster_phases/phase08_magnification_maps_visualization.md -->

## Sliced 2026-11-02 (human approved; re-audit after phases 4–7)

8a SHIPPED 2026-11-02 (record `complete/2026/11/magnification-maps-image-plane.md`; Galaxy#690, Lens#815, ws#614) → 8b SHIPPED 2026-11-02 (record `complete/2026/11/magnification-maps-source-plane.md`; Array#674, Galaxy#691, Lens#816, ws#615) →
8c SHIPPED 2026-11-02 (record `complete/2026/11/magnification-maps-uncertainty.md`; Galaxy#693, Lens#817, ws#616) → 8d `magnification_maps_8d_wiring_pretty.md`. One at a time via /start_dev.

## Re-scoped 2026-11-05 — what is left (draft-queue sweep)

- **Done:** 8a (PyAutoGalaxy#690, PyAutoLens#815, autolens_workspace#614), 8b (PyAutoArray#674, PyAutoGalaxy#691, PyAutoLens#816), 8c (PyAutoGalaxy#693, PyAutoLens#817, autolens_workspace#616).
- **Remaining:** 8d (wiring + "pretty" pass) only, already issued as `active/magnification_maps_8d_wiring_pretty.md`. Close this draft when 8d ships.

_Evidence from the 2026-11-05 read-only sweep (Mind ledger + GitHub search); remaining items are the live scope of this prompt._
