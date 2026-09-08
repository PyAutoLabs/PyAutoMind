# Build `nufft_precision_operator_from` as a type-1 NUFFT — 35 minutes to 7 seconds

Type: feature
Target: autoarray
Repos:
- PyAutoArray
Themes:
- interferometer
- nufft
- likelihood-profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Epic: numba-interferometer-revisit
Filed: 2026-09-08

Follow-up derived from `autolens_profiling#229` (phase 3 of `numba-interferometer-revisit`)
— not a user request. Every number below is measured, and the working is in
`autolens_profiling/results/notes/numba_interferometer_verdict.md` **section 7 ("The
preload")** plus
`results/breakdown/interferometer/preload_breakdown_{sma,alma,alma_high}_v2026.8.17.1.json`.

## What

`nufft_precision_operator_from` in
`autoarray/inversion/inversion/interferometer/inversion_interferometer_util.py` builds the
`W~` preload by brute force: one cosine per (real-space offset, visibility) pair over the
mask's bounding extent, `O(N_pix·K)`. Every w-tilde arm pays it once per dataset before a
single likelihood is evaluated.

That array is *exactly* `Re` of a **type-1 (adjoint) NUFFT** of the weights `1/σ²` on the
doubled extent grid, and should be built as one:

```
x, y = 2π·u·Δ_rad, 2π·v·Δ_rad          # the transformer's own _x/_y (transformer.py:334-335)
f = nufftax.nufft2d1(−x, y, w, n_modes=(2Nx, 2Ny), eps, isign=+1)
P = ifftshift(Re f)
P[Ny, :] = 0;  P[:, Nx] = 0            # the FFT padding row/column the brute force never fills
```

**Do not route this through `image_from`** — that path applies a half-pixel shift and a row
flip, and neither belongs here.

Reference implementation, already written and pinned:
`autolens_profiling/scripts/misc/numba_interferometer/preload.py::nufft_preload_from`.

## Why

Wall seconds (CPU-seconds in brackets), single-threaded pinning where it takes:

| instrument | `K` | `N_pix` | current `numpy` builder | **type-1 NUFFT** (`eps=1e-12`) |
|---|---|---|---|---|
| sma | 190 | 3 852 | 0.1643 s (0.164) | 0.0210 s (0.031) |
| alma | 1 000 000 | 15 380 | 2101.5 s (2097.1) | **7.278 s (18.84)** |
| alma_high | 5 000 000 | 61 572 | refused (hours) | **22.15 s (89.99)** |

`289×` on wall clock at alma, `111×` on CPU-seconds. It removes a scaling wall rather than a
constant — the brute force is linear in `K`, the NUFFT is `K·nspread² + M log M` — so the gap
widens with instrument size (predicted `1590×` at alma_high). And it is not an approximation:
at `eps=1e-12` the log evidence at alma is bit-identical to the brute force's
(`-12050103.936303042`, rel diff `0`).

It costs the library nothing new: `nufftax` is already a hard dependency of
`TransformerNUFFT`, the mapping uses that transformer's own convention, and the same call
runs on GPU.

## Requirements

- **Keep `nufft_precision_operator_via_np_from` as the test reference.** Pin the new path
  against it at a small `K` with the *mixed* tolerance
  `allclose(rtol=1e-10, atol=1e-10·P[0,0])` — a type-1 NUFFT bounds its error against
  `Σ_k|c_k|`, i.e. against the peak, so the preload's near-zero entries (five orders below
  it, at the fp64 noise floor) carry no relative guarantee and a relative-only test there
  measures round-off, not the builder.
- **Carry the structural pins, not just a smoke test.** The exactly-zero padding row/column
  (with non-zero neighbours, so the pin is not vacuous), `P[i,j] == P[−i,−j]`, and a control
  in which a wrong index permutation must *fail* the parity rule. Six of the eight candidate
  mappings (axis swap × sign of `x` × sign of `y`) are wrong by 21 % of the peak while being
  structurally plausible; the mapping is convention-bound and must be pinned as such.
- **Default `eps=1e-12`.** Every value tested (`1e-6`, `1e-9`, `1e-12`) holds the `rtol=1e-6`
  log-evidence pin by at least five orders of margin, so the dial is not load-bearing for
  correctness — but `1e-12` is the only one that also holds the *array* pin at sma, it
  saturates fp64 (`1e-14` moves `max|Δ|` from `1.7e-17` only to `1.4e-17`), and it costs
  seconds. A preload is reused by every likelihood call in a fit; error budget spent here is
  spent for the whole run.
- **Visibility chunking is mandatory, not optional.** The spreader's gather buffer is
  `K·nspread²` complex128; alma_high's 5 M visibilities need ~15 GB in one shot and were
  OOM-killed in the profiling run before chunking was added. Chunk at the transformer's
  existing `chunk_size` (PyAutoArray#330) and pin chunked == one-shot.
- **This applies to every backend.** The JAX chunked builder becomes redundant, and the
  dirty image already goes through the same adjoint — so the NUFFT path is the one builder,
  not a GPU-only alternative. It also gives the GPU path a preload it does not currently
  have.

## Caveat to record

The wall-clock ratio is not a single-core ratio. XLA's CPU runtime keeps its own intra-op
pool that `--xla_cpu_multi_thread_eigen=false` does not close, so the NUFFT builder ran at
`2.59×` cores at alma and `4.06×` at alma_high. Quote the CPU-seconds column (`111×`) before
claiming a speed-up over a single-threaded loop.

## Side finding (not this task, but worth knowing)

The recovered numba brute-force builder is the *only* one of four that fails the alma array
pin, at `2.195e-11` of the peak against a `1e-11` bound. It is summation round-off, not an
algebraic disagreement: it accumulates all `10⁶` visibilities into one running scalar per
offset while the NumPy reference sums them in `chunk_k = 2048` blocks, so the two diverge
with `K` (`2e-15` at `K = 190`, `2e-11` at `K = 10⁶`, on 11 of 78 400 entries). The NUFFT
agrees with the reference a thousand times better than that numba builder does
(`1.9e-14` vs `2.2e-11`). A `10⁶`-term naive accumulation is worth knowing about wherever
else one lives.
