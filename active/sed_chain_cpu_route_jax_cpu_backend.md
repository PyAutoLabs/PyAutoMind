# SED chain (Sersic + waveband fits) runs on CPU by default, JAX on the CPU backend like vis_lp

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- hpc
Difficulty: easy
Autonomy: safe
Priority: high
Status: active
Consequence: judge
Review-minutes: 10
Unattended: ready
Filed: 2026-09-11
Issued: 2026-09-11

User request (verbatim, 2026-09-11, after the SED chain for the eight finished
dr1_prelim tiles was submitted as GPU job 342648 from `hpc/batch_gpu/submit_sersic_waveband`):

"""
this was also meant to run on CPU, not GPU, everything is CPU. This run is fine on GPU so
dont cancel anything but update the project to ensure all future runs use CPU, I guess
using the JAX LH Function siilar to the vis_lp
"""

## Context (surveyed 2026-09-11)

- The only SED-chain submit script is `hpc/batch_gpu/submit_sersic_waveband`
  (`--partition=gpu`, `--gres=gpu:1`, `--cpus-per-task=1`, 8 h, array 0-9,
  `PYAUTO_OUTPUT_DIR=output_sed`); it refuses to run unless
  `jax.default_backend() == "gpu"`, then runs
  `scripts/sersic_lens_model_waveband.py --sample --dataset`. There is no
  `hpc/batch_cpu/` counterpart, and `hpc/README.md`'s route table lists no CPU
  route for the SED chain.
- `scripts/sersic_lens_model.py` (`use_jax=True`, "JAX is always on for this
  search") and `scripts/lens_model_waveband.py` (`use_jax=True`) are already JAX
  likelihoods, so on CPU they should run the way `vis_lp` does in
  `hpc/batch_cpu/submit_initial_lens_model_two_stage`: JAX pinned to the CPU
  backend (`JAX_PLATFORMS=cpu`) with the thread counts set from
  `$SLURM_CPUS_PER_TASK`, on `--partition=ral`. Both scripts accept `--use_cpu`
  and `--number_of_cores`; check what those do to the Sersic and waveband
  searches (they must not switch the likelihood to Numba the way `vis_pix` does
  under `--use_cpu`) before deciding whether the CPU route passes them.
- The chain seeds from `output_sed/<sample>/<tile>/initial_lens_model/vis_lp/<hash>.zip`
  (copied from `output/`), and `sersic_lens_model_waveband.py` forces `stage="vis_lp"`;
  the CPU route must keep that hash reproducible (same search settings, no
  `number_of_cores` on the `vis_lp` search).
- Job 342648 (GPU, 8 tiles) is running and must not be cancelled or resubmitted;
  this task changes the project so the *next* submissions (tiles 102007299 and
  102007903 once 342629 lands, and every future sample) run on CPU.

## Deliverable

1. `hpc/batch_cpu/submit_sersic_waveband` — the CPU submit for the SED chain
   (partition `ral`, `--cpus-per-task` matching the two-stage script, JAX on the
   CPU backend via the same `env JAX_PLATFORMS=cpu …` pattern as stage 1 of
   `submit_initial_lens_model_two_stage`, a backend assertion that the backend is
   `cpu`, walltime sized from the euclid precedent 319273/319369 plus the Sersic
   stage, array 0-9, same dataset list and `PYAUTO_OUTPUT_DIR=output_sed`).
2. `hpc/batch_gpu/submit_sersic_waveband` stays as the optional GPU route but
   is no longer the default: `hpc/README.md` route table gains the CPU SED row
   marked as the default, the GPU row is marked optional, and the Cortex task
   `## Where to look` SED line is updated to the CPU script.
3. `hpc/sync submit` usage text and any docstring in
   `scripts/sersic_lens_model_waveband.py` that names the GPU script are updated.
4. The 8-tile copy `hpc/batch_gpu/submit_sersic_waveband_8tiles` (science-clone
   commit 6ffdc52, one-off for 342648) is not part of the pipeline repo; do not
   port it.

Verification: a local dry run of the CPU command line on one tile with
`--stage`-free invocation confirming `JAX backend: cpu` and that `vis_lp` short-
circuits ("Fit Already Completed") against a seeded zip; the hash of the seeded
`vis_lp` must be unchanged.
