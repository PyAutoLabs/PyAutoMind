# Likelihood lifecycle phase 2x: record cores-per-call and peak memory on every profiling row, and project per-node throughput in the catalogue

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: every 2a imaging row (53 cells) carries cpus_per_eval and peak_rss_gb; the catalogue publishes projected_node_throughput for each declared reference host, labelled basis projected with the declared parallel efficiency; build_catalogue --check, coverage_matrix --check and pytest pass
Review-minutes: 30
Unattended: never
Epic: likelihood-lifecycle
Phase: 2
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-25

Phase 2 sub-task 2x of the `likelihood-lifecycle` epic. **Run it before 2b**, so 2b–2g rows carry these fields from the start. Human approval 2026-10-25 ("Yes do all that I approve").

## Why

Numba CPU setups run serially, one worker process per core under Nautilus multiprocessing. Comparing one numba call with one A100 call is therefore the wrong comparison. 2a examples:

| Cell | numba (1 core) | A100 dense | ral node projection |
|---|---|---|---|
| hst Delaunay | 0.95 s per call, ~1 GB per worker | 35 ms per call (~28 calls/s) | ~250 workers ≈ 260 calls/s × efficiency |
| ao Delaunay | 8.7 s per call, ~25 GB per worker | 0.37 s per call (~2.7 calls/s) | memory caps it at ~36 workers ≈ 4 calls/s × efficiency |

The human ruled that this is **projected** in the research, numbers and dashboard, and **not** run as multi-worker jobs during profiling or on RAL. Phase 4 measures the parallel efficiency.

## Scope

1. **Row fields, producer side.**
   - `cpus_per_eval`: numba 1, because BLAS and numba threads are pinned to 1; JAX CPU = NPROC threads (8); GPU = one device, with host threads recorded.
   - `peak_rss_gb`: from the job's sacct MaxRSS, written by the campaign submit wrapper after each leg. One leg per array task makes this per-leg. Inside a multi-leg A100 job, record the per-leg peak from in-process `resource.getrusage(RUSAGE_SELF).ru_maxrss`, or mark it null with a reason.
   - Add the in-process measurement in `_profile_cli`, so future rows carry it without needing sacct.
2. **2a backfill.**
   - Pull `sacct -o JobID,MaxRSS` for batch 1 (412923–412926; 412927, 412943–412945) and batch 0 from RAL.
   - Attach the values to the committed 2a rows through a committed sidecar (e.g. `catalogue/peak_rss_backfill.json`), not by editing rows.
   - The A100 jobs are multi-leg: where only the job-level peak exists, record it as a job-level upper bound, `basis: job_maxrss`.
3. **Reference hosts.** Add a declared table to the repo, e.g. `catalogue/reference_hosts.json`:
   - `ral_cpu_node`: 236 cores, 921 GB (smallest ral node);
   - `ral_gpu_node`: 124 cores, 885 GB, 4×A100;
   - `laptop`: 8 cores, 32 GB, no GPU (human may revise).

   Values come from `sinfo` on 2026-10-25.
4. **Projection, in the catalogue builder.** Per row and per reference host where the setup's device class exists:
   - CPU: workers = min(floor(host_cores / cpus_per_eval), floor(host_mem / peak_rss)).
   - GPU: gpus_per_host independent devices.
   - Throughput = workers × η / per_call_s.

   per_call_s comes from vmap per-call for JAX and the warm iid median for numba. η is a declared assumption, `parallel_efficiency: 1.0 (upper bound, unmeasured)`, until phase 4 supplies a measured value per (setup, host).

   Publish `projected_node_throughput` with `basis: projected`, the η value and its source, and which limit bound the worker count (cores or memory). Note in the row that the sampler batch ceiling (Nautilus `n_batch`) is not modelled.
5. **Pulse contract.** Check whether `profiling-summary@3` accepts these as additive record fields or as a second `metric`. If it needs a version bump, stop and ask.
6. **Docs.**
   - Add a "Comparing CPU and GPU setups" paragraph to the 2a wiki page and to the campaigns README.
   - Never headline a "GPU is N× faster" figure from per-call latency alone.

## Not in scope

- Running multi-worker jobs: that is phase 4.
- The Pulse display and research page: that is `draft/feature/pyautopulse/likelihood_lifecycle_p2x_throughput_view.md`.
- Designating setups: that is phase 3.
