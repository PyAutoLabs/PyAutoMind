# Streaming visibilities for memory efficiency on the sparse interferometer path

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
Themes:
- interferometer
- sparse-operator
- memory
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: active
Issued: 2026-09-29
Consequence: glance
Witness: a fit built from chunked visibilities (`Interferometer.from_stream` / `apply_sparse_operator_streamed`) matches the in-memory `apply_sparse_operator` fit to 1e-8 in chi_squared, model image, residual map and dirty image; `fast_chi_squared` and `noise_normalization` read precomputed scalars when present; a pixelization-only `FitInterferometer` allocates no N_vis arrays per evaluation.
Review-minutes: 10

Source: GitHub Discussion https://github.com/orgs/PyAutoLabs/discussions/13
("Streaming visibilities for memory efficiency", Ideas & Proposals, HRSAstro, 2026-09-15).
Reference implementation: https://github.com/HRSAstro/pyuvimage `src/pyuvimage/streaming.py`
(TermsAccumulator / accumulate_sparse_terms / stub_dataset_from_terms) and
`tests/test_streaming.py::test_streamed_fit_matches_the_in_memory_sparse_fit`.

## Request (verbatim from the discussion)

### Problem

On the sparse path (Interferometer.apply_sparse_operator + InversionInterferometerSparse) the inversion itself is independent of the number of visibilities, but the dataset and the fit are not: every visibility stays resident for the whole run, and every likelihood evaluation still does O(N_vis) work. Building the sparse operator by streaming the visibilities once, and carrying the handful of per-visibility sums the fit needs alongside it, makes both the resident memory and the per-likelihood cost independent of N_vis. We have this working in [pyuvimage](https://github.com/HRSAstro/pyuvimage) on top of autoarray's sparse inversion, verified against the in-memory sparse fit to 1e-8, and it would be a natural addition upstream.

**What the current sparse path holds and computes**

Resident for the whole fit, per visibility (as Interferometer is built today):

data (complex128, 16 B), noise_map (complex128, 16 B), uv_wavelengths (2 x float64, 16 B) — 48 B/visibility minimum, ~10 GB at 2e8 visibilities, before from_fits load temporaries and the NUFFT plan.

Per likelihood evaluation, all O(N_vis) in time and transient memory, even though the sparse inversion has already reduced the data to W~ and the dirty image:

FitInterferometer.profile_visibilities allocates an N_vis array (Visibilities.zeros when there are no light profiles) and profile_subtracted_visibilities = data - profile_visibilities allocates another (autogalaxy fit_interferometer.py).
fast_chi_squared recomputes sum(d_r^2/sigma_r^2) + sum(d_i^2/sigma_i^2) over the full arrays on every call (inversion/interferometer/abstract.py), a data-only constant.
noise_normalization recomputes sum(log(2 pi sigma^2)) over the full noise map on every call.
apply_sparse_operator itself needs the whole dataset in memory to form data.real * noise_map.real**-2 + 1j * ... and the np.allclose(noise_real, noise_imag) check.

So the sparse path removes N_vis from the linear algebra but not from the process: RSS scales with N_vis and the fit does several full passes over the visibilities per likelihood call.



### Proposed Solution

**What streaming looks like**

Read the visibilities once in chunks (from .npz, FITS, or a memory-mapped source) and accumulate, per chunk, every quantity downstream of the data that is a sum over visibilities:

quantity  |  accumulated as  |  consumer
W~ (2Ny, 2Nx)  |  nufft_precision_operator_from per chunk, summed (it is sum_k w_k cos(...))  |  curvature matrix
dirty image F^H W d  |  adjoint of d_r/sigma_r^2 + i d_i/sigma_i^2 per chunk, summed  |  data vector
sum d^2/sigma^2  |  scalar  |  fast_chi_squared term 3
sum log 2 pi sigma^2  |  scalar  |  noise_normalization
sum w, dirty beam  |  adjoint of w per chunk	 |  normalised dirty/residual images

Then discard the chunk. The fit is built from InterferometerSparseOperator.from_nufft_precision_operator(W~, dirty_image) plus the two scalars; chi_squared is s^T F s - 2 s^T D + const with no visibilities touched, and the residual dirty image is dirty(data) - W~ * (M s) via the same FFT-multiply the operator already uses. Nothing per visibility survives the load.

Measured in pyuvimage (peak RSS of the accumulation from a compressed .npz, 400-pixel image, 4096-visibility chunks, fresh process each):

N_vis | peak RSS over baseline | resident if held (48 B/vis, autoarray minimum)
5e5 | 36 MB | 24 MB
1e6 | 36 MB | 48 MB
2e6 | 36 MB | 96 MB
4e6 | 36 MB | 192 MB

Flat across 8x; the in-memory path grows linearly and, on a real 2e8-sample ALMA MFS cube, is the difference between a laptop and a node

Parity: the streamed fit matches the in-memory sparse fit to 1e-8 in chi^2, model image, residual map and dirty image (W~ to 2e-16, dirty image to 5e-16). It extends directly to per-channel (cube) fits, since the MFS terms are the sum of the channel terms, and to phase-centre shifts applied chunk by chunk.

**Suggested shape upstream**

1. Interferometer.apply_sparse_operator (or a new Interferometer.from_stream(...) / apply_sparse_operator_streamed(...)) that accepts an iterable of (uv_wavelengths, data, noise_map) chunks, accumulates W~, the dirty image, sum d^2/sigma^2 and sum log 2 pi sigma^2, and returns a dataset that carries those scalars instead of the visibility arrays.

2. fast_chi_squared and noise_normalization read the precomputed scalars when present, rather than reducing the full arrays per call. This alone removes two O(N_vis) reductions from every likelihood evaluation on the current in-memory sparse path as well.

3. FitInterferometer.profile_subtracted_visibilities skipped when there are no light profiles, so a pixelization-only fit does not allocate two N_vis arrays per evaluation.

Item 2 and 3 are independent of streaming and benefit every sparse-path user today.


**Reference implementation**

src/pyuvimage/streaming.py in https://github.com/HRSAstro/pyuvimage — TermsAccumulator / accumulate_sparse_terms (the per-chunk sums), stub_dataset_from_terms (the Interferometer built from the operator alone), and tests/test_streaming.py::test_streamed_fit_matches_the_in_memory_sparse_fit for the parity check. 

### Alternatives Considered

_No response_
