- Library: PyAutoArray
- Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/539 (closed, completed)
- PR: https://github.com/PyAutoLabs/PyAutoArray/pull/541 (MERGED, merge commit `9bd76799`, head `61f07fd8`)
- Epic: numba-interferometer-revisit (phase 3), follow-up from `autolens_profiling#229`
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/541

The branch was opened stacked on `interferometer-apply-operator-rfft2` (PyAutoArray#540,
merged 2026-09-08 as `7a4cb700`, record `complete/2026/09/interferometer-apply-operator-rfft2.md`);
GitHub retargeted PR#541 to `main` when #540 landed, and the merge that shipped this work is
against `main`.

## What shipped

**The preload is built as a type-1 NUFFT.** `nufft_precision_operator_from`
(`autoarray/inversion/inversion/interferometer/inversion_interferometer_util.py`) built the
interferometer sparse-operator preload — the compact `(2Ny, 2Nx)` array that depends only on
the `(dy, dx)` offset between image pixels — by brute force, an `O(N_pix · K)` cosine
accumulation over every image pixel x visibility pair. That array is exactly the real part of
a **type-1 (adjoint) NUFFT** of the inverse-variance weights `w = 1/sigma^2` on the
doubled-extent grid, and is now built as one:

```
P = Re nufft2d1(-x, y, w, (2Nx, 2Ny), eps, isign=+1)  with x = 2*pi*u*delta, y = 2*pi*v*delta
    -> ifftshift -> zero the Nyquist row Ny and column Nx -> contiguous float64
```

costing `O(N_vis · nspread^2 + M log M)` for `M = 4·Ny·Nx`. The sign convention (`-x, +y`,
isign `+1`) is the one of eight candidate mappings that reproduces the brute force; the
derivation and the search over the other seven are recorded in the function's docstring.

**`method="nufft"` is the new default**, with `eps=1e-12`. That value saturates fp64 at every
instrument profiled — the measured `max|delta|` is already at the round-off floor — and it is
the only value that also holds the array pin at sma, at a cost of seconds. A preload is reused
by every likelihood call in a fit, so error budget spent here is spent for the whole run.

**Chunking is driven by the transformer.** When `chunk_size` is not given it is taken from the
transformer's own `chunk_size` if it is a `TransformerNUFFT`. This is a memory ceiling, not an
optimisation: the spreader's gather buffer is `K · nspread^2` complex128, ~15 GB in one shot at
K = 5e6, which OOM-killed the profiling run before chunking was added. `chunk_k` is unchanged
and still chunks the brute-force builders.

**The brute-force builders are kept as the reference implementations.** The numpy
(`nufft_precision_operator_via_np_from`) and JAX builders are untouched; they are what the
NUFFT is pinned against, and `method="numpy"` / `method="jax"` are the explicit ways to ask for
them. New public builder: `nufft_precision_operator_via_nufft_from(...)`.

**`use_jax` no longer demotes to a brute force** (second commit, `61f07fd8`). Under the default
`method="nufft"` the kwarg is a no-op — the NUFFT already runs on JAX — so an existing caller
passing `use_jax=True` lands on the fast path with no edit rather than being routed back to the
JAX brute force. It is honoured only when a brute-force method is explicitly selected.

Two **loud, logged** fallbacks to `method="numpy"`, never silent: `PYAUTO_DISABLE_JAX=1` (the
test-mode kill switch already honoured in `dataset.py`), and nufftax not importable. Both emit a
`logger.warning` naming the `O(N_pix · K)` cost being paid. Any other unusable `method` raises.

Diff: 4 files, +934/-56 — `inversion_interferometer_util.py` (+324/-6),
`dataset/interferometer/dataset.py` (+105/-44, including the rewritten "N_vis · N_pix crossover"
warning, which is now about the DFT transformer rather than the preload),
`test_inversion_interferometer_util.py` (+378/-6), `test_dataset.py` (+127/-0).

## Evidence

- **Parity against the numpy reference**, seeded 16x16 mask at K=300, mixed tolerance
  (`rtol=1e-10, atol=1e-10·P[0,0]`): max deviation **4.4e-14** of peak. The tolerance is mixed
  because a type-1 NUFFT bounds its error against the peak, so the preload's near-zero entries
  carry no relative guarantee and a relative-only test there would pin round-off.
- **Chunk invariance**: chunked (`chunk_size=64`, K > 64) == one-shot at **5.3e-14**.
- **Wrong-sign control**: negating `uv[:, 0]` fails the pin at **0.187** of peak — the pin has
  real discriminating power, which matters because six of the eight candidate mappings are wrong
  by ~21 % of the peak while being structurally plausible.
- **Structural pins**: padding row `Ny` / column `Nx` exactly zero with non-zero neighbours (so
  the pin is not vacuous); `P[i, j] == P[-i, -j]`.
- **End-to-end**: the existing `test_interferometer.py` sparse-vs-mapping comparisons run through
  the new default unchanged. `pytest test_autoarray/inversion test_autoarray/dataset
  test_autoarray/operators -q` -> 685 passed.
- **Measured** (`autolens_profiling#229`, phase 3): at `alma` (K = 1e6, N_pix = 15 380) the
  brute force takes **2101 s** and the NUFFT **7.3 s** wall — **289x** wall, **111x** in
  CPU-seconds. The CPU-seconds figure is the honest one: the brute-force builder is
  single-threaded and the NUFFT spreader is not (2.59x cores at alma, 4.06x at alma_high); the
  wall-clock number is what a user experiences on a workstation. At `alma_high` (K = 5e6) the
  NUFFT takes 22 s where the brute force refused (hours).
- **CI**: all three legs green on head `61f07fd8` — `unittest (3.12)`, `unittest (3.13)`,
  `unittest-nojax` (run 34256932439). `MERGEABLE` / `CLEAN` and base `main` re-verified
  immediately before the merge; Heart freeze flag clear.

## Compatibility

The array is the same object to within the pins above, so existing workspace `.npy` preload
caches remain valid and nothing needs regenerating. Every pre-existing keyword keeps its
meaning; the change is additive plus the default-method switch, so no caller breaks.

## Downstream follow-up

`autogalaxy_workspace/scripts/interferometer/features/pixelization/many_visibilities_preparation.py`
still documents the preload as taking minutes to hours and presents the `.npy` cache as a run-time
necessity. That prose is falsified by this merge and is being corrected under
`interferometer-preload-prose` (autogalaxy_workspace), which waits on this PR's release.

## Heart ack carried from the active.md row

- heart-ack: 2026-09-08 in-session, two reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" and "release validation incomplete: no rehearsal for current source" — organism-scope; neither names PyAutoArray or a library test, and the 685-test PyAutoArray suite is green on this branch

## Original prompt

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
Issued: 2026-09-08
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/539

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
