# Phase-4 wall estimates miss by up to 90×: no sampler-overhead floor, and an eval-count proxy that is 2.7–2.9× low for multi_galaxy

Type: bug
Target: autolens_inference
Repos:
- autolens_inference
Themes:
- inference
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: Re-running the estimate for every phase-4 leg that has a COMPLETED, non-resumed row gives actual/estimate within 0.5–2× for every leg (today 0.55–89.5×), using only inputs available before a run. The submit generator's --time follows the new estimate, and `check_submits --check` and `validation_p4 --check` stay green. The same wall model is what phase 5's run-time estimator is told to reuse (a note in the phase-5 context).
Review-minutes: 15
Unattended: never
Lane: ral
Epic: likelihood-lifecycle
Phase: 4
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-06

## Finding

On 2026-11-06 the phase-4 submit generator's per-leg wall estimate (the "The estimate is N s" header in each `hpc/batch_*/submit_p4_validation_*`, from `scripts/misc/campaigns/validation_p4.py` and `scripts/misc/wall/`) was compared with SLURM ElapsedRaw for every COMPLETED leg. Actual over estimate, by leg:

| leg | estimate s | actual s (max seed) | actual/est |
|---|---|---|---|
| multi_galaxy_mge_hst_jax_gpu_dense | 106 | 9490 | 89.5 |
| point_source_source jax_cpu_na / jax_gpu_na | 1 | 81 / 76 | 81 / 76 |
| cluster_source_plane jax_gpu_na | 11 | 546 | 49.6 |
| weak jax_gpu_dense / jax_cpu_dense | 1 / 2 | 39 / 48 | 39 / 24 |
| cluster_image_plane jax_gpu_na | 41 | 1331 | 32.5 |
| group_mge_euclid jax_gpu_dense | 151 | 3871 | 25.6 |
| cluster_source_plane jax_cpu_na | 50 | 413 | 8.3 |
| point_source_image jax_gpu_na / jax_cpu_na | 20 / 47 | 131 / 107 | 6.6 / 2.3 |
| multi_galaxy_rectangular / delaunay jax_gpu_dense | 5356 / 7480 | 13590 / 18140 | 2.5 / 2.4 |
| **multi_galaxy_mge_hst jax_cpu_dense** | 4835 | ≥ 21600 (TIMEOUT at 6 h, 414160; fresh rerun 414392 running) | **≥ 4.5** |
| group_delaunay / group_rectangular numba_cpu_sparse | 33938 / 37985 | 56322 / 55073 | 1.66 / 1.45 |
| group_mge_euclid jax_cpu_dense | 6797 | 10151 | 1.49 |
| delaunay_nn / delaunay hst jax_gpu_dense | 5800 / 4751 | 6722 / 5493 | 1.16 |
| delaunay_hst numba seed_0, cluster_image cpu | 28545 / 1230 | 27340 / 1063 | 0.96 / 0.86 |
| group_delaunay / group_rectangular jax_gpu_dense | 12352 / 10077 | 10565 / 6759 | 0.86 / 0.67 |
| multi_dataset_delaunay jax_gpu_dense | 43239 | 23771 | 0.55 |

Three mechanisms (from the exporter's walltime records on the 4e branch, autolens_inference#59):

1. **No sampler-overhead floor.** The estimate is roughly profiled per-call × evals. For cheap likelihoods the profiled call is µs–ms, but a Nautilus evaluation costs about 5–10 ms ("implied_ms_per_eval": weak 4.9–5.3, point_source 8–10, cluster 6–22, MGE on A100 7–9). Startup (imports, JAX compile, dataset load) is also unpriced. These misses were harmless only because `--time` floors at 6 h.
2. **The eval-count proxy is low for multi_galaxy.** 414160 source_lp[1] used 250,550 / 271,650 evals against a proxy of 92,550 (2.7–2.9×), at about 61 ms/eval against 26.6 ms priced (2.3×). It is the only leg that actually ran out of time.
3. **The per-eval basis is wrong in places.** multi_dataset's profiled per-call is a vmap batch-3 OOM fallback (176 ms > its own single-jit 110 ms), which over-estimates (0.55×). On numba at 8 cores, multiprocessing efficiency (0.55 at 8 cores, from the cores sweep) is not in the model.

The interferometer and datacube submits carry no estimate (5-day containment cap), so they are not covered by the table.

## Fix direction

- Add a per-evaluation floor (sampler overhead) and a fixed startup term, calibrated from the phase-4 walltime rows (`implied_ms_per_eval` on the cheap likelihoods; first-stage start offsets in the .out logs).
- Calibrate evals per stage by model dimension and n_live from the phase-4 rows (measured `likelihood_evals` per stage), instead of the current proxy.
- Use the parallel-efficiency curve for CPU legs (1/0.68/0.62/0.55/0.36/0.28 at 1–32 cores). Prefer a profiled single-jit per-call when the vmap record is an OOM-fallback batch.
- Exclude resumed-stage rows (Nautilus `samples_info` time across a kill+resume reads 3–4× high; 414362) from any calibration.
- Point phase 5's run-time estimator at the same wall model, so it isn't rebuilt from scratch.

## Original request (verbatim, 2026-11-06)

"yes file the estimate fix" (after the human was told: "the generator also under-estimated this leg by 3.6×, which is worth fixing in the time estimates before phase 5 relies on them").
