# RAL category paths — last repo: autolens_profiling, then drop the last RAL links

Type: refactor
Target: cortex
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/67
Filed: 2026-10-15
Blocked-by: none — the autolens_profiling claim by hst-mge-pilot-qualification cleared (autolens_profiling#418 merged 2026-10-17; record complete/2026/10/hst-mge-pilot-qualification.md)
Witness: `git grep` over autolens_profiling live config finds no `/mnt/ral/jnightin/{autolens_profiling,autolens_profiling_wt,autolens_profiling_corpus}` path (results/, provenance JSON, captured logs, archive/ exempt); any committed generated summary/check in the repo still passes (`--check` tools, lint tests).
Review-minutes: 10

Remainder of `complete/2026/10/ral-category-paths.md` and `complete/2026/10/ral-category-paths-phase2.md`. Same design as autolens_inference#22 / autofit_inference#15: overridable root variable in SLURM templates (`AP_ROOT=${AP_ROOT:-/mnt/ral/jnightin/profiling/autolens_profiling}`), mechanical old→new rewrite of the ~77 live files (activate.sh usage, hpc/README.md, submit scripts, AGENTS.md, `hpc/sync.conf.example` `HPC_BASE=/mnt/ral/jnightin/profiling`), never rewrite history. Also the `hpc/sync` line-62 `LOCAL_PULL_ROOT` default (missing `Science/inference_programme`) → `/mnt/c/Users/Jammy/Science/profiling/autolens_profiling`. Watch for producer-path / generated-summary freshness checks (autofit_inference#15 needed `dashboard/summary.json` regenerated). Submit scripts pointing at the deleted `/mnt/ral/jnightin/PyAuto_wt/…` and `p2d_check` dirs are history of finished runs — leave them.

After merge (human-run): `git pull` in RAL `profiling/autolens_profiling`, then remove the last links autolens_profiling, autolens_profiling_wt, autolens_profiling_corpus.
