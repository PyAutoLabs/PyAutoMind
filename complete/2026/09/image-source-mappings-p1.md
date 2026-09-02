## image-source-mappings-p1
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/515 (closed completed 2026-09-02)
- completed: 2026-09-02
- library-pr: PyAutoArray https://github.com/PyAutoLabs/PyAutoArray/pull/517 (head `36b75e07`, merge `501c373fdb0f1cd0545ccdc593b2f74d35fbac0d`) — label `pending-release`
- classification: feature (library) — epic `image-source-mappings`, phase 1 of 3 (ledger
  `draft/feature/autoarray/image_source_mappings_epic.md`). Fable session; execution delegated to Opus.
- ci: `Tests` — one workflow run, all 3 legs green (`3.12`, `3.13`, `nojax`). Local
  `pytest test_autoarray` — 1382 passed.
- heart-ack (carried from the `active.md` entry): "PyAutoArray: open PR 10d old"; "release validation
  incomplete: no rehearsal for current source".
- parallel-claim: PyAutoArray was simultaneously held by `numpy-deflections-p1` (#514) in its own
  worktree; file sets disjoint, own worktree approved by the human 2026-09-02. That claim and its
  worktree were left untouched by this close-out.

- summary: New `autoarray/inversion/mappings/` package — `Mapping` / `ImageRegion` result objects,
  `connected_components_from` (BFS over the mesh graph), `image_regions_from` (image-plane regions
  derived from `Mapper.mapping_matrix`, not the sub-slim `slim_indexes_for_pix_indexes`),
  `source_contours_from` and arcsec boundary polygons. `Inversion.source_clumps_from` (threshold /
  `min_pixels` / `total_clumps` / `pix_indexes` bypass) plus `Inversion.mappings_from` and
  `Mapper.mappings_from`. A generic `regions=` / `region_colors` / `region_alpha` / `region_labels`
  polygon overlay on `plot_array` and `plot_inversion_reconstruction`. `subplot_mappings` rewritten
  as the one-look 2x2 colour-matched figure (image regions in both image panels, clumps in both
  source panels, labels matched across the planes).
- files: 17 changed — `autoarray/inversion/mappings/{__init__,mapping}.py` (new, 761 lines),
  `inversion/inversion/abstract.py`, `inversion/mappers/abstract.py`,
  `inversion/plot/{inversion_plots,mapper_plots}.py`, `plot/{array,inversion,utils}.py`,
  `config/visualize/general.yaml`, `__init__.py`, plus five test modules including the new
  `test_autoarray/inversion/mappings/test_mapping.py`.

- not shipped (deliberate, already re-filed): the prompt's **optional** `Shape.contains(points_yx)` /
  `Shape.boundary(n)` on `autoarray/structures/triangles/shape.py` did not make this PR
  (`shape.py` is untouched by #517). The prompt names the fallback and the Phase 2 draft already
  carries it as **Phase 2a** — a tiny PyAutoArray PR that must merge and release *before* the
  PyAutoLens PR opens (`draft/feature/autolens/mappings_shape_solver_fit_subplot.md`, "Files"
  section). Nothing new was filed; the remainder was already in the backlog.
- leftovers / traps:
  - Pre-existing silent `except: pass` guards remain in `subplot_mappings` — not introduced here,
    not removed here.
  - `black` reformatted ~40 unrelated lines in the touched `autoarray/plot/` files; the PR diff is
    correspondingly wider than the change.
  - Workspace configs still carry the old `total_mappings_pixels` key. The library reads it as a
    fallback for one release (`config/visualize/general.yaml` now also carries the new
    `inversion:` keys); **Phase 3 sweeps the workspace configs** — do not remove the fallback before
    then.
- next: a PyAutoArray **release** is the gate. Phase 2 (PyAutoLens, ShapeSolver engine + validation
  suite) stays blocked on that release landing and is the human's call to open — it was deliberately
  not unblocked at close-out. Phase 3 (workspace + tutorials) opens only after Phase 2 releases.

## Original prompt

# Image-plane region mappings, source clump finding and a restored `subplot_mappings` in PyAutoArray

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: image-source-mappings
Phase: 1
Filed: 2026-09-02

Image-plane region mappings, source clump finding and a restored `subplot_mappings` in PyAutoArray.

> Phase 1 of the `image-source-mappings` epic — ledger
> `draft/feature/autoarray/image_source_mappings_epic.md`, which holds the context (the feature died in
> `0cb75ebd`, 2025-07-21), the user decisions and the original request verbatim. This phase lands the
> plotting-agnostic result objects, the pixelized-source engine (engine A) and the generic `regions=`
> overlay, so that Phase 2 (PyAutoLens, ShapeSolver) and Phase 3 (guide + tutorials) have something to
> build on. **Must merge AND release before Phase 2 opens.**

## Architecture (this phase's half)

A **mapping** = one source-plane region + the list of image-plane connected regions (the multiple images) it maps to,
sharing one colour. Two engines produce the same result objects; rendering is one generic `regions=` overlay on
`plot_array` and `plot_inversion_reconstruction`. Numpy-only, never jitted (plotting/diagnostic code).

```
autoarray/inversion/mappings/mapping.py           (new package — not inside mappers/)
  @dataclass ImageRegion: slim_indexes, mask(Mask2D), contours[(N,2) yx arcsec], centre,
                          area(), brightest_coordinate_from(array), centroid_from(array), flux_from(array)
  @dataclass Mapping:     pix_indexes, source_contours, source_centre, image_regions[ImageRegion], peak_value
  connected_components_from(indexes, neighbors) -> List[np.ndarray]      # BFS on mesh graph
  image_regions_from_slim_mask(mask2d, slim_bool, min_pixels) -> List[ImageRegion]   # ndimage.label(8-conn) + contours
  image_regions_from(mapper, pix_indexes, weight_threshold=0.0, min_pixels=1) -> List[ImageRegion]   # via mapping_matrix
  source_contours_from(mapper, pix_indexes) -> List[np.ndarray]   # rectangular cells / Delaunay Voronoi cells
  contours_from_bool_native(bool_native, geometry) -> List[np.ndarray]   # pixel-edge boundary loops → arcsec
```

**Engine A** (pixelized, this phase): `Inversion.source_clumps_from(...)` thresholds the reconstruction at
`threshold * max`, takes connected components over `mapper.neighbors`, drops `< min_pixels`, sorts by peak, truncates to
`total_clumps`; `pix_indexes=[[...],[...]]` bypasses clump finding (the tutorial path). `Inversion.mappings_from(...)`
composes it with `image_regions_from`. **The threshold is the documented knob**: ~0.5 one smooth source, ~0.2 merges two
galaxies into one, ~0.8 splits star-forming knots.

Rendering: `plot_array` / `plot_inversion_reconstruction` gain `regions`, `region_colors`, `region_alpha=0.25`,
`region_labels`; each polygon is `ax.fill` + `ax.plot` outline + optional numbered label; colour cycle reuses `plot_grid`'s
`["r","g","b","m","c","y"]`. `plot_grid(indexes=...)` (point-level) is untouched.

## Verified facts (do not re-derive)

1. `Mapper.slim_indexes_for_pix_indexes` (`mappers/abstract.py:504`) returns **sub-slim** (over-sampled) indexes despite its
   name — never use it to build an image-plane pixel region. Use `Mapper.mapping_matrix` (`:256`, shape
   `[mask_pixels, mesh_pixels]`, already folded over sub-pixels) — the same idiom as `pixelization/delaunay.py:1305`.
2. `plot_array` calls `zoom_array(array)` (`plot/array.py:124`) before drawing, so overlays must be **arcsec-space polygons**,
   not boolean pixel arrays. All existing overlays (`mask`, `border`, `positions`, `lines`) are coordinate-space.
4. `_plot_delaunay` uses flat `tripcolor`; a Delaunay "pixel" is a vertex, its natural polygon is its Voronoi cell
   (`mesh_geometry/delaunay.py:167 voronoi`). Rectangular cells come from the mesh geometry edges.
6. `scipy.ndimage` is already a hard dependency (`mask_2d_util.py:609`). `Neighbors` (`inversion/linear_obj/neighbors.py`)
   is an ndarray with `-1` sentinels and `.sizes`.

(Numbering matches the ledger's list; facts 3, 5 and 7 belong to Phases 2/3.)

## Files

- **new** `autoarray/inversion/mappings/{__init__,mapping}.py` — the objects + functions above.
- `autoarray/inversion/inversion/abstract.py` — add
  `source_clumps_from(mapper_index=0, threshold=0.5, min_pixels=3, total_clumps=None, pix_indexes=None) -> List[np.ndarray]`
  and `mappings_from(mapper_index=0, weight_threshold=0.0, **clump_kwargs) -> List[Mapping]`. `np.asarray` the
  reconstruction (may be a jax array). Empty/non-positive max → `[]`. Leave `max_pixel_list_from` as is.
- `autoarray/plot/array.py`, `autoarray/plot/inversion.py` — the `regions` overlay (drawn after `lines`).
- `autoarray/inversion/plot/inversion_plots.py::subplot_mappings` — rewrite the body; keep the name, `pixelization_index`
  and the `mappings_{i}` filename. Add `threshold`, `min_pixels`, `total_clumps`, `pix_indexes`, `weight_threshold`.
  Layout 2×2: data-subtracted + image regions | reconstructed image + image regions | source recon zoomed + clumps |
  source recon unzoomed + clumps; matched colours, labels 1..N in both planes. Interferometer: keep the existing
  `Visibilities` → `transformer.image_from` conversion; regions are real-space so they work unchanged.
- `autoarray/inversion/plot/mapper_plots.py::subplot_image_and_mapper` — accept `regions`/`region_colors` pass-through so a
  bare `Mapper` (no inversion — the tutorial_2 case) can show `pix_indexes` mappings: helper
  `mapper.mappings_from(pix_indexes) -> List[Mapping]` on `Mapper` (thin wrapper over `image_regions_from` +
  `source_contours_from`).
- `autoarray/config/visualize/general.yaml` — replace `total_mappings_pixels` with `inversion: total_mappings: 5`,
  `mappings_threshold: 0.5`, `mappings_min_pixels: 3`; read the old key as a fallback for one release.
- `autoarray/plot/__init__.py` — export nothing new beyond what exists (`subplot_mappings` is already exported); export
  `Mapping`, `ImageRegion` from `autoarray/__init__.py`.

## Optional — ship here if timing allows

`autoarray/structures/triangles/shape.py` — add `Shape.contains(points_yx) -> bool array` (Circle radial, Triangle
barycentric, Polygon even-odd, Square bounds, Point raises pointing at Circle/PointSolver) and
`Shape.boundary(n=100) -> (N,2) yx`. Takes `(y, x)`; the docstring must note the legacy `(x, y)` order of
`mask(triangles)` (verified fact 3: the `Shape` classes today have `mask(triangles)` only, no point containment).
This is Phase 2's first bullet — a small PyAutoArray change. Ship it in this PR if timing allows; otherwise it becomes a
tiny Phase 2a PyAutoArray PR that must precede the PyAutoLens one.

## Tests

Existing `plot_path`/`plot_patch` fixture pattern; fixtures `rectangular_inversion_7x7_3x3`, `delaunay_mapper_9_3x3`.

- `test_autoarray/inversion/mappings/test_mapping.py` — `connected_components_from` on a synthetic `Neighbors`;
  `image_regions_from` splitting a bimodal mapping matrix into two regions; contour loops closed;
  `brightest_coordinate_from`.
- `test_autoarray/inversion/inversion/test_abstract.py` — `source_clumps_from`: two groups for a two-peak vector, one at
  low threshold, `pix_indexes` passthrough, `total_clumps` truncation.
- `test_inversion_plotters.py` — keep the existing `subplot_mappings` assertion; add a Delaunay case and a `pix_indexes=` case.
- `test_autoarray/plot/` — `regions=` smoke on `plot_array` and `plot_inversion_reconstruction`.

## Verification

`source activate.sh && pytest test_autoarray/inversion test_autoarray/plot -q`; then run
`autogalaxy_workspace/scripts/imaging/features/pixelization/plot.py` and
`autolens_workspace/scripts/imaging/features/pixelization/fit.py` under the smoke profile and **eyeball**
`mappings_0.png`: a two-clump source must show distinct colours, each clump's images outlined in the same colour in both
image panels, and labels matching across the planes.
