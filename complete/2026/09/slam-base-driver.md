## slam-base-driver
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/2 (closed completed 2026-09-11)
- completed: 2026-09-11
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/3
- shipped: 2026-09-11 — one PR on `feature/slam-base-driver` (commits `6a9e3cc` +
  `2a8dfe2`, merge `874bff5`); CI `lint [pull_request]` run 34618322248 green on every
  step (ruff check, ruff format --check, `build_readme.py --check`,
  `wall/check_submits.py --check`, `pytest scripts/misc/test/` 38 passed, lychee, the
  simulators + SLaM driver smoke leg). No library PR — the library-first merge gate is
  n/a, and `autolens_inference` is `category: project`, so the Heart freeze gate does not
  apply (`pyauto-heart freeze --show` read `not frozen` at merge time anyway).
- classification: feature (autolens_inference) — epic `autolens-inference`, phase 3 of 4.
  Consequence tier `judge`, so no shadow row.
- summary: the backend-parameterised SLaM base-run driver, the one script the repo exists
  for. A thin leaf `scripts/imaging/slam/hst.py` sits over a new
  `scripts/misc/slam/_runner.py` (1411 lines) which runs the standard 5-stage HST SLaM
  chain under any of `{numba_cpu, jax_cpu, jax_gpu} × {dense, sparse}` and writes a
  schema-v1 `results/slam/imaging/hst/<config>/stages_seed<n>.json` (plus a PNG) with one
  comparable row per stage: wall, compile split, reject-inclusive evals, log Z, posterior,
  truth delta/sigma, `positions.info` presence. Also: `--cores` / `--stages` /
  `--output-dir` on `_inference_cli.py`; a stage-flattening parity view in
  `build_readme.py`; a **repo-wide** cell-id change in `wall/check_submits.py`
  (`<dataset>/<task>/<leaf>`, re-keying every existing submit's wall-basis contract); six
  production SLURM submits (`hpc/batch_cpu/submit_slam_hst_{numba_cpu,jax_cpu}_{dense,sparse}`,
  `hpc/batch_gpu/submit_slam_hst_jax_gpu_{dense,sparse}`) plus the A100 rate probe
  `hpc/batch_gpu/submit_slam_hst_rate_jax_gpu`; three new test modules (38 tests total);
  the `lint.yml` smoke leg and a `profile.yml` euclid dispatch witness; and docs
  (`README.md`, `AGENTS.md`, `hpc/README.md`, `scripts/imaging/slam/README.md`,
  `scripts/misc/wall/README.md`) with the `wiki/project/state.md` journal entry.
- rates: the first numbers ever measured in this repo — `laptop_numba_cpu` **0.06831
  s/eval** (17,950 evals / 1,226 s) and `laptop_jax_cpu` **0.04925 s/eval** (25,500 evals
  / 1,256 s). Both are PARTIAL `source_lp[1]`-only probes at production settings on the
  8-core laptop, run sequentially in matched windows and stopped by hand; their
  `PROVENANCE` entries say what they may not be used for. `jax_cpu` was 1.39× faster per
  evaluation than `numba_cpu` on that stage — an observation about `source_lp[1]`, not
  about the chain.
- witness: numba HST legs green (5 stages, `positions.info` present on all pixelized
  stages); `jax_cpu` HST legs **OOM** on the 15 GB laptop (13 GB dense / 21.6 GB sparse at
  `source_pix[1]` with `n_batch=20`) and were proven instead on `--instrument euclid`;
  `jax_gpu` refuses cleanly with exit 2 on a host with no GPU. That OOM is a measurement,
  not an inconvenience: the two JAX-CPU legs of the parity row exist only as RAL jobs.
- decisions and departures: a **positions likelihood on all four pixelized stages** (the
  workspace chain attaches one to `source_pix[1]` and `mass_total[1]` only; a mesh stage
  with no `positions.info` beside it is not citable here, and the phase-4 witness reads
  `positions_info_present` on every one); `log_evidence_err: null` with a sibling note
  (nautilus 1.0.5 exposes no `log_z_err`, and a derived one would be an invention); the
  over-sample map is kept and sparse is re-applied on top of it; test-mode positions are
  read from the simulator's `positions.json`; `--output-dir` overrides the PyAutoFit
  output root; a failure-writing `try/except` records partial chains rather than losing
  them; and every production submit ships `source: unmeasured  probe-first: yes` with a
  containment `--time` (12 h on the A100 legs, 5 days on the RAL CPU legs) rather than a
  `2 × rate × steps` budget — after ~21 minutes neither probe had left nautilus's
  exploration phase (128 evals per live point × 725 live points ≈ 92,800 evaluations is a
  *floor* on the chain), and a floor multiplied by a laptop rate for a different kind of
  stage is an invention.
- bugs the witness caught (four, all fixed in the PR):
  1. `jax.default_backend` **raises** rather than returning a value on a host with no CUDA.
  2. `samples_info` `time` and `log_evidence` come back as **strings**.
  3. `model.all_names` yields alias **tuples**, not plain names.
  4. Zero-sigma keys blew up the truth-delta computation.

## Follow-ups

- **A100 rate unmeasured.** RAL job **342695** (`submit_slam_hst_rate_jax_gpu`) is
  PENDING(Priority) behind seven of our own 12-hour `gpu` jobs and three foreign jobs on
  `euclid-ral-gpu-2`. When it lands: `hpc/sync pull`, fill the `a100` row in
  `scripts/misc/wall/rates.py`, and flip the two GPU submits from `source: unmeasured` to
  measured.
- **`results/` is empty** — no production stage completed, so no parity row exists. It
  fills when phase 4's Cortex task `slam_hst_base` runs (six legs × two seeds).
- **Hygiene:** `PyAutoBrain/bin/ensure_workspace_labels.sh`'s `REPOS` list lacks both
  `autolens_inference` and `autolens_profiling`.

## Heart at ship

Shipped under a human-acknowledged **YELLOW** (2026-09-11, score 40, no RED reasons). The
`heart-ack` reasons carried on the `active.md` row, preserved here as that row is pruned:

- "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)"
- "profiling drift: runtime/imaging/mge/mge_likelihood_summary_hst_v2026.8.17.1.json [eager, full, vmap]"
- "profiling drift: runtime/imaging/mge_mass_jax/mge_mass_jax_likelihood_summary_hst_v2026.8.17.1.json [jax_mge_mass]"
- "profiling drift: runtime/imaging/pixelization_numba_mge_mass/pixelization_numba_mge_mass_likelihood_summary_hst_v2026.8.17.1.json [numba_cpu_mge_mass]"
- "release validation incomplete: no rehearsal for current source"
- "Acknowledged by the human in-session 2026-09-11 (YELLOW, score 40, no RED reasons). All five are organism-scope; none names autolens_inference, which is not in the release chain. No library PR — library-first merge gate n/a."

## Original prompt

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
Status: formalised
Consequence: judge
Witness: `PYAUTO_TEST_MODE=1 python scripts/imaging/slam/hst.py --backend <b> --inversion <i> --config-name local_<b>_<i>_fp64` exits 0 for all six (b, i) in {jax_cpu, numba_cpu} × {dense, sparse} plus jax_gpu×{dense,sparse} on a CUDA host, each writing `results/slam/imaging/hst/<config_name>/stages.json` with five stage rows; `build_readme.py --check` renders the six rows; `wall/check_submits.py --check` passes on six real submit scripts whose WALL-BASIS cites a rate measured on this cell
Review-minutes: 45
Unattended: ready
Filed: 2026-09-10
Issued: 2026-09-11
Issue: https://github.com/PyAutoLabs/autolens_inference/issues/2

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
