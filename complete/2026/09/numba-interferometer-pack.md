# Phase 1: the numba w-tilde interferometer likelihood recovered as a profiling pack, bit-identical to the JAX sparse path, with breakdown scripts mirroring the imaging numba ones

- **Issue:** autolens_profiling#223 (closed) · **PR:** autolens_profiling#225 (`5d84540`, merged 99f4b533b52cda974f62c59e8b2995ccb941474b) — merged 2026-09-07
- **Repos:** autolens_profiling (`scripts/misc/numba_interferometer/`, `scripts/interferometer/likelihood_breakdown/{delaunay,pixelization}_numba.py`, `results/breakdown/interferometer/`, `results/simulators/`). PyAutoArray read-only.
- **Epic:** `numba-interferometer-revisit` — **phase 1 of 3**; ledger `draft/research/autolens_profiling/numba_interferometer_likelihood_revisit.md`; phase 2 `draft/research/autolens_profiling/numba_interferometer_kernel_levers.md`, phase 3 `draft/research/autolens_profiling/interferometer_preload_cpu.md`
- **Status: SHIPPED.** The pack exists, parity is pinned, the breakdown scripts run; the reinstatement question is phase 2's.

## The headline

The numba interferometer likelihood was never "secret" code in git: the private modules were untracked overlays that PyAutoArray PR #161 (`d76904e8`, 2025-03-19) published, and PR #201 (`c9605b5b`, 2025-12-19) then PR #204 (`222ee046`, 2026-02-02) deleted. Recovered from snapshot `0b90c401` into `scripts/misc/numba_interferometer/` and wired to today's `Mapper` / `Mask2D` / `AbstractInversionInterferometer` API. **The algebra is identical to the current `InterferometerSparseOperator`** — same preload `W~[dy,dx] = Σ_k σ_k⁻² cos(2π(dx·u_k + dy·v_k))`, same `D = Mᵀ·dirty_image`, same `F = Mᵀ W~ M`, same `fast_chi_squared` — so nothing had to be re-derived. Only the application differs: a numba scatter over image-pixel pairs (`O(N_pix² P²)`, independent of visibility count) versus a padded FFT convolution batched over source columns.

Parity on sma (3852 masked pixels, 190 visibilities, Hilbert-1500 Delaunay): log evidence **bit-identical** to the JAX sparse path (`-3169.6493766794806`; rectangular `-3168.280345651575`), `F` max rel 1.1e-14, `D` exact, reconstruction 7.2e-15, preload vs `nufft_precision_operator_via_np_from` 5.2e-12. `test_parity.py` 16 passed, with two control tests whose deliberately broken kernel constant (×1.01) fails the pin — verified non-vacuous (`DID NOT RAISE` when the break is removed).

First numbers (sma, `OMP_NUM_THREADS=1`, n_repeats=10): 0.515 s per Delaunay evaluation, 0.451 s rectangular. The `F: mapper×mapper [numba preload scatter]` row is **45 % (Delaunay, P=3) and 82 % (bilinear rectangular, P=4)** of the evaluation, and unlike imaging it does not depend on the source-pixel count. That row is phase 2's lever.

## Findings

- **The recovered kernel returns a complete symmetric `F` with no mirroring pass** — it loops the full N×N pair space, unlike `imaging_numba/sparse.py` and `InversionInterferometerSparse`. Pinned (`test_curvature_matrix_is_symmetric_without_mirroring`), not assumed; it is also the free 2× symmetric-halving lever phase 2 measures.
- **`InterferometerSparseOperator` does not keep the real-space preload** — only `Khat = fft2(preload)`. `NumbaPreload.from_sparse_operator` takes `dirty_image` off the operator and rebuilds the preload with `nufft_precision_operator_via_np_from` using the arguments `apply_sparse_operator` used, pinned elementwise. `DatasetInterface` has no `uv_wavelengths`; the pack reads them off `dataset.transformer`.
- **Over-sampling is a hard precondition.** The modern sparse triplets fold `over_sampler.sub_fraction` in; the recovered kernel does not. The pack raises on `sub_fraction != 1` (and on func-lists, multiple mappers, non-NumPy `xp`, unknown `kernel=`) rather than agreeing by accident.
- **`W~` has no compact support for an interferometer.** The imaging numba win came from PSF-sized support; here the only sparsity is the mapper's P entries per pixel, so the quadratic-in-N scaling is intrinsic to the scatter form. The design review's synthetic bake-off (to be reproduced in phase 2) puts a direct extent-grid convolution at ~4.6× the recovered kernel and ahead of an FFT up to ALMA-scale grids, and a real-FFT (`rfft2`) path at 1.6–2.2× the library's complex `fft2` for every backend.

