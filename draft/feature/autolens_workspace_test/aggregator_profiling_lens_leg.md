# Aggregator profiling — lens-level leg (Phase C)

Type: feature
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase C of the aggregator profiling task (PyAutoFit#1375, phases A+B merged 2026-07-16
as PyAutoFit#1376 + autofit_workspace_test#48). Deferred at ship time because
autolens_workspace_test was claimed by the viz-render-gallery task.

Extend the aggregator profiling harness (autofit_workspace_test
`scripts/profiling/aggregator/` — mirror its structure) with lens-level profiling in
@autolens_workspace_test:

- Mock lens results (tracer/galaxies/fit outputs) or reuse `_quick_fit`-style cheap
  fits so no real modeling runs.
- Time the lens loading pathways: `TracerAgg`, `ImagingAgg`/`FitImagingAgg`
  reconstruction costs, and the workflow catalogue makers mirrored from
  `autolens_workspace/scripts/guides/results/workflow/` (csv_make/fits_make/png_make
  patterns).
- Same conventions as Phase A: outputs under `output/` (gitignored), tiny cell under
  PYAUTO_TEST_MODE, not in smoke_tests.txt.

Baseline findings to build on: samples-per-result dominates generic loading;
AggregateCSV scales with model complexity; lens-specific question is what
FitImagingAgg reconstruction adds on top.
