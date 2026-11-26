# Nautilus on the CPU pool: sampler work runs serially in the parent and stalls 24-worker fits for hours

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Consequence: judge
Filed: 2026-11-26

## Finding (RAL array 416981, 2026-11-26)

`Science/development/adapt_snr_cap` ran the Delaunay SLaM on CPU (`SLAM_BACKEND=cpu`: numba,
sparse operator, `SettingsSearch(number_of_cores=24)`, `ral` partition, 24 cores, 96 GB;
`OMP/OPENBLAS/MKL/NUMBA_NUM_THREADS=1` in `hpc/batch_cpu/submit_slam_cpu`).

- Task 18 (`cowls/COSJ100012+022015_F150W`, `cap3` `mass_total[1]`, Nautilus): the checkpoint was
  last written at 02:15; at 08:55 all 24 pool workers had been idle in `futex_do_wait` for ~6.5 h
  (1h19 CPU each over 8h25 wall) while the parent ran at 100% of one core (14.5 h CPU). gdb samples
  of the parent's main thread: `dgemm_kernel_HASWELL` (OpenBLAS), `DOUBLE_maximum`, `memset`,
  `tupledealloc` — numpy work in Python, no I/O wait. 150 threads, the XLA ones idle.
- Other tasks on the same node (SDSSJ2228+1205, COSJ095950+022057_F277W `cap3 mass_total[1]`) were
  9+ h into a search the A100 finished in 40 min (52,660 samples), workers ~85% busy.
- CPU seconds per sample 2-5x the A100's when five tasks share a 252-core node (the pilot alone on
  a node: 1.5x).

## Likely cause

`autofit/non_linear/search/nest/nautilus/search.py` `fit_multiprocessing` passes
`pool=(pool, None)`: likelihoods go to the pool (`pool_l`), but every sampler calculation
(`pool_s`: neural-network bound training **and** drawing new points from the bounds) runs serially
in the parent. The code comment calls this "negligible: 4 small MLPs fit on at most a few hundred
points" (the change came from #1547, a hang when a worker died mid-`map`). With the BLAS thread
variables pinned to 1 for the workers, the parent is single-threaded too, and when a bound's volume
efficiency is low (many shells, many rejected draws) the parent spends hours drawing points while
the 24 workers wait.

## What to do

1. Reproduce on a small CPU fit and measure parent vs worker time per Nautilus iteration
   (training, sampling, likelihood), e.g. with py-spy or Nautilus's own timing.
2. Options to judge: give `pool_s` a pool again with the #1547 dead-worker protection
   (`_LikelihoodWorkerPool`'s watchdog) applied to it; or let the parent use several BLAS threads
   while the workers stay at 1; or cap the sampler's rejection effort. Keep #1547 fixed.
3. Check whether the GPU / JAX path (vectorized, `pool=None`) has the same serial-parent cost.

Evidence: `Science/development/adapt_snr_cap/wiki/project/state.md` (2026-11-26 log entry), RAL
`/mnt/ral/jnightin/development/adapt_snr_cap/hpc/batch_cpu/{output,error}/slam_cpu.416981_18.*`.
