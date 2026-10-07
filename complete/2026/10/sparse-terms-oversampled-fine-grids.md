# SparseTerms oversample=q: fine precision-operator and dirty-image grids for analytic uv-plane components

Completed 2026-10-07 under human `/prm` (PyAutoArray merged 2026-10-07T10:54:57Z, PyAutoGalaxy 2026-10-07T10:55:04Z; Array first).

Merged PyAutoArray#621 (https://github.com/PyAutoLabs/PyAutoArray/pull/621,
merge commit 8a293d2d, head 3c541485) and PyAutoGalaxy#650
(https://github.com/PyAutoLabs/PyAutoGalaxy/pull/650, merge commit 0cee03f2,
head 3e655583); both heads verified ancestors of origin/main. Issue
https://github.com/PyAutoLabs/PyAutoArray/issues/620 closed by "Closes #620";
Shipped comment https://github.com/PyAutoLabs/PyAutoArray/issues/620#issuecomment-6036437461.

`sparse_terms_from_chunks(..., oversample=q, oversample_pad=0.25)` (even q,
NUFFT transformer only) accumulates two fine grids in the same streaming pass:
`precision_operator_fine` (K at arbitrary lags, full native shape plus a
quarter-field lag pad) and `dirty_image_fine` (D at arbitrary positions, twice
the field), carried on `SparseTerms`; `__add__` refuses mismatched `oversample`
or fine/no-fine operands. PyAutoGalaxy persists them as optional
`PRECISION_OPERATOR_FINE` / `DIRTY_IMAGE_FINE` HDUs, written only on request
(`include_fine_grids=True`, not into `dataset.fits` by default); older files
load with the fine grids as None.

Measured cost (100x100 native, 2 chunks x 1e5 visibilities):

| oversample | wall | peak RSS |
|---|---|---|
| None | 2.1 s | 2016 MB |
| q=4 | 5.2 s | 2159 MB |
| q=8 | 5.0 s | 2533 MB |

