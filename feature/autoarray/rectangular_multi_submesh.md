# Follow-up to `rectangular_adapt_cdf.md` (issue #322) and Path A

Type: feature
Target: PyAutoArray
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Follow-up to `rectangular_adapt_cdf.md` (issue #322) and Path A
(`RectangularRotatedAdaptImage`). The PCA-rotation hack we shipped fully
fixes the ghost-peak failure for K=2 (and approximately-colinear K) but
leaves residual ghosts for arbitrary K ≥ 3 non-colinear peaks. Path B is
the multi-sub-mesh approach for that general case.

The artefacts to read before issuing this prompt:

- `PyAutoArray/files/cdf_audit.md` — how the existing separable CDF works
- `PyAutoArray/files/ghost_peak_findings.md` — the empirical separability
  problem and the three possible fixes (A / B / C); this prompt is Path B
- `PyAutoArray/files/ghost_peak.png` and `pca_rotation.png` — the
  empirical visualisations of why Path A works for K=2 and only partially
  for K=3+
- `PyAutoArray/autoarray/inversion/mesh/mesh/rectangular_rotated_adapt_image.py`
  — Path A's mesh class; Path B subclasses or composes alongside it

The fundamental claim of Path B:

> For K ≥ 3 source-plane bright regions at arbitrary (non-collinear)
> positions, the separable per-axis CDF cannot adapt to all of them
> without burning some pixel budget on off-axis ghosts. Rather than
> generalising the CDF (Path C — non-axis-aligned cells), pre-segment
> the adapt image into K modes, build one `RectangularSplineAdaptImage`
> per mode, and combine them into a `MultiRectangularAdapt` container
> that presents a single mesh interface to the inversion pipeline.

The approach in more detail:

1. Detect K modes in the adapt image. Candidates: Gaussian mixture
   model (sklearn), k-means on brightness-weighted points, or simple
   quantile-thresholded connected-component labelling. The segmentation
   runs ONCE per fit on a numpy preprocessing step — not inside the JIT
   compiled likelihood — so it can use any scipy/sklearn machinery
   without breaking JAX compatibility downstream.
2. For each detected mode, build a separate
   `RectangularSplineAdaptImage` (or `RectangularRotatedAdaptImage` if
   the mode itself has internal sub-structure) covering that mode's
   bounding box. Each sub-mesh runs the existing single-mode CDF code
   unchanged — no ghosts within a single mode because each sub-mesh sees
   only one peak.
3. Wrap the K sub-meshes in a `MultiRectangularAdapt` container that:
   - Presents the union as a single mesh to the inversion: the K
     sub-meshes' pixels concatenate into one big linear-object index
     space.
   - Forwards `interpolator_from` to construct a composite interpolator
     that delegates to each sub-mesh's interpolator and merges their
     mappings / sizes / weights.
   - Forwards `mesh_geometry` to a composite geometry that knows about
     all K sub-mesh bounds for plotting.

The hard parts (must be settled in the issue planning, not pre-committed
in this prompt):

- How K sub-meshes register a single `Pixelization` to the existing
  inversion API. The inversion currently expects one `Mesh` per
  `Pixelization`. Either:
  (a) `MultiRectangularAdapt` *is* a Mesh — implements the Mesh
      interface but internally delegates to the K children. Inversion
      code is unaware.
  (b) `Pixelization` learns to hold a list of meshes — bigger API
      change, ripples through PyAutoGalaxy / PyAutoLens.
  Strongly prefer (a) for minimal blast radius.
- How regions of the source plane that lie between detected modes are
  handled. Options:
  (a) Leave un-meshed (gaps). Acceptable for high-contrast multi-modal
      sources but produces a coverage hole.
  (b) Add a low-resolution "background" sub-mesh covering the whole
      source plane, weighted lightly. Catches scattered light without
      eating the high-resolution budget.
  Recommend (b) as the default.
- How K is chosen. Auto-detection (BIC / AIC on mixture model fits) vs
  user-supplied. Recommend auto-detection with a user-overridable cap.
- How the per-sub-mesh bounding boxes are chosen. Tight (just enclosing
  the mode + sigma margin) vs Voronoi (tessellating the source plane
  by nearest mode). Voronoi gives gapless coverage but creates
  sub-meshes of awkward shapes.

Out of scope for Path B (gated on Path A + B results):

- Path C (Knothe-Rosenblatt non-axis-aligned cells) — the principled
  full fix but much bigger surgery. Only justified if Path B turns out
  to have its own failure modes we can't engineer around.
- Adaptive K detection per iteration (e.g. residual-driven new-mode
  spawning). Phase-out problem.

Workspace impact:

- A `rect_adapt_trio` (or similar) demo under
  `autolens_workspace_developer/`, mirroring the structure of
  `rect_adapt_duo` (which exercises Path A on K=2). Should simulate a
  K=3 triangular source and compare:
  baseline `RectangularSplineAdaptImage` vs
  `RectangularRotatedAdaptImage` (Path A — partial fix) vs
  `MultiRectangularAdapt` (Path B — full fix).

JAX compatibility checklist (preserved from Path A):

- Each sub-mesh's per-likelihood-eval cost is identical to a stand-alone
  `RectangularSplineAdaptImage`. JAX-traceable, no scipy callbacks
  inside the likelihood.
- The composite mapping/sizes/weights concatenation is a fixed-shape
  operation (K is decided before the likelihood; fixed during the
  search).
- The segmentation is a once-per-fit numpy step, not traced.

Suggested branch name when the prompt is issued: `feature/rectangular-multi-submesh`.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
