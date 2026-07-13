## cache-fit-properties
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/340
- completed: 2026-05-27
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/341, https://github.com/PyAutoLabs/PyAutoGalaxy/pull/462, https://github.com/PyAutoLabs/PyAutoLens/pull/548
- repos: PyAutoArray, PyAutoGalaxy, PyAutoLens
- notes: Changed 38 @property to @functools.cached_property on FitDataset/FitImaging/FitInterferometer. Eliminates redundant recomputation cascades (model_data was recomputed 2-3x per visualization pass at 5-20s each for Delaunay inversions). Safe because Fit objects are immutable after construction. 2072 tests pass.
