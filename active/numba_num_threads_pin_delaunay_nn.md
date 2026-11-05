Filed: 2026-11-05 (from Pulse task `PyAutoPulse/tasks/numba_num_threads_pin_and_delaunay_nn_remeasure.md`, PyAutoPulse#90; human request in chat: "yes file the profiling follow-up in Pulse"; started via `/start_dev tasks/numba_num_threads_pin_and_delaunay_nn_remeasure.md`)
Issued: 2026-11-05
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/519

# Pin `NUMBA_NUM_THREADS=1` in the DelaunayNN numba profiling cells (phase 1 of the DelaunayNN Optimal re-measure)

Type: feature
Target: autolens_profiling
Repos:
- @autolens_profiling
Themes:
- numba-cpu
- profiling
Difficulty: small
Priority: medium
Status: draft

## Source

The full finding, evidence and four steps are in the Pulse task
`PyAutoPulse/tasks/numba_num_threads_pin_and_delaunay_nn_remeasure.md` (merged in PyAutoPulse#90).
In short: `_production_config.pin_thread_env` pins five BLAS/OpenMP thread variables but not
`NUMBA_NUM_THREADS`, and numba ignores `OMP_NUM_THREADS`. Before PyAutoArray#677 the Sibson
interpolator was always a `parallel=True` kernel, so the day-zero Optimal cell
`imaging/delaunay_nn/hst numba_cpu_sparse_fp64@hpc_ral_cpu` (RAL 412955, 8-CPU task) ran Sibson on up
to 8 cores. Production workers are one process per core, so the profiled number is optimistic
(about 3–10%).

## Human decision (2026-11-05, start_dev)

Step 1 of the Pulse task said "add `NUMBA_NUM_THREADS` to `_production_config.THREAD_ENV_VARS`". That
conflicts with the recorded decision in `scripts/imaging/pixelized/fixed_light_numba.py:245`: the
tuple is written verbatim into every cell's `configuration.thread_env`, so widening it changes every
cell's recorded block. The human chose a **cell-local pin**: set `NUMBA_NUM_THREADS=1` only in the
cells that run a parallel numba kernel (the DelaunayNN runtime and breakdown cells, i.e.
`scripts/imaging/delaunay/likelihood_{runtime,breakdown}_numba.py --mesh-class delaunay_nn`), and
record it in a separate `numba_thread_env` block, as `fixed_light_numba.py` does.
`THREAD_ENV_VARS` and every other cell's record stay unchanged.

## Human direction (2026-11-05): think in terms of Nautilus' Python multiprocessing

Nautilus parallelises with a Python `multiprocessing` pool: the parent evaluates the likelihood once,
then forks N workers, one per core. Since PyAutoArray#677, `numba_util.parallel_kernel_allowed()` is
False whenever `multiprocessing.parent_process()` is set, so every worker runs
`_sibson_from_tables_serial` (the `parallel=False` compilation, no numba threading layer). A
single-process profiling cell is MainProcess, so it would still take the `prange` kernel. With
`NUMBA_NUM_THREADS=1` alone it would time the prange kernel on one thread (threading-layer and
parfor overhead), which is not the code a worker runs.

So the pin in the DelaunayNN cells is:
1. force the worker route: patch `autoarray.numba_util.parallel_kernel_allowed` to return False
   (looked up at call time in `sibson.py:682-685`);
2. set `NUMBA_NUM_THREADS=1` before numba import, as a backstop;
3. record the route actually taken (from `_SIBSON_NUMBA_CACHE` keys) and the thread setting in a
   separate `numba_thread_env` block; on a pre-#677 library (no serial route) record
   "parallel kernel @1 thread";
4. a laptop witness: per-call Sibson cost with the patch in-process vs inside a real forked
   `multiprocessing` child after a parent evaluation (the Nautilus pattern), against the prange
   kernel at 1 and 8 threads. Patched-in-process must match the real worker.

The human overrode the `gradient-correctness-sweep` claim on autolens_profiling (different files,
#517 paused on RAL 413991).

## Later (phase 2, filed separately, gated)

After the release that carries PyAutoArray#677: re-measure the DelaunayNN numba runtime + breakdown
cell on `hpc_ral_cpu` (human go for the RAL job), mark the 2026.10.25.1 rows `superseded`, decide
with the human whether the new row replaces the day-zero designation, and cross-check against the
autolens_inference validation leg (RAL 414189). Steps 2–4 of the Pulse task.
