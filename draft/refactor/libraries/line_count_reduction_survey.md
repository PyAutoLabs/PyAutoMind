# Line-count reduction across PyAutoArray, PyAutoGalaxy and PyAutoLens — feasibility survey and ranked refactor candidates

Type: refactor
Target: libraries
Repos:
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
Themes:
- hygiene
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: survey — never issued; candidates are formalised one at a time via /intake and routed through /refactor
Consequence: glance
Lane: any
Review-minutes: 0
Unattended: never
Filed: 2026-11-09

Written 2026-11-09 by the Refactor Agent session (`/refactor`) from read-only shallow clones of
PyAutoArray `1482dd9`, PyAutoGalaxy `bc3918a`, PyAutoLens `bb87dad` (plus PyAutoFit and
PyAutoNerves at `main` for the framework contracts). Nothing was edited and no suite was run; the
size numbers are `ast` walks of the clones, the candidate evidence is file:line references
re-checked in the clones. The profiles module has its own epic
(`draft/refactor/autogalaxy/profiles_unified_api_epic.md` + `_report.md`); this file is the
general assessment the human asked for beside it.

## 0. Summary

Across the three libraries (145,727 source lines, 3,917 test functions) roughly **10,500–11,500
source lines (≈ 7–8 %) and ≈ 150 test functions (≈ 4 % by count, ≈ 10 % of test lines) can be
removed with no public-API change and no numerical change**, all of it witnessed by the existing
NumPy suites plus the workspace_test JAX parity scripts. Half of that is one module — the profiles
epic. The rest is small, mechanical, and already evidence-backed to file:line.

Where the lines actually are, in order of lever size:

1. **Framework-driven class boilerplate** — `autogalaxy/profiles/` (≈ −4,000; its own epic).
2. **Data masquerading as code** — the 1,056-line colormap table in `autoarray/plot/segmentdata.py` (≈ −1,040).
3. **Dead code with zero references across all five repos** — ≈ 574 lines in PyAutoArray, ≈ 650 in
   PyAutoGalaxy/PyAutoLens (the `ag.util.chaining` module is 57 % dead and untested).
4. **Thin subclasses that are really tables** — 18 regularization/kernel/mesh classes in PyAutoArray
   (≈ −950 with their copied docstrings).
5. **Sibling copy-paste** — imaging vs interferometer, numpy vs numba, linear vs log10, tangential vs
   radial, galaxies vs tracer (≈ −1,500 across the three libraries).
6. **Test-support boilerplate** — 159 identical three-line fixture wrappers across the three
   `conftest.py` files (≈ −600), and copy-pasted test blocks that parametrise (≈ 100 functions).
7. **Prose** — 35 % of all source lines are docstrings, and the same paragraphs recur up to 16 times
   (≈ −500 to −700 by moving them to the owning base class; wording, not behaviour).

What is **not** feasible without API decisions: a 20 %+ cut. PyAutoArray's four inversion back-ends
share names, not algorithms; the `xp` dual-backend convention duplicates very little; the linear /
SNR / light-and-mass profile *namespaces* are public; and the dead public helpers (`ag.util.chaining.*`,
`ag.convert.*`, `*.model_util.*`, `aa.grid_dec`, `aa.preprocess`) need a workspace grep or a
deprecation shim before deletion. Those are listed in §4 for the human, not proposed here.

Recommended order: the profiles epic (largest lever, own ledger, one repo) → the per-repo "dead code
+ data file" PRs (small, `safe`, unblock the rest) → the table/mixin candidates per repo → test
consolidation last, once the surviving tests are the witnesses.

## 1. Where the lines are

| Library | src files | src lines | code lines | docstring lines | classes | test files | test lines | test functions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| PyAutoArray | 241 | 67,131 | 52,885 | 25,041 (37 %) | 188 | 201 | 53,211 | 1,673 |
| PyAutoGalaxy | 241 | 42,921 | 34,476 | 15,891 (37 %) | 276 | 168 | 29,019 | 1,349 |
| PyAutoLens | 151 | 35,675 | 29,265 | 10,479 (29 %) | 121 | 139 | 26,835 | 895 |
| **total** | **633** | **145,727** | **116,626** | **51,411 (35 %)** | **585** | **508** | **109,065** | **3,917** |

"code lines" are non-blank, non-comment lines; docstring lines are counted inside them. Roughly a
third of every library is prose inside the source.

Largest subpackages (src lines / test lines / test functions):

