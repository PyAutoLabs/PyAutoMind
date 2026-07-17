## aggregator-lens-profiling
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/171
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1384 (MERGED)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/172 + https://github.com/PyAutoLabs/autofit_workspace_test/pull/50 (both MERGED)
- summary: Aggregator Phase C (lens leg) + PYAUTO_TEST_MODE_SAMPLES integration. New autolens_workspace_test scripts/profiling/aggregator/ (mock lens results via TEST_MODE=2 bypass fit on al.fixtures; TracerAgg/FitImagingAgg/AggregateCSV timing grid). Both harnesses' templates now written by the canonical bypass generator (Fit#1381) — hand-rolled sample synthesis deleted; --representative cell (10k samples × 18-param, ~9MB SLaM parity) added to both autofit grids.
- BUG FOUND+FIXED (Fit#1384): from_dict "dict" branch dropped entries with falsy values (`if value`) — parameters exactly 0.0 vanished on load. Exposed by bypass output (lens centres/ell_comps have zero prior medians → summaries lost 8/15 params, TracerAgg KeyError). Pre-existing, affected any stored dict with legit zero values. Only None skipped now.
- findings: lens reconstruction flat ~150-280ms/result, deserialization-dominated (TracerAgg/FitImagingAgg add only ~20-60% over the summary load at 7×7 fixture scale). REPRESENTATIVE-SCALE SQLITE UPDATE: full-samples read comparable to directory (150 vs 165 ms/result) — Phase D's "2-10× slower" was measured on smaller/less production-shaped data; sqlite tax that stands = ~0.35s/result build + ~1.7MB/result.
- traps: test-mode env var changes the output path segment — resolve paths.output_path INSIDE the bypass env context; conf.instance.push clobbers with_config decorator overrides (set config keys after the push); alwt output.yaml has samples: false.
- shipped+merged 2026-07-17 through 5-reason pre-existing Heart RED on user ack (ship+merge).

## Original prompt

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
