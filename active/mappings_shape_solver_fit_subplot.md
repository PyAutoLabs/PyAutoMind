# ShapeSolver-based source-to-image region mappings, fit-level `subplot_mappings`, brightest multiple-image positions, and the ShapeSolver validation suite in PyAutoLens

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
- PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: image-source-mappings
Phase: 2
Filed: 2026-09-02
Issued: 2026-09-02

ShapeSolver-based source-to-image region mappings, fit-level `subplot_mappings`, brightest multiple-image positions, and the ShapeSolver validation suite in PyAutoLens.

> Phase 2 of the `image-source-mappings` epic — ledger
> `draft/feature/autoarray/image_source_mappings_epic.md`. **Depends on Phase 1
> (`complete/2026/09/image-source-mappings-p1.md` — merged 2026-09-02 as PyAutoArray#517, **not yet released**)
> being merged AND released**: this phase imports
> `Mapping` / `ImageRegion` and the `regions=` overlay from the released PyAutoArray. Phase 3 (workspace + tutorials)
> opens only after this one releases.

## Engine B — ShapeSolver as the source→image engine

User decision (mid-plan revision, 2026-09-02): for non-pixelized sources, **reuse as much `ShapeSolver` code as
possible** so the same code serves the shape-tracing visuals AND the precise numerical calculations (magnification,
source size) — and this phase becomes the validation ShapeSolver never had. The simpler grid-trace membership approach
is kept only as a **test oracle** (pixel-resolution cross-check), never as API.

`ShapeSolver.for_grid(grid, pixel_scale_precision, ...)` → `solve_triangles(tracer, shape, plane_redshift)` returns the
kept image-plane triangles whose traced images contain the source `Shape`. From them: (i) group triangles into connected
components by shared vertices (the separate multiple images), (ii) each component's polygons = its triangles (drawn as
filled triangles, union outline optional), (iii) pixel coverage = image pixels containing any kept-triangle vertex or
centroid → `slim_indexes`/`mask` on the same `ImageRegion` object as engine A, so `brightest_coordinate_from` etc. work
identically. Sub-pixel sources still produce regions because the triangles carry the geometry, not the pixel grid.
`steps()` exposes every refinement level for the guide's "how the solver homes in" figure (Phase 3).
`find_magnification` gives the per-image / total magnification numerically. Default shape for a parametric source:
`Circle` at the profile centre, radius = `half_light_radius` (`autogalaxy/profiles/light/abstract.py:150`).
`PointSolver.solve` stays the point-level overlay of the centre. Test oracle only: trace the image grid,
`shape.contains(points)` → slim bool → `image_regions_from_slim_mask`; the ShapeSolver regions must agree with it to
within a pixel for sources larger than a few pixels.

## Verified facts (do not re-derive)

3. `Shape` classes (`autoarray/structures/triangles/shape.py`) only have `mask(triangles)` (which reads `(x, y)` order);
   there is no point-containment method.
5. `Array2D.from_fits` retains the FITS header (`uniform_2d.py:900`), so `dataset.data.header` carries WCS keywords when the
   source FITS had them — enough for the guide-level astropy recipe (Phase 3).
7. `PointSolver.solve` short-circuits under `PYAUTO_SMALL_DATASETS` to a fixed pair — never assert on its values in smoke.

(Numbering matches the ledger's list; facts 1, 2, 4 and 6 are Phase 1's.)

## Cross-reference — the existing ShapeSolver audit

`draft/feature/autolens/area_magnification_leggos.md` (cluster-strong-lensing phase 6) carries the **ShapeSolver audit
verdict of 2026-08-19**: effectively unmaintained — one method (`find_magnification` = kept-triangle image area /
source `shape.area`), its only test commented out since ~2024-09, `use_jax=True` silently ignored (`find_magnification`
hardcodes `xp=np` and never consults `self._xp`), the JAX triangle `area` cannot survive `jax.jit` (`__len__` returns a
traced `count_nonzero`), no per-image split, no magnification-threshold filter, no error estimate, and image area
over-covers by up to one triangle edge per boundary with no convergence check; sole consumer is one unused demo in the
workspace `point_source/fit.py`. That prompt frames it as "rehabilitate or retire" against a LEGGOS per-pixel-inversion
primary API. **Do not merge the two prompts.** This phase settles the *rehabilitate* half from the mappings side — the
per-image split, the `xp` dispatch, the revived tests and the convergence statement are all listed below — and the
LEGGOS prompt keeps its own scope (area magnification of an arc via the μ-map). Read that audit before touching
`shape_solver.py` and reconcile any finding that has since changed.

## Files

- `PyAutoArray/autoarray/structures/triangles/shape.py` — add `Shape.contains(points_yx) -> bool array` (Circle radial,
  Triangle barycentric, Polygon even-odd, Square bounds, Point raises pointing at Circle/PointSolver) and
  `Shape.boundary(n=100) -> (N,2) yx`. Takes `(y, x)`; the docstring notes the legacy `(x, y)` order of
  `mask(triangles)`. Small PyAutoArray change — it did **not** ship in the Phase 1 PR (#517 leaves `shape.py`
  untouched), so it **is** the tiny **Phase 2a** PyAutoArray PR, and it must merge and release *before* the
  PyAutoLens PR opens.
