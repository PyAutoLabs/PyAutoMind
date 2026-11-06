## cti-api-rst-rewrite
- issue: https://github.com/PyAutoLabs/PyAutoCTI/issues/123
- completed: 2026-11-06
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/124
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/324

Merged 2026-11-06 by glance-tier auto-merge (plan approved by the human; Heart STALE human-acknowledged). Issue PyAutoCTI#123 closed. cti-upkeep phase 5c.

- `docs/api/plot.rst` was rewritten for the functional `autocti.plot` API (the style of PyAutoFit's plot.rst): Dataset 1D, Charge Injection Imaging, General, Non-linear Search (autofit re-exports), Figure Output, Visualization During a Fit (`PlotterDataset1D`, `PlotterImagingCI`).
- `data.rst` re-export-or-remove call: REMOVE (human-approved plan). The Grid2D/Grid2DIrregular/Grid1D entries and the grid prose were dropped; `LayoutDataset1D` → `Layout1D`; `SettingsDataset1D` dropped (doesn't exist). The PySwarms entries in modeling.rst had already gone.
- PyAutoHeart `skills/audit_docs/SKILL.md` covers PyAutoCTI (four repos).

Evidence: import+hasattr audit 84 entries / 53 dead → 64 / 0. Local sphinx-build (a scratch venv on PyAuto313 + docs requirements; a venv-on-venv needs a .pth to PyAuto313's site-packages or it picks up the system numpy): 159 warnings (53 on api/) → 53 (0 on api/). test_autocti 279 passed (serial), Heart 1313 passed, CI green.

For phase 3c: docs/conf.py clones PyAutoFit/PyAutoArray from the old rhayes777/Jammy2211 URLs at build time and puts them on sys.path (needs pyprojroot); docs/requirements.txt pins autonerves==2024.11.6.1 and arcticpy==2.6. RTD installs `.[docs]` via .readthedocs.yaml plus an arcticpy post_install.

## Original prompt

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
Consequence: glance
Witness: Every autosummary entry under `PyAutoCTI/docs/api/` imports and `hasattr`-resolves against the installed `autocti` (the `/audit_docs` sweep reports 0 dead, was 55 of 89), `plot.rst` documents the function-style `autocti.plot` exports, the `data.rst` re-export-or-remove call is recorded, and `PyAutoHeart/skills/audit_docs/SKILL.md` lists PyAutoCTI.
Review-minutes: 3
Unattended: ready
Epic: cti-upkeep
Phase: 5
Filed: 2026-08-06 (backfilled from git)
Issued: 2026-11-06

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