| Library | Subpackage | src | tests | test fns | note |
|---|---|---:|---:|---:|---|
| PyAutoArray | `inversion/` | 31,403 | 28,530 | 754 | 47 % of the library; 104 files |
| PyAutoArray | `structures/` | 9,501 | 6,078 | 261 | grids, arrays, vectors, decorators |
| PyAutoArray | `operators/` | 4,799 | 3,029 | 95 | convolver, transformer, over-sampling |
| PyAutoArray | `dataset/` | 4,541 | 3,869 | 125 | imaging / interferometer twins |
| PyAutoArray | `mask/` | 4,161 | 2,778 | 87 | |
| PyAutoGalaxy | `profiles/` | 20,842 | 13,468 | 735 | the profiles epic |
| PyAutoGalaxy | `operate/` | 3,637 | 2,272 | 89 | `OperateImage`, `LensCalc` |
| PyAutoGalaxy | `galaxy/` | 3,542 | 2,642 | 140 | `Galaxy`, `Galaxies`, `MassField`, `to_inversion` |
| PyAutoLens | `point/` | 10,197 | 7,531 | 246 | 38 files, 35 classes |
| PyAutoLens | `lens/` | 5,857 | 5,351 | 194 | `Tracer`, `to_inversion`, `LensCalc` wrappers |
| PyAutoLens | `potential_correction/` | 4,762 | 1,219 | 60 | |
| PyAutoLens | `twins/` | 3,188 | 1,639 | 56 | |

## 2. The refactor backlog that already exists

`draft/refactor/` holds 13 prompts before this survey (`pyauto-brain refactor candidates`,
2026-11-09). The library ones and how they relate to the candidates below:

| Prompt | Difficulty | Relation |
|---|---|---|
| `autoarray/matern_vendor_bessel_kve.md` | large | dependency removal, not line reduction; independent |
| `autoarray/sparse_operator_int32_indexes.md` | — | memory, not lines; independent |
| `autogalaxy/critical_curves_dispatch_cluster.md` | too-large | its remaining item "engine dedupe" overlaps candidate G-PLOTUTILS below (the byte-identical `plot_utils.py` twins) |
| `autogalaxy/zero_contour_pytree_compile_cache.md` | medium | gated on a profiling result; independent |
| `autolens/cache_readers_fall_back_to_zip_member.md` | small | independent |
| `autolens/one_construction_path_for_plane_bound_lensing.md` | medium | the same shape as candidate L-LENSCALC below; fold together |
| `autolens/witt_wynne_solver_library_home.md` | medium | adds lines (a library home); independent |

## 3. Ranked candidates

Lines are source lines saved (estimates from AST extents and hand diffs in the clones); tests are
functions removed or collapsed by parametrisation. "Witness" names the existing tests that must stay
green. API-risk: `none` (names, signatures, defaults, numerics all unchanged), `internal-only`
(private helpers move), `API-risk` (a public name would disappear — route via `feature/` or shim).
Evidence for the PyAutoArray rows (A-) and the PyAutoGalaxy/PyAutoLens rows (G-/L-/X-) was gathered
by two read-only audits of the clones on 2026-11-09 and the headline claims re-checked by the
session (dead-symbol reference counts, file sizes, wrapper counts, twin definitions).

