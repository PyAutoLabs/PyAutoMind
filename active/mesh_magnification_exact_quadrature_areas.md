# Mesh magnification: exact-quadrature areas for KNN meshes (phase 4b)

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace_test
Themes:
- pixelization
- cluster
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Epic: cluster-strong-lensing
Phase: 4b
Parent: draft/test/workspaces/mesh_magnification_correctness.md
Arc: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-10-28
Issued: 2026-10-29
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/665

## Human rulings (2026-10-28, verbatim answers to the 4a flagged decisions)

"1 I authroi,e 2 perform proper fix 3 add to 4b fix 4 file this yes"
- 2 = adaptive rectangular areas: perform the proper (exact hat-quadrature) fix.
- 3 = KNearestNeighbor / KNNBarycentric: add to this 4b fix.
- 4 = zeroed-ring guard-row mismatch filed separately as PyAutoArray#660 (not this phase).

NOTE: this renumbers the old parent's "4b" (library flux-ratio magnification promotion) — that and the
source_science recovery sweep become 4c/4d when issued.

## Scope change (2026-10-29)

Human 2026-10-29 chose "Fix adaptive rect first": the adaptive rectangular exact hat quadrature
(work item 1 below) was folded INTO 4a (PyAutoArray#659, `adaptive_rectangular_hat_areas_from`)
before its PRs opened. Measured after: lensed BilinearAdaptImage +14.43% -> -0.57%, RTUAdaptImage
+8.56% -> +0.08%; identity BilinearAdaptDensity +11.23% -> -0.34%; tolerances tightened to 1%
(RTUAdaptDensity lensed stays -1.82%, unchanged by the areas). Open item from it: on a strongly
distorted toy (radial a=0.3, BilinearAdaptImage) the bbox-domain hat areas sit +6.5% / +13% vs the
traced-region quadrature (domain mismatch, separable interpolant extends into untraced bbox corners);
the lensed simulator check is unaffected. 4b is now items 2-4 (KNN / KNNBarycentric) only.

## Measured bias at 4a (PyAutoArray#659; tolerances in 4a document these)

| mesh | unit μ_id−1 | integ. lensed | integ. identity |
|---|---|---|---|
| RectangularBilinearAdaptDensity | +3.1e-2 | −0.21% | +11.23% |
| RectangularBilinearAdaptImage | +2.4e-1 | +14.43% | +1.31% |
| RectangularRTUAdaptImage | +8.0e-2 | +8.56% | +1.05% |
| RectangularRTUAdaptDensity | +2.5e-3 | −1.82% | −0.24% |
| KNearestNeighbor | +1.6e-2 | +6.10% | −5.11% |
| KNNBarycentric | −4.4e-2 | −1.71% | −3.57% |

## Work

1. DONE IN 4a (see scope change). Adaptive rectangular (mesh_geometry/rectangular.py): replace node-midpoint CDF-transformed cell areas
   with the exact per-axis quadrature of each node's bilinear hat through the CDF,
   q(i) = ∫ hat_i(U(x)) dx, outer-product per axis. A 4a scratch prototype
   (/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2aa32082-3125-4533-a9ef-6b0e392688b6/scratchpad/measure.py,
   copy it into the task before /tmp is swept) took unit errors to ~1e-3 (Bilinear density
   2.8e-2→2e-6, RTU image −6.5e-2→2e-3); one strongly distorted toy stayed +6.5% (suspected domain
   mismatch: data region smaller than its bbox — confirm). Must stay JAX-jit/grad safe; check plotting
   (`edges_transformed` consumers) keeps drawing cell edges, i.e. split "areas" from "edges" if needed;
   measure cost.
2. KNN / KNNBarycentric: areas = exact quadrature of their interpolants (∫ of the per-node Wendland /
   barycentric-KNN weights), e.g. via the mapping-matrix column sums over a fine quadrature grid, or a
   loud documented approximation if exact is infeasible — measure.
3. Tighten the 4a tolerances (unit test test_areas_for_magnification.py and autolens_workspace_test
   scripts/imaging/mesh_magnification.py) to the new measurements (~1.5× measured, floor 1%).
4. RectangularUniform could optionally adopt the exact per-axis 9/8, 7/8 edge weights (review note);
   negligible for interior sources.
