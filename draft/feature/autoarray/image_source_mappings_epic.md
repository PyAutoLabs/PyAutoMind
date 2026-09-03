# Image ↔ source plane mappings — regions, clumps, `subplot_mappings`, ShapeSolver validation, guide — epic

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoLens
- autolens_workspace
- HowToLens
- HowToGalaxy
- autogalaxy_workspace
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: image-source-mappings
Filed: 2026-09-02

Epic slug: `image-source-mappings`
Born: 2026-09-02.

## Context

The mapping-colouring feature (coloured source pixels + their matched image-plane counterparts) died in
PyAutoArray `0cb75ebd` (2025-07-21, "visual clean up complete") and the whole `Visuals2D`/`MapperPlotter`
stack followed in 2026-03 when plotting became standalone matplotlib functions. What remains today:

- `aplt.subplot_mappings(inversion, pixelization_index)` (`PyAutoArray/autoarray/inversion/plot/inversion_plots.py:238`)
  computes peak source pixels, calls `mapper.slim_indexes_for_pix_indexes(...)` and **discards the result** — it is a plain
  2×2 data/model/recon subplot. Workspace prose (`autolens_workspace/scripts/imaging/features/pixelization/fit.py:254`)
  still promises coloured mapping circles. Nothing in PyAutoLens/PyAutoGalaxy calls it; `plots.yaml: subplot_mappings` is dead.
- `HowToLens/scripts/chapter_3_pixelizations/tutorial_2_mappers.py` self-flags "VISUALS SLIGHTLY BUGGY" (line 10); it
  computes `indexes`/`pix_indexes` (lines 166/182/205/265) and never draws them. Same dead sections in
  `autolens_workspace/.../pixelization/delaunay.py:1283`, interferometer `delaunay.py:1083`, the `likelihood_function.py`
  scripts, and the HowToGalaxy mirror. Known and deferred in PyAutoMind (`complete/2026/07/slam-adapt-inversion-cascade.md:117`).
- `max_pixel_list_from` (`inversion/abstract.py:1226`) returns ONE list of peak pixels, never per-clump groups.
- `max_pixel_list_from` has zero workspace usages; there is no 4MOST / spectroscopic follow-up material anywhere
  (workspace, assistant, Mind, Memory).

Goal: one clean "one look" figure showing how the brightest regions of the source map to the image plane and back,
working for pixelized AND parametric sources, with per-clump colours (1 clump / 2 merging galaxies / many knots), plus the
brightest image-plane coordinate of each lensed image for fibre pointing, plus a step-by-step guide and a fixed tutorial.

## Decisions taken (user, 2026-09-02)

- **Three-phase epic**, one issue + PR per phase, library-first (Phase 1 PyAutoArray → Phase 2 PyAutoLens → Phase 3 workspace).
- **ShapeSolver is the source→image engine for non-pixelized sources** (user, mid-plan revision): reuse as much of
  `autolens/point/solver/shape_solver.py` as possible so the same code serves the shape-tracing visuals AND the precise
  numerical calculations (magnification, source size), and Phase 2 becomes the validation ShapeSolver never had. The
  simpler grid-trace membership approach is kept only as a **test oracle** (pixel-resolution cross-check), not as API.
- **WCS stays guide-level**: library returns arcsec + pixel coordinates; the guide shows the astropy conversion inline.

## Standing assumptions (hold for the whole epic)

- The `ci-timing-fast-tests` epic pause rule ("ALL other source/workspace development is paused while this epic runs")
  is on record in `epics.md`. It is **not** treated as blocking here: `numpy-deflections-cpu` phase 1 also started
  2026-09-02, so by user decision (2026-09-02) this epic proceeds alongside. Recorded here, not re-asked per phase.
- Everything in "Verified facts" below was derived in the 2026-09-02 survey — **do not re-derive it**; if a fact turns
  out false, correct it here in the ledger and say so in the phase PR body.

## Verified facts that shape the design (do not re-derive)

1. `Mapper.slim_indexes_for_pix_indexes` (`mappers/abstract.py:504`) returns **sub-slim** (over-sampled) indexes despite its
   name — never use it to build an image-plane pixel region. Use `Mapper.mapping_matrix` (`:256`, shape
   `[mask_pixels, mesh_pixels]`, already folded over sub-pixels) — the same idiom as `pixelization/delaunay.py:1305`.
2. `plot_array` calls `zoom_array(array)` (`plot/array.py:124`) before drawing, so overlays must be **arcsec-space polygons**,
   not boolean pixel arrays. All existing overlays (`mask`, `border`, `positions`, `lines`) are coordinate-space.
