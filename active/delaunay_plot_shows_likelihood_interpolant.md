# Delaunay source plots: show the piecewise-linear interpolant the likelihood uses

Type: feature
Target: autoarray
Repos:
- PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: medium
Consequence: judge
Community: https://github.com/PyAutoLabs/.github/discussions/46
Filed: 2026-11-17
Issued: 2026-11-17

From @Lasloruhberg on hub #46 (Bugs & Errors, 2026-11-13, with a minimal script and figure).

## What

`autoarray/plot/inversion.py` `_plot_delaunay` draws Delaunay/KNN reconstructions with
`ax.tripcolor` default *flat* shading: one colour per triangle (mean of its vertices). Its
docstring now justifies this (the area integral per triangle equals the linear interpolant's),
but the figure is blocky and is not the reconstruction the likelihood uses between vertices.
The reporter's example: a perfect source (true Sersic at the mesh vertices) is visibly
misrepresented by the plot.

Design decided by the human on 2026-11-17 (and promised to the reporter on #46,
https://github.com/PyAutoLabs/.github/discussions/46#discussioncomment-19681331):

- **Keep flat-shaded triangles as the default** source plot. They show how much resolution the
  mesh spends where: small triangles mean fine structure is being resolved, which an
  interpolated image hides. Fix the docstring/tutorial wording so it says this plainly.
- **Add the interpolated view** (reporter's method: evaluate the mapper's own interpolator on a
  uniform plotting grid over the source extent, via a fresh interpolator of the same type,
  `mesh` and `mesh_grid`, with `data_grid` = the plot grid, then `imshow`), so the figure is
  exactly the barycentric interpolant the likelihood uses.
- **`inversion_#.png`**: the interpolated reconstruction always appears as an extra panel.
- **`fit.png`**: a visualization-config switch, **off by default**, to show the interpolated
  panel as well.
- Mind cost for big meshes (default grid ~400x400, configurable), KNN mappers (their own
  interpolant) and log colour scales.

## Witness

The reporter's minimal example (true Sersic on a Hilbert-Delaunay mesh) shows the plot matching
the interpolant, and the autolens_visualization / autogalaxy_visualization Delaunay figures are
re-rendered and look right.
