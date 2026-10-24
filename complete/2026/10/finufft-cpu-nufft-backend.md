# finufft as the CPU NUFFT backend + likelihood warm-up before forking (PyAutoArray#654)

- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/655
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1715

## What shipped
- **PyAutoArray#655** (`0f12fac7`): `TransformerNUFFT` (forward, adjoint, mapping-matrix transform) and the NUFFT precision-operator / sparse-terms builders use finufft on the NumPy path; nufftax only on JAX branches. `use_jax` now selects the operator builder backend. finufft is a platform-marked core dependency (Linux/Windows x86_64, macOS arm64; Intel macOS `<2.5`) with a nufftax fallback + one-time warning. Type-1 runs single-threaded (bitwise-reproducible dirty image / operator; multithreaded spread order is non-deterministic). Forked children pinned to one finufft thread (libgomp fork deadlock).
- **PyAutoFit#1715** (`ceef8af3`): `Fitness.prepare_for_fork()` runs the likelihood once (NumPy path only) and imports numba before any likelihood pool forks — Nautilus `fit_multiprocessing`, `PoolFactory.__call__` (Zeus, Dynesty), `SneakyPool` (Emcee, initializer). Watchdog: specific SIGSEGV message.

## Key findings
- finufft vs nufftax on 5.5M ALMA visibilities (RAL EPYC 7763, 8 threads): operator 0.37 s vs 8.7 s, dirty image 0.27 vs 9.0, forward 0.26 vs 10.4; agreement ~1e-14. End-to-end preprocessing 2.4 s (was ~20 s, ~44 GB unchunked peak).
- **Segfault root cause = numba first-imported inside forked workers, NOT JAX.** `autoarray.numba_util` defers `import numba` since 2026.8.20.1 (3aea5428). Imaging parents run numba pre-fork (Overlay/Hilbert mesh) → safe; an interferometer parent with NUFFT prep + NumPy meshes never does → ≥16 forked workers segfault in llvmlite init. Evidence: 12/12 crashes (with and without JAX imported); parent `import numba` 2/2 OK; trivial njit 2/2 OK; this fix 2/2 OK at 28 cores (33–34 evals/s).
- The initial JAX hypothesis was wrong (an untested inference); corrected on the issue.

## Gates
CI green on every leg (both repos); PyAutoArray 2191 passed (also multithreaded), no-JAX emulation green; PyAutoFit 3900 passed; smoke 165/165 across six workspaces (autocti envs failed arcticpy install, unrelated); Heart YELLOW acknowledged by the human.

## Follow-ups (not filed)
- `analysis/multiprocessing.py` (`AnalysisPool`) forks without a Fitness — same failure class possible with many numba analyses.
- Visualisation for `use_jax=True` analyses still eager JAX (~9 min end-of-phase on 5.5M vis) — human deferred out of phase 1.
- `AnalysisInterferometer` construction imports `jax` (no backend) — harmless, noted.

## Phase 2 (in progress in-session, no code)
RAL SLaM end to end on the collaborator's data (scratch `aris_cpu_check_20261024/e2e`): source_pix[0] 114 s (JAX), source_pix[1] 271 s (28 cores numba), mass[1] sampling ~46 evals/s; then a Slack handoff with updated runner/utils copies.

## Original prompt

Consequence: judge
Issued: 2026-10-24
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/654

# finufft as the CPU NUFFT backend (JAX-free numba interferometer runs)

@PyAutoArray @PyAutoFit

## Request (verbatim, human 2026-10-24)

> ok I approve of this, do it. I think dont do the warm up but making put an Exception in that catches
> that event? Once finufft is in do an SLaM run on RAL for an end to end test using Aris's data and we'll
> then produce Aris a handoff slack message

Approved proposal it refers to: make finufft the default CPU NUFFT backend in PyAutoArray as a core
dependency (precision-operator builder, `TransformerNUFFT.image_from` / `visibilities_from` on the
NumPy path); nufftax only when `use_jax` / inside JAX tracing; PyAutoFit raises a specific exception
when a Nautilus multiprocessing worker dies by SIGSEGV after the parent initialised JAX (no warm-up).

## Evidence (2026-10-24, Aris collaborator re-check)

- A numba-only interferometer run still initialises JAX in the parent: `apply_sparse_operator`'s dirty
  image goes through `TransformerNUFFT.image_from` → nufftax (importing nufftax alone starts XLA), and
  the NUFFT precision-operator builder always runs nufftax (`use_jax` ignored there).
- Nautilus with ≥16 forked workers then segfaults (8/8 runs at 16–28 workers on RAL, jobs
  412841–412862): workers die in numba NRT/LLVM init (`numba_util.lazy` → `curvature_matrix_diag`)
  after fork from a JAX-threaded parent; a pre-filled numba cache does not help; a parent warm-up
  call does (3/3), but the human chose an exception over a warm-up.
- finufft 2.5.1 dropped in for `nufftax.nufft2d1/2d2` (modes transposed) on Aris's 5.5M visibilities,
  125×125 mask, eps 1e-12 (RAL job 412863, EPYC 7763, 8 threads): operator 0.37 s vs 8.7 s, dirty
  image 0.27 s vs 9.0 s, forward `visibilities_from` 0.26 s vs 10.4 s; agreement 1.5e-14 / 2.0e-14 /
  4.7e-13 relative. Raw single-thread type-1 ≈ 0.9 s. NumPy brute-force builder ≈ 56 min (not viable).

## Deliverables

1. PyAutoArray: finufft core dependency; NumPy-path NUFFTs via finufft; JAX path unchanged.
2. PyAutoFit: specific exception for SIGSEGV worker death after JAX initialised in the parent.
3. RAL SLaM end-to-end run on Aris's data (numba, multiprocessing) with the new code.
4. A Slack handoff message for Aris.