- `autolens/point/solver/shape_solver.py` — **ShapeSolver audit + reuse**: read `solve_triangles`, `steps`,
  `find_magnification`, the triangle containers (`autoarray/structures/triangles/{array,coordinate_array}*.py`:
  `containing_indices`, `neighborhood`, `up_sample`, `for_indexes`) and the `PYAUTO_SMALL_DATASETS` / JAX paths; fix
  what the validation below exposes (**bugs fixed in place, each with a regression test — never worked around in the
  mappings layer**). Add `ShapeSolver.image_regions_from(tracer, shape, plane_redshift=None) -> List[ImageRegion]`
  (triangle grouping by shared vertices → per-image triangle polygons + pixel coverage on the solver's grid mask) and
  `ShapeSolver.mapping_from(tracer, shape, ...) -> Mapping` (source contour = `shape.boundary()`).
- **new** `autolens/lens/mappings.py`:
  - `source_mapping_from(tracer, grid, shape, plane_index=-1, plane_redshift=None, pixel_scale_precision=None) -> Mapping`
    — builds `ShapeSolver.for_grid` and delegates (thin).
  - `traced_region_from(tracer, region_grid, plane_index=-1) -> np.ndarray` (source-plane convex hull of a traced region).
  - `mappings_from_fit(fit, plane_index=-1, shape=None, **clump_kwargs) -> List[Mapping]` — engine A when the plane
    `has(cls=aa.Pixelization)` (predicate at `fit_imaging_plots.py:~105`), engine B (ShapeSolver) otherwise (Circle at
    the first light profile centre, `half_light_radius`).
  - `multiple_image_positions_from(fit, plane_index=-1, use_centroid=False) -> aa.Grid2DIrregular` — per image region,
    brightest pixel (or flux-weighted centroid) of `fit.model_images_of_planes_list[plane_index]`; plus
    `multiple_image_pixel_coordinates_from(...)` via `Geometry2D.pixel_coordinates_wcs_2d_from`.
    **No RA/Dec in the library** — WCS/RA-Dec conversion is guide-level only (user decision, 2026-09-02): the library
    returns arcsec + pixel coordinates and the Phase 3 guide shows the astropy conversion inline.
  - `magnifications_from(fit, plane_index=-1)` — per-image flux over source-plane flux.
- `autolens/imaging/plot/fit_imaging_plots.py::subplot_mappings(fit, plane_index=-1, ...)` — lens-subtracted data +
  regions + critical curves (`_compute_critical_curves_from_fit`, `:25`); model image + regions; source plane via
  `_plot_source_plane` (`:68`) + clumps/shape + caustics; unzoomed source. Export from `autolens/plot/__init__.py`; wire
  `plots.yaml subplot_mappings` into the imaging visualizer (`autolens/imaging/model/visualizer.py`) so the key goes live.

## Tests

- `test_autolens/lens/test_mappings.py` — Isothermal + `Circle` inside the caustic → ≥2 regions; outside → 1; parametric
  vs pixelized dispatch.
- `test_fit_imaging_plots.py` — `subplot_mappings` on `fit_imaging_x2_plane_7x7` and the inversion fixture.
- `test_autoarray/structures/triangles/test_shape.py` — `contains` / `boundary` per shape.

**ShapeSolver validation suite** (`test_autolens/point/solver/test_shape_solver.py`, extending what exists):

(a) SIS lens, small `Circle` source on-axis → Einstein ring; off-axis inside the Einstein radius → two images whose
`find_magnification` matches the analytic SIS magnification `|θ/(θ−θ_E)|` summed over images to ~1% as the circle
radius → 0; (b) ShapeSolver regions vs the grid-trace oracle agree to within one pixel for a source spanning ≥5 pixels;
(c) `steps()` refinement is monotone (kept area converges); (d) `Triangle`/`Polygon`/`Square` shapes behave like `Circle`;
(e) `plane_redshift` on a three-plane tracer; (f) the JAX (`use_jax=True`) and numpy paths give identical kept triangles.

**Failures here are ShapeSolver bugs to fix in this phase**, reported in the PR body under a "ShapeSolver audit" heading.

## Verification

`pytest test_autolens/lens/test_mappings.py test_autolens/point/solver test_autolens/imaging/plot -q`; a parametric fit
produces the same figure with a `Circle` in the source plane and its ShapeSolver triangles filled in the image plane;
`multiple_image_positions_from` on a simulated quad returns 4 positions within a pixel of the `PointSolver` positions of
the centre (**full-res dataset, not smoke** — verified fact 7: `PointSolver.solve` short-circuits under
`PYAUTO_SMALL_DATASETS`); the ShapeSolver validation suite passes and its audit findings are listed in the PR body.
