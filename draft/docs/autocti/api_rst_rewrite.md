# Rewrite PyAutoCTI docs/api — 55 of 89 autosummary entries are dead

Type: docs
Target: PyAutoCTI
Repos:
- PyAutoCTI
Themes:
- docs-hub
- cti
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-06 (backfilled from git)

Filed 2026-08-06 from a full `/audit_docs` sweep (every autosummary entry
verified by import + `hasattr` against installed source). PyAutoCTI's
`docs/api/` is RTD-published but untouched since 2024-09-27; 62% of its
documented symbols don't exist.

- **`docs/api/plot.rst` (49 dead entries)** — the file is an unadapted copy of
  the Lens/Galaxy class-heavy plot-doc template; none of the documented class
  hierarchy (`Array2DPlotter`…`FitImagingCIPlotter`, `MatPlot1D/2D`,
  `Include*`, `Visuals*`, 22 matplotlib-wrapper classes, and the
  `NestPlotter`/`MCMCPlotter`/`MLEPlotter` trio removed from autofit in the
  class→function refactor `bc917452e`) ever existed in CTI
  (`git log -S "class MatPlot2D"` returns nothing). Rewrite from scratch
  against the actual `autocti/plot/__init__.py` exports (function-based
  `plot_array`, `plot_yx`, `subplot_*`, `figure_*` + classes
  `PlotterDataset1D`, `PlotterImagingCI`), following the corrected
  function-style pattern planned for PyAutoFit's `plot.rst`
  (existing draft `docs/libraries/pyautofit_plot_rst_dead_plotters.md` —
  re-confirmed by this audit; ship that one first as the reference).
- **`docs/api/data.rst` (5 dead)** — `Grid2D`, `Grid2DIrregular`, `Grid1D`
  (exist in autoarray but never re-exported by `autocti/__init__.py`) and
  `LayoutDataset1D`/`SettingsDataset1D` (don't exist anywhere; `Layout1D`
  does). Maintainer call: remove the entries or add the re-exports first.
- **`docs/api/modeling.rst` (2 dead)** — `PySwarmsLocal`/`PySwarmsGlobal`,
  removed from autofit in `cc9fd6df4`; drop them.
- `arctic.rst`, `clocking.rst`, `fitting.rst` are clean; Fit/Galaxy/Lens api
  docs are otherwise fully green (447 symbols verified).
- **Process gap:** `PyAutoHeart/skills/audit_docs/SKILL.md`'s repo table omits
  PyAutoCTI even though it has published `docs/api/` — add it so future audits
  don't silently skip the one repo that drifts.