## Traps recorded

- **`scripts/interferometer/likelihood_breakdown/delaunay.py` is OOM-killed on `sma`** (exit 137, 14.6 GB RSS) in its PART B per-step JIT profiling — pre-existing, unrelated to this task. PART A's `figure_of_merit_eager` was reproduced to cross-check parity. Filed `draft/bug/autolens_profiling/interferometer_delaunay_breakdown_oom_sma.md`; until fixed, the JAX-CPU per-step comparator has to come from the pack's own JAX reference.
- **`inversion_path` must be `"sparse_numba"`** for `build_readme.py` to label the dashboard row; the formalism is carried separately as `"formalism": "w_tilde_numba"`.
- **Uncached inversion properties double-count in a step-by-step breakdown.** `fast_chi_squared`, `regularization_term` and the log-dets are uncached; re-reading them in the final row pushed coverage to 122 %. Each term row records its own value and the final row times only `log_evidence_from` + `noise_normalization` (coverage 99.5 % / 99.0 %). `data_vector` is left uncached on purpose — the real likelihood builds it twice.
- **`/smoke_test` has no lane for autolens_profiling** (its map covers six workspaces); the gate is the pack's pytest + ruff, and the repo's only CI leg is `lint`.

## Heart YELLOW at ship — human acknowledgement

Shipped over Heart **YELLOW score 70**: `"workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)"` — organism-scope, autolens_workspace JAX scripts; nothing in this branch is in the release chain. Acknowledged in-session 2026-09-07 (recorded on the `active.md` row as `heart-ack`).

## What this leaves

Phase 2 (`numba_interferometer_kernel_levers.md`): synthetic bake-off with a kill gate, the direct extent-grid convolution, thread scaling, in-situ numba vs JAX-CPU with XLA pinned to one thread, and the verdict (reinstate / keep as pack / drop / the `rfft2` library change). Phase 3 (`interferometer_preload_cpu.md`): the preload as an adjoint type-1 NUFFT with peak-scaled parity.

## Original prompt

# Recover the numba w-tilde interferometer likelihood as a standalone profiling pack, with breakdown scripts mirroring the imaging numba ones

Type: feature
Target: autolens_profiling
Repos:
- @autolens_profiling
Themes:
- numba-cpu
- interferometer
- likelihood-profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Epic: numba-interferometer-revisit
Phase: 1
Filed: 2026-09-07
Issued: 2026-09-07