3. `Shape` classes (`autoarray/structures/triangles/shape.py`) only have `mask(triangles)` (which reads `(x, y)` order);
   there is no point-containment method.
4. `_plot_delaunay` uses flat `tripcolor`; a Delaunay "pixel" is a vertex, its natural polygon is its Voronoi cell
   (`mesh_geometry/delaunay.py:167 voronoi`). Rectangular cells come from the mesh geometry edges.
5. `Array2D.from_fits` retains the FITS header (`uniform_2d.py:900`), so `dataset.data.header` carries WCS keywords when the
   source FITS had them — enough for the guide-level astropy recipe.
6. `scipy.ndimage` is already a hard dependency (`mask_2d_util.py:609`). `Neighbors` (`inversion/linear_obj/neighbors.py`)
   is an ndarray with `-1` sentinels and `.sizes`.
7. `PointSolver.solve` short-circuits under `PYAUTO_SMALL_DATASETS` to a fixed pair — never assert on its values in smoke.

## Architecture

A **mapping** = one source-plane region + the list of image-plane connected regions (the multiple images) it maps to,
sharing one colour. Two engines produce the same plotting-agnostic result objects; rendering is one generic
`regions=` overlay on `plot_array` and `plot_inversion_reconstruction`. Numpy-only, never jitted (plotting/diagnostic code).

```
autoarray/inversion/mappings/mapping.py           (Phase 1, new package — not inside mappers/)
  @dataclass ImageRegion: slim_indexes, mask(Mask2D), contours[(N,2) yx arcsec], centre,
                          area(), brightest_coordinate_from(array), centroid_from(array), flux_from(array)
  @dataclass Mapping:     pix_indexes, source_contours, source_centre, image_regions[ImageRegion], peak_value
  connected_components_from(indexes, neighbors) -> List[np.ndarray]      # BFS on mesh graph
  image_regions_from_slim_mask(mask2d, slim_bool, min_pixels) -> List[ImageRegion]   # ndimage.label(8-conn) + contours
  image_regions_from(mapper, pix_indexes, weight_threshold=0.0, min_pixels=1) -> List[ImageRegion]   # via mapping_matrix
  source_contours_from(mapper, pix_indexes) -> List[np.ndarray]   # rectangular cells / Delaunay Voronoi cells
  contours_from_bool_native(bool_native, geometry) -> List[np.ndarray]   # pixel-edge boundary loops → arcsec
```

**Engine A** (pixelized, PyAutoArray): `Inversion.source_clumps_from(...)` thresholds the reconstruction at
`threshold * max`, takes connected components over `mapper.neighbors`, drops `< min_pixels`, sorts by peak, truncates to
`total_clumps`; `pix_indexes=[[...],[...]]` bypasses clump finding (tutorial path). `Inversion.mappings_from(...)`
composes it with `image_regions_from`. **The threshold is the documented knob**: ~0.5 one smooth source, ~0.2 merges two
galaxies into one, ~0.8 splits star-forming knots.

**Engine B** (any source, PyAutoLens, **ShapeSolver-based**): `ShapeSolver.for_grid(grid, pixel_scale_precision, ...)`
→ `solve_triangles(tracer, shape, plane_redshift)` returns the kept image-plane triangles whose traced images contain the
source `Shape`. From them: (i) group triangles into connected components by shared vertices (the separate multiple
images), (ii) each component's polygons = its triangles (drawn as filled triangles, union outline optional), (iii) pixel
coverage = image pixels containing any kept-triangle vertex or centroid → `slim_indexes`/`mask` on the same `ImageRegion`
object as engine A, so `brightest_coordinate_from` etc. work identically. Sub-pixel sources still produce regions because
the triangles carry the geometry, not the pixel grid. `steps()` exposes every refinement level for the guide's
"how the solver homes in" figure. `find_magnification` gives the per-image / total magnification numerically.
Default shape for a parametric source: `Circle` at the profile centre, radius = `half_light_radius`
(`autogalaxy/profiles/light/abstract.py:150`). `PointSolver.solve` stays the point-level overlay of the centre.
Test oracle only: trace the image grid, `shape.contains(points)` → slim bool → `image_regions_from_slim_mask`; the
ShapeSolver regions must agree with it to within a pixel for sources larger than a few pixels.

Rendering: `plot_array` / `plot_inversion_reconstruction` gain `regions`, `region_colors`, `region_alpha=0.25`,
`region_labels`; each polygon is `ax.fill` + `ax.plot` outline + optional numbered label; colour cycle reuses `plot_grid`'s
`["r","g","b","m","c","y"]`. `plot_grid(indexes=...)` (point-level) is untouched.

## Phases

