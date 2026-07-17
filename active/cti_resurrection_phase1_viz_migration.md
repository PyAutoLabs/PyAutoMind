# CTI resurrection — Phase 1: Plotter → matplotlib visualization migration

Type: feature
Target: PyAutoCTI
Repos:
- @PyAutoCTI
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 1 of the CTI resurrection epic (Phase 0: PyAutoCTI#82 / PR #83, merged
2026-07-17). Rewrite PyAutoCTI's quarantined visualization layer — which still
targets the autoarray Plotter/MatPlot/Visuals/Include object API removed from
the stack — onto the **matplotlib function API** used by PyAutoGalaxy/PyAutoLens
(module-level `subplot_*` / plot functions built on `autoarray.plot.utils`,
plus slim `af.Visualizer` classes driving them during fits).

## Scope

1. **Delete the Plotter object stack**: `autocti/plot/abstract_plotters.py`,
   `autocti/plot/get_visuals/`, the 5 Plotter classes
   (`dataset_1d/plot/{dataset_1d_plotters,fit_plotters}.py`,
   `charge_injection/plot/{imaging_ci_plotters,fit_ci_plotters}.py`) and the 3
   PlotterInterface classes (`model/plotter_interface.py`,
   `dataset_1d/model/plotter_interface.py`,
   `charge_injection/model/plotter_interface.py`).
2. **Function modules per domain**, mirroring PyAutoGalaxy's
   `imaging/plot/fit_imaging_plots.py` shape:
   - `dataset_1d/plot/dataset_1d_plots.py` — dataset figures/subplot (data,
     noise map, pre-CTI data, S/N) as 1D line plots.
   - `dataset_1d/plot/fit_plots.py` — fit figures/subplot (data/model/
     residuals/normalized residuals/chi-squared) + region variants.
   - `charge_injection/plot/imaging_ci_plots.py` — 2D dataset figures/subplot
     + 1D binned region plots (parallel/serial FPR + EPER).
   - `charge_injection/plot/fit_ci_plots.py` — 2D fit figures/subplot + 1D
     binned region fit plots.
   - CTI-specific **region overlays** (parallel/serial overscan, serial
     prescan, FPR/EPER extract regions — formerly autoarray `wrap` objects
     `ParallelOverscanPlot`/`SerialOverscanPlot`/`SerialPrescanPlot`) become
     CTI-local matplotlib helpers in `autocti/util/plot_utils.py` (analogue of
     `autogalaxy/util/plot_utils.py`).
3. **Rebuild `autocti/plot/__init__.py`** as the function-API namespace
   (`aplt.subplot_dataset_1d`, `aplt.subplot_imaging_ci`, …) re-exporting the
   relevant autofit search plots and autoarray plot functions as ag does;
   restore `from . import plot` in `autocti/__init__.py`.
4. **Rewire the visualizers**: both `model/visualizer.py` classes call the new
   functions directly per `config/visualize/plots.yaml` keys (remove the
   Phase-0 try/except-ImportError quarantine); align the plots.yaml schema
   with current PyAutoGalaxy where keys overlap.
5. **Tests**: replace the quarantined plot tests (`test_autocti/plot/`,
   `test_autocti/*/plot/`, `test_autocti/*/model/test_plotter_interface_*.py`)
   with tests of the new function modules + visualizers in the current
   PyAutoGalaxy test style (plot_patch / output-file assertions); remove the
   `collect_ignore` quarantine from `test_autocti/conftest.py`.

## Out of scope

Aggregator factor-graph port (5 skipped tests — Phase 2), CI workflows and
ecosystem plumbing (Phase 3), autocti_workspace scripts/notebooks (Phase 4).

## Context

- Phase-0 record: `PyAutoMind/complete/2026/07/cti-resurrection-phase0.md`
  (traps: worktree.sh lacks CTI on PYTHONPATH — prepend manually).
- Target-pattern references: `autogalaxy/imaging/plot/fit_imaging_plots.py`,
  `autogalaxy/util/plot_utils.py`, `autogalaxy/imaging/model/visualizer.py`,
  `autoarray/plot/utils.py`, `autoarray/structures/plot/structure_plots.py`
  (`plot_array_2d`, `plot_yx_1d`).
- The old Plotter classes define the figure inventory to reproduce; read them
  before deleting (git history preserves them after).
