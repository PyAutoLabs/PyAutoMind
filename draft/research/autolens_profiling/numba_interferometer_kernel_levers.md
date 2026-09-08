# Numba vs JAX-CPU interferometer curvature: synthetic bake-off, kernel levers, and the reinstatement verdict

Type: research
Target: autolens_profiling
Repos:
- @autolens_profiling
Themes:
- numba-cpu
- interferometer
- likelihood-profiling
Difficulty: hard
Autonomy: supervised
Priority: high
Epic: numba-interferometer-revisit
Phase: 2
Filed: 2026-09-07

Phase 2 of `draft/research/autolens_profiling/numba_interferometer_likelihood_revisit.md`.
Requires phase 1's pack (`scripts/misc/numba_interferometer/`). PyAutoArray stays
read-only; anything the verdict justifies is filed as a follow-up prompt.

## Framing (from the 2026-09-07 design review; numbers are estimates to reproduce)

`W~` has no compact support for an interferometer, so the recovered scatter kernel is
O(N^2 P^2) and the FFT convolution is O(S·M log M) (M = extent Ny·Nx). A single-thread
synthetic bake-off on an i9-10885H gave, for one curvature build at Delaunay S=1500, P=3:

| geometry (N_pix, extent, K) | recovered scatter | numba direct extent-conv | scipy `rfft2` conv | complex `fft2` conv (= JAX algorithm) |
|---|---|---|---|---|
| sma (3.9k, 70², 190) | 0.36 s | 0.11 s | 0.48 s | 0.74 s |
| alma (15k, 140², 1M) | 7.6 s | 1.65 s | 1.99 s | 3.2 s |
| alma_high (62k, 280², 5M) | ~120 s | 28 s | 7.9 s | 17 s |

Crossover rule: FFT wins once a source column touches more than ~35–45 image pixels
(nnz/column is 7.7 at sma, 31 at alma, 123 at alma_high). The winning numba form is a
**direct extent-grid convolution** (the imaging two-stage source-space accumulator fused with
extent-flat indexing: `a_i0 = (W~A)[i0,:]` accumulated over the rectangle, then row AXPYs),
not the recovered pair-loop. Symmetric halving (2×) and hoisted gathers (1.1–1.3×) apply
only to the pair-loop form. A dense `W~` BLAS route is dominated at every geometry (1.9 GB
streamed per call at alma) — oracle only. And the library's `apply_operator` pads real
input to complex and calls `fft2`; a real `rfft2`/`irfft2` path is 1.6–2.2× faster for
every user on every backend — that is the fair baseline, not a lever.

## Steps

1. **Synthetic bake-off** — `scripts/misc/numba_interferometer/bakeoff.py`, no PyAutoLens
   stack: synthetic COO triplets at sma / alma / alma_high × {Delaunay S=1500 P=3, rect
   S=784 P=4} × kernels {recovered scatter, +hoisted gathers, +symmetric halving, two-stage
   pair-loop, direct extent-grid convolution, NumPy `rfft2` convolution, complex `fft2`
   convolution}; 5 reps, single thread. Every variant parity-pinned to the reference kernel
   (`rtol=1e-10` on F) before its time is believed; a broken constant must fail the pin.
   **Kill gate:** if no numba variant beats `rfft2` by >1.3× at sma *or* alma, stop the
   numba lever work and go straight to step 4.
2. **Thread scaling** — direct-conv `prange` and `rfft2 workers=` at 1 vs 8 threads at sma
   and alma; record the pool caveat (no kernel threads under a Nautilus pool).
3. **In-situ** — add the surviving variants to the pack's `kernel=` switch; run
   `delaunay_numba.py` and the existing JAX `delaunay.py` on sma and alma with JAX pinned to
   one thread (`XLA_FLAGS=--xla_cpu_multi_thread_eigen=false
   --xla_force_host_platform_device_count=1`, recorded per arm — `OMP_NUM_THREADS=1` does not
   pin XLA). Paired B/A/B/A, arms interleaved (laptop throttling), first round discarded
   (numba cache recompile on arm switch). Control rows: `log det (F+H) [Cholesky]` (arm-
   invariant, magnitude-matched) plus a fixed-size `dgemm` micro-benchmark at the head and
   tail of every arm as a machine-speed normaliser.
4. **Verdict** — `results/notes/numba_interferometer_verdict.md`: per-geometry tables, the
   measured crossover, the recommendation among (a) reinstate numba as
   `autoarray/inversion/inversion/interferometer_numba/` with the direct-conv kernel,
   (b) keep as profiling pack, (c) drop, (d) the real-FFT (`rfft2`/`irfft2`) change to
   `InterferometerSparseOperator.apply_operator` (~10 lines, every backend), possibly with
   a NumPy `rfft2` no-JAX CPU path. File follow-up prompts via `/intake` only for what the
   numbers justify.

## Acceptance

- Bake-off JSON + in-situ JSON/PNG committed under `results/breakdown/interferometer/`.
- Every timed variant has a passing parity pin and a recorded control.
- The verdict note names the recommendation and the numbers that decide it.
