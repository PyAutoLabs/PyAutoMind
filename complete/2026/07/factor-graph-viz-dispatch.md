## factor-graph-viz-dispatch
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1339
- completed: 2026-07-09
- pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1340 (merged)
- notes: Weak follow-up 3 (--auto, refactor cap = safe effective). FactorGraphModel.visualize_combined + perform_quick_update now group (factor, instance) pairs by the analysis Visualizer class (order preserved) and issue one combined call per group — fixes the producer of the mixed-graph crash PyAutoLens#587 papered over; those filters stay as defence in depth. Homogeneous graphs = single group = byte-identical (tested with stub recording Visualizers; af.mock.MockAnalysis + af.ex.Gaussian is the test-fixture pattern — af.Gaussian does not exist). Base af.Visualizer.visualize_combined is a no-op, so groups whose Visualizer defines nothing (e.g. VisualizerWeak) dispatch safely. Parallel to ep-diagnostics + ep-graphical-docs PyAutoFit claims (disjoint files) — 8th+9th clean parallel-worktree uses.
