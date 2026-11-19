## delaunay-interpolated-plot
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/700
- completed: 2026-11-18
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/701
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/864
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/678
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/367
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/137
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/187
- workspace-pr: https://github.com/PyAutoLabs/autolens_visualization/pull/19
- community: https://github.com/PyAutoLabs/.github/discussions/46. The update is drafted for the human and NOT posted; the human will ask for it.

**What shipped:**
- autoarray `plot_mapper(..., interpolated=True)` evaluates the mapper's own interpolant on a uniform grid (`interpolated_reconstruction_from`). NaN outside the mesh hull; the image is drawn square with imshow.
- Source column, top to bottom:
  - Source Plane (Max Zoom);
  - Source Plane (Interpolated) for Delaunay/KNN with `fit: subplot_fit_source_interpolated: true` (the default, human 2026-11-17 / 2026-11-18), otherwise Mid Zoom;
  - Source Plane (No Zoom), always bottom right.
- That column appears in imaging fit.png and fit_log10.png, in interferometer fit.png (Dirty S/N removed, Dirty Model Image in panel 2, shared source vmax), and in the Delaunay/KNN inversion_#.png. Rectangular inversions are unchanged.

**History:** built in a cloud session (session_016nhQ8MtKvVD9fBkNBqcMb4) that could not run smoke tests or gallery renders. Laptop follow-ups on 2026-11-18:
- smoke 124/124;
- autolens_visualization and autogalaxy_visualization re-rendered and pixel-diffed against main: 6 changed as intended, 44 identical, and the rectangular control identical;
- the human reviewed the figures and asked for round-2 layout changes (title, square panel, inversion column, fit_log10, interferometer S/N removal, No Zoom bottom right), which were applied and then approved.
- Results: https://github.com/PyAutoLabs/PyAutoArray/issues/700#issuecomment-6975110365

**Traps and notes:**
- When a feature branch exists only on the remote, `worktree_create` builds a NEW local branch from origin/main. Re-point it with `git checkout -B <branch> origin/<branch>` before running anything.
- The `interferometer_fit_png_show_zoomed_no_zoom` draft was superseded by this task (PyAutoLens#864 1e212b43b) and retired at close-out.
- Left unchanged, all pre-existing on main:
  - the interferometer Max Zoom barely zooms on noisy reconstructions (`zoom_to_brightest`);
  - `_plot_rectangular` panels are not square (`imshow(aspect="auto")`);
  - the rectangular Max Zoom is off-centre;
  - rectangular inversion panels 10 and 12 are empty.
- Re-rendered gallery PNGs were not committed. They refresh at release.

## Original prompt

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
