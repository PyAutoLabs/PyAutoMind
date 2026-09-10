# Backend-parameterised SLaM base-run driver, per-stage results and submits (autolens-inference phase 3)

Type: feature
Target: autolens_inference
Repos:
- autolens_inference
Themes:
- inference
- slam
- jax
- numba
- hpc
Difficulty: hard
Autonomy: supervised
Priority: high
Epic: autolens-inference
Phase: 3
Status: draft
Consequence: judge
Witness: `PYAUTO_TEST_MODE=1 python scripts/imaging/slam/hst.py --backend <b> --inversion <i> --config-name local_<b>_<i>_fp64` exits 0 for all six (b, i) in {jax_cpu, numba_cpu} × {dense, sparse} plus jax_gpu×{dense,sparse} on a CUDA host, each writing `results/slam/imaging/hst/<config_name>/stages.json` with five stage rows; `build_readme.py --check` renders the six rows; `wall/check_submits.py --check` passes on six real submit scripts whose WALL-BASIS cites a rate measured on this cell
Review-minutes: 45
Unattended: ready
Filed: 2026-09-10

Builds the thing the repo exists for: one script that runs the standard imaging SLaM chain
end to end under any of the three backends and either inversion path, records every stage
as a comparable row, and can be submitted to RAL. Phase 4 then files the Cortex task
`slam_hst_base` that runs the six legs and rules on parity. Design record: the phase-1
prompt `complete/2026/09/autolens-inference-birth.md` and PyAutoMind#399; nothing from the retired
`inference_programme` is reused.

## The chain (mirror `autolens_workspace/scripts/guides/modeling/slam_start_here.py`)

`source_lp[1]` (Nautilus n_live 200 / n_batch 50) → `source_pix[1]` (150/20) →
`source_pix[2]` (75/20) → `light[1]` (150/20) → `mass_total[1]` (150/20). Workspace-default
mesh: `RectangularBilinearAdaptDensity` (28×28) then `RectangularBilinearAdaptImage` with
`reg.Adapt` (both jittable everywhere); MGE 20×2 lens light / 20×1 source;
`Isothermal + ExternalShear` → `PowerLaw`. Nautilus everywhere. Positions likelihood on
for the pixelized stages (a mesh stage with no `positions.info` is not citable). Decide and
record whether the non-uniform `over_sample_size_pixelization` map before `source_pix[2]`
stays (it triples JAX compile per stage); default: keep it, it is the workspace default.

## Driver contract — `scripts/imaging/slam/hst.py` over `scripts/misc/slam/_runner.py`

- Thin leaf: `run_slam(dataset_class="imaging", default_instrument="hst")`; the runner
  owns everything. Instrument is `--instrument` (from `instruments/imaging.py`), never a
  directory; the HST cell is the simulated dataset from
  `scripts/misc/simulators/imaging.py --instrument hst` (auto-simulated if missing, so RAL
  needs no data transfer; truth in `dataset/imaging/hst/tracer.json`).
- `--backend {jax_cpu, numba_cpu, jax_gpu}` (from `_inference_cli.py`):
  `numba_cpu` → `use_jax=False` on every Analysis, `PYAUTO_DISABLE_JAX=1` exported before
  autolens import, `SettingsSearch(number_of_cores=N)` with N from `--cores` /
  `SLURM_CPUS_PER_TASK`; `jax_cpu` → `JAX_PLATFORMS=cpu`, `NPROC` = cores; `jax_gpu` →
  assert `jax.default_backend() == "gpu"` at start, else exit non-zero (no silent CPU
  fallback). `JAX_ENABLE_X64=True` always; `--use-mixed-precision` maps to `_mp`.
- `--inversion {dense, sparse}`: `sparse` → `dataset.apply_sparse_operator()` under JAX
  (any device) or `dataset.apply_sparse_operator_cpu()` under numba, applied after mask +
  over-sampling and re-applied after any dataset re-derivation (see
  `autolens_workspace/scripts/imaging/features/pixelization/cpu_fast_modeling.py`);
  `dense` → neither call (`InversionImagingMapping`). MGE-only stages are unaffected;
  say so in the row.
