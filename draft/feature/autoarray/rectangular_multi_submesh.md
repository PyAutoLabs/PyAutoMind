# Follow-up to `rectangular_adapt_cdf.md` (issue #322) and Path A

Type: feature
Target: PyAutoArray
Themes:
- pixelization
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: STALE PREMISE — needs re-basing before it can be issued (2026-08-09)
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-05-17 (backfilled from git)

## 2026-08-09 — the implementation base named below no longer exists

Found by the `draft/` sweep, verified against PyAutoArray main (`efaf3041`).

Path B is written as "subclass or compose alongside" `RectangularRotatedAdaptImage`
(Path A's mesh class), building one `RectangularSplineAdaptImage` per detected
mode. **Neither class is on main.** The mesh package is now exactly:

```
autoarray/inversion/mesh/mesh/{delaunay,knn,rectangular_adapt_density,
                               rectangular_adapt_image,rectangular_uniform}.py
```

They were removed by the rectangular-mesh consolidation (#402/#403), which also
moved the kernel-CDF machinery into `mesh_geometry/rectangular.py` and
`interpolator/rectangular.py`. So the class names, the subclassing plan, and the
"each sub-mesh runs the existing single-mode CDF code unchanged" claim all need
re-deriving against the consolidated classes before this can be issued.

**The research context survives intact** — all four artefacts this prompt tells
you to read first are still present in the repo: `files/cdf_audit.md`,
`files/ghost_peak_findings.md`, `files/ghost_peak.png`, `files/pca_rotation.png`
(plus `ghost_peak_experiment.py` / `pca_rotation_experiment.py`). The separability
problem and the A/B/C fork are unaffected; only the code the plan attaches to moved.

Before issuing: re-read the consolidated mesh classes, decide which one now plays
Path A's role (the PCA-rotation behaviour may live as a parameter rather than a
class), and rewrite § "The approach in more detail" step 2 against it. Everything
below this line predates the consolidation.

---

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
