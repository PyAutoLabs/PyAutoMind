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

From @Lasloruhberg on hub #46 (Bugs & Errors, 2026-11-13, with a minimal script and figure).

## What

`autoarray/plot/inversion.py` `_plot_delaunay` draws Delaunay/KNN reconstructions with
`ax.tripcolor` default *flat* shading: one colour per triangle (mean of its vertices). Its
docstring now justifies this (the area integral per triangle equals the linear interpolant's),
but the figure is blocky and is not the reconstruction the likelihood uses between vertices.
The reporter's example: a perfect source (true Sersic at the mesh vertices) is visibly
misrepresented by the plot.

Proposal (reporter's, verified against the code path): evaluate the mapper's own interpolator
on a uniform plotting grid over the source extent (a fresh interpolator of the same type,
`mesh` and `mesh_grid`, with `data_grid` = the plot grid) and draw it with `imshow`, so the
figure is exactly the barycentric interpolant. Keep flat `tripcolor` as an option (e.g. for
showing the mesh), and consider `shading="gouraud"` only if it interpolates data values, not
colours. Mind the cost for big meshes (a 400x400 grid default, configurable), KNN mappers
(their own interpolant), and log colour scales.

## Witness

The reporter's minimal example (true Sersic on a Hilbert-Delaunay mesh) shows the plot matching
the interpolant, and the autolens_visualization / autogalaxy_visualization Delaunay figures are
re-rendered and look right.
