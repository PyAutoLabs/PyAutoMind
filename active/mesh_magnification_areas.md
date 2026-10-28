# Mesh magnification areas — per-mesh correctness tests + integration sanity check (phase 4a)

Type: test
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace_test
Themes:
- pixelization
- cluster
- ci-smoke
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Epic: cluster-strong-lensing
Phase: 4a
Parent: draft/test/workspaces/mesh_magnification_correctness.md
Arc: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-10-28

## Original request (verbatim, 2026-10-28)

> ok this sounds like a good task, do it in auto mode making sure we have a robust integration
> test or sanity check in autolens_workspace_test, I guess including on area but also
> magnification values

Approved plan (same session): phase 4a = audit + direct tests of `areas_for_magnification`
on every mesh; checkpoint if any mesh is biased (accept-as-approximation / loud raise / 4b fix).

## Re-audit vs the 2026-08-19 parent prompt (stale points)

- Rectangular +6.2 % / +28.5 % guard-ring lead: likely fixed by PyAutoArray#608 (20ed237a,
  2026-10-02, areas aligned with node-midpoint cell edges) — never confirmed end to end.
- DelaunayNN / KNearestNeighbor / KNNBarycentric subclass `Delaunay` and so inherit
  barycentric dual areas (PyAutoArray#524). Dual areas are the exact quadrature weights only
  of the linear barycentric interpolant; for Sibson NN and KNN interpolants they are an
  untested approximation.
- `areas_for_magnification` now has a library consumer: PyAutoLens `analysis/latent.py`.

## Scope

1. PyAutoArray — for all 8 meshes (RectangularUniform, RectangularBilinearAdaptDensity/Image,
   RectangularRTUAdaptDensity/Image, Delaunay, DelaunayNN, KNearestNeighbor, KNNBarycentric):
   - area-sum identity: Σ areas = area of the covered domain (analytic).
   - flux-integral identity: reconstruct a known analytic source on the mesh,
     Σ s_i · A_i vs the analytic integral (= identity-lens magnification 1).
   - pinned boundary/guard-cell semantics.
   Direct unit tests in `test_autoarray/inversion/pixelization/mesh_geometry/`.
2. autolens_workspace_test — integration sanity script: simulate a lens with known true
   magnification (simulator truth, μ = total image flux / source flux) and, for every mesh,
   fit with the true mass model and assert (a) mesh areas sane, (b) recovered magnification
   within a stated per-mesh tolerance; plus an identity-lens (no mass) leg asserting μ ≈ 1.
   Wired into the smoke/integration lane.
3. Per-mesh measured bias table in the PR body.

Checkpoint (decide-and-flag under --auto): a mesh biased beyond tolerance → small fix inline;
otherwise document as an approximation with the measured tolerance, flagged in the PR for the
human's ruling (raise vs accept vs 4b fix). Never silently loosen a tolerance.

Out of scope: library flux-ratio magnification promotion (4b), workspace source_science
recovery campaign over every script (4c).
