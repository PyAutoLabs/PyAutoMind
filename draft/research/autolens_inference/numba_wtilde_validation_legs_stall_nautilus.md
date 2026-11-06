# Phase-4 numba W~ validation legs stall Nautilus: datacube (both seeds) and interferometer rectangular seed 1 stop making sampler progress

Type: research
Target: autolens_inference
Repos:
- autolens_inference
- PyAutoArray
Themes:
- inference
- interferometer
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: A mechanism is identified with a controlled reproduction: the stalled stage's likelihood is evaluated on the frozen live set / prior draws from the cancelled runs' Nautilus checkpoints and compared with the converging routes (A100 jax_gpu_sparse_wtilde; seed 0 numba). Either the cause is fixed and a fresh rerun converges, or the stall is recorded as a limitation of the numba W~ route with its trigger.
Review-minutes: 20
Unattended: never
Epic: likelihood-lifecycle
Phase: 4
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-06

## Finding (2026-11-06; cancelled on human ruling)

The phase-4 CPU validation legs on pin 2026.10.25.1 (RAL ral partition, 8 cores, XLA eigen workaround; autolens_inference a24e993):

| Leg | Stage | Calls at cancel | Stall | Best log L (frozen) |
|---|---|---|---|---|
| datacube/delaunay sma `numba_cpu_sparse_fp64_wtilde` seed 0 (414148_0) | single `delaunay` search, n_live 100 | 81,740 | bound count stuck at 20 from ~11k calls; N_eff ≈ 1; live fraction 1.0 | −103,833.4 |
| … seed 1 (414148_1) | same | 80,080 | stuck at 19 bounds from ~15k calls | −103,903.4 |
| interferometer/rectangular sma `numba_cpu_sparse_fp64_wtilde` seed 1 (414156_1) | `mass_total[1]`, n_live 150 | ~99,700 | 11 bounds / 5 ellipses; N_eff frozen at 96 from ~57k calls; live fraction swinging 0.20–0.34 | −3158.37 |

- **Comparisons:** interferometer rectangular seed 0 on the same route finished `mass_total[1]` in 12,240 evals (log Z −3160.5). The A100 `jax_gpu_sparse_wtilde` legs (413974, both seeds) finished in about 13 min. There is no other datacube validation leg.
- **Evidence:** logs are `hpc/batch_cpu/output/output.{414148_0,414148_1,414156_1}.out` and `error/…err` on the RAL checkout `/mnt/ral/jnightin/inference/autolens_inference`. Nautilus checkpoints are under `output/p4_validation/validation_{datacube_delaunay_sma_numba_cpu_sparse_wtilde,interferometer_rectangular_sma_numba_cpu_sparse_wtilde}/…/search_internal/checkpoint.hdf5`. Keep them; they are the reproduction input.

## Candidates (none tested)

- **Likelihood plateaus:** many points returning the same log L (resample-replaced evaluations above the magnitude ceiling, solver floors, or positive-only solver ties). Nautilus cannot shrink a bound through a flat region. Check the fraction of identical log L values in the live set and the recent samples.
- **Route-specific numba W~ behaviour** in the sparse precision path (PyAutoArray interferometer_numba / W~ preload) in the regions these seeds reach, against the JAX GPU route.
- **Not the explanation as measured:** phase-6 hazard D (`draft/research/autolens_profiling/noisy_interferometer_rectangular_likelihood_fd_c.md`). Its noise is about 1e-6 in log L, far below what moves a nested sampler, but it touches the same likelihood and is worth cross-reading.

## Impact

Phase 4 has no CPU validation row for datacube/delaunay, and only one seed for interferometer/rectangular numba. The 4e ingest (autolens_inference#59) records them as did-not-converge. Production users on the numba W~ route could hit the same stall, so this matters beyond the timing campaign.

## Original request (verbatim, 2026-11-06)

"Cancel + record + file" (human, answering whether to cancel the stalled legs 414148 and 414156_1).
