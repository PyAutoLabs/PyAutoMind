Filed: 2026-11-05 (phase 2 of autolens_profiling#519; Pulse task `PyAutoPulse/tasks/numba_num_threads_pin_and_delaunay_nn_remeasure.md` steps 2-4)

# Re-measure the DelaunayNN numba Optimal cell on the Nautilus worker route (after the release carrying PyAutoArray#677)

Type: feature
Target: autolens_profiling
Repos:
- @autolens_profiling
- @PyAutoPulse
Themes:
- numba-cpu
- profiling
Difficulty: small
Priority: medium
Status: draft
Gate: a PyPI release carrying PyAutoArray#677 (merged 2026-11-05) AND a human go for the RAL job

## What phase 1 (#519) shipped

The DelaunayNN numba runtime and breakdown cells (`scripts/imaging/delaunay/likelihood_{runtime,breakdown}_numba.py --mesh-class delaunay_nn`, production variant) now pin `NUMBA_NUM_THREADS=1` and force `autoarray.numba_util.parallel_kernel_allowed` False, so they time the serial Sibson compilation a Nautilus multiprocessing worker runs. Each row records a `numba_worker_route` block (`route`, `routes_called`). A laptop witness (`scripts/misc/delaunay_nn/worker_route_witness.py`) shows the patched cell matches a real forked worker call by call.

## Steps

1. After the release: re-run the two cells on `hpc_ral_cpu` (the flags in `scripts/misc/campaigns/imaging_p2a.py`, `--standard-size --mesh-class delaunay_nn --config-name hpc_ral_cpu_fp64`, an 8-CPU array task as before). Check each row's `numba_worker_route.routes_called == ["serial"]`; a `prange` entry means the RAL install predates #677.
2. Mark the 2026.10.25.1 rows (RAL 412955) `superseded` and keep them.
3. Pulse: decide with the human whether the new row replaces the day-zero designation for this cell (a one-cell day-zero re-freeze) or stands as a post-day-zero current record. Record the decision in Pulse.
4. Cross-check against the autolens_inference validation leg (RAL 414189: pin + #677), whose wall implies a per-call cost with serial Sibson in workers.
5. Optional: run `worker_route_witness.py` once on a RAL CPU node, so the C14 witness has a reference-host row as well as the laptop one.

## Expectation

The laptop witness measured the worker Sibson call at roughly 3-4x the day-zero condition (prange on 8 threads), i.e. tens of ms per interpolation more than the profiled number; a call may interpolate more than once. Expect the Optimal runtime to rise by more than the Pulse task's 3-10% estimate, which assumed prange at 1 thread (the serial build is ~1.25x slower than that; see draft/bug/autoarray/sibson_serial_kernel_loses_allocation_hoisting.md).
