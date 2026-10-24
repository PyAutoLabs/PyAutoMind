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
