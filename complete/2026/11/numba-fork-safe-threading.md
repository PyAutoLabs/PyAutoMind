## What shipped

PyAutoArray#677 (merged 2026-11-05, `e2b05f00`, closes PyAutoArray#676): numba `prange` kernels never run parallel inside a Python multiprocessing search worker.

- `autoarray.numba_util.parallel_kernel_allowed()` is False in any multiprocessing child (fork, spawn or forkserver) and in a pid other than the first caller's.
- The Sibson (DelaunayNN) kernel is compiled twice from one body. The `parallel=False` build is used in workers; `numba_util.function_copy` keeps the two builds' on-disk caches separate.
- The interferometer `direct_conv` route (`_numba_parallel()`) falls back to its serial or symmetric kernels in workers.
- The `general.yaml` `numba: parallel` comment marks it single-process benchmarking only. `numba_util.jit` warns once if it is set inside a worker.
- A single-process main process keeps the parallel kernel and numba's default (omp) threading layer, so its performance is unchanged.

Design change mid-task (human, 2026-11-05): no nested numba parallelism inside multiprocessing at all. This replaced the planned threading-layer switch and `set_num_threads(1)`.

## Evidence

- Failure: RAL 414150 (likelihood-lifecycle phase 4, imaging/delaunay_nn/hst numba_cpu_sparse, both seeds). numba's GNU OpenMP `omppool` terminates children forked after PyAutoFit's parent warm-up, and Nautilus's `TimeoutError` follows.
- New `test_autoarray/test_numba_fork_safety.py` (8 tests): fails before the fix, passes after. There is an omp control and serial == parallel parity. Full suite: 2295 passed, 4 xfailed. CI green: 3.12, 3.13, nojax.
- Laptop smoke: a 2-core Nautilus DelaunayNN fit on NumPy fails on main (31× "Terminating: fork()…") and completes on the fix.
- Witness: RAL 414189 is the same leg on pin 2026.10.25.1 plus only this fix (`/mnt/ral/jnightin/profiling/PyAuto_2026.10.25.1_pr677`, Array `d24c2477`). Both seeds passed the warm-up and are sampling source_pix[1], with zero terminations.

## Follow-ups (not filed)

- The profiling numba CPU cells pin `OMP_NUM_THREADS=1` but not `NUMBA_NUM_THREADS`, so the day-zero DelaunayNN numba rows ran Sibson multi-threaded in 8-CPU jobs. The laptop Sibson kernel at the profiled size takes 14 ms with 8 threads and 56 ms with 1, about 3–10% of the 1.38 s profiled call. Pin `NUMBA_NUM_THREADS=1` and re-measure the DelaunayNN numba cells after release. Offered to the human.
- 414189's rows are on pin plus this fix, not the bare pin. The phase-4 ingest must note this.

- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/677

## Original prompt

# numba `parallel=True` kernels (Sibson, direct_conv) pick the GNU OpenMP threading layer, which kills every Nautilus worker forked after the likelihood warm-up

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Themes:
- source-reconstruction
- performance
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Consequence: glance
Witness: A PyAutoArray unit test runs the Sibson numba kernel (and the parallel direct_conv kernel) in the parent, then calls it from a fork-context multiprocessing pool, and gets the parent's result back within a timeout (today the default threading layer kills the children: TimeoutError); forked children run the kernel on one numba thread; and the RAL rerun of autolens_inference imaging/delaunay_nn/hst numba_cpu_sparse (job 414150's submit) gets past source_pix[1].
Review-minutes: 3
Unattended: ready
Filed: 2026-11-05
Updated: 2026-11-05

## Finding

2026-11-05, likelihood-lifecycle phase 4 CPU batch, RAL job 414150 (both seeds), autolens_inference
`imaging/delaunay_nn/hst` `numba_cpu_sparse_fp64`, pin 2026.10.25.1, 8 cores. At SLaM stage
`source_pix[1]`, PyAutoFit runs "the likelihood once before forking workers", then Nautilus forks its
pool. The children print `Terminating: fork() called from a process already using GNU OpenMP, this is
unsafe.`, the parent's `result.get` raises `multiprocessing.context.TimeoutError`, and the runner fails
the job (exit 1, 43 s). Log: `/mnt/ral/jnightin/inference/autolens_inference/hpc/batch_cpu/error/error.414150_0.err`.
The plain Delaunay numba leg (414149) is fine at the same stage. Its interpolator has no `prange`.

## Mechanism

`autoarray/inversion/mesh/interpolator/_sibson_numba.py` is `@numba.njit(parallel=True)` with `prange`
over queries (likewise `direct_conv_parallel_kernel` in
`inversion/interferometer_numba/inversion_interferometer_numba_util.py`). With no TBB installed, numba's
default threading layer is `omp`, built on GNU OpenMP. Its `omppool` after-fork handler terminates any
child forked from a parent that has started the pool. The parent warm-up starts it, so every forked
worker dies.

Laptop repro (numba 0.68.1, Python 3.13): a `prange` kernel called in the parent, then
`mp.get_context("fork").Pool(2).map_async(...)`. With the `default` and `omp` layers this gives
TimeoutError. With `forksafe` (falls back to workqueue without TBB) and `workqueue`, the children return
the correct results.

Second hazard: in a forked child numba starts `NUMBA_NUM_THREADS` threads, which defaults to the node's
CPU count (252 on RAL), not the job's allocation. With 8 Nautilus workers that heavily oversubscribes the
node.

## Fix direction (library, never the workspace scripts)

Mirror the finufft guard in `autoarray/operators/nufft_cpu.py` (`_openmp_pid`). One shared helper used by
both parallel kernels:
1. Before the first parallel launch, if the user has not chosen a layer (`NUMBA_THREADING_LAYER` unset /
   `numba.config.THREADING_LAYER == "default"`), select a fork-safe layer (`tbb` if importable, else
   `workqueue`).
2. Record the pid of the first launch. In any other (forked) process, call `numba.set_num_threads(1)`
   before launching.
Results must stay bit-identical: the parallel loops have no reductions, and the parity tests pin this.

## Why it matters

Every NumPy-path DelaunayNN fit with `number_of_cores > 1` dies on any machine without TBB, as does any
parallel direct_conv interferometer fit. It blocks the phase-4 delaunay_nn CPU validation leg (Pulse
likelihood-lifecycle campaign). Phase-2 profiled DelaunayNN per-call timings were single-process `omp`
runs, so an ingest note should record the layer the validation legs ran under.