| # | Id | Repo | Candidate | src lines | tests | API-risk | Difficulty |
|---|---|---|---|---:|---:|---|---|
| 1 | P | PyAutoGalaxy | profiles variants generated from factories (own epic) | −4,000 | 66 → 3; ≈ 330 → tables | none (golden-file witness) | too-large, phased |
| 2 | A10 | PyAutoArray | colormap table → packaged data file | −1,040 | 0 | none | small |
| 3 | A1 | PyAutoArray | dead code (22 defs, 0 refs in 5 repos) | −574 | −6 to −10 | internal-only (`grid_dec` is API) | small |
| 4 | G3 | PyAutoGalaxy + PyAutoLens | dead code (0 refs in 5 repos) | −650 | 0 | API-risk for 4 public helper modules | small |
| 5 | A3+A4+A9 | PyAutoArray | regularization / kernel / mesh base classes (18 thin classes) | −950 | −4 to −6 | none | small–medium |
| 6 | A11 | PyAutoArray | docstring de-dup into base classes | −400 to −700 | 0 | none | small, wide |
| 7 | X6 | all three | 159 three-line `conftest.py` fixture wrappers → one loop | −600 (test support) | 0 | none | small |
| 8 | L4 | PyAutoLens | `fit_imaging_plots` linear/log10 twins + `_plot_source_plane` copy | −330 | −4 to −6 | none | small–medium |
| 9 | A5 | PyAutoArray | one base for the two imaging sparse inversions | −275 | 0 | none | medium |
| 10 | L1 | PyAutoLens | `potential_correction` dpsi-mesh / tracer-builder mixins | −250 | −3 | internal-only | medium |
| 11 | L7 | PyAutoLens | thin re-implementations of PyAutoGalaxy (`Result`, `save_attributes`, simulators, `_xp`, `util`) | −235 | 0 | none | small |
| 12 | A12+G12 | all three | small structural bundles (grid geometry mixin, `ones/zeros`, dirty-image properties, decorator closures; tracer validators, `extract_attribute` ×3, subhalo result mixin) | −400 | 0 | internal-only | small |
| 13 | A8 | PyAutoArray | six `rectangular_*_neighbors` helpers → one | −200 | −2 to −5 | internal-only | small |
| 14 | A2 | PyAutoArray | `*_util` twin functions (numpy twins, numba loop of a one-liner) | −175 | −3 to −4 | internal-only | small |
| 15 | G10 | PyAutoLens (+Galaxy) | visualizer / `log_likelihood_function` / `shared_state_from` twins | −160 | 0 | none | medium |
| 16 | G2 | PyAutoGalaxy + PyAutoLens | pytree-registration scaffold ×5 + `jax/registration.py` helper trio | −150 | 0 | internal-only | small (JAX) |
| 17 | A7+G7 | all three | one `is_jax(xp)` / `_xp` helper for 20 copies and 3 detection idioms | −130 | 0 | none | small |
| 18 | G6 | PyAutoGalaxy + PyAutoLens | aggregator `_x_from` / `*Agg` boilerplate (8 modules) | −120 (+250 doc) | 0 | none | small |
| 19 | G5 | PyAutoLens | `latent.py` helpers re-declared + 4 µJy wrappers | −95 | −3 | none | small |
| 20 | G8 | PyAutoGalaxy | `lens_calc` tangential/radial pairs + zero-contour kwarg wrappers | −90 | 14 → 7 | none | small |
| 21 | G9 | PyAutoGalaxy + PyAutoLens | instance → galaxy-list fold + subhalo relocation ×4 | −60 | 0 | none | small |
| 22 | A13+G11 | all three | test consolidation (shadowed duplicate, number-normalised pairs, sub-2 block, container layers, sparse interferometer copies, log10 pairs) | 0 | −70 to −85 functions, ≈ −1,200 lines | none | small–medium |

### 3.1 PyAutoArray

- **A10 — colormap table → data file.** `autoarray/plot/segmentdata.py` is 1,056 lines of a literal
  `segmentdata = {"red": np.array([[…` with one call site (`plot/utils.py:992`). Store as a packaged
  `.npz`/`.json`, load lazily in `register()`; add to package data. Witness: `test_autoarray/plot/test_utils.py`
  (36 tests). Keep float64.
- **A1 — dead code.** 22 top-level defs with zero callers in `autoarray/`, `test_autoarray/` and the
  four sibling clones, e.g. `curvature_matrix_off_diags_via_mapper_and_linear_func_curvature_vector_from`
  (`inversion/inversion/imaging_numba/inversion_imaging_numba_util.py:1077-1164`, 89 lines),
  `curvature_matrix_via_sparse_operator_reference_from` (`:859-917`, test-only kernel),
  `rectangular_edges_from` (`inversion/mesh/mesh_geometry/rectangular.py:305-352`), `jax_sibson`
  (`inversion/mesh/interpolator/sibson.py:856-894`), `convert_array_2d_to_native` / `_to_slim` /
  `check_array_2d` (`structures/arrays/array_2d_util.py`), `convert_grid_2d_to_native`,
  `grid_2d_of_points_within_radius` (`structures/grids/grid_2d_util.py`),
  `rotate_pattern_ci_via_roe_corner_from` (`layout/layout_util.py:105-136`), four `inversion_util`
  / `inversion_interferometer_util` functions referenced only by their own tests, `PlottingException`,
  two unwired fixtures and two mock helpers. The `aa.util.*`-reachable ones have zero downstream uses
  but are namespace-public: delete with a note in the PR, not a shim. Keep `make_grid_2d_7x7_simple`,
  `make_imaging_7x7_sub_2`, `make_interferometer_7_grid` (used downstream). `grid_dec`
  (`autoarray/__init__.py:99`) is a documented deprecated alias with zero uses anywhere — API, so
  announce rather than silently drop. Do this first: it removes two numba kernels and unblocks A2/A5.
