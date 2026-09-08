# Phase 3: the interferometer preload is exactly a type-1 NUFFT — 35 minutes of build becomes 7 seconds

- **Issue:** autolens_profiling#229 (closed) · **PR:** autolens_profiling#234 (`fe157a0` + `b1be857`, merged `7ce9c02ac0dbda08d11cc1c8ba8d738d8fb1f24c`) — merged 2026-09-08
- **Repos:** autolens_profiling (`scripts/interferometer/likelihood_breakdown/preload_numba.py` (new, 1241 lines), `scripts/misc/numba_interferometer/{preload,test_parity}.py`, `results/breakdown/interferometer/preload_breakdown_{sma,alma,alma_high}_v2026.8.17.1.{json,png}`, `results/notes/numba_interferometer_verdict.md` §7, `.gitignore`, README auto-tables). PyAutoArray read-only.
- **Epic:** `numba-interferometer-revisit` — **phase 3 of 3, the last one; the epic is COMPLETE.** Ledger `draft/research/autolens_profiling/numba_interferometer_likelihood_revisit.md` (retired to `complete/archive/epics/` at this close-out); phase 1 `complete/2026/09/numba-interferometer-pack.md`, phase 2 `complete/2026/09/numba-interferometer-kernel-levers.md`.
- **Status: SHIPPED.** The design review's hypothesis is confirmed empirically and the library follow-up is filed.

## The headline

The preload `P[i,j] = Σ_k w_k cos(2π(dx·u_k + dy·v_k))`, `w_k = 1/σ_k²` — the `O(N_pix·K)` array every w-tilde arm builds once per dataset, numba and JAX alike, and which no breakdown cell had ever timed — **is exactly `Re` of a type-1 (adjoint) NUFFT of the weights**, not an approximation of one:

```
f = nufftax.nufft2d1(−x, y, w, n_modes=(2Nx, 2Ny), eps, isign=+1)
P = ifftshift(Re f);   P[Ny, :] = 0;   P[:, Nx] = 0
```

with the transformer's own scaled frequencies (`transformer.py:334-335`). Of the eight candidate index mappings exactly **two** reproduce the brute force (`(−x,+y)` and `(+x,−y)`, conjugates with equal real parts) at `8.7e-14` of the peak; the other six are wrong by `2.1e-1` of it. Thirteen orders separate right from wrong, so the identification is not marginal — but it is convention-bound, which is why the permutation is pinned in `test_parity.py`, not smoke-tested.

| instrument | `K` | preload | `numba` | `numpy` (library default) | `jax_cpu` | **`nufft`** (`eps=1e-12`) |
|---|---|---|---|---|---|---|
| sma | 190 | 140×140 | 0.254 s | 0.164 s | 0.736 s | **0.021 s** |
| alma | 1 000 000 | 280×280 | 3258.6 s | 2101.5 s | 1046.2 s | **7.278 s** |
| alma_high | 5 000 000 | 560×560 | refused | refused | refused | **22.15 s** |

**At alma a 35-minute build becomes 7 seconds — `289×` on wall clock, `111×` on CPU-seconds** against the library's own NumPy default. It removes a scaling wall rather than a constant (brute force is linear in `K`; the NUFFT is `K·nspread²` plus a fixed FFT), so the gap widens with instrument size — predicted `1590×` at alma_high, where the brute force is simply not runnable here.

