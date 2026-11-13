Filed: 2026-11-05 (found by the autolens_profiling#519 worker-route witness)
Lane: any

# Sibson serial kernel (the one every Nautilus worker runs since #677) is ~1.25x slower than the prange kernel at one thread: numba hoists its per-query scratch allocations only under parallel=True

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
Themes:
- numba-cpu
- performance
- delaunay
Difficulty: small
Priority: medium
Status: draft

## Finding

PyAutoArray#677 compiles one body, `_sibson_numba._sibson_from_tables`, twice: `parallel=True` (`prange`) for single-process use and `parallel=False` for multiprocessing search workers (`numba_util.parallel_kernel_allowed`). So every production DelaunayNN likelihood evaluation under Nautilus runs the serial build.

The body allocates about 13 small scratch arrays per query inside the loop (`cavity`, `unique_ids`, `compact_weights`, `vx`, `vy`, `vid`, `rx`, `ry`, `ivalid`, `contribution`, ...; `_sibson_numba.py:148-194`), plus `_pairwise_sum`'s four 64-element buffers. numba's parfor pass hoists these out of the loop under `parallel=True` (`parallel_diagnostics(level=4)`: "Allocation hoisting ... hoisted out of the parallel loop ... reused inside the loop"). The serial build keeps them per query: ~800k allocations per call at the profiled HST size (61,600 queries).

Measured (laptop i9-10885H, `autolens_profiling/scripts/misc/delaunay_nn/worker_route_witness.py`, `paired_kernels` leg: serial and prange alternated call by call in one process at NUMBA_NUM_THREADS=1, 5 rounds): serial / prange@1 = 1.249-1.263 (two runs, per-round range 1.21-1.27). The serial build is also noisier (allocator), and a real forked worker pays the serial cost. Outputs are bit-identical.

## Proposed fix

Make the serial build as fast as prange at one thread without changing results:
- hoist the per-query scratch arrays manually in a serial body (allocate once per call, reset per query), keeping the prange body for parallel; or
- move the per-query work into a helper taking preallocated buffers, with the prange body allocating per chunk/thread.

Witness: `_sibson_from_tables_serial` outputs bit-identical to the current kernel (`test_numba_fork_safety.py::test__sibson_serial_kernel_equals_parallel_kernel`), and the paired_kernels ratio at or below ~1.02.

## Why it matters

It is a production cost: every Nautilus worker on every DelaunayNN fit pays it, on the most-used numba mesh path. Gains are in the worker, so they also show in the #519 phase-2 re-measure.
