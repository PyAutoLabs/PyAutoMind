# The interferometer preload on CPU: builder timings and the adjoint-NUFFT construction

Type: research
Target: autolens_profiling
Repos:
- @autolens_profiling
Themes:
- numba-cpu
- interferometer
- nufft
Difficulty: medium
Autonomy: supervised
Priority: high
Epic: numba-interferometer-revisit
Phase: 3
Filed: 2026-09-07
Issued: 2026-09-08

Phase 3 of `draft/research/autolens_profiling/numba_interferometer_likelihood_revisit.md`.
The user asked for the preload curvature build to be treated as its own line of work: it has
a dedicated CPU approach but never got near GPU speed. Requires phase 1's pack. PyAutoArray
stays read-only.

## The hypothesis (design review 2026-09-07 — confirmed on paper, to be verified)

The preload is `preload[i,j] = Σ_k w_k cos(2π Δ_rad(−j·u_k + i·v_k))`, `w_k = 1/σ_r,k²`,
over the doubled `(2Ny, 2Nx)` offset grid at the dataset pixel scale. That is `Re` of a
**type-1 (adjoint) NUFFT** of the real weights onto a `2Ny×2Nx` mode grid — O(K·nspread² +
4M log 4M) ≈ 1–3 s at alma, versus 4·M·K = 7.8e10 cosines (400–800 s) for the recovered
numba and the current NumPy/JAX chunked builders. At alma_high the brute force is 2–4 h and
the NUFFT ~10 s.

Construction: call `nufftax.nufft2d1(_x, _y, w, n_modes=(2Nx, 2Ny), eps, +1)` directly from
the pack with the transformer's own `_x/_y` (`autoarray/operators/transformer.py:334-335`),
then `ifftshift` the centred modes to wraparound offsets and pin the index permutation
against the fp64 brute force at sma. Do not go through `TransformerNUFFT.image_from` — it
applies a half-pixel `_shift` (`:451`) and a row flip (`:462`) that would have to be undone.

## Steps

1. `scripts/interferometer/likelihood_breakdown/preload_numba.py`: time the builders
   {recovered numba `w_tilde_curvature_preload_interferometer_from`,
   `nufft_precision_operator_via_np_from`, `nufft_precision_operator_via_jax_from` (CPU),
   type-1 NUFFT} at sma and alma. Run each O(N·K) builder **once** at alma and cache the
   array to disk; never run them at alma_high. Run the NUFFT route at alma_high too, to show
   the scaling.
2. Parity discipline: sma elementwise `rtol=1e-10` against the brute force; alma
   `max|Δ| ≤ 10·eps·preload[0,0]` (peak-scaled — type-1 error is bounded relative to
   Σ|w_k| = the peak, and the fp64 brute force itself is only ~1e-13·peak); downstream
   `log_evidence` through the pack's inversion at `rtol=1e-6`. Sweep
   `eps ∈ {1e-6, 1e-9, 1e-12}` and report the eps that holds the log-evidence pin.
3. JSON under `results/breakdown/interferometer/preload_*`; a preload section in
   `results/notes/numba_interferometer_verdict.md`; a PyAutoArray follow-up prompt via
   `/intake` if the NUFFT route holds the pin and is materially faster (it replaces
   `nufft_precision_operator_from`'s chunked cosines for every backend, and the dirty image
   already goes through the same adjoint).

## Acceptance

- The NUFFT-built preload passes the sma and alma pins, with the eps sweep recorded.
- Builder timings at sma and alma committed; the alma brute-force array cached, not
  recomputed.
- Verdict note updated; follow-up filed only if justified.
