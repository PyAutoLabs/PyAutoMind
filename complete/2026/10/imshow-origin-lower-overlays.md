Shipped 2026-10-07 as PyAutoArray#616 (93961c68, merged to main), closing PyAutoArray#565 — the
development tracker for community Discussion #14 by @ClarkGuilty (originally PyAutoArray#535).

## What was completed

- `autoarray/plot/utils.py`: private helpers `_overlay_yx_for_origin` and `_vector_yx_for_origin`
  reflect overlay y about the raster extent's y midpoint when `imshow_origin == "lower"` (the quiver
  variant also negates dy). `"upper"` returns the input unchanged; `extent=None` applies no reflection
  (matplotlib draws pixel-index coordinates identically under either origin).
- `autoarray/plot/array.py`: every `plot_array` overlay (mask edge, border, origin marker, grid, mesh
  grid, positions, lines, regions polygons, quiver) routed through the helpers before drawing. Patches
  documented as not origin-aware. `_apply_contours` untouched.
- `autoarray/plot/inversion.py`: the uniform rectangular mesh path of `plot_inversion_reconstruction`
  (an `imshow` honouring the origin) had the identical defect; `_plot_rectangular` now returns its
  raster extent and lines/regions/grid overlays are reflected under `"lower"`. pcolormesh/tripcolor
  panels and `plot/grid.py` draw in data coordinates and were left alone.
- `autoarray/config/visualize/general.yaml`: `imshow_origin` comment records that the setting is
  presentation only and that under `lower` the displayed y axis and model y parameters disagree in sign.
- New `test_autoarray/plot/test_array.py`: three origin-agnostic regression tests (positions marker,
  asymmetric polyline, uniform-mesh inversion grid) parametrised over both origins; red on unfixed main
  for every `lower` case (`assert 0.0 == 1.0`), green after. Witness satisfied.
- Evidence: plot suite 41 passed; full suite 1981 passed / 4 xfailed; CI 3.12, 3.13, nojax all green.
- Heart YELLOW at ship (manifest drift: shared-standards blocks; release validation stale), acknowledged
  by the human in-session.

## Pending release


PyAutoArray#616 merged 2026-10-07, unreleased. Discussion #14 reply drafted; post
after human approval, and post again / mark as answer once a release carries the fix.

## Left out (follow-up candidates)

- `zoom_to_brightest` in `plot_inversion_reconstruction` computes its zoom window from an unreflected
  extent, so on a uniform mesh under `lower` the zoom can sit over the wrong part of the image.
  Pre-existing; noted on PyAutoArray#565.

## Original prompt

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
