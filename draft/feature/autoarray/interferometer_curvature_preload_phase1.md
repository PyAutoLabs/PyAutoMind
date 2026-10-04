# Fixed-mapper interferometer searches, phase 1: pin the `preloads.curvature_matrix` reuse invariant and measure it on a CPU breakdown cell

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- interferometer
- pixelization
- inversion
- likelihood-profiling
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Witness: (1) correctness: on a fixed instance whose mapper is held fixed and whose regularization coefficients differ from the ones F was built at, `log_evidence` / `figure_of_merit` with `aa.PreloadsInterferometer(curvature_matrix=F)` injected matches the no-preload build bit-identically (assert `abs(Δ) <= 1e-9` nats), on `InversionInterferometerSparse(xp=np)` and `InversionInterferometerSparseNumba`; (2) timing: the alma (and sma) Delaunay-1500 and rectangular CPU breakdown cells gain a `fixed_mapper` lever arm whose per-call saving matches the same JSON's F row within noise, with the ≤ 1e-9 nats match recorded in the row. No GPU.
Review-minutes: 10
Unattended: ready
Lane: local-dev
Epic: interferometer-likelihood-campaign
Filed: 2026-10-04

Phase 1 of the Pulse task
[interferometer_fixed_mapper_curvature_preload](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/interferometer_fixed_mapper_curvature_preload.md)
(lever 3 of autolens_profiling#320, `results/notes/interferometer_mesh_a100_breakdown_2026_09.md`
"Ranked levers" §3). That task is `needs-slicing`; this is the bounded first slice.

## Context

**The hook already exists.** `InversionInterferometerSparse.curvature_matrix`
(PyAutoArray `autoarray/inversion/inversion/interferometer/sparse.py:164-165`) returns
`self._preloads.curvature_matrix` untouched when one is injected. The numba class
`InversionInterferometerSparseNumba` (`interferometer_numba/sparse.py:22`) subclasses it and does
not override `curvature_matrix`, so it honours the preload too. The dense
`InversionInterferometerMapping.curvature_matrix` (`interferometer/mapping.py:77`) ignores
preloads. The container is `aa.PreloadsInterferometer(curvature_matrix=...)`
(`autoarray/preloads/interferometer.py`). It reaches the inversion through
`AnalysisInterferometer.fit_from(instance, preloads=...)` → `FitInterferometer(preloads=...)`
(PyAutoLens `autolens/interferometer/model/analysis.py:229-273`).

**Only the datacube uses it today.** `AnalysisInterferometer(shared_preloads=True)` builds F once
per evaluation in `shared_state_from` (`analysis.py:185-227`) and shares it across channels. That
reuses F across channels within one call. Nothing reuses F across calls.

**The invariant.**

- F = Aᵀ W~ A (plus the `no_regularization_add_to_curvature_diag_value` diagonal add) depends
  only on the mapping matrix A and on W~. A depends on the mapper: the traced grid (mass and
  `fields`), the image-plane mesh (adapt image and image-mesh parameters) and the source-mesh
  parameters. W~ (`dataset.sparse_operator`) depends only on `uv_wavelengths`, the noise map and
  the real-space mask, which are fixed for the dataset.
- So when the mass, the fields, the adapt images and every mesh/image-mesh parameter are fixed,
  F is constant across calls and can be preloaded. The data vector D = Aᵀ(dirty image) is constant
  too.
- Per call you must still recompute the regularization matrix H (its coefficients are the free
  parameters), F + H and its solve, log det(F + H), log det H and the reconstruction-dependent χ²
  terms. The preloaded F must be the post-diag-add `inversion.curvature_matrix` of the same
  linear-object list, because the preload short-circuits the diagonal add at `sparse.py:183-188`.

**Do not preload `mapper_galaxy_dict` for this.** `to_inversion.py:418-419` (PyAutoLens) would
return the preloaded mappers, but a `Mapper` carries its `regularization` object
(`autoarray/inversion/mappers/abstract.py:24`). Preloading it would freeze the regularization
coefficients the search is fitting. The phase-1 preload key is `curvature_matrix` only, and the
mapper is rebuilt every call.

**Census finding: no production stage qualifies as configured.** The interferometer SLaM
`source_pix_2` (autolens_workspace `scripts/interferometer/features/pixelization/slam.py:281-348`)
fixes the mass (`source_pix_result_1.instance...mass`, :330), the fields (:342) and the adapt
images. Its mesh, however, is `af.Model(al.mesh.RectangularBilinearAdaptImage, shape=mesh_shape)`
(:602), which leaves `weight_power` (Uniform 0–10) and `weight_floor` (LogUniform 1e-5–1)
free. The default priors are at PyAutoGalaxy
`config/priors/mesh/rectangular_bilinear_adapt_image.yaml:22,32`. Both parameters feed
`mesh_weight_map_from` (`mesh/mesh/rectangular_rtu_adapt_image.py:96-116`), which feeds the
rank-CDF interpolator (`mesh/interpolator/rectangular.py:186-305`). They change the mapping, so
the mapper is not fixed in that stage. A qualifying configuration is a regularization-only
search: mass, fields and adapt images fixed, plus mesh parameters fixed as instances (e.g.
Delaunay + Hilbert(pixels=N) on a fixed adapt image, or an AdaptImage rect mesh with
`weight_power` / `weight_floor` fixed). Phase 1 measures that configuration. Whether a pipeline
should add such a stage is a later-phase decision.