Phase 1 of `draft/research/autolens_profiling/numba_interferometer_likelihood_revisit.md`
(the epic ledger; the user's request is verbatim there). PyAutoArray is **read-only** for
this phase: the pack imports it, never edits it.

## Where the code is

PyAutoArray `0b90c401` (2025-12-17, "fast chi squared implemented") is the last commit with
the whole numba w-tilde interferometer likelihood intact:

```
git -C PyAutoArray show 0b90c401:autoarray/inversion/inversion/interferometer/inversion_interferometer_util.py
git -C PyAutoArray show 0b90c401:autoarray/inversion/inversion/interferometer/w_tilde.py
git -C PyAutoArray show 0b90c401:autoarray/dataset/interferometer/w_tilde.py
git -C PyAutoArray show 0b90c401:test_autoarray/inversion/inversion/interferometer/test_inversion_interferometer_util.py
```

Kernels to keep (lines 13–608 of the util module, plus `sub_slim_indexes_for_pix_index` at
~1838): `w_tilde_data_interferometer_from`, `w_tilde_curvature_interferometer_from`,
`w_tilde_curvature_preload_interferometer_from`, `w_tilde_via_preload_from`,
`curvature_matrix_via_w_tilde_curvature_preload_interferometer_from`, `…_from_2`. Drop the
COSMA `parallel_*` / `jit_loop*` experiments and the staged/chunked preload.

The algebra is identical to today's `InterferometerSparseOperator`: same preload array
(`curvature_preload` == `nufft_precision_operator`), same `D = M^T dirty_image`, same
`F = M^T W~ M`, same `fast_chi_squared`. Only the application differs (numba scatter over
image-pixel pairs, O(N^2 P^2), vs a padded FFT convolution batched over source columns).

## Deliverables

`scripts/misc/numba_interferometer/`
- `inversion_interferometer_numba_util.py` — the recovered kernels, provenance header with
  the SHA, `jit` from `autoarray.numba_util` (still on main).
- `preload.py` — `NumbaPreload` dataclass (`curvature_preload`, `dirty_image`,
  `real_space_mask`, `native_index_for_slim_index`); `from_sparse_operator(dataset)` reads
  `dataset.sparse_operator.nufft_precision_operator` + `.dirty_image` (identical array, no
  recomputation); `via_numba(dataset)` uses the recovered preload kernel (phase 3 uses it).
- `inversion.py` — `InversionInterferometerNumba(AbstractInversionInterferometer)` with the
  5-arg `__init__(dataset, linear_obj_list, settings, preloads=None, xp=np)`;
  `data_vector = mapping_matrix.T @ dirty_image`; `curvature_matrix` via the scatter kernel
  over `mapper.pix_indexes/sizes/weights_for_sub_slim_index` and
  `mask.derive_indexes.native_for_slim`, mirrored/diag-regularised the way
  `autoarray/inversion/inversion/imaging_numba/sparse.py` does it; a `kernel=` switch
  (`"reference"` only in this phase; phase 2 adds variants);
  `mapped_reconstructed_operated_data_dict` via the transformer. **Raises** (no silent
  fallback) on linear-func lists, multiple mappers, and `over_sample_size != 1` — the modern
  sparse triplets fold `over_sampler.sub_fraction` in and the recovered kernel does not;
  assert the precondition rather than agree by accident.
- `fit.py` — `numba_log_evidence_from(fit: al.FitInterferometer) -> (log_evidence, inversion)`
  reusing the fit's `linear_obj_list` (mapper built by the normal tracer path) so a
  whole-likelihood timing exists without touching PyAutoArray's factory.
- `test_parity.py` — pytest on a small simulated SMA dataset
  (`_profile_cli.auto_simulate_if_missing`): preload == `nufft_precision_operator_via_np_from`
  (elementwise `rtol=1e-10`, valid at K=190); `F`, `D`, reconstruction and `log_evidence`
  vs `InversionInterferometerSparse` (JAX CPU) at `rtol=1e-6`; dense oracle
  `F == M.T @ W~ @ M` via `w_tilde_via_preload_from` on a tiny mask; a control test that a
  deliberately wrong constant fails the pin.
- `README.md` — provenance, the algebra note, the "W~ has no compact support for an
  interferometer" caveat, how to run.

`scripts/interferometer/likelihood_breakdown/delaunay_numba.py` and `pixelization_numba.py`
- Clone the structure of `scripts/imaging/likelihood_breakdown/delaunay_numba.py` /
  `pixelization_numba.py`: sequential cached-property `STEP_ACCESSORS`, warmup absorbs the
  numba compile, `n_repeats=10`, residual-row convention, `_profile_cli.resolve_output_paths`
  + `record_pinned_check`, `OMP_NUM_THREADS` recorded in `configuration`.
- Rows (lean — the curvature build is ~70 % of the likelihood at SMA, ~99 % at ALMA):
  `FitInterferometer construct`, `Inversion build (trace+Delaunay+mapper)`,
  `Mapper index/weight arrays`, `Data vector D [numba]`, `F: mapper×mapper [numba preload
  scatter]`, `Curvature matrix F [residual: mirror + diag-add]`, `Regularization matrix H`,
  `F + H`, `Reconstruction solve`, `Fast chi^2`, `log det (F+H) [Cholesky]`, `log det H`,
  `Regularization term`, `Log evidence`. Hilbert build untimed.
  `direct_log_likelihood_function_per_call` via `fit.py`.
- Instruments from `instruments.interferometer.INSTRUMENTS` (default `sma`; `alma` allowed,
  reference kernel is ~8 s per call there so scale `n_repeats` down); JSON+PNG under
  `results/breakdown/interferometer/` as `{cell}_numba_breakdown_{instrument}_v{al_version}`;
  pinned log evidence recorded from the first run per instrument.
- The JAX-CPU comparator is the existing `delaunay.py`; phase 2 ingests its rows.

## Acceptance

- `python -m pytest scripts/misc/numba_interferometer/test_parity.py` green; the control
  test demonstrably fails when the constant is broken.
- Both breakdown scripts run end-to-end on `sma` and commit their JSON+PNG.
- `ruff format --check` clean (the repo's only CI leg).
- No PyAutoArray edits.
