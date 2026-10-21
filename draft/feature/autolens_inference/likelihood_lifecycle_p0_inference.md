# Likelihood lifecycle phase 0C: autolens_inference committed clean-slate rows, mirrored tree, `walltime-validation@1` exporter and Pulse registry row

Type: feature
Target: autolens_inference
Repos:
- autolens_inference
- PyAutoPulse
Themes:
- profiling
- samplers
- dashboard
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: `export_inference_summary --check` is current for both artefacts (`dashboard/summary.json` inference-summary with `setup_mode`/`setup_resolved`/`setup_id`/`model_variant`, and `dashboard/walltime_validation.json` as `walltime-validation@1`); `pyauto-pulse check` accepts a new `lens-walltime` registry row pointing at autolens_inference and its receipt ingests the validation document; `tests/test_results_mirror_scripts.py` passes for `results/<dataset_type>/<variant>/`
Review-minutes: 30
Unattended: never
Epic: likelihood-lifecycle
Phase: 0
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-10-21

Phase 0 sub-issue 0C of the `likelihood-lifecycle` epic (ledger `draft/research/autolens_profiling/likelihood_lifecycle_epic.md`; report §3.2, §3.7, §4 phase 0; survey `likelihood_lifecycle_epic_surveys/01_profiling_inference_layout.md` §2, §5). Depends on 0A only (PyAutoPulse#70 merged 2026-10-21 defines `walltime-validation@1`: records keyed by likelihood, instrument, setup_id, host_class, model_variant, sampler, seed with `wall_s`, `likelihood_evals`, `implied_ms_per_eval`, `reference_runtime_record_id`, `predicted_ms_per_eval`, `ratio_measured_over_predicted`, `cores`, `parallel_efficiency`, `release_pin`, `slurm_job_id`, `max_log_likelihood`, `parity_status`; all producer-computed). 0B (autolens_profiling) is queued behind the cluster-pointsolver claim; 0C does not wait for it — `reference_runtime_record_id` points at the Pulse `lens` v2 record ids that exist today and is re-pointed when the `lens` pin moves to @3.

## Rulings applied (confirmed 2026-10-21)

R1 `setup_id` grammar `<backend>_<device>_<operator>_<precision>[_<transformer>]` with `host_class` separate (the current folder names `hpc_a100_jax_cpu_dense_fp64` etc. map to `setup_id` + `host_class`; older CPU rows carrying `hpc_a100` are relabelled `hpc_ral_cpu` only where the row's own host provenance proves it, else kept with a limitation); R7 `local_*` rows are never `current`; R8 (recommended, confirm in the plan) sampler folders `…/samplers/<model_variant>/<sampler>/{auto|explicit/<setup_id>}/seed_<n>`.

## What, as separate PRs in this order (data guard: content and moves never in one PR)

1. **Commit the untracked clean-slate rows first, their own PR**: the 40 files under `results/slam/imaging/hst/` (slam_base, slam_base_light_fixed, slam_delaunay, slam_delaunay_light_fixed × their configs), `prepared/` (7 hash dirs, 84 KB) and `results/archive/2026-10-19_numba_thread_oversubscription/`. Nothing is edited; `README.md` "No pipeline runs yet" is retired in the same PR because it is falsified by the commit.
2. **Move-only PR** (git mv only) to the §3.7 layout: `scripts/<dataset_type>/<variant>/{validation,samplers}/…`, `scripts/misc/<group>/…`; `results/<dataset_type>/<variant>/<instrument>/validation/<model_variant>/<setup_id>/seed_<n>/stages.json` for the SLaM rows; `results/<dataset_type>/<variant>/<instrument>/samplers/<model_variant>/<sampler>/explicit/<setup_id>/seed_<n>/` for the point-source search rows; `results/misc/`; the three dated `results/archive/` dirs re-homed to `archive/YYYY/MM/<slug>/`; `wiki/setups/*.md` keyed by `<dataset_type>/<variant>`; Cortex ledger paths (`PyAutoCortex/projects/autolens_inference.md`) and `wiki/project/state.md` updated by a pointer, never rewritten. `tests/test_results_mirror_scripts.py` added.
3. **Exporter**: `scripts/misc/tooling/export_inference_summary.py` gains `setup_mode` ∈ {auto, explicit} (every existing row `explicit`), `setup_resolved {backend, device, operator, precision, transformer, threads}`, `setup_id`, `host_class`, `model_variant` (`default` / `light_fixed`) on inference-summary records (additive, no version bump unless Insight refuses unknown keys — coordinate with 0D); a second artefact `dashboard/walltime_validation.json` as `walltime-validation@1` built from the SLaM validation rows: `implied_ms_per_eval = wall_s / likelihood_evals × 1000` per stage and per chain, `reference_runtime_record_id` and `predicted_ms_per_eval` taken from the Pulse `lens` snapshot record matching (likelihood, instrument, setup_id, host_class) when one exists (else null with a limitation), `ratio_measured_over_predicted`, `parallel_efficiency` where a 1-core row of the same key exists (else null), `parity_status` from the existing backend-parity view (`match` / `diverged` — the 2026-10-18 jax_gpu_sparse light_fixed divergence is the first `diverged` row); `--check` covers both artefacts; `INFERENCE_SUMMARY.md` documents the second artefact and the clocks.
4. **Pulse registry row** (one-line PyAutoPulse PR): `instance: lens-walltime`, `repo: autolens_inference`, `summary_path: dashboard/walltime_validation.json`, `supported_schema: walltime-validation@1`; receipt fetched; the Pulse board shows the walltime table.

## Out of scope

New runs (phase 4 runs the validation campaign under the Optimal setups with ≥ 2 seeds and the cores sweep); Insight-side changes (0D); sampler campaigns (phase 7); re-labelling any row `current`/`optimal` — walltime records carry no class.

## Blocked-by (operational, not a header gate)

None. autolens_inference PR #30 (docs(hpc) pin table, branch `fix/pin-readme-peeled-commits`, unregistered worktree `pin-readme-peeled`) is open and touches only README; rebase after it merges if it lands first.