| Phase | Prompt | State |
|---|---|---|
| 1 | complete/2026/09/image-source-mappings-p1.md | **SHIPPED** 2026-09-02 — PyAutoArray#517 merged (`501c373f`), issue #515 closed. `pending-release`: the PyAutoArray **release** is still outstanding, and Phase 2 is gated on it. |
| 2 | complete/2026/09/image-source-mappings-p2.md | **SHIPPED** 2026-09-02 — PyAutoArray#518 merged (`c9f67e78`, phase 2a + three solver/overlay fixes) → PyAutoLens#720 merged (`091fbdff`, ShapeSolver validation suite + `al.mappings` + `subplot_mappings`), issue #719 closed. Both repos `pending-release`: **both releases are still outstanding**, and Phase 3 is gated on them. |
| 3 | active/mappings_guide_and_tutorial_rewrite.md | **ACTIVE** 2026-09-03 — autolens_workspace#525, worktree `image-source-mappings-p3` (autolens_workspace, HowToLens, HowToGalaxy, autogalaxy_workspace). Opened by user decision ahead of both library releases; every PR `pending-release`. |

## Sequencing rule

**Library-first, strictly.** Phase 1 (PyAutoArray) must be merged AND released before Phase 2 opens, because Phase 2's
`autolens/lens/mappings.py` imports `Mapping`/`ImageRegion` and the `regions=` overlay from the released PyAutoArray.
Phase 3 (workspace + tutorials) was gated on BOTH Phase 1 and Phase 2 releasing, since the guide and the
rewritten `tutorial_2_mappers.py` call both libraries' APIs. **Waived by the user 2026-09-03** (as for Phase 2): workspace CI
installs the libraries from source, so Phase 3 develops and ships now with `pending-release` on every PR.

Issue **ONE phase at a time** — no bulk issue queues. One issue + one PR per phase. Fable stays architect: plans,
reviews the returned diff against the verified facts above, writes PR bodies; implementation is delegated one rung down.

## Original request (verbatim)

```
We have pockets of functionality for producing mappings between the source and image plane, including visualization,
but it is limited. For example, tutorial_2_mappers.py describes how we can put points in the image and source plane 
which map to one another, often putting them on images side by side to illustrate lensing.

We also have tools which find the brightest regions of the source in the source plane, which for a parametric light
profile is its centre but for an inversion requires us to use the "max_pixel_list_from" of similar things to find
the brightest regions of the source plane, which then map bak to the image plane. 

Functionality for computing the the brightest positions or regions of of the lensed source ocmponents,
which for a single source is 2 or 4 multiple images but if there are multiple clumps in the source plane is 2 or 4
images per component. For example, if the source plane were tow merging galaxies we might want to see which
multiple images in the image plane correspond to each galaxy. Ideally, we'd have some sort of matplotlib visual which
iohglight polygons or borders around the source pixels in one color and their images in the same colors in the
image plane.

I am picturing a new type of matplotlib subplot, probably the subplot_mappings, which is literally a clean beautiful way
to in one look assess exactly how the brightest regions of the source, given the lens model, map from the image
to source plane and visa verse. WE did in fact have visuals and tools to do this in the past but I think they were
removed from the soruce code for not functioning to a high enough quality.

I want you to basically implement this feature again, but aim to do it better so this image is most useful. This
will hopefully lead to an improvement in a tutorial like tutorial_2_mappers.py which will show mappings not just
via points but also polygons. Review different approaches we can take, most of this type of mapping currently uses
Inversions and their Mapper quantities to produce each side, but this means parametric profiles need separate
tools. The ShapeSolver could maybe be used here, albeit that was originally built for more numerially demanding calculations
like working out the size of a finite sized small source in the source plane, but maybe it can be adapted to this.

For a mesh source reconstrucction this does all mean that care needs to be taken in ensuring we can identify the
brightest clumps in a source, and this really needs to know if there is one bright clump, two (e.g. merging galaxies)
or lots (e.g. star forming knots). One use case is going to be that people who work on 4MOST are going to need to know
where the brightest coordinate (WCS) of the source in the image plane are so they can carefully point a spectra fiber
over that specific region, nearly all spectroscopic follow needs this information if I'm honest.

So yeah, this issue all falls uner the umbrella of image to source mappings but has lots of different use cases,
so working out the best approach probably has trade offs.

The end result will probably also include a guide which gives the usual contents + docstring style step by
step guide to all the ways we can map sourcde to image plane and visa versa and offers help on ensuring you get things
like brightest image regions for 4MOST.
```

Mid-plan revision (user, 2026-09-02): for non-pixelized sources reuse as much ShapeSolver code as possible so the same code serves the shape-tracing visuals and the precise numerical calculations, and this becomes the validation ShapeSolver never had.