- **A3+A4+A9 — regularization, kernel and mesh base classes.** `autoarray/inversion/regularization/`
  is 60 % docstring. Four "Power" classes share one `regularization_weights_from` body
  (`adapt_split_power.py:82-97`, `adapt_split_zeroth_power.py:84-99`, `matern_adapt_power_kernel.py:90-105`,
  `adapt_power.py:87-112`); `Zeroth`, `CurvatureMask`, `FourthOrderMask`, `Constant` share
  `__init__(coefficient)` and `coefficient * xp.ones(...)` weights; `CurvatureMask` vs
  `FourthOrderMask` differ only in `max_order=2` vs `4`. `GaussianKernel` / `ExponentialKernel` /
  `MaternKernel` (`gaussian_kernel.py:59-248`, `exponential_kernel.py:67-229`, `matern_kernel.py:266-432`)
  have identical `__init__`, `jitter_value`, `regularization_weights_from`, `log_det_…` and
  `regularization_term_from` (similarity 0.95–1.00); only the covariance differs. Five mesh classes
  (`rectangular_bilinear_adapt_*.py`, `delaunay_nn.py`, `rectangular_uniform.py`, `knn.py:94-121`)
  have `__init__`s that forward the parent's exact signature. Refactor: `AbstractRegularization.__init__`
  + default weights; a `_PowerWeights` mixin; one `_MaskRegularization` with a `max_order` class
  attribute; `AbstractKernelRegularization` with an abstract `_covariance_matrix_from`; delete the
  forwarding mesh `__init__`s (inheritance keeps the signature PyAutoFit reads). Class names and
  kwargs stay (they are prior-config names). Witness: `test_autoarray/inversion/regularizations/*`
  (the kernel tests are already parametrised over the three classes), `inversion/inversion/test_abstract.py`,
  `pixelization/mesh/*`. Gotchas: `__eq__` compares `__dict__` — a mixin must add no instance
  attributes beyond `power`; `is_split_regularization` class attrs must survive; the
  `jitter=None ≡ 1e-8` identity is asserted (`test_kernel_log_det.py:62`).
- **A5 — one base for the imaging sparse inversions.** `inversion/inversion/imaging/sparse.py` (645)
  vs `imaging_numba/sparse.py` (815): `__init__`, `data_vector`, `_curvature_matrix_x1_mapper`,
  `mapped_reconstructed_data_dict`, `mapped_reconstructed_operated_data_dict` byte-identical (120
  lines) and four more members > 0.88 similar whose only difference is which util module they call.
  Refactor: `AbstractInversionImagingSparse` with a `_util` hook; the same `__init__` duplication
  exists between `imaging/mapping.py` and `interferometer/mapping.py` (0.96). Witness:
  `inversion/inversion/imaging/test_imaging.py` (14), `test_sparse_numba_operated_memo.py`,
  `test_curvature_matrix_func_list_blocks.py`, `test_factory.py`. Gotcha: pytree registration
  flattens `__dict__`, so the base must add no instance attributes.
- **A11 — docstrings.** The paragraph "Parameters / linear_obj The linear object (e.g. a ``Mapper``)
  which uses these weights…" appears 16× across 15 regularization files; the two-mapper example 10×
  in 7 inversion files; the linear-algebra paper reference 10×; the regularization-weights
  definition 9×; the curvature-matrix definition 8×. Write each once on the owning base
  (`AbstractRegularization`, `AbstractInversion`, `AbstractInversionImaging`,
  `MeshGeometryRectangular`, `Array2D`) and leave overrides undocumented (autodoc inherits).
- **A8 — rectangular neighbours.** `inversion/mesh/mesh_geometry/rectangular.py:9-304`: six
  corner/edge/centre helpers of ~12 numpy lines each plus a 20-line docstring copied 6×, called in
  sequence by `rectangular_neighbors_from`. One `np.where` over a `(rows, cols)` index grid gives the
  same `[total_pixels, 4]` tables; `test_rectangular.py` asserts the literal tables.
