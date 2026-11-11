# Likelihood lifecycle phase 4e follow-up: ingest the three fresh reruns (414639–414641) and close phase 4

Type: research
Target: autolens_inference
Repos:
- autolens_inference
Themes:
- profiling
- inference
Difficulty: small
Autonomy: supervised
Priority: high
Status: issued
Issue: https://github.com/PyAutoLabs/autolens_inference/issues/63
Issued: 2026-11-11
Consequence: judge
Witness: autolens_inference main carries clean rows for multi_dataset/delaunay numba (414639), multi_galaxy/delaunay numba (414640) and multi_galaxy/mge JAX CPU (414641), both seeds each. Each row's slurm job is COMPLETED, none of them was requeued or resumed, and every stage was started fresh. The exporter's --check and the CI lint pass, and the dashboard is regenerated AFTER the final results commit (the exporter stamps the last results revision). The Pulse lens-walltime instance shows the new records after a refresh.
Review-minutes: 10
Unattended: never
Epic: likelihood-lifecycle
Phase: 4
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-09

## Context

- The phase-4e ingest shipped as autolens_inference#60 (merged 2026-11-09, `3a7261bd`; record `complete/2026/11/likelihood-lifecycle-p4e-ingest.md`) with 103 rows / 297 walltime records. Human ruling 2026-11-09: "PR now + rerun". This prompt is the remainder.
- Reruns (fresh, outputs moved aside, `sbatch --no-requeue`, XLA eigen flag, human-approved scheduler-guard exception), submitted 2026-11-09 17:25 UTC from the RAL checkout at a24e993:
  - 414639: multi_dataset/delaunay/hst numba_cpu_sparse_fp64, `--time 3-06:00:00`. The first run 414158 died after 25.5 h on a filesystem EIO.
  - 414640: multi_galaxy/delaunay/hst numba_cpu_sparse_fp64, `--time 2-00:00:00`. The first run 414159 hit its 24 h TIMEOUT in mass_total[1].
  - 414641: multi_galaxy/mge/hst jax_cpu_dense_fp64, `--time 1-00:00:00`. Earlier attempts: 414160 TIMEOUT, then 414362 (resumed, invalid walls), then 414392 (SLURM auto-requeue after NODE_FAIL, so a silent resume).
- Before ingesting, check sacct for any requeue (`sacct -D`), and that the .out shows "Starting new" (never "Resuming") for every timed stage.
- Out of scope: datacube/delaunay numba and interferometer/rectangular numba seed 1 (stalled, cancelled), filed as `draft/research/autolens_inference/numba_wtilde_validation_legs_stall_nautilus.md`.

## Steps

1. When all three are COMPLETED: rsync their `results/**/validation/**` rows into a branch and verify job ids and status.
2. Commit the rows, THEN run the exporter and build_readme, commit the dashboard, and run every lint gate post-commit.
3. PR (human /prm). After the merge, dispatch the PyAutoPulse refresh.
4. Update the phase-4 witness in the epic ledger and propose closing phase 4 (with its gaps listed) to the human.

## Original request (verbatim, 2026-11-09)

"PR now + rerun" (human ruling on how to finish 4e after the 11-06 RAL infrastructure failures).
