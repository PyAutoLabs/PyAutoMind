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
