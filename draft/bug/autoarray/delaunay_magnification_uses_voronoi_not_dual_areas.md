# Delaunay magnification denominator uses Voronoi cell areas; the barycentric-linear mapper's exact quadrature weight is the dual area

Type: bug
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace
Themes:
- pixelization
- euclid
Difficulty: small-medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: euclid-dr1-prep
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-09-04

## The finding

`MeshGeometryDelaunay.areas_for_magnification`
(`PyAutoArray/autoarray/inversion/mesh/mesh_geometry/delaunay.py:195-207`) returns
*Voronoi* cell areas, with only the strictly **unbounded** cells zeroed via the `-1`
sentinel at `:205`. But the Delaunay mapper is a **barycentric-linear** interpolant:
`pixel_weights_delaunay_from`
(`PyAutoArray/autoarray/inversion/mesh/interpolator/delaunay.py:509-586`) forms the three
sub-triangle areas at `:546-552` and normalises by their sum at `:556-560` — textbook
barycentric coordinates. For a piecewise-linear function on a triangulation,
`∫_hull f = Σ_tri area_tri · mean(3 vertices) = Σ_i s_i · dual_i`, so `Σ sᵢ·dual_areaᵢ`
with `barycentric_dual_area_from` (`.../interpolator/delaunay.py:342-398`) is the
**exact** integral of the reconstruction, not an approximation. That dual area is
already computed one module away and is currently used only to position regularisation
split points.

The identity-lens test settles it numerically. With the source-plane data grid equal to
the image-plane data grid the true magnification is exactly 1.0. The dual areas recover
μ = 1.0 to ≤ 2e-5 in **every** configuration tested (five source shapes including a
random positive reconstruction, three mesh resolutions) — the identity is geometric, not
a property of the source. The Voronoi areas never do: +0.03 %…+9.3 % on a hull pinned to
the data square (error growing monotonically with reconstruction weight near the
boundary), **−13 %…−53 %** on an adaptive-style mesh drawn from the source's own
brightness, and **−95 %…−99 %** when the source fills the hull. The mechanism is that
scipy hands some *bounded* boundary sites enormous Voronoi cells (circumcentres of very
flat boundary triangles): bounded cells one ring inside the convex hull reach **1e5×**
their dual area, with one cell measured at 973 arcsec² on a hull of area 4.15 arcsec²
(234× the entire mesh). The apparent ±0.4 % accuracy for a perfectly compact source is a
knife edge — those pathological cells simply multiply a reconstruction value of ≈ 0, and
a pedestal of one part in ten thousand of the peak already costs −3 %…−5 %. A real
non-negative solver will not sit on that knife edge. Direction of the bias on realistic
meshes is **negative**: magnification systematically under-estimated. `zeroed_pixels`
cannot rescue it — hull-ring peeling shows ring 0 (the convex hull itself) has **zero**
pathological cells because they are already unbounded and zeroed, while ring 1 carries
14 of them (max area/dual 17374.9); zeroing one hull ring moves the flat-source bias from
−97.63 % to −97.69 %, i.e. nothing.

## Consumers

`areas_for_magnification` has **no library caller**. Its only consumers are the four
`source_science.py` pixelized scripts in autolens_workspace —
`scripts/imaging/features/pixelization/source_science.py:399`,
`scripts/group/features/pixelization/source_science.py:404`,
`scripts/multi_galaxy/features/pixelization/source_science.py:411`,
`scripts/interferometer/features/pixelization/source_science.py:387` — and only when the
user swaps the mesh to a Delaunay one (all four ship with a rectangular mesh; see the
lead recorded in `draft/test/workspaces/mesh_magnification_correctness.md`). The Euclid
pipeline's `latent.magnification` never touches this code at all — it is broken for a
different reason, filed separately as
`draft/bug/autolens/magnification_latent_zero_for_pixelized_source.md`.

## Proposed fix (for the implementer to verify, not to take on trust)

1. Make the Delaunay `areas_for_magnification` return the **barycentric dual areas**,
   reusing `barycentric_dual_area_from` on `mesh_grid_xy` plus the interpolator's
   simplices. (Padded `-1` simplex rows are harmless: `-1` indexing wraps to the last
   vertex and gives a degenerate zero-area triangle — verified identical to the unpadded
   result.)
2. Keep the Voronoi areas available under their own name; they are correct arithmetic,
   just the wrong quantity for this use.
3. Update the docstring to say which quadrature it is and why.
4. Add the identity-lens regression test from the audit's `part1_flux_integral.py`
   construction — `F_dual == Σ (mapping_matrix @ s) × pixel_area` on a hull pinned to the
   data footprint, with the outer mesh ring pinned un-jittered so no data pixel takes the
   out-of-hull nearest-vertex fallback (`interpolator/delaunay.py:568-580`) — rather than
   re-pinning the existing snapshot. `areas_for_magnification` has no direct test in any
   repository today, and the one test that touches `voronoi_areas`
   (`PyAutoArray/test_autoarray/inversion/pixelization/mesh_geometry/test_delaunay.py:41-57`)
   pins the pathology: it asserts a 29.8 arcsec² boundary cell on a mesh whose real cells
   are O(1).
5. The two phase-8 tests that pin the current semantics —
   `test__areas_for_magnification__bounded_boundary_cells_are_kept` and the
   `sums_to_convex_hull_area` divergence assertion — must be **flipped deliberately in
   the same PR**, not left to fail.

## Two incidental docstring items to fold in

