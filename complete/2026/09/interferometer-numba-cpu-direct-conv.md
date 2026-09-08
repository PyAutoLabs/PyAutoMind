- Library: PyAutoArray
- Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/543 (closed, completed)
- PR: https://github.com/PyAutoLabs/PyAutoArray/pull/545 (MERGED, merge commit `35aa681f`, head `825b2453`)
- Epic: numba-interferometer-revisit — **the last library follow-up of the retired epic.** The epic itself was already recorded COMPLETE at `complete/2026/09/interferometer-preload-cpu.md` and its ledger retired to `complete/archive/epics/numba_interferometer_likelihood_revisit.md`; this task is the final PyAutoArray-side item that fell out of the `autolens_profiling#226` verdict.
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/545
- heart-ack: 2026-09-08 in-session, reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" and "release validation incomplete: no rehearsal for current source" — organism-scope; neither names the interferometer inversion path or PyAutoArray

## What shipped

A new package `autoarray/inversion/inversion/interferometer_numba/` carrying the numba CPU
`direct_conv` curvature path, and the routing that reaches it.

**The kernel** (`inversion_interferometer_numba_util.py`) is ported from the
autolens_profiling investigation pack (`autolens_profiling#226`). Instead of transforming
each source column of the mapping operator to the uv-plane, `curvature_direct_conv`
convolves it over the real-space extent rectangle, at a cost that scales with the column's
non-zeros. The serial form is a `@numba_util.jit()` function; the `prange` form is built
lazily by `direct_conv_parallel_kernel()` rather than decorated at import, so a serial run
never pays the parallel compile.

**The class** (`sparse.py`) is `InversionInterferometerSparseNumba`, a subclass of
`InversionInterferometerSparse` that overrides `curvature_matrix_diag` and nothing else —
data vector, regularization, solve and evidence are all inherited, so the two routes cannot
diverge outside the curvature matrix. It **raises** `InversionException` on every
configuration the kernel cannot represent: a non-NumPy `xp`, more than one mapper, any
`AbstractLinearObjFuncList`, over-sampling.

**The gate** is `Settings.interferometer_numba_nnz_per_source_max`, in mean non-zeros per
source column (`mapper.pix_sizes_for_sub_slim_index.sum() / mapper.params`). Default `60.0`,
packaged in `autoarray/config/general.yaml`, with a `KeyError` fallback to the same value so
no workspace config needs the key; `0` disables the path entirely.
`inversion_interferometer_from` gained `_use_interferometer_numba(...)`, which routes to the
numba class only when all of `xp is np`, gate > 0, exactly one `Mapper` and no
`AbstractLinearObjFuncList`, no over-sampling, mean nnz per source column at or below the
gate, and `import numba` succeeds. The factory's checks are silent fall-through; the class's
are fatal — same meaning, different consequence, so they cannot drift.

Diff: 7 files, +1201 — the two new kernel/class modules, `factory.py` (+102),
`settings.py` (+49), `general.yaml` (+1), and a new 514-line test module.

## Behaviour change (the default CPU route moved)

**This task changed the default.** A sparse-operator interferometer inversion with `xp=np`,
one mapper, no linear-object function lists and no over-sampling, whose mapping operator is
at or below the gate, now runs the numba `direct_conv` curvature path instead of the FFT
one — whenever numba is installed. The results are numerically equivalent; the kernel, the
run time and the first-call compile are what change.

Escape hatch: `inversion: interferometer_numba_nnz_per_source_max: 0` in `general.yaml`, or
`Settings(interferometer_numba_nnz_per_source_max=0)`.

## The crossovers, and why the constant is machine-dependent

The numba kernel's cost scales with the operator's density; the FFT route's does not, so
they cross at a roughly fixed nnz-per-source-column — exactly the gate quantity. Measured
(`autolens_profiling#226` verdict §2): **≈60 on Delaunay meshes, ≈77 on rectangular**, with
the numba kernel 2–7× faster than the JAX/FFT route well below the crossover. The default
takes the conservative of the two.

The constant is set by the ratio of scalar AXPY throughput to FFT throughput on the CPU
running the fit, so a machine with a different cache hierarchy or FFT library crosses
elsewhere. Both the config comment and the `Settings` property docstring say so.

## Parity

Against the sparse NumPy path (`test_autoarray/inversion/inversion/interferometer_numba/test_interferometer_numba.py`):
curvature matrix `F` max abs diff **1.8e-15**, data vector `D` **exact**, reconstruction
**4.9e-17**; the parallel kernel is **exactly** equal to the serial one; the 1 %
perturbation control **fails**, as it must.

## Validation

`pytest test_autoarray` — **1501 passed** in the task worktree. `black --check` clean on all
seven files. CI green on all three legs of the single `Tests [pull_request]` run
(py3.12, py3.13, nojax); this repo has no push-event workflow, so that run is the whole
signal. Heart YELLOW on two organism-scope reasons, acknowledged in-session (above).

## Downstream

The new config key lives in PyAutoArray's own packaged `general.yaml` and the property falls
back to `60.0` on `KeyError`, so **no workspace config needs to change**. Swept every
`general.yaml` under the workspaces, HowTo repos and the Euclid pipeline: every one carries a
curated subset of the `inversion:` block (none of them has `log_det_method`,
`regularization_term_method` or the `nnls_*` keys either), so **no workspace copies
PyAutoArray's file wholesale** and there is no config-sync task to file.

## Follow-up

