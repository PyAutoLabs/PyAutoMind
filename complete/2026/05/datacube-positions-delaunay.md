## datacube-positions-delaunay
- issue: none — direct followup to autolens_workspace#120
- completed: 2026-05-05
- workspace-prs:
  - https://github.com/PyAutoLabs/autolens_workspace/pull/123 (delaunay.py + RectangularAdaptDensity + positions + PositionsLH)
  - https://github.com/PyAutoLabs/autolens_workspace_developer/pull/48 (mesh swap in likelihood_function.py)
- repos: autolens_workspace, autolens_workspace_developer
- notes: Three datacube follow-ups on top of PR #122. (1) Mesh swap RectangularUniform → RectangularAdaptDensity (modeling, start_here, dev likelihood walkthrough). (2) New delaunay.py sibling using `Overlay` image-mesh, `append_with_circle_edge_points` edge zeroing, `ConstantSplit` regularization, with `AdaptImages` paired with the source galaxy. (3) `PointSolver` positions block in simulator.py writes `positions.json`; all four modeling scripts load it and pass `PositionsLH(threshold=0.3)` to every per-channel `AnalysisInterferometer`. PositionsLH is essentially required for pixelized fits — without it the search routinely converges on demagnified-source local maxima.