- **A2 — util twins.** `curvature_matrix_with_added_to_diag_from` (`inversion_util.py:39-82` ≡
  `inversion_imaging_util.py:318-369`, plus a numba loop at `inversion_imaging_numba_util.py:469-532`),
  `curvature_matrix_mirrored_from` (`inversion_util.py:84-94` ≡ `inversion_imaging_util.py:276-316`),
  `data_vector_via_blurred_mapping_matrix_from` (one-liner at `inversion_imaging_util.py:198-216`
  vs the numba double loop at `…_numba_util.py:388-419`), `forward_interp`/`_np` and
  `reverse_interp`/`_np` (`interpolator/rectangular.py:65-110`), and a duplicated import block
  (`util/__init__.py:17-22`). Keep one implementation, re-export from both modules (both are
  `aa.util.*`-reachable). Gotcha: unify the JAX test on `xp is np` (the AGENTS.md convention) — the
  twins disagree (`xp.__name__.startswith("jax")`).
- **A7 — `is_jax`.** The identical 6-line `_xp` property is copied 12× (`mesh_geometry/abstract.py:35`,
  `interpolator/abstract.py:26`, `linear_obj/linear_obj.py:34`, `inversion/abstract.py:103`,
  `fit/fit_dataset.py:165`, `decorators/abstract.py:70`, `abstract_ndarray.py:166`,
  `mask/abstract_mask.py:67`, `mask/derive/grid_2d.py:68`, `indexes_2d.py:69`, both simulators) and
  "am I on JAX" is spelled three ways at 73 sites. One `xp_util.is_jax(xp)` / `xp_from(use_jax)`;
  `abstract_ndarray._xp` keeps its tracer-detection override.
- **A12 — bundle.** `Grid2D`/`Grid2DIrregular` share `scaled_maxima`/`scaled_minima`/
  `extent_with_buffer_from`/`squared_distances_to_coordinate_from` (~70 lines → a geometry mixin);
  `Array2D`/`Array1D`/`VectorYX2D` `ones`/`zeros` are `full(1.0/0.0)` (~100 lines, mostly
  docstring); seven `dirty_*` properties on `FitInterferometer` (`fit/fit_interferometer.py:307-361`)
  and six on `Interferometer` (`dataset/interferometer/dataset.py:1167-1221`) are
  `transformer.image_from(visibilities=self.<x>)` (a property factory, names kept); the three
  output decorators repeat one closure and one list-or-single branch (`_make_decorator`,
  `_map_result` in `decorators/abstract.py`, hot path — keep `functools.wraps` and the positional
  `(obj, grid, xp)` order).
- **A13 — tests.** `structures/grids/test_grid_2d_util.py:208` and `:256` both define
  `test__grid_2d_via_shape_native_from` (the first never runs); 25 number-normalised duplicate
  bodies parametrise (`inversion/inversion/test_abstract.py:401/445`, `:419/463`, `:588/603`,
  `test_regularization_util.py`, `fit/test_fit_util.py`, `structures/arrays/test_uniform_2d.py`,
  `test_validate.py`, `layout/test_region.py`, `dataset/imaging/test_dataset.py`). The numba/numpy
  and imaging/interferometer suites are *not* copy-pasted (zero shared test names), so the
  test-count lever in PyAutoArray is small; the big files are long because each test hand-builds
  ~60 lines of inputs (a shared-fixture readability refactor, not a count reduction).

### 3.2 PyAutoGalaxy (outside profiles) and PyAutoLens

- **G3 — dead code.** Zero references across the five repos (src, tests, docs): in
  `autogalaxy/analysis/chaining_util.py` (679 lines, exported as `ag.util.chaining`)
  `extra_galaxies_from` (:198-276), `lp_chain_tracer_from` (:277-320), `basis_no_linear_from`
  (:321-384), `mass_light_dark_lmp_from` (:385-466), `mass_light_dark_from` (:550-627), `link_ratios`
  (:628-679) — 389 lines, 57 % of the module, none unit-tested; `convert.multipole_k_m_phi_m_and_shape_angle_from`
  (`convert.py:386-456`); `model_util.random_galaxy_for_simulation_from` (`:423-467`);
  `fit_interferometer.sparse_dirty_image_from` (`:110-153`); `agg_util.mesh_grids_of_planes_list_from`
  (`:196-232`). In PyAutoLens: `substructure_util.precompute_scaling_matrix` / `los_realizations_to_arrays`
  / `batched_simulate_substructure` (`lens/substructure_util.py:81-99, 245-330`),
  `los.light_cone_radius_at_z` (`:488-527`), `positions_panel.plot_observed_positions` (`:156-191`),
  `analysis/model_util.random_galaxies_for_simulation_from` (`:47-125`). **Workspaces and HowTo
  repos were not on disk**: grep `autogalaxy_workspace`, `autolens_workspace`, `HowToGalaxy`,
  `HowToLens`, `autolens_workspace_test` before deleting the public ones, or ship a five-line
  deprecation shim each.
