# `imshow_origin: lower` mirrors the raster but not the vector overlays in `plot_array`

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Themes:
- visualization
Difficulty: easy
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: A regression test in `test_autoarray/plot/` builds a 50x50 array with a bright block at rows 10:14, cols 23:27, plots it with a `positions` marker at the block centre under both `imshow_origin` values, reads the marker's drawn offset back from `ax.collections`, maps it through the image's own extent and `origin`, and asserts the array is bright at that pixel for BOTH `"upper"` and `"lower"` (fails red on unfixed main under `"lower"`: lands on `array[37, 25] == 0`).
Review-minutes: 3
Unattended: ready
Filed: 2026-10-07
Updated: 2026-10-07
Community: https://github.com/orgs/PyAutoLabs/discussions/14
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/565

## Finding

Community report by @ClarkGuilty (Discussion #14, 2026-09-08, originally
PyAutoArray#535; dev tracker PyAutoArray#565 opened 2026-09-21). Verified
still present on PyAutoArray `main` 58bdda0a (2026-10-07): `plot_array` in
`autoarray/plot/array.py` passes `origin=origin_imshow` to the three `imshow`
calls (RGB, scalar, `array_overlay`) but every vector overlay — mask edge,
border, origin marker, grid, mesh grid, positions, lines, regions polygons,
quiver vectors, patches — is drawn in raw `(y, x)` data coordinates. Under
`"lower"` the raster is reflected about the extent's y midpoint relative to
the overlays; nothing raises, so critical curves/caustics silently slide off
the arcs. `_apply_contours` in `plot/utils.py` already handles the origin
correctly, which is the pattern to follow.

## Original request (verbatim, from the user)

> I think its just ClarkGuilty, do his task

Full reproducer, root cause, suggested resolution and proposed regression
test are in the Discussion body (quoted on #565).