The crossover numbers were measured on the standalone prototype pack, not the shipped
library dispatch. The in-situ re-measurement — running `delaunay_numba.py`'s arms through
`aa.Inversion` at sma and alma so the library's own routing is what is timed, and confirming
60/77 on that machine — is filed as
`draft/research/autolens_profiling/interferometer_numba_library_dispatch_insitu.md`. It
carries a **step 0**: `autolens_profiling/scripts/interferometer/likelihood_breakdown/datacube/delaunay.py:1011`
calls `sparse_operator.curvature_matrix_diag_from(...)` inside a `jit` with traced arrays and
no `xp`, which since PyAutoArray#544 takes the NumPy branch and dies on `np.asarray(tracer)`;
`delaunay_numba.py:433` and `pixelization_numba.py:425` have the same shape.

## Traps

- The branch was cut from task 3's tip (`c2469b9d`). #544 merged first with `c2469b9d` as
  its first parent, so the branch diffed cleanly against `main` with no rebase — the
  `git log origin/main..HEAD` / `git diff --stat origin/main` check is what proved it rather
  than assumed it.
- The new package directories had been `git add -N`'d, which shows as `A ` in
  `git status --short` but stages nothing; they had to be added for real before the commit.
- PyAutoMind's shared index held another session's staged
  `draft/bug/autolens_profiling/breakdown_pixelization_stale_module_import.md`, so every Mind
  push in this task went through a detached temp worktree at `origin/main` rather than the
  canonical checkout. The canonical `PyAutoMind` main still carries its own unpushed copy of
  the task-3 close-out commit (`141453f5`, pushed as `729a7e03`) and is behind origin.

## Original prompt

# Reinstate a numba CPU interferometer curvature path — the extent-grid convolution, geometry-gated

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- numba-cpu
- interferometer
- likelihood-profiling
Difficulty: large
Autonomy: supervised
Priority: high
Epic: numba-interferometer-revisit
Filed: 2026-09-07
Issued: 2026-09-08
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/543

Follow-up from `autolens_profiling#226` (phase 2 of `numba-interferometer-revisit`). The
verdict, the bake-off and the in-situ arms are in
`autolens_profiling/results/notes/numba_interferometer_verdict.md`.

## What

Add `autoarray/inversion/inversion/interferometer_numba/` mirroring the live
`imaging_numba/` package, with **one** kernel: the extent-grid direct convolution prototyped
as `direct_conv` in `autolens_profiling/scripts/misc/numba_interferometer/kernels.py`. For
each source column of `A`, convolve it over the `(Ny, Nx)` unmasked-extent rectangle with
contiguous `W~` preload rows, then project with `Aᵀ`. Cost `O(nnz·M + S·nnz)`.

**Do not reinstate the deleted kernel.** The recovered `O(N² P²)` pair loop beats a NumPy
`rfft2` convolution at only one of six measured cells; `direct_conv` beats it by 2.9-4.8× on
the real likelihood's `F` row.

## Measured (single thread, i9-10885H, autolens 2026.8.17.1)

In-situ `F: mapper×mapper` row, real likelihood, arms interleaved with `dgemm` controls:

| instrument | mesh | recovered kernel | `direct_conv` | JAX/FFT (jit-warm) | direct_conv vs JAX |
|---|---|---|---|---|---|
| sma | Delaunay 1500 | 0.2475 s | 0.0844 s | 0.5917 s | **7.01×** |
| sma | rect 32² | 0.3967 s | 0.0998 s | 0.4101 s | **4.11×** |
| alma | Delaunay 1500 | 4.0710 s | 1.2250 s | 2.4297 s | **1.98×** |
| alma | rect 32² | 7.0205 s | 1.4631 s | 1.6110 s | 1.10× |

Whole evaluation, with the jit-warm `F` substituted into the measured non-`F` cost:
2.43× (sma Delaunay), 2.76× (sma rect), 1.77× (alma Delaunay), 1.08× (alma rect) faster than
JAX-CPU.

## The gate this needs

The controlling variable is **non-zeros per source column**, `nnz/S = N_pix·P/S`. Measured
crossover against a NumPy `rfft2` convolution: **≈60 (Delaunay) to ≈77 (rectangular)**. Below
it the numba kernel wins (up to 5.93×); above it the FFT wins (by 1.6× at alma_high Delaunay,
3.7× at alma_high rectangular). So the path must be *selected*, not defaulted to — a
dispatch rule on `nnz/S` with the constant measured on the target machine, or an explicit
user setting with the rule documented.

## Scope

- `interferometer_numba/inversion_interferometer_numba_util.py` — the `direct_conv` kernel
  and its `prange` sibling (3.5× at sma, 4.6× at alma on 8 threads; see the pool caveat).
- `interferometer_numba/sparse.py` — `InversionInterferometerSparseNumba`, mirroring
  `imaging_numba/sparse.py`, dispatched from `inversion/factory.py`.
- The mapper must emit the CSR/CSC + extent-flat layout directly (as
  `_sparse_triplets_curvature_from` already emits COO), so the kernel does not marshal its
  own inputs per evaluation.
- Preconditions to raise on, not work around (the profiling pack already does): linear-
  function lists, multiple mappers, `over_sample_size != 1`, non-NumPy `xp`.
- Parity gate: `F`, `D`, reconstruction and log evidence against
  `InversionInterferometerSparse` at `rtol=1e-10` on `F` with `atol` scaled by `max|F|`,
  plus a control that a 1 % scale fails the pin.
- The real-space `W~` preload must be kept on the dataset: `InterferometerSparseOperator`
  currently stores only `Khat = fft2(preload)` and discards the array this kernel indexes.
