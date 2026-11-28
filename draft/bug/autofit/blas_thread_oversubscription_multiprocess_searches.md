# Guard setup="auto" / number_of_cores="auto" against BLAS/OpenMP thread oversubscription

## Request (verbatim, 2026-11-27)

Make PyAutoLabs' setup="auto" / number_of_cores="auto" framework guard against BLAS/OpenMP
thread oversubscription in multi-process CPU searches.

What happened (Science/active/cowls_diana_v2, RAL `ral` partition, 2026-11-26/27):
- A 4-CPU SLURM job (--cpus-per-task=4) ran AnalysisImaging(setup="auto"). For the pixelized
  searches auto chose numba_cpu_sparse_fp64, and Nautilus number_of_cores="auto" correctly took 4
  workers from SLURM_CPUS_PER_TASK ("Parallel: 4 workers (auto: detected cores)").
- The submit script did not set OPENBLAS_NUM_THREADS / MKL_NUM_THREADS / OMP_NUM_THREADS /
  VECLIB_MAXIMUM_THREADS / NUMEXPR_NUM_THREADS. Each worker's BLAS pool sized itself to the
  node's ~236 cores. Pix1 (DelaunayNN + AdaptSplit, ~7,800 image pixels, 31x31 PSF) ran at
  ~5 likelihoods/min for 12 hours, against ~165/min for an equivalent SLACS run on the same
  library base (PyAuto_wt/sdssj0946-v2) whose script pins all five to 1. With the pins added
  and nothing else changed, the same search resumed at >100/min.
- The job's only hint was an empty-message SearchWarning from
  autofit/non_linear/search/runtime.py:114, which said nothing about threads.
- A laptop test did not show the problem: few cores means little oversubscription.
- numba itself is already kept serial inside workers (autoarray/numba_util.py). The gap is the
  BLAS/OpenMP pools of the linear algebra.

What to do (library-first, through the normal dev workflow):
1. When a search runs N>1 worker processes, cap the BLAS/OpenMP pools in each worker to
   max(1, allocated_cores // N). Allocated cores come from SLURM_CPUS_PER_TASK, then CPU affinity,
   then os.cpu_count(), the same order as autofit/non_linear/parallel/resources.py. Do it either
   by setting the env vars before the pool forks, or with threadpoolctl inside each worker, since
   numpy/scipy have already loaded BLAS by then. Respect any value the user set explicitly.
2. Log the effective thread counts on the "Setup:" / "Parallel:" lines, e.g.
   "Parallel: 4 workers x 1 BLAS thread (OpenBLAS, capped from 236)".
3. If oversubscription is detected and cannot be fixed (e.g. a BLAS backend that ignores the cap),
   warn with a message that names the variables to set. Fix the empty SearchWarning at
   runtime.py:114 so it says what it is warning about.
4. Add a test that runs a small multi-worker numba-sparse search with an artificially large
   detected core count and asserts each worker sees 1 BLAS thread (threadpoolctl.threadpool_info()).
5. Document it in the workspace auto_setup guide (scripts/guides/advanced/auto_setup.py),
   "What Auto Decides" -> Threads, and in the HPC submit-script templates.

## Plan drafted in chat (2026-11-27, not yet approved; Feature Agent: large, split into phases)

Tier + merge mode: effective level: human-required; merge mode: human /prm.

Phase 1, library (PyAutoFit + a small PyAutoNerves change):
1. New `autofit/non_linear/parallel/threads.py`: `blas_threads_per_worker(n_workers)` from
   `resources.detected_cores()`; a top-level (picklable) `cap_worker_threads(limit, apis)` that runs
   `threadpoolctl.threadpool_limits` in each worker for the APIs the user did not set (blas, openmp)
   and sets `NUMEXPR_NUM_THREADS` if unset; `wrap_initializer(initializer, initargs, n_workers)` that
   runs the cap then the pool's own initializer; `blas_summary()` from `threadpool_info()` in the
   parent (library name, starting thread count) for the banner. `threadpoolctl>=3.1.0` is already a
   PyAutoFit dependency.
2. Hook every pool creation site: `FitParallel.__call__` (`parallel/pool.py`), the Nautilus pool
   (`search/nest/nautilus/search.py` ~line 757, wrapping `initialize_worker`), `SneakyPool`
   (`parallel/sneaky.py`), `Process` (`parallel/process.py`).
3. `ParallelResolution` banner (`pool.py` ~224-244): `Parallel: 4 workers × 1 BLAS thread
   (OpenBLAS, capped from 236)`.
4. `runtime.py`: replace `warn_if_threads_unpinned` with a check on the effective thread count
   (user-set values that oversubscribe, or a backend that ignored the cap); drop
   `SearchWarning("")`, give the warning the real message; keep the `warn_environment_variables`
   switch.
5. PyAutoNerves `jax_wrapper.py`: `PYAUTO_SETUP=cpu` sets OMP/MKL/OPENBLAS to all detected cores
   (right for one process, wrong per worker). Record what it set (e.g. `PYAUTO_NERVES_SET_THREADS`)
   so autofit treats those as library-set, not user-set, and caps them.
6. Tests (`test_autofit/non_linear/parallel/test_threads.py`): `SLURM_CPUS_PER_TASK=4`, parent BLAS
   forced to 8 threads, 4-worker pool returning `threadpool_info()` → every worker reports 1;
   user-set value respected and warned; banner text. Deviation from the request: autofit cannot
   import numba-sparse code, so the multi-worker test uses a toy likelihood; ask the human whether a
   numba-sparse version is wanted in PyAutoLens too.

Phase 2, workspaces: `autolens_workspace/scripts/guides/advanced/auto_setup.py` (What Auto Decides →
Threads); `scripts/guides/hpc/batch_cpu/submit` and `guides/hpc/README.md` in autolens_workspace and
autogalaxy_workspace currently export all five variables as `$SLURM_CPUS_PER_TASK` (the COWLS bug
once Nautilus runs that many workers): drop the exports or set 1 with a comment; regenerate
notebooks.

Branch: `feature/blas-thread-oversubscription`, worktree `~/Code/PyAutoLabs-wt/blas-thread-oversubscription/`.
Known claim: PyAutoFit is claimed by parked task vmap-jit-recompiles-per-nautilus-batch-length
(PyAutoFit#1811, awaiting-input, no branch). Science projects (cowls_diana_v2,
slacs_bells_subhalo_grid) already pin all five variables to 1 in their submit scripts.
