# Mesh magnification correctness: simulate-and-recover across every mesh variant

Type: test
Target: workspaces
Repos:
- PyAutoArray
- autolens_workspace
- autolens_workspace_test
Themes:
- pixelization
- cluster
- ci-smoke
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: cluster-strong-lensing
Phase: 4
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-08-19 (backfilled from git)

# Mesh magnification correctness: simulate-and-recover across every mesh variant

Part of the Source & Cluster arc (phase 4 of 12). User request (verbatim): "Source
science and improved Magnification tests and calculations including all pixelization
meshes. This task basically involves simulating lenses, making sure all the
source_science.py examples recover their magnifications correctly and in particular runs
explicit tests on all mesh variants (rectangular, delaunay, delaunay_nn, knn) as they
were not tested properly. Things like areas could cause issues."

Audit findings (2026-08-19) confirming the "not tested properly" suspicion:
- `areas_for_magnification` exists for only TWO mesh geometries — rectangular-adaptive
  (mesh_geometry/rectangular.py:471, delegates to areas_transformed) and Delaunay
  (mesh_geometry/delaunay.py:195, voronoi_areas with boundary cells zeroed). It has
  **zero library callers** (serves only 4 workspace scripts) and **no direct test** —
  only its delegates are tested.
- Mesh classes in play: RectangularUniform / RectangularAdaptDensity /
  RectangularAdaptImage, Delaunay, DelaunayNN, KNearestNeighbor, KNNBarycentric (no
  Voronoi mesh exists any more). DelaunayNN and the KNN meshes have no area/magnification
  path at all.
- The source_science.py family: light-profile tier (imaging/group/multi_galaxy/
  interferometer + MGE variants; flux-ratio magnification assembled by hand) and
  pixelized tier (imaging/group/multi_galaxy/interferometer features/pixelization
  variants; interpolated-grid flux ratio + areas_for_magnification). All magnification
  numbers are single max-likelihood point estimates.

Work:
1. Library: promote the hand-rolled flux-ratio magnification into a tested library-level
   calculation (lean existing lever — one method consumed by all scripts), and implement
   per-mesh-pixel areas for the missing geometries (DelaunayNN, KNN/KNNBarycentric,
   RectangularUniform) or explicitly declare them unsupported with a loud error (no
   silent guards). Boundary-cell area semantics (the -1 sentinel zeroing) need a
   documented, tested definition — this is the "areas could cause issues" risk.
2. Tests: direct unit tests for areas_for_magnification on every supported geometry
   against analytic areas on known configurations.
3. Verification campaign: simulate lenses with known true magnification (simulator truth)
   and assert every source_science.py variant recovers it within tolerance — explicit
   per-mesh runs (rectangular, delaunay, delaunay_nn, knn) in autolens_workspace_test.

Blocks: source-plane magnification plots (needs per-mesh-pixel machinery), cluster
source science, per-source pixelized cluster refinement.

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/483da28c-8c96-4c83-ad87-a43448ca2164/scratchpad/source_cluster_phases/phase04_mesh_magnification_correctness.md -->
