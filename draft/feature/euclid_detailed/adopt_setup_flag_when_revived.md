# euclid_detailed: adopt `--setup` (automatic compute setup) instead of `--use_cpu` when the project is revived

Type: feature
Target: euclid_detailed
Repos:
- euclid_detailed
Themes:
- hpc-gpu
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: judge
Witness: `active/euclid_detailed` (PyAutoLabs/euclid_detailed) uses the same CLI as euclid_strong_lens_modeling_pipeline after likelihood-lifecycle 5H: `--setup <auto|cpu|gpu|setup_id>` (default auto) and `--number_of_cores auto`, with `--use_cpu` as a deprecated alias. `scripts/slam.py` passes `setup=setup` to each stage's analysis instead of `use_jax=not use_cpu`, and the `hpc/batch_cpu/submit_slam_*` scripts match.
Review-minutes: 10
Unattended: no
Lane: any
Filed: 2026-11-25
Gate: the project is revived (Cortex: dormant since 2026-11-13); euclid_strong_lens_modeling_pipeline 5H (issue #141) merged; the library release.
Epic: likelihood-lifecycle
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md

## Context

Deferred from 5H (design call 4, human-approved 2026-11-25), because the project is dormant and lives in the human's Science area. The survey found:
- `util.py:1669-1776` holds a forked `parse_fit_args`;
- `scripts/slam.py:8-869` has 6× `use_jax=not use_cpu`, plus `JAX_PLATFORMS=cpu` for source_lp;
- `hpc/batch_cpu/submit_slam_pipeline:80` and `submit_slam_source_lp:40` pass `--use_cpu`.

Mirror the pipeline's 5H change, including the `--use_cpu` → `--setup cpu` alias.
