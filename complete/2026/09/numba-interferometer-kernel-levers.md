# Phase 2: numba vs JAX-CPU interferometer curvature — the recovered kernel is not worth reinstating, a new extent-grid kernel is, and the biggest CPU win is a real FFT

- **Issue:** autolens_profiling#226 (closed) · **PR:** autolens_profiling#228 (`2f2adf2`, merged 2ad7b8faee0813b159f4a1ed504fc1b072692cd1) — merged 2026-09-07
- **Repos:** autolens_profiling (`scripts/misc/numba_interferometer/{kernels,bakeoff,inversion,preload,test_parity}.py`, `scripts/interferometer/likelihood_breakdown/{delaunay,pixelization}_numba.py`, `results/breakdown/interferometer/`, `results/notes/numba_interferometer_verdict.md`). PyAutoArray read-only.
- **Epic:** `numba-interferometer-revisit` — **phase 2 of 3**; ledger `draft/research/autolens_profiling/numba_interferometer_likelihood_revisit.md`; phase 1 `complete/2026/09/numba-interferometer-pack.md`; phase 3 `draft/research/autolens_profiling/interferometer_preload_cpu.md`
- **Status: SHIPPED.** The question the epic was opened for is answered with measurements; three library follow-ups filed.

## The headline

Nine curvature kernels on identical synthetic triplets at sma / alma / alma_high × Delaunay-1500 / rect-784, each pinned to the recovered kernel on `F` at `rtol=1e-10` before any timing counted (a ×1.01 control fails the pin in every cell), then the survivors in situ on the real likelihood with arms interleaved and `dgemm` / Cholesky control rows. Every number is read from a committed JSON under `results/breakdown/interferometer/`.

| kernel (single thread, s per F build) | sma Delaunay | alma Delaunay | alma_high Delaunay |
|---|---|---|---|
| `reference` (recovered pair loop) | 0.68 | 12.9 | ~207 (extrapolated) |
| `direct_conv` (new extent-grid convolution) | **0.21** | **2.85** | 17.4 |
| `rfft2_numpy` (NumPy real FFT) | 1.27 | 4.40 | **11.0** |
| `fft2_jax` (the library, CPU) | 1.52 | 5.52 | 13.0 |

- **The recovered kernel is not worth reinstating.** It beats a plain NumPy `rfft2` convolution in one of six cells (sma Delaunay, 1.86×) and loses the rest; its only sparsity is the mapper's, `W~` has no compact support for an interferometer, and the pair loop is O(N_pix² P²).
- **`direct_conv` is** — the imaging two-stage accumulator fused with extent-flat indexing. In situ it beats the JAX-CPU `F` row by **7.0× / 4.1× / 2.0× / 1.1×** (sma Delaunay / sma rect / alma Delaunay / alma rect) and the recovered kernel by 2.9–4.8×; at alma_high the FFT wins 1.6×. Measured crossover **≈60 (Delaunay) / ≈77 (rect) non-zeros per source column** (`N_pix·P/S`), ~1.7× above the design review's prior.
- **The largest, cheapest CPU win is not numba.** `InterferometerSparseOperator.apply_operator` pads real input to complex and calls `fft2`; `rfft2`/`irfft2` is exact and **1.27–1.61× less FFT work on every backend**, GPU included, ~10 lines.
- **No-GPU users have no NumPy path today** (every sparse-operator method imports `jax.numpy`); `rfft2_numpy` beats JAX-CPU by 1.10–1.30× at every cell.
- Thread scaling: `direct_conv` `prange` 3.5× (sma) / 4.6× (alma) on 8 threads; `rfft2 workers=8` 1.5× / 2.5× — moot under a Nautilus pool, where the single-thread number is the production number.
- Every arm returns the identical log evidence (sma Delaunay `-3169.6493766794806`, the phase-1 pin).

**Verdict:** (d) the `rfft2` change first, regardless; then (a) reinstate a numba CPU curvature path on the new `direct_conv` kernel, geometry-gated on nnz per source column below ≈60–80; a NumPy `rfft2` application path for the far side. Follow-ups filed 2026-09-07: `draft/feature/autoarray/interferometer_apply_operator_rfft2.md`, `interferometer_numba_cpu_direct_conv.md`, `interferometer_sparse_operator_numpy_cpu_path.md`.

## Traps recorded

- **A timing harness that does not pass the switch it is measuring times the wrong code.** `direct_log_evidence()` did not pass `kernel=`, so the whole-likelihood row measured the reference kernel on every arm. The step-coverage percentage caught it (37 % vs 97 %); fixed, and the entire in-situ campaign re-run. Coverage is a control row, not a decoration.
- **The recovered `sub_slim_indexes_for_pix_index` reads padding on real mappers** (ignores `pix_size_for_sub_slim_index`, float64 index defaults are a numba typing error); fixed in `kernels.py`.
- **Machine drift is a control problem, not a noise problem.** The bake-off ran with the host ~2.7× slower than quiet; a re-run of the sma cell under quiet conditions moved the deciding ratio 8 % and no ordering. Interleave arms, record `dgemm` at head and tail, report ratios.
- **The JAX in-situ arm cannot be walked property-by-property**: `curvature_matrix` / `data_vector` are uncached on `InversionInterferometerSparse`, so an eager walk rebuilds `F` three times. The arm is flagged `steps_are_partial` and the jit-warm `F` row is the fair number; the dashboard's `*_numba_jax` totals are partial by construction.
- **The alma O(N·K) preload costs ~33 min single-threaded.** Cached beside the dataset (gitignored) via `NumbaPreload.from_curvature_preload`; this cost is phase 3's subject.
- **Kernel name belongs in the artifact basename.** Arms overwrote each other until `--kernel` went into the output name; the phase-1 `*_numba_breakdown_sma_*` rows were replaced by `_reference_` names.
- **`/smoke_test` has no lane for autolens_profiling**; gate = pack pytest + ruff + `build_readme.py --check`; CI is the `lint` leg.

## Heart YELLOW at ship — human acknowledgement

Shipped over Heart **YELLOW score 70**: `"workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)"` — organism-scope, autolens_workspace JAX scripts; nothing in this branch is in the release chain. Acknowledged in-session 2026-09-07 (`heart-ack` on the `active.md` row).

## What this leaves

Phase 3 (`interferometer_preload_cpu.md`): the preload as an adjoint type-1 NUFFT with peak-scaled parity, against the ~33 min brute-force build. The three library follow-ups above are the epic's product; the `rfft2` one is small and safe.

## Original prompt

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
Issued: 2026-09-07

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