- **Every `eps` from `1e-6` to `1e-12` holds the `rtol=1e-6` log-evidence pin**, by at least five orders of margin. At `eps=1e-12` and alma the log evidence is **bit-identical** to the brute force's (`-12050103.936303042`, rel diff `0`). `eps=1e-12` is the recommendation anyway: it is the only value that also holds the *array* pin at sma, it saturates fp64 (`1e-14` moves `max|Δ|` only `1.7e-17` → `1.4e-17`), and it costs seconds — a preload is reused by every likelihood call in a fit.
- **The recovered numba builder is the slowest of the four** (54.3 min at alma, 1.55× the NumPy one) **and is the one pin that fails**: `2.195e-11` of peak against a `1e-11` bound, on 11 of 78 400 entries. Recorded, not loosened. Cause: it accumulates all `10⁶` visibilities into one running scalar per offset while the reference sums in `chunk_k = 2048` blocks — summation-order round-off that grows with `K` (`2e-15` at sma's `K=190`). A floating-point property of the kernel, not an algebraic disagreement; the NUFFT agrees with the reference a thousand times better than the numba brute force does.
- **XLA ignores thread pinning.** `OMP/MKL/OPENBLAS/NUMBA_NUM_THREADS=1` pin NumPy's BLAS and numba (measured 1.00× / 0.99×), but XLA's CPU runtime keeps its own intra-op pool that `--xla_cpu_multi_thread_eigen=false` does not close, so both JAX-backed builders run 1.5–4.1× multi-core. Every row therefore records `build_cpu_s` (`time.process_time()`) and `threads_effective` — quote the CPU-seconds column before claiming a speed-up over a single-threaded loop.
- **Chunking is required, not optional.** The spreader's gather buffer is `K·nspread²` complex128; alma_high's 5 M visibilities need ~15 GB in one shot and were OOM-killed before the chunked builder was written. Chunked and one-shot arrays are pinned equal.
- Also pinned: the exactly-zero Nyquist row/column (and that its neighbours are *not* zero, so the pin is not vacuous), `P[i,j] == P[−i,−j]` evenness, invariance to visibility chunking, a square-pixel guard, and a control in which a wrong permutation must fail.

**Verdict** (write-up: `results/notes/numba_interferometer_verdict.md` §7): file the PyAutoArray follow-up — `nufft_precision_operator_from` should build via the transformer's own type-1 NUFFT with the brute-force builders kept as the reference it is pinned against. It costs the library nothing new (`nufftax` is already a hard `TransformerNUFFT` dependency, the same call runs on GPU, and it gives the GPU path a preload it does not currently have). Filed as `draft/feature/autoarray/interferometer_preload_nufft_type1.md`, carrying all four caveats above.

## Traps recorded

- **The peak-scaled bound is the wrong ruler for an exact-but-unchunked builder.** `10·eps·P[0,0]` is the right rule for a type-1 NUFFT (whose error is bounded against `Σ|w_k|`, i.e. the peak) and it is what fails the numba brute force — which has no `eps` at all. Two parity rules are reported for every row so neither has to be taken on trust; at sma the rule is deliberately **mixed** (`rtol=1e-10`, `atol=1e-10·P[0,0]`) because the preload's near-zero entries sit five orders below the peak at the fp64 noise floor and a relative-only test there measures round-off, not the builder.
- **A wall-clock ratio is not a single-core ratio.** The NUFFT builder ran at 2.6× cores at alma: `289×` wall, `111×` CPU-s. Both are in the JSON. The machine also drifted between the two measurements (`control_dgemm_s` 0.2550 → 0.3162), which makes the reported ratio conservative rather than flattering.
- **Do not go through `TransformerNUFFT.image_from`** — it applies a half-pixel `_shift` and a row flip that would have to be undone. Call `nufft2d1` from the pack with the transformer's own `_x`/`_y`.
- **`ifftshift` vs `fftshift` is not a choice here**: both axes have even length `2N`, for which the two shifts are the same permutation. The padding row/column is at index `N`, not `N−1`; after the shift that index carries the Nyquist mode, which the brute force never evaluates and the NUFFT does, so it is zeroed explicitly.
- **`alma_high` hard-refuses the brute-force builders** by design (`O(61572 × 5e6)` is hours each, and nothing needs it) — the NUFFT builder is pinned where a pin is affordable, and at alma_high only against `eps` self-consistency.
- A lint miss on the first commit meant the README auto-tables needed regenerating; `b1be857` is that regen. Gate = pack pytest + ruff + `build_readme.py --check`; CI here is the single `lint` workflow (run 34248629740, green on `b1be857`).

## Heart YELLOW at ship — human acknowledgement

Shipped over Heart **YELLOW score 70**, no red reasons, acknowledged in-session 2026-09-08 (`heart-ack` on the `active.md` row). Two reasons, both organism-scope: `"workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)"` and `"release validation incomplete: no rehearsal for current source"`. Neither names autolens_profiling and nothing in this branch is in the release chain.

## Original prompt

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
