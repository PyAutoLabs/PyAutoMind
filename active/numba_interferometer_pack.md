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