- **L4 — plot twins.** `autolens/imaging/plot/fit_imaging_plots.py` (1,195 lines): `subplot_fit`
  (:184) vs `subplot_fit_log10` (:402), `subplot_fit_x1_plane` (:336) vs `…_log10_x1_plane` (:536),
  `subplot_fit_combined` (:796) vs `…_combined_log10` (:881) differ only by `use_log10=True` per
  panel; `_plot_source_plane` (:68-183) and `subplot_tracer_from_fit` (:670-795) are copied into
  `interferometer/plot/fit_interferometer_plots.py` (:27-114, :554-689). One private implementation
  with a `use_log10` flag behind the six public names; the source-plane helper moves to
  `autolens/lens/plot/`. Witness: `test_fit_imaging_plots.py`, `test_fit_interferometer_plots.py`;
  the log10 tests parametrise. Gotcha: residual panels stay linear in the log10 variant — thread the
  flag per panel.
- **L1 — potential_correction mixins.** `FitDpsiImaging`, `FitDpsiSrcImaging`
  (`potential_correction/fit.py`), `FitDpsiSrcInterferometer` (`fit_interferometer.py`),
  `IterFitDpsiSrcImaging` (`iterative.py`), `IterFitDpsiSrcInterferometer` (`iterative_interferometer.py`)
  each carry the same `hasattr`-cached `pair_dpsi_data_obj` / `dpsi_gradient_matrix` / `dpsi_points` /
  `dpsi_regularization_matrix` block (`fit.py:105-150, 417-463`; `fit_interferometer.py:214-310`;
  `iterative.py:179-224`; `iterative_interferometer.py:185-232`) and the two iterative classes share
  `_updated_lens_galaxies_from_dpsi` / `_build_pix_src_tracer` / `_init_source_inversion`
  (`iterative.py:226-330` vs `iterative_interferometer.py:257-343`, differing in `masked_imaging`→`dataset`
  and `FitImaging`→`FitInterferometer`). `_DpsiMeshMixin` + `_PixSrcIterMixin` with `cached_property`;
  numpy/scipy-sparse only, no JAX. Witness: the four `potential_correction` test files (24 tests).
  Gotcha: `src_map_mat` / `src_reg_mat` attribute names are read by `solve_joint_optimization`.
- **L7 — thin twins of PyAutoGalaxy.** `max_log_likelihood_fit`, `max_log_likelihood_galaxies|tracer`,
  `real_space_mask`, `adapt_images_from` re-declared in four `Result` modules (`ag imaging/model/result.py:10-44`,
  `interferometer/model/result.py:11-63`, `al imaging/model/result.py:8-45`,
  `interferometer/model/result.py:9-58`); `AnalysisImaging.save_attributes` byte-identical between
  `al imaging/model/analysis.py:240-281` and `ag :228-291` (and the interferometer pair); `SimulatorImaging.via_tracer_from`
  (`al imaging/simulator.py:10-60`) is `ag via_galaxies_from` with `galaxies`→`tracer`; `FitInterferometer`
  re-declares `use_jax`/`_xp` that `AbstractFitInversion` provides (`ag abstract_fit.py:36-45`), and
  `_xp` is defined 8× across the two libraries; `al util/__init__.py` is `ag util/__init__.py` plus one
  line. Gotchas: `ag Result.max_log_likelihood_galaxies` calls `analysis.galaxies_via_instance_from`,
  which PyAutoLens analyses do not define — keep the override; `FitInterferometer` is
  pytree-registered, so removing the `use_jax` leaf changes its flatten — verify with the parity
  script.
- **G10 — visualizer and analysis twins.** `al AnalysisImaging.log_likelihood_function`
  (`imaging/model/analysis.py:85-146`) ≡ `AnalysisInterferometer` (`:123-184`); `shared_state_from`
  differs only in the `Preloads*` constructor; the two `Visualizer.visualize` bodies share the
  fit → positions → inversion-guard → tracer → galaxies → inversion structure. Move
  `log_likelihood_function` to `al AnalysisDataset`, abstract `_preloads_from_fit`, one
  `_visualize_tracer_and_inversion` helper. Gotcha: the interferometer visualizer swallows an
  `IndexError` the imaging one does not — keep per-class behaviour behind a flag.