`_plot_delaunay` (`PyAutoArray/autoarray/plot/inversion.py:269-322`) calls
`ax.tripcolor(...)` at `:319` with neither `shading=` nor `triangles=`. Its docstring at
`:272` claims Gouraud shading, but matplotlib defaults to `shading='flat'`; with
point-valued `C` flat shading paints each triangle with the mean of its three vertices,
whose area-weighted sum equals the Gouraud integral by linearity, so the inaccuracy is
integral-neutral — but the docstring should not be relied on and should be corrected.
Second, without `triangles=` matplotlib rebuilds its own Qhull triangulation instead of
reusing `mapper.interpolator.delaunay.simplices`; on the audit's test mesh the two
simplex sets were *identical* (780 vs 780 triangles, 0 differences), so this is latent
fragility (co-circular points could diverge), not an active defect — pass
`triangles=mapper.interpolator.delaunay.simplices`. Note that the plotted surface already
integrates to `F_dual` exactly (`1.00000000`) and exceeds `F_vor` by 18.47×: the picture
and the mapper agree with each other, and `areas_for_magnification` is the odd one out.

## Provenance

Proven by the euclid-dr1-prep phase 8 audit, PyAutoArray#522 (audit posted on the issue);
reproduction scripts `part1_flux_integral.py`, `part1b_irregular_hull.py`,
`part1c_pedestal.py`, `part1d_zeroed_ring.py` were in the session scratchpad — the
implementer re-derives from the construction described here.

## Gate note

Cortex phase 7 (`PyAutoCortex/phases/euclid/magnification_robustness.md`) must not score
its Delaunay rung with the current denominator until this ships.

## Implementation design (architect, 2026-09-04 — approved plan; execute from this)

**Sequence:** `/prm PyAutoArray#523` first (phase 8 audit PR, CI green) — it frees the PyAutoArray
claim and this fix edits the same files, so branch from `main` after the merge, no parallel worktree.
Then `/start_dev` this prompt → task `delaunay-dual-area-magnification`, worktree **PyAutoArray only**.

**Facts (do not re-derive):** the dual areas are already computed by both interpolator paths —
numpy `scipy_delaunay` (`autoarray/inversion/mesh/interpolator/delaunay.py:39`, via
`barycentric_dual_area_from` `:342-398`) and in-graph JAX `jax_delaunay` (`:309-318`, scatter-add on
`simplices_padded`) — then discarded after the `areas_factor * sqrt(areas)` split-point offsets.
`DelaunayInterface` (`:589-608`) carries the results; `InterpolatorDelaunay.mesh_geometry`
(`:657-668`) builds `MeshGeometryDelaunay(mesh, mesh_grid, data_grid, xp)` with no area information.
The matern variants (`:440-495`) return no areas. PyAutoLens latents run inside a per-sample JAX jit
(`LatentLens.BATCH_MODE = "jit"`), so `areas_for_magnification` must be trace-safe under `xp=jnp`:
expose the interpolator's in-graph areas, never call scipy at latent time.

**Changes:**
1. `interpolator/delaunay.py` — `scipy_delaunay` and `jax_delaunay` add the dual `areas` to their
   return tuple; the matern variants compute them too via
   `barycentric_dual_area_from(points, simplices[simplices[:, 0] >= 0])` (one definition);
   `DelaunayInterface` gains `dual_areas`; `InterpolatorDelaunay.mesh_geometry` passes
   `dual_areas=self.delaunay.dual_areas`.
2. `mesh_geometry/delaunay.py` — `MeshGeometryDelaunay.__init__(..., dual_areas=None)`;
   `areas_for_magnification` returns the supplied `dual_areas`, else a numpy fallback
   `barycentric_dual_area_from(mesh_grid_xy, scipy.spatial.Delaunay(mesh_grid_xy).simplices)` for
   standalone construction (tests). `voronoi_areas` / `voronoi_areas_numpy` untouched. Docstring:
   dual areas = exact integral of the piecewise-linear reconstruction.
3. `plot/inversion.py::_plot_delaunay` — fix the Gouraud claim (tripcolor default is flat) and pass
   `triangles=` from the mapper's simplices with the `-1` padded rows dropped.
4. Tests — flip the phase-8 pins deliberately: in
   `test_autoarray/inversion/pixelization/mesh_geometry/test_delaunay.py`,
   `bounded_boundary_cells_are_kept` → `areas_for_magnification__equals_barycentric_dual_area`
   (indices 3 and 4 equal their dual areas, none zeroed); `uniform_lattice` → interior 1.0, sum ==
   `(n-1)**2` (hull area); `repeat_calls_agree` stays. In
   `test_autoarray/inversion/pixelization/interpolator/test_delaunay.py` the
   `sums_to_convex_hull_area` divergence assertion becomes equality for `areas_for_magnification`.
   **New** mapper-level identity test (mapper test file for Delaunay): a `MapperDelaunay` whose mesh
   outer ring is pinned to the data footprint, random positive `s`:
   `Σ (mapping_matrix @ s) × pixel_area == Σ s × mesh_geometry.areas_for_magnification` to rel 1e-4;
   JAX parity of `areas_for_magnification` under the directory's `requires_jax` pattern.
5. `pytest test_autoarray -x`; `ship_library` → PR-open, `pending-release`. `## API Changes`:
   Changed behaviour — `MeshGeometryDelaunay.areas_for_magnification` returns barycentric dual areas
   (was Voronoi cell areas with unbounded cells zeroed); Added `MeshGeometryDelaunay(dual_areas=)`,
   `DelaunayInterface.dual_areas`. Workspace impact: the four `source_science.py` scripts call the same
   attribute — no code change, option (iii). Post the identity-test numbers on the issue.

Out of scope: rectangular areas (cluster epic lead), DelaunayNN/KNN area definitions, a library-level
magnification API.


<!-- formalised by the Intake (Conception) Agent on 2026-09-04 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/4974a870-2ecf-47c9-9592-6a344294c707/scratchpad/raw_prompt1.md -->
