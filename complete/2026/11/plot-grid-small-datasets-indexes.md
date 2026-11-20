`plot_grid(indexes=...)` raised `IndexError` when a highlighted index lay outside the grid. HowToLens `chapter_1_introduction/tutorial_2_ray_tracing.py` picks indexes for its 101x101 grid, and `PYAUTO_SMALL_DATASETS=1` caps that grid to 256 points, so the tutorial crashed under small datasets.

Shipped in PyAutoArray#706 (merged 0f4e8a0f, 2026-11-20, human /prm after the shift 2026-11-20-am review): `plot_grid` now drops out-of-range indexes and logs one INFO line with the count; a group with nothing left is skipped and each surviving group keeps its colour. Boolean-mask index groups are kept as masks (`flatnonzero`), a decision taken by the worker against the plan's int conversion after the independent review flagged the dtype.

Witness: `test_autoarray/plot` 72 passed (the new `test_grid.py` fails 2/3 on main); `tutorial_2_ray_tracing.py` exits 0 under small and full datasets (exit 1 on main under small). Targeted smoke 7/7 (autogalaxy 2, autolens 5). Issue PyAutoArray#705 closed.

## Original prompt

# plot_grid IndexError under small datasets

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- HowToLens
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: HowToLens scripts/chapter_1_introduction/tutorial_2_ray_tracing.py exits 0 with PYAUTO_SMALL_DATASETS=1 (and still exits 0 without it).
Review-minutes: 3
Unattended: ready
Verified: 2026-11-20 47758380 (HowToLens), e398b808 (PyAutoArray)
Lane: local-dev

@HowToLens `scripts/chapter_1_introduction/tutorial_2_ray_tracing.py` fails under `PYAUTO_SMALL_DATASETS=1`:

```
File ".../HowToLens/scripts/chapter_1_introduction/tutorial_2_ray_tracing.py", line 489, in <module>
    aplt.plot_grid(grid=image_plane_grid, ... extent=(-5.5, 5.5, -5.5, 5.5))
File ".../PyAutoArray/autoarray/plot/grid.py", line 175, in plot_grid
    grid[idx_list, 1],
IndexError: index 5118 is out of bounds for axis 0 with size 256
```

Likely cause: small-datasets mode caps the grid to 256 points while @PyAutoArray `plot_grid` indexes with `idx_list` values computed for the full-size grid. Fix belongs in the library (guard or recompute the indexes when the grid is capped), not in the tutorial.

Pre-existing: reproduced on HowToLens `main` without any change (2026-11-17); the script runs cleanly without `PYAUTO_SMALL_DATASETS`. The script is on no HowToLens smoke list, so CI does not catch it — consider adding it once fixed.

Found while shipping autolens_workspace#677 / HowToLens#136 (redshift-angles-guide).

<!-- formalised by the Intake (Conception) Agent on 2026-11-17 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/7aa77bdb-c157-49b3-bbd7-6f49b392c568/scratchpad/plot_grid_bug.md -->