- **G2 — pytree scaffold.** Five `_register_fit_*_pytrees` staticmethods repeat a 25-line skeleton
  (module flag, `global`, lazy imports, autofit cross-population, 2–3 `register_instance_pytree`
  calls): `ag imaging/model/analysis.py:179-227`, `interferometer/model/analysis.py:398-441`,
  `ellipse/model/analysis.py:185-242`, `al imaging/model/analysis.py:282-331`,
  `interferometer/model/analysis.py:275-319`; `autolens/jax/registration.py:77-134` re-declares the
  three private helpers of `autogalaxy/jax/registration.py:58-115` (docstring-only diff). One
  `register_fit_pytrees(fit_cls, no_flatten, extra)` in `autogalaxy/analysis/jax_pytrees.py`; import
  the helpers. JAX-only: validate with the workspace_test parity scripts; keep registration lazy and
  the `ImportError` fallback.
- **G6 — aggregators.** `_fit_imaging_from` / `_fit_interferometer_from` (both libraries) and
  `_ellipses_from` / `_multipoles_from` have identical bodies modulo the loader and class
  (`ag aggregator/imaging/fit_imaging.py:32-104` vs `interferometer/fit_interferometer.py:33-107`;
  `al aggregator/fit_imaging.py:33-102` vs `fit_interferometer.py:34-103`; `ellipse/ellipses.py:29-77`
  vs `multipoles.py:30-80`); eight `*Agg` classes carry ~45 lines of docstring around a 5-line
  method. Two helpers in `agg_util.py` taking `fit_cls` as a parameter (the lazy import avoids a
  cycle). Names stay; the private `_x_from` functions are imported across modules, so keep them as
  wrappers.
- **G5 — latent.** `_maybe_magzero_warn` and `latent_keys_enabled` are re-declared in
  `autolens/analysis/latent.py` (:80-101, :485-516) with a zero-line diff from
  `autogalaxy/imaging/model/latent.py` (:30-51, :133-165); the four µJy functions re-implement
  `flux_mujy_via_ab_mag_from(ab_mag_via_flux_from(linear(fit), magzero))` inline instead of
  wrapping the linear functions that already exist. Import + a `_mujy_variant` factory; `xp` must
  thread (`xp.nan`).
- **G8 — lens_calc.** `autogalaxy/operate/lens_calc.py` (2,347 lines): tangential/radial
  critical-curve, caustic and area methods are identical bodies with one function swapped
  (`:1063-1236`); six `*_via_zero_contour_from` wrappers each forward the same six kwargs
  (`:1741-1958`), repeated again by the Einstein-radius variants (`:1959-2054`). Private
  `_…_from(kind, …)` behind the public names; keep `@evaluation_grid` on the public methods.
  Witness: `test_autogalaxy/operate/test_deflections.py` (41), of which 14 parametrise to 7.
- **G9 — instance → galaxy list.** The `galaxies + extra_galaxies + scaling_galaxies` fold and the
  subhalo-centre relocation appear in `ag analysis/analysis/analysis.py:59-91`,
  `al analysis/analysis/lens.py:83-145`, `ag aggregator/galaxies.py:31-80`, `al aggregator/tracer.py:32-111`
  (the last marked `# TODO : These are ugly as hell`). One `galaxy_list_via_instance_from` in
  autogalaxy and one `tracer_via_instance_from(instance, cosmology, xp=np)` in `autolens/lens/tracer_util.py`.
  Keep the in-place mutation of `instance.galaxies.subhalo.mass.centre` (read back downstream).
- **G12 — bundle.** `Tracer._validate_galaxies` vs `_validate_fields` (`lens/tracer.py:183-298`,
  "mirrors" by its own docstring) → `_validate_members(kind)`, and 223 lines of validation helpers
  out of `tracer.py`; `extract_attribute` ×3 (`galaxy/galaxies.py:344-386`, `mass_aggregate.py:154-197`,
  `lens/tracer.py:1325-1380`) — note the Galaxy version filters `None`s and the others do not, so
  the shared helper keeps a flag; `SubhaloGridSearchResult` vs `SubhaloSensitivityResult`
  (`lens/subhalo.py:53-156`, `sensitivity.py:51-148`) → a mixin with a `_pixel_scales` hook; four
  identical 3-line coercions in `point/plot`; `_is_external_shear` defined twice in `twins/`.
  Already done, no action: the `autogalaxy/plot/plot_utils.py` vs `util/plot_utils.py` twin named in
  `draft/refactor/autogalaxy/critical_curves_dispatch_cluster.md` was removed in commit `247e4a3a`;
  that prompt's "engine dedupe" item should be re-scoped to G8.
