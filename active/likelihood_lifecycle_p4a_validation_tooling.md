# Likelihood lifecycle phase 4a: inference wall-time validation tooling (submit generator, efficiency, day-zero reference)

Type: research
Target: autolens_inference
Repos:
- autolens_inference
Themes:
- profiling
- inference
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Issue: https://github.com/PyAutoLabs/autolens_inference/issues/51
Issued: 2026-11-02
Consequence: judge
Witness: autolens_inference main carries (1) a phase-4 validation campaign generator whose --check passes and whose submits cover the imaging/hst gaps (delaunay Optimal GPU jax_gpu_dense + Secondary CPU jax_cpu_sparse, 2 seeds; rectangular Secondary CPU jax_cpu_sparse seed 1) and a RAL cores sweep (one pixelized stage, cores 1..32) on the libraries at 2026.10.25.1; (2) export_inference_summary computing parallel_efficiency from cores-sweep rows (null stays null without a 1-core row) and marking the adopted 2026.10.17.1 rows; (3) its cached Pulse reference refreshed to the day-zero snapshot; lint and tests green
Review-minutes: 20
Unattended: never
Epic: likelihood-lifecycle
Phase: 4
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-02

## Context

- Phase 4 (epic): inference wall-time validation on RAL. Per likelihood, run the full model (SLaM where it exists) under Optimal GPU, Optimal CPU and Secondary CPU, seeds >= 2, plus a cores sweep on ral for the CPU likelihoods. Publish records with implied_ms_per_eval, ratio_measured_over_predicted, parallel_efficiency and parity_status as walltime-validation@1.
- Human rulings 2026-11-02:
  - "I am happy for day zero to span a few different versions": adopt the 56 existing 2026.10.17.1 imaging/hst rows; no re-run.
  - Scope: one reference instrument per likelihood ("One per likelihood").
  - "Yes, start 4a".
  - Focus on non-gradient (Nautilus) work while gradient bugs are fixed in another chat.
- State (survey 2026-11-02):
  - autolens_inference `dashboard/walltime_validation.json` holds 56 records, all 2026.10.17.1, imaging/hst only.
  - Rectangular has numba_cpu_sparse 8+2 (light_fixed), jax_cpu_dense 10+2, jax_cpu_sparse 5 (seed 0 only), jax_gpu_dense 10+2 and jax_gpu_sparse 10+2.
  - Delaunay has numba_cpu_sparse 4+1 only.
  - parallel_efficiency is null everywhere. 17 jax_cpu rows carry host_class hpc_a100.
  - Exporter `scripts/misc/tooling/export_inference_summary.py` (build_walltime :622, parallel_efficiency=None :738). SLaM runner `scripts/misc/slam/_runner.py` is imaging only. Other dataset types have README stubs only.
  - Setups come from autolens_profiling `catalogue/runtime_estimates.yaml`. Imaging pixelized: Optimal CPU numba_cpu_sparse_fp64, Optimal GPU jax_gpu_dense_fp64, Secondary CPU jax_cpu_sparse_fp64.
- The jax_gpu_sparse light_fixed divergence (2026-10-18; rectangular mass_total[1], +274σ einstein_radius) is not on an imaging Optimal setup. Check it in 4c, where interferometer's Optimal GPU is jax_gpu_sparse_wtilde.

## Plan (phase 4, approved 2026-11-02; this task is 4a)

- **4a (this task, no compute):**
  - Campaign generator for the validation legs (pattern of autolens_profiling `gradient_p6.py`): imaging/hst gaps plus the cores sweep. Walls come from runtime_estimates ms/eval × the Nautilus eval counts of the adopted rows; `--write` / `--check`; tests.
  - Exporter: parallel_efficiency from cores-sweep rows, and an adopted-pin note on the 2026.10.17.1 rows.
  - Refresh the cached Pulse reference to the day-zero snapshot.
  - Pin: reuse /mnt/ral/jnightin/profiling/PyAuto_2026.10.25.1 via PYAUTO_LIB_BASE (document in hpc/README.md).
- **4b (compute, human go):** imaging/hst gap legs and the cores sweep.
- **4c:** interferometer (sma) and point_source_source runners, then legs (human go).
- **4d:** runners for the remaining likelihoods, one reference instrument each, then legs (human go).
- **4e:** ingest, the Pulse walltime snapshot, and the estimator export for 5E.

## Rules

No compute without the human's go per batch. CPU jobs only on --partition=ral. Merge only by the human's /prm.

## Request (human, 2026-11-02, verbatim)

"yes do 1 and 2, then plan phase 4, I think we are able to do a lot of tasks which dont use gradients (e.g. Nautilus base sampling campaign doesnt use them) so lets focus on them whilst I bug fix in another chat!"