## What

1. **PyAutoArray: pin the invariant with tests (no behaviour change on the default path).**
   - Unit test in `test_autoarray/inversion/inversion/interferometer/`. Build a sparse-path
     inversion with a fixed mapper and regularization coefficients θ₁ and take
     `F = inversion.curvature_matrix`. Build a second inversion with the same mapper at θ₂ ≠ θ₁:
     once fresh, and once with `preloads=aa.PreloadsInterferometer(curvature_matrix=F)`. Assert
     `log_evidence` agrees to `<= 1e-9` (expect exact equality), on both the `xp=np` sparse and the
     numba classes. Also cover the `no_regularization_index_list` case, i.e. F carries the diag
     add.
   - Cheap guard in `sparse.py`: an injected F whose shape is not
     `(total_params, total_params)` raises a clear `InversionException` naming the fixed-mapper
     contract, instead of an opaque broadcast error later. Shape check only, no hashing.
   - Docstring on `PreloadsInterferometer` / `AbstractPreloads.curvature_matrix`: state the
     fixed-mapper invariant above, the post-diag-add requirement and the
     "never `mapper_galaxy_dict` when regularization is free" warning.
2. **autolens_profiling: a `fixed_mapper` lever arm on the CPU breakdown cells.** Add it to the
   shared harness `scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py`, alongside
   the #332 `--levers threads,memo,logdet,marshal` arms, so that
   `scripts/interferometer/likelihood_breakdown/{delaunay,pixelization}_numba.py --levers fixed_mapper`
   runs it.
   - The arm holds mass and mesh fixed and draws an instance stream that varies only the
     regularization coefficients.
   - It builds F once, outside the timed region, from the first instance's fit, and times
     `FitInterferometer(..., xp=np, preloads=PreloadsInterferometer(curvature_matrix=F))` against
     the library row on the same stream. Do not time the arm against the existing iid
     (mass-varying) stream: there F is not constant, and the comparison would be invalid.
   - It records the per-call time, the saving against the same JSON's F row and the max
     |Δ figure_of_merit| over the stream.
   - Run alma and sma for Delaunay-1500 and rectangular 39×39 on CPU: laptop, or the RAL `ral`
     partition only under the CPU-partition rule; never `gpu`. Commit the JSON(s) and regenerate
     the README dashboards (`build_readme.py --check`).
3. Append a one-paragraph result to the Pulse task (or a ledger note in autolens_profiling)
   covering the measured CPU saving, the 1e-9 match and the census finding above.

## Done when

- The PyAutoArray tests pass, including the exact or `<= 1e-9` nats `log_evidence` match under a
  preloaded F at different regularization coefficients, on sparse NumPy and numba. The shape
  guard raises on a mismatched F. The default (no-preload) path is unchanged: the existing
  interferometer inversion tests pass unmodified.
- autolens_profiling has committed CPU `fixed_mapper` rows for alma and sma, Delaunay and
  rectangular. Each row's max |Δ figure_of_merit| is `<= 1e-9` nats and its saving is reported
  against that JSON's F row (any gap beyond noise is explained).
- The census finding (source_pix_2 frees `weight_power` / `weight_floor`, so its mapper is not
  fixed) is recorded with the citations above.

## Out of scope (later phases)

- **Search-side population (phase 2):** an opt-in on `AnalysisInterferometer`, e.g.
  `fixed_mapper=True`. It would build F once (lazily on the first `log_likelihood_function` call, or
  in `modify_before_fit` from the initial instance), cache it on the analysis and pass it to
  `fit_from(preloads=...)`, reusing the `shared_preloads` plumbing. The user or pipeline asserts the
  invariant. A debug-mode check that recomputes F every k calls is optional.
- **JAX:** `jit` / `jit(vmap)` behaviour, and whether a closed-over F (preloads is
  `no_flatten` aux data in the `FitInterferometer` pytree, `analysis.py:313`) bloats the compiled
  program. A100 and jvla rows (the 91–92 % F share and the 563 → ~53 ms bound) belong there too.
- **Also preloading the data vector D** (it is fixed under the same invariant) and a
  regularization-free mapper preload (rebuilding the mapper geometry costs time every call).
- **A pipeline / SLaM regularization-only stage** with mesh parameters fixed, or fixing
  `weight_power` / `weight_floor` after source_pix_1. That is a workspace science decision.
- **Mixed mapper + MGE / linear-light-profile inversions** (only the mapper–mapper block is
  reusable), the dense `InversionInterferometerMapping` path, and datacube channel sharing
  (already shipped).