- **G11 — tests.** `test_autolens/imaging/test_fit_imaging.py:270-580`: 11
  `test__figure_of_merit__sub_2_oversampling__*` functions are copies of the sub-1 tests above them
  (first pair differs by 11 lines) → one parametrised body. `test_galaxy.py` (19), `test_galaxies.py`
  (21), `test_tracer.py` (16) re-test the same `operated_only` ×3, list ×3, dict ×3, sum, `cls_list_from`,
  `extract_attribute` semantics against the same profiles → one `test_container_quantities.py`
  parametrised over the three containers, keeping one tracer-specific lensed-plane test per
  quantity (≈ −20 to −25 functions). Twelve `sparse_operator` / `array_free_dataset` tests in
  `al test_fit_interferometer.py` share names and bodies with the `ag` ones modulo `Galaxies`→`Tracer`
  (they test autoarray's sparse path) → three smoke tests. Log10 plot pairs and the four
  `potential_correction` mesh-property tests parametrise.

### 3.3 Cross-cutting

- **X6 — conftest wrappers.** `test_autoarray/conftest.py` has 45, `test_autogalaxy/conftest.py` 60
  and `test_autolens/conftest.py` 54 fixtures of the exact shape
  `@pytest.fixture(name="X") / def make_X(): return fixtures.make_X()` (159 wrappers, ≈ 640 lines).
  A six-line loop over `dir(fixtures)` binds the same names into module globals; the handful of
  non-trivial fixtures (`set_config_path`, `make_plot_patch`, `remove_logs`, `make_acs_quadrant`,
  `_regime_independent_test_output`) stay explicit. Fixture names unchanged; zero tests touched.
  Five `make_*` functions in `autoarray/fixtures.py` are not wired at all — two are dead (A1), three
  are used downstream and stay.
- **Docstrings** are 37 % of PyAutoArray, 37 % of PyAutoGalaxy, 29 % of PyAutoLens. A11 is the
  measured, paragraph-level de-dup; a broader "constructor kwargs documented once on the class, not
  again on every forwarding `__init__`" policy is what the profiles epic applies and what the mesh /
  regularization classes need. That is a style decision for the human, applied per package, and is
  the only lever beyond the table above that moves the total by thousands of lines.

## 4. Flagged, not proposed (API-risk or too-large)

- `structures/triangles/array.py` + `coordinate_array.py` (JAX, 1,147 lines) vs `array_np.py` +
  `coordinate_array_np.py` (554): only ~150 lines are literal twins; the rest differ algorithmically
  (fixed-shape padding for JIT), and `ArrayTrianglesNp` is used in PyAutoLens — an `xp`-parametrised
  merge is medium–large and API-risk.
- `inversion_imaging_numba_util.py:469-920` four `curvature_matrix_via_sparse_operator_*` variants: a
  size-heuristic dispatcher; only the dead reference copy (A1) is removable without touching numerics.
- `nufft_precision_operator_via_{nufft,np,jax}_from` and `Imaging.apply_sparse_operator` vs
  `apply_sparse_operator_cpu`: twins by name, different algorithms/contracts (similarity 0.07–0.48).
- `aa.preprocess` (nine functions referenced only by tests), `aa.util.*` modules, `aa.grid_dec`: public
  documented names with zero downstream uses in the clones — removal is a workspace-grep-then-deprecate
  decision, not a refactor.
- `ResultInterferometer.adapt_images_from(use_model_images)` ignores its argument in both libraries
  (`ag :39-63`, `al :37-58`) — a behaviour question for `/bug` or `/feature`, not a refactor.
- Very long functions (`inversion_util.reconstruction_positive_only_from` 292 lines with warm-start
  state threaded through; `plot/array.py:33 plot_array` 275; `sparse_terms_from_chunks` 234;
  `fnnls_cholesky` 211): splitting is readability-only, no line or test payoff, and the first carries
  nnls state — leave.
- Everything in `draft/refactor/autogalaxy/profiles_unified_api_report.md` §5 (composition-time
  profile variants): a feature epic on ruling D1.

## 5. How to run this

Every candidate is behaviour-preserving by construction and routes as `refactor/` at the `safe`
cap: `/intake` formalises one prompt from its row (the witness column is the `Witness:` header),
`/refactor` plans it, `/start_dev --auto` runs it to an open PR, merge is the human's at `glance`.
Order of value: the profiles epic first (one repo, largest lever, its own ledger), then the
PyAutoArray inversion candidates (largest repo lever), then the Galaxy/Lens twins. Never more than
one open refactor PR per repo at a time — the golden-file and parity witnesses are per-repo and
conflict otherwise.
