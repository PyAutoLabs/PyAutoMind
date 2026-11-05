# numba-num-threads-pin-delaunay-nn — DelaunayNN numba cells time the Nautilus worker route

- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/519 (closed 2026-11-05)
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/520 MERGED 2026-11-05 (207ae03a) via human /prm
- source: PyAutoPulse task `tasks/numba_num_threads_pin_and_delaunay_nn_remeasure.md` (PyAutoPulse#90), phase 1
- tier: judge (human /prm)
- claim-override: HUMAN 2026-11-05 overrode gradient-correctness-sweep's autolens_profiling claim (different files; #517 paused on RAL 413991)
- heart-ack: STALE "release validation stale: source moved since rehearsal (PyAutoNerves)" — human ack at ship

## What shipped

The production variant of `scripts/imaging/delaunay/likelihood_{runtime,breakdown}_numba.py --mesh-class delaunay_nn` now:
- pins `NUMBA_NUM_THREADS=1` before numba import;
- forces `autoarray.numba_util.parallel_kernel_allowed` False, so it runs the serial Sibson compilation a Nautilus multiprocessing worker runs since PyAutoArray#677.

Each row records a `configuration.numba_worker_route` block (`route`, `routes_called`), written by the helpers `_production_config.numba_worker_route_pin` and `apply_numba_worker_route`. On a pre-#677 library the block says "prange kernel @1 thread".

`THREAD_ENV_VARS` and every other cell's recorded configuration are unchanged. That was the human decision (cell-local pin), honouring `fixed_light_numba.py:245`.

## Why not just NUMBA_NUM_THREADS=1 (human direction: think in Nautilus multiprocessing terms)

A single-process cell is MainProcess, so it takes the `prange` build. A thread pin alone times `prange` on one thread. numba hoists the kernel's per-query scratch allocations out of the loop only under `parallel=True` (confirmed with `parallel_diagnostics`), so the serial build workers run costs more.

## Witness — `scripts/misc/delaunay_nn/worker_route_witness.py` (laptop i9-10885H, 5 rounds, 1,280 × 61,600)

- patched in-process / real forked worker, call by call: **1.024, 90% paired round-bootstrap CI [1.000, 1.033] — PASS** vs 1 ± 10% (timing-noise inventory row C14);
- serial / prange@1, call by call: 1.248 [1.226, 1.294];
- forked worker / prange@8 (the day-zero condition): 4.67 [2.79, 5.37];
- outputs bit-identical across all legs and rounds.

Lesson: sequential laptop legs drifted up to 2.5× between runs, and two early readings were withdrawn. Only call-by-call pairings with the round bootstrap were trusted.

## Real cell runs (laptop, RAL flags)

- DelaunayNN runtime + breakdown: `routes_called == ["serial"]`, 1 thread; log_likelihood equal to the day-zero row to 4e-12.
- Plain Delaunay control: configuration keys identical to its day-zero row.

## CI notes

Lint needed three generated-artefact regenerations, one per CI cycle:
1. the catalogue shard for the new witness JSON;
2. a full `dashboard/` re-render, which also absorbs the 2026-11-03 Brain `board/` change (the known Brain-theme drift);
3. `coverage_matrix`.

Lesson: run the whole `lint.yml` `--check` sequence locally before pushing.

One infra flake: the browser-setup apt mirror stalled, and the 15-min job cap cancelled the run. It was re-run on the same commit with the human's go and went fully green.

## Follow-ups (filed as Mind drafts, f4a8fc04)

- `draft/feature/autolens_profiling/delaunay_nn_numba_optimal_remeasure_after_677.md`: phase 2. RAL re-measure after the release carrying PyAutoArray#677 (human go), supersede the 2026.10.25.1 rows, Pulse day-zero decision, cross-check against RAL 414189.
- `draft/bug/autoarray/sibson_serial_kernel_loses_allocation_hoisting.md`: the serial Sibson build every worker runs is about 1.25× prange@1.

## Original prompt

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
