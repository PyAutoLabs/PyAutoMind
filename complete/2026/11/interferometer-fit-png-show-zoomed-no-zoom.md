## interferometer-fit-png-show-zoomed-no-zoom
- completed: 2026-11-18
- superseded-by: complete/2026/11/delaunay-interpolated-plot.md
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/864

**Retired at the delaunay-interpolated-plot close-out:** the merged PyAutoLens#864 (commit 1e212b43b) already does what this draft asked. The interferometer 3x4 fit.png now shows Source Plane (Max Zoom), Source Plane (Interpolated) and Source Plane (No Zoom) down the right-hand column, and Mid Zoom replaces Interpolated when the key is off or the source is rectangular or parametric. To make room, Dirty Signal-To-Noise Map was removed and Dirty Model Image moved to panel 2. The array-free 2x3 layout was left as it was.

## Original prompt

# Interferometer fit.png: show zoomed, no-zoom and interpolated source panels

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_visualization
Difficulty: small
Autonomy: human-required
Priority: medium
Status: superseded (2026-11-18: done in PyAutoLens#864 commit 1e212b43b, interferometer fit.png now Max Zoom / Interpolated / No Zoom; delete at delaunay-interpolated-plot close-out)
Consequence: judge
Witness: interferometer fit.png with a Delaunay source and the key on has Zoomed, No Zoom and Interpolated panels (unit test); key off unchanged; autolens_visualization interferometer Delaunay fit.png re-rendered and looked at
Review-minutes: 20
Unattended: never
Lane: local-dev

# Interferometer fit.png: show zoomed, no-zoom and interpolated source panels

Type: feature
Target: autolens
Repos:
- PyAutoLens
- autolens_visualization
Difficulty: small
Autonomy: human-required
Priority: medium
Lane: local-dev
Consequence: judge
Witness: interferometer fit.png with a Delaunay source and the key on has Zoomed, No Zoom and Interpolated panels (unit test); key off unchanged; autolens_visualization interferometer Delaunay fit.png re-rendered and looked at
builds-on: PyAutoLabs/PyAutoArray#700 (PyAutoLabs/PyAutoLens#864, branch feature/delaunay-interpolated-plot)

@PyAutoLens

## Human request (2026-11-17, verbatim)

> Interferometer should have both intake an issue to make its fit subplot have both

## Context

PyAutoLens#864 adds `fit: subplot_fit_source_interpolated` (default true). For a Delaunay / kNN
source the imaging `fit.png` right-hand column is Max Zoom / No Zoom (flat triangles) / Interpolated
(bottom right, max-zoom extent); `false` restores max / mid / no zoom.

The interferometer 3x4 `subplot_fit` (`autolens/interferometer/plot/fit_interferometer_plots.py`)
has only two source panels: 7 (Zoomed) and 11 (No Zoom). As shipped in #864, with the key on it
shows Zoomed (7) + Interpolated (11) and **drops No Zoom**. The array-free 2x3 layout already keeps
Zoomed + No Zoom and adds Interpolated in its free sixth panel.

## What

Make the interferometer 3x4 `fit.png` show **both** the zoomed and the no-zoom flat-triangle source
panels **and** the interpolated panel when the key is on, mirroring imaging (zoom / no zoom /
interpolated down the right-hand column). This needs a layout decision: find a third source slot
(e.g. move or drop one of the residual / UV panels, or reorder the grid) without losing a
diagnostic the interferometer fit needs. Present the layout options to the human before coding.
With the key off, or for rectangular / parametric sources, keep the current zoomed + no-zoom layout.

## Witness

Unit test: the interferometer `fit.png` with a Delaunay source and the key on has Zoomed, No Zoom
and Interpolated panels (interpolated is a raster, the other two triangles); key off is unchanged.
Re-render the autolens_visualization interferometer Delaunay `fit.png` and look at it.

<!-- formalised by the Intake (Conception) Agent on 2026-11-17 from file:/tmp/claude-0/-home-user/a5df5063-0e48-570d-9ab5-4c73568bdf72/scratchpad/intake_raw.md -->
