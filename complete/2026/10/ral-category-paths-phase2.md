Phase 2 of the RAL category-layout path repoint (PyAutoCortex#67).

- autofit_inference#15: SLURM template uses overridable `AP_ROOT=${AP_ROOT:-/mnt/ral/jnightin/inference/autofit_inference}`; 11 wave-2 submit scripts, the `plan_wave2.py` `RAL_ROOT` generator constant, hpc/README.md, AGENTS.md, activate.sh usage, wiki state and `hpc/sync.conf.example` (`HPC_BASE=/mnt/ral/jnightin/inference`). `_wave2.py` is an exporter producer path, so `dashboard/summary.json` was regenerated after lint caught `test_committed_summary_is_current`.
- PyAutoCortex#69: every row's `ral_root` mirrors its laptop `local_path` category; `subhalo` registered active with a ledger (decision 61: the non-git exception to 52(a)); `euclid` stays dormant, superseded by euclid_dr1 (euclid_dr1_prelim defunct) per the human; schema comment example `/mnt/ral/jnightin/<category>/<project>`.
- PyAutoMemory: no change needed (remaining mentions are historical); claim released.
- Heart RED development override carried from phase 1 (recorded on PyAutoCortex#67).

Remainder (autolens_profiling, blocked on autolens_profiling#418) re-filed as `draft/refactor/cortex/ral_category_paths_autolens_profiling.md`; PyAutoCortex#67 stays open for it.

## Original prompt

# RAL category paths — phase 2: repoint the claimed repos, then drop the last RAL links

Type: refactor
Target: cortex
Repos:
- autolens_profiling
- autofit_inference
- PyAutoCortex
- PyAutoMemory
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/67
Filed: 2026-10-15
Issued: 2026-10-15
Blocked-by: autolens_profiling claimed by hst-mge-pilot-qualification (autolens_profiling#418 awaiting merge); autofit_inference + PyAutoCortex released by search-ext-b5b2-remainder 2026-10-15 (wave 2 closed)
Witness: `git grep` over the edited repos' live config finds no `/mnt/ral/jnightin/{autolens_profiling,autolens_profiling_wt,autolens_profiling_corpus,autofit_inference,autofit_inference_b5a_dryrun}` path (results/, provenance JSON, captured logs, archive/ exempt); `cortex.py check` OK; every active Cortex row's `ral_root` exists on RAL.
Review-minutes: 10

Remainder of `complete/2026/10/ral-category-paths.md` (phase 1 shipped 2026-10-15: autolens_inference#22, autofit_profiling#6, PyAutoMind#504, euclid scripts). Same design: overridable root variable in SLURM templates (`AP_ROOT=${AP_ROOT:-/mnt/ral/jnightin/<category>/<repo>}`), mechanical old→new rewrite of submit scripts, AGENTS.md and `hpc/sync.conf.example` `HPC_BASE` included; never rewrite history.

1. autolens_profiling (~77 files; + _wt, _corpus): → `/mnt/ral/jnightin/profiling/autolens_profiling…`; also `hpc/sync` line 62 `LOCAL_PULL_ROOT` default (missing `Science/inference_programme`) → `/mnt/c/Users/Jammy/Science/profiling/autolens_profiling`.
2. autofit_inference (~15 files; + b5a_dryrun) → `/mnt/ral/jnightin/inference/autofit_inference…`.
3. PyAutoCortex `projects.yaml`: `ral_root` for every remaining row into the category layout; register `subhalo` (active, `Science/active/subhalo`, `/mnt/ral/jnightin/active/subhalo`); `euclid` status → active, `ral_root` → `/mnt/ral/jnightin/active/euclid` (currently the deleted euclid_strong_lens_modeling_pipeline folder); schema comment example; re-render with `--cortex <wt>`.
4. PyAutoMemory: the one live path mention.
5. After merge (human-run): `git pull` on RAL in each repo, then remove the remaining links autolens_profiling, autolens_profiling_wt, autolens_profiling_corpus, autofit_inference, autofit_inference_b5a_dryrun.
