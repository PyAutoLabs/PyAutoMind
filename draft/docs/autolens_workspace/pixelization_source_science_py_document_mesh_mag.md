# Pixelization source_science.py: document mesh magnification areas properly…

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: high
Memory: reading-queue.md; wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/cosmos-survey.md
Status: formalised
Consequence: judge
Witness: grep finds no `mesh_areas` in the four pixelization source_science.py scripts, each states the areas are the pixels' basis-function integrals and which mesh is approximate, and all four run clean in smoke.
Review-minutes: 20
Unattended: ready

# Pixelization source_science.py: document mesh magnification areas properly (arc phase 4 docs, before phase 6)

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Epic: cluster-strong-lensing
Phase: 4e
Arc: draft/feature/autolens/source_cluster_arc.md
Consequence: judge
Autonomy: supervised
Priority: high
Difficulty: medium
Witness: grep finds no `mesh_areas` in the four pixelization source_science.py scripts, each states the areas are the pixels' basis-function integrals and which mesh is approximate, and all four run clean in smoke.

## Original request (verbatim, 2026-10-29)

> intake workspace updates to ensure this is documented properly in source_science.py scripts of pixelization feature before we do 6

## Context

Arc phases 4a (PyAutoArray#664, merged; pending release) and 4b (PyAutoArray#665, in flight) made
`mapper.mesh_geometry.areas_for_magnification` the integral of each mesh pixel's interpolation basis function
(the quadrature weights for which `sum(reconstruction * areas)` is the reconstructed source's integral) on
every mesh: exact for Delaunay (barycentric dual areas), RectangularUniform (uniform cells), the four adaptive
rectangular meshes (per-axis hat quadrature through the CDF) and KNearestNeighbor / KNNBarycentric
(quadrature of their own weights over the hull); DelaunayNN still uses the Delaunay dual areas (approximation,
within 0.5%). Measured against simulator truth (autolens_workspace_test `scripts/imaging/mesh_magnification.py`)
every mesh recovers the true magnification within 1% except RectangularRTUAdaptDensity lensed (-1.82%,
reconstruction-limited).

## Problem

The four pixelization source_science scripts compute magnification from these areas, but their prose predates
the fixes:
- `scripts/imaging/features/pixelization/source_science.py` (`__Magnification via Mesh__`, ~L390-408)
- `scripts/interferometer/features/pixelization/source_science.py`
- `scripts/group/features/pixelization/source_science.py`
- `scripts/multi_galaxy/features/pixelization/source_science.py`

Stale points seen 2026-10-29: the text says the areas are "accessed via the `mesh_areas` attribute" (no such
attribute; the code uses `mapper.mesh_geometry.areas_for_magnification`); it calls them simply "areas of every
pixel", not the quadrature weights of the interpolated source; it does not say which meshes are exact or how
accurate, nor how the mesh route compares with the 1000x1000 interpolation-grid route above it; it does not
point at the PyAutoLens `magnification` latent that computes the same quantity during a fit.

## Work

1. In all four scripts, rewrite the magnification-via-mesh docs: what `areas_for_magnification` is (integral of
   each pixel's basis function, so the sum is the reconstructed source flux), that it is exact on every mesh
   except DelaunayNN (≈0.5%), the measured accuracy, and when to prefer it over the interpolation-grid route.
2. Fix the `mesh_areas` misnomer; keep the four scripts consistent (same wording, same API).
3. Mention the `magnification` latent (PyAutoLens `analysis/latent.py`) as the in-fit equivalent.
4. Check the non-pixelization `source_science.py` siblings and the HowToLens / autolens_assistant mirrors for the
   same stale claims; fix or list them.
5. Smoke the four scripts. Release gate: the text describes PyAutoArray#664/#665 behaviour, so ship after (or
   with) the release carrying them, or word it version-neutrally.

Must land before arc phase 6 (LEGGOS area magnification builds on these areas).

<!-- formalised by the Intake (Conception) Agent on 2026-10-29 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/82a81821-91bc-4bc6-b073-34d547f8bfc1/scratchpad/intake_ss.md -->
