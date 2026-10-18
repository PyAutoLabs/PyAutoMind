## Summary
Last repo of the RAL category-layout move (PyAutoCortex#67). autolens_profiling#437 (merge 173ab272) repoints every live hard-coded `/mnt/ral/jnightin/autolens_profiling{,_wt,_corpus}` to `/mnt/ral/jnightin/profiling/…`: 84 files, path-only (91 lines changed). SLURM templates use an overridable `AP_ROOT=${AP_ROOT:-/mnt/ral/jnightin/profiling/autolens_profiling}`. `hpc/sync.conf.example` now has `HPC_BASE=/mnt/ral/jnightin/profiling`, and the `LOCAL_PULL_ROOT` default, which pointed at the missing `Science/inference_programme`, now points at `Science/profiling/autolens_profiling`.

Scope note: the prompt estimated ~77 files and a narrow grep found 29. The real count is 84, because a comment containing `…autolens_profiling:` is repeated in ~50 submit scripts; use a loose grep for path moves.

Validation: Witness grep empty outside results/ and archive/; lint.yml steps local PASS; pytest 1457 passed, 6 skipped; CI lint green. Shipped under a human Heart-RED development override (recorded on #67, the PR, active.md and autonomy_log). Merged on a separate human `/prm` command.

Ran in a parallel worktree beside cluster-pointsolver-robust-settings (#436), human-approved; the files are disjoint.

After merge (2026-10-18, this session): RAL `profiling/autolens_profiling` ff 9ad12abd → 173ab272 (326 commits; 16 byte-identical untracked fixed_light_trace results moved to `scratch/ap_aside_20261018/`), then the root links autolens_profiling, autolens_profiling_wt and autolens_profiling_corpus removed; only `euclid_dr1` remains. PyAutoCortex#67 closed.

## Original prompt

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
