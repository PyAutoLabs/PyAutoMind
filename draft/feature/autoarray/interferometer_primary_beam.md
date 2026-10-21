# Primary beam correction for interferometer datasets, transformers and the sparse w-tilde inversion

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
Difficulty: large
Autonomy: supervised
Priority: high
Community: https://github.com/PyAutoLabs/.github/discussions/35
Status: formalised
Consequence: glance
Witness: tests asserting (i) primary_beam=None and primary_beam=ones leave transformer outputs, sparse and mapping curvature, data vector and fast_chi_squared bit-identical on numpy and under JAX jit, and (ii) with a non-trivial P the sparse curvature equals the brute-force Mᵀ diag(P) W̃ diag(P) M and the data vector equals Mᵀ diag(P) D̃ to 1e-10 on the 7×7 Delaunay fixture
Review-minutes: 8
Unattended: ready
Filed: 2026-10-21
user-facing: true

## Why

Community proposal by @HRSAstro (Ideas & Proposals, 2026-10-07, accepted 2026-10-21). autoarray has no primary-beam handling: the transformer maps the image straight to visibilities, so an inversion reconstructs the apparent sky (P × true sky), which breaks surface-brightness conservation for lens modelling. With P on the image grid the response becomes A' = T P M, so F' = Mᵀ P W̃ P M and D' = Mᵀ P D̃; the w-tilde kernel, dirty image and dᵀN⁻¹d are unchanged. The maintainer's reply fixed the design: P lives on the `Interferometer` dataset as an optional image on the real-space mask and is applied inside both the transformer and the sparse operator, so light profiles, linear light profiles and mappers all see the same P; user-supplied beam image is the core API with a Gaussian helper (FWHM ≈ 1.13 λ/D); mosaics deferred. The contributor's regularisation-wrapper form (P⁻¹ H P⁻¹ on the mesh) is only exact when P is constant across a mesh pixel and evaluates P in the wrong plane for lensed sources, so it is not adopted, but remains expressible via a custom regularisation. Reference snippet: https://github.com/user-attachments/files/33762670/upstream_snippets.py section 7 (`primary_beam_map`, `pb_correct`).

## What to build (survey of main, 2026-10-21; paths under autoarray/)

1. New `dataset/interferometer/primary_beam.py`: `primary_beam_gaussian_from(mask, frequency_hz, dish_diameter_m, pb_factor=1.13, centre=(0.0, 0.0)) -> Array2D` (FWHM = pb_factor·c/ν/D in arcsec, peak 1 at centre, coordinates via `Grid2D.from_mask`); export from `autoarray/__init__.py`.
2. `operators/transformer.py`: `primary_beam=None` on both transformers, stored slim; `with_primary_beam(P)` shallow copy; multiply on the slim grid before the scatter in `visibilities_from` and `transform_mapping_matrix` (DFT and NUFFT, numpy and JAX). `image_from` stays the un-beamed adjoint (D̃ must not change); docstring says so.
3. `dataset/interferometer/dataset.py`: `primary_beam: Optional[Array2D] = None` constructor arg, shape-validated against `real_space_mask` (native or slim accepted), `primary_beam_slim` property; after the transformer is built set `self.transformer = self.transformer.with_primary_beam(P)` (idempotent, safe for lambda-returned transformers); forward P in the pooled-noise branch (~599), `apply_sparse_operator` (~699), `apply_sparse_operator_from_chunks` (~865), `from_sparse_terms`/`from_stream`/`from_fits` (`primary_beam_path`); pass `primary_beam_slim` into the operator constructors (~691, ~859).
4. `inversion/inversion/interferometer/inversion_interferometer_util.py`: `InterferometerSparseOperator` gains `primary_beam_slim: Optional[np.ndarray] = None`, threaded through `from_nufft_precision_operator` and `from_sparse_terms` (SparseTerms and chunk accumulation are beam-independent, unchanged); `sparse_profile_terms_from` applies `image ← P·image` (~2163) so sparse_dirty_image = D̃ − W̃ P i and data_term = dᵀN⁻¹d − 2(Pi)ᵀD̃ + (Pi)ᵀW̃(Pi).
5. `inversion/pixelization/mappers/mapper_util.py`: `slim_weights=None` kwarg on `sparse_triplets_from`, `vals *= slim_weights[slim_rows]` (numpy ~332, JAX ~358), so A' = P·A and the FFT kernels/preloads stay untouched.
6. `inversion/inversion/interferometer/sparse.py`: read `P = getattr(self.dataset.sparse_operator, "primary_beam_slim", None)` (works for PyAutoGalaxy's DatasetInterface); pass as `slim_weights` in `_sparse_triplets_slim_from` and `_sparse_triplets_curvature_from`; scale linear-func mapping matrices by `P[:, None]` in the data vector (~123) and mixed blocks (~443-445). Model visibilities via `transformer.visibilities_from` pick P up automatically; `mapped_reconstructed_data_dict` stays the un-beamed true-sky image.
7. `fit/fit_interferometer.py`: apply P in `dirty_model_image_natural_from` (~52).
8. `dataset/interferometer/simulator.py`: `primary_beam=None` arg, add to the pytree `no_flatten` list, `with_primary_beam` on the built transformer, forward P to the returned Interferometer.
9. Dense path: `operated_mapping_matrix_override` docstring states P is the caller's job.
10. PyAutoGalaxy: no fitting changes (DatasetInterface receives the dataset's transformer and sparse_operator). Follow-up prompt: persist P in `analysis.py` save_attributes and the aggregator rebuild.

## Tests

- P=None / P=ones parity, bit-for-bit (`np.array_equal`) on numpy and jit, extending test_interferometer.py ~878 and ~1349.
- Brute force on the 7×7 Delaunay fixture with a non-trivial P: dense W̃ from DFT `transform_mapping_matrix(identity)` with P=None; sparse curvature vs Mᵀ diag(P) W̃ diag(P) M; data vector vs Mᵀ diag(P) D̃; func_list+mapper, x2 mappers, func-list-only.
- Dense (mapping) vs sparse with P, DFT vs NUFFT, array-free `from_sparse_terms(primary_beam=)` vs in-memory.
- Transformer: `visibilities_from(img)` with P equals un-beamed `visibilities_from(P·img)`; same for mapping matrix; DFT, NUFFT, JAX.
- Dataset propagation through all four re-construction sites; shape mismatch raises; `dirty_image`/`dirty_beam` unchanged by P.
- Simulator: P-simulated visibilities equal un-beamed simulation of P·image. Gaussian helper: peak 1 at centre, 0.5 at FWHM/2.

## Acceptance

- Witness passes; nojax leg imports clean. Workspace example (`interferometer/advanced` primary-beam snippet) and docs as a follow-up workspace prompt after the library PR ships. Update the contributor on the thread at PR-open and at release.