- `--seed` (Nautilus seed), `--config-name` grammar
  `{local,hpc_a100}_{jax_cpu,numba_cpu,jax_gpu}_{dense,sparse}_{fp64,mp}`, `--output-dir`
  (default `output/slam/imaging/hst/<config_name>/seed_<n>/`), `--stages` to stop early
  (`source_lp` … `mass_total`). Outputs are kept: `hpc_mode: false`, `remove_files: false`
  (config/general.yaml already says so).
- `AUTOLENS_INFERENCE_SMOKE=1` module-top short-circuit; `PYAUTO_TEST_MODE=1` must run all
  five stages in minutes on a laptop.

## Per-stage rows — `results/slam/imaging/hst/<config_name>/stages.json` (+ PNG)

Fresh schema, version 1, top-level: `config_name`, `backend`, `inversion`, `precision`,
`instrument`, `seed`, `version` (autolens), `device` (backend/GPU/host/`SLURM_JOB_ID`),
`stages: [ … ]`. Per stage: `name`, `free_parameters`, `n_live`, `n_batch`,
`wall_s` (sampler), `total_wall_s` (incl. viz + compile), `compile_s` (JAX first-call
split, 0 under numba), `likelihood_evals` (reject-inclusive, from the sampler), `log_evidence`,
`log_evidence_err`, `max_log_likelihood`, `posterior` (median + 1σ per free parameter,
plus `einstein_radius`, `slope`, `shear_magnitude` where defined), `truth_delta_sigma`
(vs `tracer.json` where the parameter exists), `positions_info_present`, `completed`
(the `.completed` marker), `resumed` (false unless a resume marker was seen). One JSON
per (config_name, seed); `build_readme.py` renders a `slam` table with one row per
config_name × seed × stage and a parity view (same seed, backend as column, Δ in σ of
`mass_total[1]`'s posterior). Reject-inclusive evals and the truth anchor are required
fields, not optional.

## Submits — `hpc/batch_gpu/submit_slam_hst_{jax_gpu}_{dense,sparse}` and `hpc/batch_cpu/submit_slam_hst_{jax_cpu,numba_cpu}_{dense,sparse}`

From the templates. GPU: `--partition=gpu --gres=gpu:1 --cpus-per-task=4 --mem=64gb`,
`--array=0-1` (seed = array index), `JAX_ENABLE_X64=True` exported, `NPROC=$SLURM_CPUS_PER_TASK`.
CPU: `--partition=ral --cpus-per-task=8` (there is no `cpu` partition). Every submit carries a
`# WALL-BASIS:` block whose rate was **measured on this cell and backend** in this phase
(`scripts/misc/wall/rates.py` ships empty on purpose): run a `PYAUTO_TEST_MODE`-free
`source_lp[1]`-only leg per backend locally or as a 1-hour RAL job, record s/eval, fill
`STEP_RATE` with provenance, budget `--time` at 2× the estimate. Expected order of
magnitude for the full chain: 2–4 h A100, 4–8 h numba-sparse 8-core, 6–12 h JAX-CPU.

## Hazards to design around (do not rediscover)

- `JAX_ENABLE_X64` is not inherited by sbatch — export it in the submit.
- `XLA_PYTHON_CLIENT_PREALLOCATE=false` on the A100; never `MEM_FRACTION` there.
- `NPROC=1` costs ~3× on JAX-CPU; `NPROC` sizes XLA's thread pool, BLAS envs are separate.
- Nautilus under `use_jax=True` ignores the pool and vmaps with `n_batch`; under numba it
  uses `number_of_cores` — never hand it a `Pool` object.
- A frozen `Calls | 0` in `search.log` is stdout buffering; `PYTHONUNBUFFERED=1` is in
  `activate.sh`; check `checkpoint.hdf5` before calling a run dead.
- Never cite a mesh stage without `positions.info`; `apply_sparse_operator` raises if
  `psf.convolve_over_sample_size > 1`.
- An autofit identifier collision resumes a completed fit in seconds and re-stamps it —
  seed and config_name must be in the output path.

## Out of scope

Real SLACS1430 (task 2 of the Cortex project), interferometer / point-source leaves
(dirs exist, stay empty), any non-Nautilus search, hoisting `instruments/` +
`simulators/` into PyAutoLens (separate prompt).