Source: community GitHub Discussion https://github.com/orgs/PyAutoLabs/discussions/13
(external contributor @HRSAstro, pyuvimage), comment
https://github.com/PyAutoLabs/.github/discussions/13#discussioncomment-18741903 item 1
(technical review Item B1). Depended on `sparse_noise_map_pooling_option` (PyAutoArray#619, merged first).

Deferred, not in scope: B2 `point_column_terms_from` column-terms helper
(positions/widths, FFT-space Gaussian smoothing + quintic spline) — file
separately if wanted.

Not released: reaches users with the next PyAutoArray / PyAutoGalaxy release.

- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/621
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/650

## Original prompt

# SparseTerms oversample=q: accumulate fine precision-operator and dirty-image grids for analytic uv-plane components (streaming P6)

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
Themes:
- interferometer
- sparse-operator
- community
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-10-07
Issued: 2026-10-07
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/620
Difficulty: medium
Consequence: judge
Depends-on: sparse_noise_map_pooling_option (merge first; same repo claim)
Witness: with `sparse_terms_from_chunks(..., oversample=8)` (NUFFT path), (i) `precision_operator_fine` sampled at lags (i q, j q) equals `nufft_precision_operator[i, j]` within the masked extent (mixed rtol/atol per `iiu:529-531`), and (ii) `dirty_image_fine` sampled at native pixel centres equals `dirty_image_native`; today `oversample` does not exist.
Review-minutes: 20
Unattended: ready
Source: GitHub Discussion https://github.com/orgs/PyAutoLabs/discussions/13 (external contributor @HRSAstro, pyuvimage), comment https://github.com/PyAutoLabs/.github/discussions/13#discussioncomment-18741903 item 1; technical review 2026-10-07 (Item B1, accept-with-change).

## Request (verbatim)

> **1. Analytic components on the streamed path**
>
> `sparse_profile_terms_from` covers light profiles evaluated on the image grid, but a component that is analytic in the uv-plane (a point source, or a small Gaussian for a marginally resolved source) needs its terms at sub-pixel positions. All three terms of such a column are values of two image-plane functions that can be accumulated in the same streaming pass:
>
> - K(Δ) = Σ w cos(2π u·Δ), i.e. the precision operator at an arbitrary lag
> - D(x) = Re Σ (d_re/σ_re² + i d_im/σ_im²) exp(2πi u·x), i.e. the dirty image at an arbitrary position
>
> For a unit point at p, the cross-term with the mesh is Mᵀ k_p with k_p[i] = K(x_i − p), the point-point term is K(p − q) and the data term is D(p). [...]
>
> In pyuvimage we accumulate both on grids 8× finer than the image, with one extra type-1 NUFFT per batch for each, and read them with a quintic spline. [...]
>
> - The precision-operator grid needs lags beyond one field width (we pad by a quarter field), and the dirty-image grid needs twice the field. Otherwise Gaussian-widened columns near the edge pick up the wrap-around.
> [...] An optional `oversample=q` in `sparse_terms_from_chunks` that accumulates these two fine grids would be enough for us to drop our own pass. A helper that returns the column terms for given positions and widths would make it general. Our implementation is in `pyuvimage/streamed_points.py` if it's a useful reference.

## What

`iiu` = `autoarray/inversion/inversion/interferometer/inversion_interferometer_util.py` (origin/main lines). `nufft_precision_operator_via_nufft_from` (`iiu:454-624`) already builds W~ as one type-1 NUFFT onto a (2Ny, 2Nx) grid over the **masked extent** (`iiu:2220`), spacing hard-wired to the image pixel (`iiu:580`), Nyquist zeroed (`iiu:621-622`). A fine grid needs a small refactor, not a flag. The maths in the request is right; K uses w only, so it inherits the equal-sigma assumption (hence the dependency).

Scope: B1 only. **Deferred follow-up (not in scope):** B2 `point_column_terms_from(terms, positions, widths, mapping_matrix=None, *, spline_order=5)` helper (FFT-space Gaussian smoothing, quintic spline; not JAX-traceable) — file separately if we want point components in PyAutoLens's own sparse fits.

## Plan

1. Lift the W~ core loop into `_type1_real_grid_from(uv, values, n_modes, pixel_scale_radians, eps, chunk_size, centred, zero_nyquist)`; W~ calls it unchanged (existing tests pin it).
2. API: `sparse_terms_from_chunks(..., oversample: Optional[int] = None, oversample_pad: float = 0.25)`, pass-through on `from_stream` / `apply_sparse_operator_from_chunks`. Require even q (native centres land on fine grid points) and the NUFFT transformer, else raise.
3. Grids: `precision_operator_fine` shape `(2(Nk+pad)q)^2`, pad = ceil(0.25*max(Nk)), Nk = **full native shape** (points may sit anywhere in the mask), wraparound order like W~, `zero_nyquist=False` (spline reads across lag N). `dirty_image_fine` shape `(2Ny q, 2Nx q)` centred (origin at [Ny q, Nx q]) from the phase-shifted `c = d_re/s_re^2 + i d_im/s_im^2` exactly as `iiu:2233-2236`.
4. `SparseTerms` (`iiu:1880`, frozen dataclass): append `precision_operator_fine`, `dirty_image_fine`, `oversample`, `oversample_pad` (all Optional, None). `__add__` (`iiu:1951`): add `oversample`/`oversample_pad` to the provenance loop (`iiu:1977-1984`) and **refuse** when exactly one side carries fine grids (pyuvimage silently drops them; refusing is our pattern).
5. Accumulation: preallocate the two fine arrays and `+=` in place across chunks; build one `SparseTerms` at the end (do NOT `+` a fresh SparseTerms per chunk, `iiu:2272`, for 100s of MB arrays).
6. Memory/cost (document; consider a memory-estimate log line): 400x400, q=8, 25 % pad → K fine 8000^2 f64 = 512 MB, D fine 6400^2 = 328 MB, plus nufftax 2x-upsampled work grid 16000^2 c128 = 4.1 GB (K) / 2.6 GB (D): peak ~5-6 GB; q=4 ~1.5 GB; contributor's ~112 px at q=8: 40 MB + 26 MB, <0.5 GB work. Two extra type-1 NUFFTs per chunk with FFT cost independent of chunk length (seconds per chunk at 400/q8): document "use large chunks (>= ~1e6 vis) with oversample". JAX: each (K, n_modes, eps) compiles once; ragged last chunk adds signatures — pad to a fixed bucket with zero weights only if measured to matter.
7. PyAutoGalaxy persistence (`autogalaxy/interferometer/model/analysis.py:40-66`, writer ~:69, loader `autogalaxy/aggregator/interferometer/interferometer.py:62-111`): HDUs `PRECISION_OPERATOR_FINE`, `DIRTY_IMAGE_FINE` only when present; append `oversample`, `oversample_pad` to `SPARSE_TERMS_SCALARS_ORDER` (append-only, NaN = unrecorded) and header `OVERSAMP`; loader uses `_has_hdu`. **Decision: fine grids are NOT written into `dataset.fits` by default** (~840 MB per search output at 400/q8) — config flag to opt in; consider `aa.SparseTerms.output_to_fits/from_fits` as the cleaner home.

Tests: (i)/(ii) the witness; (iii) chunked == one-shot for both grids; (iv) phase_centre shifts D, not K; (v) `__add__` refuses mismatched q and fine/no-fine; (vi) PyAutoGalaxy FITS round trip incl. an old file without the new HDUs/scalars loading as None; odd q / DFT transformer raise.

Risks: memory and per-chunk FFT cost at large grids; extra JAX compiles per chunk shape; FITS bloat if the default flips.
