# Do the Nautilus costs measured on toy fits transfer to representative fits?

Type: research
Target: autofit_profiling
Consequence: judge

## Original request

> I approve of all this, would it be a fair statement to say at the moment we are doing a lot of profiling and getting run times but not getting many great leads for speed up?

> ok continue

## Approved investigation

Check existing PyAutoFit and lensing results for neural-training and bound-geometry costs. Recover the timing denominator, hardware, repeats and measurement method. Where a record contains only a likelihood estimate or total time, state which costs can be identified. Identify one CPU speedup lead and record the decision in the parent epic. Use archived data and existing domain-owned tasks.

## Findings, 24 November 2026

**Prioritise the interval between neural-bound updates for the next complete-fit comparison.** Both neural training and geometry recur when Nautilus builds a bound. The archived PyAutoFit breakdown measures their combined cost directly. A separate experiment changed update frequency and recorded fewer bound builds while retaining the neural ensemble.

| Workload | What the archive measured | What it establishes |
|---|---|---|
| PyAutoFit Gaussian profile, three free parameters, 100 pixels, NumPy CPU, one core | Three fresh fits with seed 1, four networks and output enabled. Median total wall 28.41 s, 7,501 likelihood calls each. Exclusive neural training plus geometry took 64.10%, 61.51% and 64.95% of each fit. Median individual shares were 43.37% training, 20.43% geometry, 24.53% checkpoints and 1.13% likelihood. | Training plus geometry dominated each application fit. The joint share was calculated inside each repeat before taking the median. The repeats measure timing variation on one sampling path. [Raw PyAutoFit repeats](https://github.com/PyAutoLabs/autofit_profiling/blob/e64e3a7e5c8f9d9b3e4aba3fded2c0ea04b09dbf/results/gaussian_x1/nautilus/breakdown.json) |
| Solved source-plane point lens, five free parameters, RAL JAX CPU | Five seeds took 50.38–58.51 s of search wall. Warm batched cost per evaluation multiplied by actual evaluation count accounted for an estimated 0.0405–0.0447% of that wall. | Accelerating this warm likelihood alone offers little leverage. The estimate leaves training, geometry, orchestration and I/O unresolved. [Five per-seed receipts](https://github.com/PyAutoLabs/autolens_inference/tree/b0e49501edf2d76931592ac85900066004222084/results/searches/point_source/nautilus/simple/source_plane_solved/hpc_a100_jax_cpu_dense_fp64) |
| Simulated HST imaging with 20 linear Gaussian components, JAX CPU | Two completed three-stage chains recorded 3,674 and 3,813 s summed sampler wall. The 15-parameter source stage took 2,164 and 2,225 s. Stage-level compile, evaluation count and wall fields provide no exclusive training or geometry time. | The source stage is the longest in both chains. The records leave its internal bottleneck open. [Seed 0](https://github.com/PyAutoLabs/autolens_inference/blob/0af93f6092ca4b147c570814a535cb34f7c700de/results/imaging/mge/hst/validation/default/jax_cpu_dense_fp64/seed_0/stages.json) · [Seed 1](https://github.com/PyAutoLabs/autolens_inference/blob/0af93f6092ca4b147c570814a535cb34f7c700de/results/imaging/mge/hst/validation/default/jax_cpu_dense_fp64/seed_1/stages.json) |

### Why change update frequency first?

The July 10D Gaussian sweep tried `n_update=400` at `n_live=200`. It recorded three bound builds and 7.00 s, against five builds and 20.92 s for the default. Both used 10,200 likelihood evaluations. Log evidence moved from −0.010 to −0.029. ESS moved from 10,048.5 to 10,049.4. This was one seed with the baseline run first on a laptop with substantial timing variation. The sweep's peak-finding metric was one evaluation in both arms. The standalone cadence arm was absent from the Gaussian-data rows. These limits motivate a paired test on data with a meaningful peak-finding challenge. [Sweep and run order](https://github.com/PyAutoLabs/autofit_workspace_developer/blob/24b0c4d7abc6baa13136c4787c1f6799e9f9a64f/searches_minimal/nautilus_sweep.py) · [Measured rows](https://github.com/PyAutoLabs/autofit_workspace_developer/blob/24b0c4d7abc6baa13136c4787c1f6799e9f9a64f/searches_minimal/output/nautilus_sweep_summary.txt)

The next candidate experiment is default cadence versus twice the update interval, keeping the four networks, serial training, pool safeguards and output settings fixed. Pair seeds and alternate arm order on the real Gaussian profile. Include a curved or multimodal control before adoption. Judge total fit time alongside bound count, likelihood calls, evaluations to reach the peak, recovered modes, log evidence, posterior and ESS. A slower climb or lost mode would outweigh a wall-time gain. Link the owning profiling or inference task before campaign execution. The scalar ellipsoid change remains experimental. Wider phase 0b, including the 30D evidence gate, remains open.
