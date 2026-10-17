# `@autolens_inference` HST clean slate, phase 1: lens-light mode as a run variant, pinned-release submits, row provenance

Type: feature
Target: autolens_inference
Repos:
- autolens_inference
- PyAutoInsight
- PyAutoCortex
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: a euclid-cell `PYAUTO_TEST_MODE=1` chain with `--lens-light both` writes two complete rows (`slam_base` and `slam_base_lightfixed`) from one process, each carrying the five library revisions and the job id, with the fixed-light mass stage model holding no linear light profiles; `--export-prepared` produces a verified manifest for each light mode; all four new submits pass `check_submits.py --check`; `activate.sh` honours a library-root override; CI green.
Review-minutes: 30
Unattended: needs-slicing

Why: the human opened the PyAutoInsight campaign `hst-imaging-mass-samplers` on 2026-10-17 as a clean slate ("we did kind of start a campaign but weve done lots of improvements since warranting a clean slate"). The Nautilus base of the HST SLaM chain is to be re-measured from scratch on PyAuto release 2026.10.17.1 on the A100 (`jax_gpu`, dense and sparse) and on CPU (`jax_cpu`, dense and sparse, human decision), seeds 0 and 1, with the mass stage run both with the linear lens light the chain uses today and with the lens light fixed to ordinary profiles ("Fix lens light to ordinary profiles", human decision 2026-10-17). Other samplers then run on the frozen mass-stage problems (`scripts/misc/experiments/run.py`). The runner cannot express the second light mode, a run cannot be pinned to a release on RAL, and result rows record neither library revisions nor the job id (the 2026-10-17 journal entry names that gap). No compute is part of this task.

Shape (all in `autolens_inference`, no library change):
1. `--lens-light {linear,fixed,both}` on the SLaM runner (`scripts/misc/slam/_runner.py`, `_inference_cli.py`), default `linear`, so every existing invocation is unchanged. `fixed` builds `mass_total[1]` with the lens galaxy's light taken from `light_result.max_log_likelihood_fit.model_obj_linear_light_profiles_to_light_profiles` (ordinary profiles carrying the solved intensities; grounded in `autogalaxy/abstract_fit.py`), so the inversion carries no lens-light columns; everything else in the stage (PowerLaw mass chained from the source_pix Isothermal, source, positions likelihood, Nautilus settings, seed) is identical. `both` runs stages 1 to 4 once and `mass_total[1]` twice, linear then fixed.
2. The light mode is a run variant, not a config: variant stays `slam_base` for `linear` (the name the rows are written under) and becomes `slam_base_lightfixed` for `fixed` (same rule for other meshes). The variant reaches the results path, the PyAutoFit `path_prefix` of the mass stage only (stages 1 to 4 keep the linear variant's prefix, so `fixed` resumes them), the `target` id and a new row field `lens_light_mode`. Result schema v3: add `lens_light_mode`, `library_revisions` (the import-selected checkouts, reuse `experiments/prepared.library_revisions`), `release_pin` (from an environment variable the submit exports, else null) and `slurm_job_id` (`SLURM_JOB_ID`/`SLURM_ARRAY_JOB_ID`+`SLURM_ARRAY_TASK_ID`, else null). v2 rows still read. The README parity view and `export_inference_summary.py`/`inference_catalogue.py` carry the new fields and keep the two variants in separate parity groups.
3. `--export-prepared` works under both modes and names the problem by light mode (`setup_id` or problem id distinguishes `slam_base` from `slam_base_lightfixed`), so `experiments/run.py` can later run nautilus, emcee, nuts and smc on either frozen problem; `validate_setup_binding` still passes for the rectangular family.
4. `activate.sh`: `BASE=${PYAUTO_LIB_BASE:-/mnt/ral/jnightin/PyAuto}` so a submit can point PYTHONPATH at a private pinned checkout set (five repos at their `v2026.10.17.1` tags under one directory) while sharing the venv; the shared mirror is never pulled (standing rule). Document in `hpc/README.md` how the pin directory is created on the login node (clone each repo, `git checkout v2026.10.17.1`), and that a row's `library_revisions` must equal those tags.
5. Four new submits, one job per (backend, inversion) with `--array=0-1` and `--lens-light both`: `hpc/batch_gpu/submit_hst_cleanslate_jax_gpu_{dense,sparse}` (`--partition=gpu`, `--gres=gpu:1`, 4 CPUs, 64 GB, 12 h containment) and `hpc/batch_cpu/submit_hst_cleanslate_jax_cpu_{dense,sparse}` (`--partition=ral` only, 8 CPUs, memory from the 2026-09-11 measurement: 13 GB dense, 21.6 GB sparse at source_pix[1] on jax_cpu, so 48 GB/64 GB; 5-day containment; never `gpu`, `ral,gpu` or `gpu,ral`). Each exports `PYAUTO_LIB_BASE` to the pin directory and `PYAUTO_RELEASE_PIN=2026.10.17.1`, writes to fresh output trees (config names `hpc_a100_jax_gpu_{dense,sparse}_fp64` and `hpc_a100_jax_cpu_{dense,sparse}_fp64` under a new output root `output/cleanslate/…`, or the variant level, decide-and-flag; the 2026-09-24 trees must not be resumed), and carries a WALL-BASIS block per `scripts/misc/wall/README.md` (`probe-first: yes`, no invented wall; the A100 rows of 2026-09-24 may be cited as a prior observation for the mass stage only, not as a rate).
6. Tests in `scripts/misc/test` for the variant naming, schema v3 fields, the fixed-light model containing no linear profiles (test mode, euclid cell), and the export under both modes. `wiki/setups/rectangular.md` and `scripts/imaging/slam/README.md` describe the light-mode variant. Insight task `hst_mass_base_light_modes` and the Cortex `## Now` get the phase-1 link on close-out; no Cortex run line is written (nothing submitted).

Out of scope: any library change; numba_cpu legs; the Delaunay variant; submitting jobs; sampler waves (Insight task `hst_mass_samplers_wave1`); changing priors (the `drop_1e3_prior_centring_after_631` question is carried, not decided).

Witness: a euclid-cell `PYAUTO_TEST_MODE=1` chain with `--lens-light both` writes two complete rows (`slam_base` and `slam_base_lightfixed`) from one process, each carrying the five library revisions and the job id, with the fixed-light mass stage model holding no linear light profiles; `--export-prepared` produces a verified manifest for each light mode; all four new submits pass `check_submits.py --check`; `activate.sh` honours a library-root override; CI green.

Review-minutes: 30
Unattended: needs-slicing
