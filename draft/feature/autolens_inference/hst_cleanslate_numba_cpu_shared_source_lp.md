# `@autolens_inference` HST clean slate: numba_cpu base legs that share the jax_cpu source_lp[1]

Type: feature
Target: autolens_inference
Repos:
- autolens_inference
- PyAutoInsight
- PyAutoCortex
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: on the euclid cell in test mode, a `jax_cpu` chain run with `--stages source_lp` followed by a `numba_cpu` chain with `--stages-from local_jax_cpu_dense_fp64:source_lp` completes all five stages, its row marks `source_lp[1]` as `shared_from_config: local_jax_cpu_dense_fp64` with that stage's wall excluded from the chain wall field, the numba stages report `use_jax: false`, the mass stages under `--lens-light both` export both prepared problems; a `--stages-from` pointing at an incomplete stage exits 3 without fitting; the two new submits pass `check_submits.py --check`; CI green.
Review-minutes: 20
Unattended: needs-slicing

Why: the human (2026-10-17, Insight chat) wants a numba_cpu base on 8 CPUs in the clean-slate campaign `hst-imaging-mass-samplers`, and chose that it "spawns off" the jax_cpu `source_lp[1]`: that stage is parametric (no inversion) so the two CPU backends fit the same thing, and sharing it makes the numba and jax_cpu chains identical through stage 1 (tighter parity). Decisions: in-job wait for the jax_cpu stage, submit now; rows mark the stage as shared and exclude its wall from the numba chain wall. Today the runner keys every stage path by the config name, so a numba chain would refit stage 1 from scratch.

Shape (autolens_inference only, no library change):
1. `--stages-from <config_name>:<stage>[,<stage>]` on the SLaM runner (`_inference_cli.py`, `scripts/misc/slam/_runner.py`): for the listed stages, the PyAutoFit path_prefix uses `<config_name>` in place of this run's config (same output root, variant, seed), so a completed fit there is loaded, never refitted. Refuse (exit 3, clear message, nothing fitted) when the shared stage is not complete there (no `.completed` marker / result not loadable). Only `source_lp` is allowed in this task (reject other stages). The shared stage's row entry gains `shared_from_config`, keeps the loaded fit's wall and evals for the record, and the row's chain-wall field (and the README parity/wall views) excludes shared stages, with a `chain_wall_excludes` note. The numba leg must still pass `use_jax=False` on every Analysis it builds (unchanged), and the loaded jax_cpu result is used only as a result object (prior passing), exactly as PyAutoFit resume does.
2. Two submits `hpc/batch_cpu/submit_hst_cleanslate_numba_cpu_{dense,sparse}`: `--partition=ral` only, 8 CPUs, 48gb/64gb, `--time=5-00:00:00`, `--array=0-1`, pin env (`PYAUTO_LIB_BASE=/mnt/ral/jnightin/inference/pins/2026.10.17.1`, `PYAUTO_RELEASE_PIN=2026.10.17.1`), `PYAUTO_DISABLE_JAX=1` plus `--backend numba_cpu`, `--lens-light both`, `--output-dir output/cleanslate_2026_10_17`, `--results-tag cleanslate_2026_10_17`, `--export-prepared output/prepared/cleanslate_2026_10_17/hpc_a100_numba_cpu_{dense,sparse}_fp64/seed_$SLURM_ARRAY_TASK_ID`, `--stages-from hpc_a100_jax_cpu_dense_fp64:source_lp`, config names `hpc_a100_numba_cpu_{dense,sparse}_fp64`. Before invoking the runner, an in-job wait loop polls every 5 minutes, capped at 8 h, for the jax_cpu dense seed's completed `source_lp[1]` under `output/cleanslate_2026_10_17/.../slam_base/hpc_a100_jax_cpu_dense_fp64/seed_$SLURM_ARRAY_TASK_ID/` (use the same completion test the runner uses, exposed as `python3 scripts/misc/slam/_runner.py --stage-complete <path>` or a tiny helper); on timeout exit 4 with a message. WALL-BASIS blocks per `scripts/misc/wall/README.md` (`probe-first: yes`, `source: unmeasured`; the September numba rows are superseded and may be cited only as a prior observation, not a rate).
3. Tests in `scripts/misc/test`: flag parsing and rejection of non-source_lp stages; the path substitution; the refusal on an incomplete shared stage; row field and chain-wall exclusion; submits pass check_submits.
4. Docs: `scripts/imaging/slam/README.md` (the shared-stage rule and its provenance), `wiki/setups/rectangular.md`, `AGENTS.md` backend facts (a shared stage is a declared departure, named in the row).
5. On close-out: Cortex run lines for the two arrays (job ids), Insight `tasks/hst_mass_base_light_modes.md` and `campaigns.yaml` gain the numba legs and the shared-stage rule (PR #36 branch).

Out of scope: sharing any pixelized stage; numba sampler waves; changes to the running jax_cpu or A100 jobs.

Witness: on the euclid cell in test mode, a `jax_cpu` chain run with `--stages source_lp` followed by a `numba_cpu` chain with `--stages-from local_jax_cpu_dense_fp64:source_lp` completes all five stages, its row marks `source_lp[1]` as `shared_from_config: local_jax_cpu_dense_fp64` with that stage's wall excluded from the chain wall field, the numba stages report `use_jax: false`, the mass stages under `--lens-light both` export both prepared problems; a `--stages-from` pointing at an incomplete stage exits 3 without fitting; the two new submits pass `check_submits.py --check`; CI green.

Review-minutes: 20
Unattended: needs-slicing
