## rectangular-adapt-cdf
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/322
- completed: 2026-05-17
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/323
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/71
- note: |
    Scope pivoted mid-session — original plan was a multi-component
    density framework (magnification + brightness + residual + caustic
    weighted into one mesh_weight_map). User pulled the brakes; empirical
    ghost_peak experiment confirmed the real problem was the separable
    per-axis CDF on multi-modal sources (not the signal richness). Shipped
    RectangularRotatedAdaptImage as Path A (brightness-weighted PCA
    pre-rotation). Path B (multi-sub-mesh) prompt-scoped at
    PyAutoPrompt/autoarray/rectangular_multi_submesh.md as the next step
    for arbitrary K >= 3 non-collinear peaks.

    Phase 2 density_components framework (compose_density +
    uniform_density_component, 9 tests) kept as scaffolding for future
    multi-signal work even though Path A didn't end up using it.

    Demo package rect_adapt_duo shipped under autolens_workspace_developer
    with a documented chi^2 caveat (rotated mesh delivers ~2x effective
    resolution per real peak, so under-smooths at fixed regularization;
    real lens-modelling search would tune coefficient per mesh).

## Original prompt

We have an existing JAX-compatible adaptive rectangular source-plane implementation already in the codebase. The current implementation uses a CDF-style adaptive coordinate transform where rectangular pixels become progressively smaller in regions of interest while preserving a fixed rectangular topology. The implementation works scientifically, but currently requires relatively high source resolutions (~4000+ pixels) to recover detailed source structure.

Your task is NOT to redesign this from scratch. Instead:

1. Inspect the existing implementation carefully.
2. Understand exactly how the current adaptive coordinate transform works.
3. Build on top of the existing approach to investigate more sophisticated adaptive-density formulations that retain:
   - fixed rectangular topology,
   - fixed array shapes,
   - JAX/JIT compatibility,
   - differentiability where possible,
   - no Delaunay triangulation,
   - no scipy spatial callbacks,
   - no dynamic topology changes.

The key conceptual direction is:

Instead of adapting mesh connectivity (like Delaunay), adapt the coordinate system itself via smooth density-driven coordinate warps.

We believe this may preserve many advantages of adaptive Delaunay source planes (high effective resolution in important regions with relatively few pixels) while remaining far more accelerator/JAX friendly.

The current implementation likely already resembles:

density -> cumulative distribution -> adaptive rectangular edges

We now want to generalize this.

Please investigate architectures where the adaptive density field is constructed from multiple weighted components, for example:

rho(x,y) =
floor
+ w1 * magnification_density
+ w2 * source_brightness_density
+ w3 * residual_gradient_density
+ w4 * caustic_proximity_density

Key goals:

- Concentrate source-plane resolution where scientifically useful.
- Keep total source pixel count relatively low (~500-1500 if possible).
- Preserve full JAX compatibility.
- Maintain smooth coordinate warps rather than topology changes.
- Avoid the scientific/topological failure modes encountered with kNN/Wendland-style meshless interpolation.
- Keep the implementation differentiable where practical.

Important:
The adaptive rectangular topology itself is NOT the problem. The likely problem is how intelligently the pixels are distributed.

Please specifically investigate:

1. Whether multiple density bases can be combined cleanly.
2. Whether separable x/y marginal CDFs are sufficient.
3. Whether low-rank or separable adaptive density fields are viable.
4. Whether bilinear interpolation on warped grids gives sufficiently smooth gradients.
5. Whether the source-plane interpolation operator remains well-conditioned at low pixel counts.
6. Whether adaptive rectangular grids can recover Delaunay-like effective resolution while remaining JAX-native.
7. Whether gradients wrt adaptivity weights or lens parameters remain tractable.
8. Whether the implementation can remain matrix-free or sparse-friendly.

Please also assess:

- likely bottlenecks,
- memory scaling,
- sparsity structure,
- curvature matrix structure,
- whether NNLS or positivity-constrained solves become dominant,
- and whether matrix-free iterative methods become preferable.

Do NOT spend time pursuing:

- pure JAX Delaunay triangulation,
- kNN interpolation variants,
- RBF/Wendland meshless methods,
- or dynamic topology approaches.

The current hypothesis is that:
“adaptive coordinates with fixed topology” may be the correct JAX-native formulation for adaptive source reconstruction.

Start by locating and understanding the existing adaptive rectangular implementation in detail before proposing modifications