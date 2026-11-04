Arc phase 8a: image-plane magnification map. `plot_magnification_2d(mass_obj, grid, ...)` plots log10 |mu| for any
mass object (Galaxy, Galaxies, Tracer) with a 1st/99th-percentile colour range, labelled contours of constant |mu|
(default 2, 5, 10, 20, 50, 100; out-of-range levels skipped) and an optional critical-curve overlay, as in LEGGOS II
figure 4. Exported as `aplt.plot_magnification_2d`; shown in `imaging/source_science.py` (`__Magnification Map__`) and
`guides/lens_calc.py`.

Shipped (merged 2026-11-02, human /prm "prm when green"):
- PyAutoGalaxy#690 (`467a5ed7`) — function + tests (test_autogalaxy 1469 passed)
- PyAutoLens#815 (`ef7f5733`) — aplt export + two/three-plane tracer tests (test_autolens 1018 passed, 1 xfailed)
- autolens_workspace#614 (`6567940d`) — scripts + navigator catalogue

Scope note: the planned PyAutoArray `contour_levels` option was dropped (repo claimed by
rectangular-gradient-rtu-sparse); the contours are drawn on the axes `plot_array` already accepts.
For a multi-plane tracer the map is the magnification of a source in the last plane (no plane_j option yet).


## Original prompt

# Magnification maps 8a: image-plane log|mu| map with constant-mu contours and critical curves

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace
Themes:
- visualization
- cluster
Epic: cluster-strong-lensing
Phase: 8a
Parent: draft/feature/autolens/magnification_maps_visualization.md
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: no
Filed: 2026-11-02
Issued: 2026-11-02
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/689

## Original request (human, 2026-11-02)

> yes go ahead with 8a

(Slice of phase 8 `magnification_maps_visualization.md`, sliced 8a→8d after a 2026-11-02 re-audit.)

## Re-audit (2026-11-02)

- The image-plane magnification is only the 9th panel of `subplot_fit` in `fit_imaging_plots.py` (~l.730/789) and
  `fit_interferometer_plots.py` (~l.612/685), on a LINEAR colour scale; no standalone plot function; no aplt export.
- `plot_array(contours=int)` (autoarray/plot/array.py, `_apply_contours` in autoarray/plot/utils.py:849) takes a level
  COUNT only — no explicit mu levels.
- Critical curves: `_critical_curves_from(mass_obj, grid)` in autogalaxy/util/plot_utils.py:492.
- `guides/lens_calc.py` (~l.318) plots magnification manually with `aplt.plot_array`.

## Work

1. (Dropped 2026-11-02: PyAutoArray is claimed by rectangular-gradient-rtu-sparse; no PyAutoArray change —
   `plot_array` takes `ax`, so the explicit-level contours are drawn on that axes inside the PyAutoGalaxy function.)
2. PyAutoGalaxy: `plot_magnification_2d(mass_obj, grid, ...)` — log10|mu| image-plane map, colour range capped near the
   critical lines, constant-mu contours (default 2, 5, 10, 20, 50, 100), optional critical-curve overlay; works for any
   mass object (Galaxies, Tracer); exported from `autogalaxy.plot`. Unit tests.
3. PyAutoLens: export via `aplt`; Tracer test (incl. multi-plane).
4. autolens_workspace: use it in `guides/lens_calc.py` and `imaging/source_science.py`; regenerate the navigator
   catalogue (`regenerate_navigator.py autolens`); smoke.

Witness: `aplt.plot_magnification_2d(tracer, grid)` renders log|mu| with labelled constant-mu contours and critical
curves for the imaging `simple__no_lens_light` lens and a multi_galaxy lens; library tests pass; workspace scripts
smoke clean.
