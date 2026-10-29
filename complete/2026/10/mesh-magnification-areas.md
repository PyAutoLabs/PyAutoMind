Source & Cluster arc phase 4a — mesh magnification areas: per-mesh correctness tests plus an integration check against simulator truth, with two library fixes.

- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/664

## Shipped
- PyAutoArray#664 (merge `7fb38053`, closes #659):
  - RectangularUniform `areas_for_magnification` now uses its own uniform cells; it was −77% to +259% off.
  - The adaptive rectangular meshes now use exact per-axis hat quadrature through the mapper's forward CDF (`adaptive_rectangular_hat_areas_from`), replacing node-midpoint cells that were up to +14.4% / +11.2% off. These areas are also non-zero exactly where the mapper puts flux; the old cells zeroed a live row on coarse meshes.
  - `test_areas_for_magnification.py` covers all 9 meshes.
  - JAX jit/grad work; numpy and JAX agree to 1e-14.
- autolens_workspace_test#348 (merge `6a7990d5`): `imaging/mesh_magnification.py` checks lensed (true μ 14.2474) and identity fits on every mesh against simulator truth and against the PyAutoLens latent. It is in smoke.

## Measured (lensed / identity vs truth)
Within 1%: RectangularUniform, Delaunay, DelaunayNN, BilinearAdaptDensity (−0.61/−0.34), BilinearAdaptImage (−0.57/−0.49), RTUAdaptImage (+0.08/+0.12). RTUAdaptDensity −1.82/−0.26 (reconstruction-limited, unchanged by areas). KNN +6.10/−5.11, KNNBarycentric −1.71/−3.57 (approximations → 4b).

## Follow-ups
- Phase 4b `draft/feature/autoarray/mesh_magnification_exact_quadrature_areas.md`, rescoped to KNN / KNNBarycentric. It also notes the bbox-domain mismatch on strongly distorted toys (BilinearAdaptImage +6–13% vs traced-region quadrature).
- PyAutoArray#660: zeroed_pixels zeroes the wrong guard row (separate).
- CI note: KNN tests needed `importorskip("jax")` for the unittest-nojax leg (fixed in-PR).

## Original prompt

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
