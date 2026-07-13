## point-source-fit-positions-len
- completed: 2026-05-07
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/132
- repos: autolens_workspace
- notes: |
    Cluster E of the recent release-prep triage. scripts/point_source/fit.py
    crashed with `ValueError: operands could not be broadcast together with
    shapes (2,) (4,)` at autoarray/abstract_ndarray.py:326 under
    PYAUTO_SMALL_DATASETS=1. Root cause: PointSolver.solve() short-circuits
    to a fixed 2-position pair [(1.0,0.0),(0.0,1.0)] when SMALL_DATASETS=1
    (PyAutoLens/autolens/point/solver/point_solver.py:90-91), but the script
    hardcoded a 4-element positions_data and 4-element positions_noise_map.
    FitPositionsImagePairRepeat then divided a 2-element residual by the
    4-element noise_map and broadcasts failed. Same family as PR #119
    (Cluster E: deblending simulator) which fixed
    point_source/features/deblending/simulator.py with a
    range(len(positions)) dict comprehension; PR #119 didn't touch fit.py.
    Mechanical port of PR #119's pattern: replace hardcoded 4-element
    lists with `Grid2DIrregular(positions)` + `[0.005] * len(positions)`.
    Hardcoded values were demonstrative only — they matched solver output
    exactly, so the new code produces an identical demo (zero residuals)
    while adapting to N positions. Prose updated from "we manually
    specify" to describe the new derivation. Verified locally under
    SMALL_DATASETS (2-element residual_map) and full (4-element).
