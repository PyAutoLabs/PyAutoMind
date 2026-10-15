# Science + RAL folder restructure — point live path config at the new category layout

Type: refactor
Target: cortex
Repos:
- PyAutoCortex
- PyAutoMind
- PyAutoPulse
- PyAutoMemory
- autolens_profiling
- autolens_inference
- autofit_profiling
- autofit_inference
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: `cortex.py check` passes on the edited projects.yaml; every active row's `local_path` and `ral_root` exist (laptop `test -d`, RAL `ssh test -d` once the RAL moves ran); `grep -rn` over the edited repos' live config (projects.yaml, policy/hpc_ral.md, activate.sh, hpc/ submit defaults) finds no top-level `/mnt/ral/jnightin/<project>` or `Science/<project>` path for a moved project; history (results/, provenance, archive/, complete/, rulings, Cortex archive/) untouched.
Review-minutes: 10
Issued: 2026-10-15

## Original request (verbatim, 2026-10-14)

> Ok I removed a load of old folders on RAL, so now do the folder updates but I want to sync this with updates in the "Science" Folder which have active, complete (instead of archive?), inference, profiling, scratch. I also want PyAutoCortex to be updated to use this structure and any other organs

> I want to get rid of these weird z_ folders, I guess complete does that for z_projects_Complete, maybe archieve is still warranted as a way to dump unifished projects and we probably need a generic dataset folder like we do now.

Human decisions (same session): euclid_dr1 is NOT moved now (sorted separately later); `euclid` → active; `subhalo` → active and registered in the Cortex; `collaborator/` stays a top-level Science folder; `admin_jammy` to be deleted (held in archive/ — it has uncommitted edits, human to confirm); old-path symlinks kept one month, then a Gut sweep.

## Layout (laptop `/mnt/c/Users/Jammy/Science` ⇄ RAL `/mnt/ral/jnightin`) — DONE 2026-10-15

- `active/` — analytic_gaussian, ep_toy_gaussian, euclid, ic50_workspace, slope_hierarchy_scale, subhalo, subhalo_validation
- `inference/` — RAL: autolens_inference, autofit_inference, autofit_inference_b5a_dryrun (laptop: pull roots only)
- `profiling/` — RAL: autolens_profiling (+_wt, _corpus, _delaunay), autofit_profiling, tune_profiling (laptop: pull roots only)
- `archive/`, `complete/`, `scratch/`, `dataset/`, `collaborator/` (laptop only)
- RAL `PyAuto/` and (for now) `euclid_dr1/` stay top-level.

## Status (2026-10-15)

- Laptop: moved; old-path symlinks REMOVED (PyCharm clutter); Cortex `local_path`/`mirror` repointed (PyAutoCortex#64, #66 merged). `~/.bashrc` ProjectEuclid/ProjectSubhalo repointed.
- RAL: moved via `scratch/ral_reorg_20261015.sh` (human-run) + toys to active/; worktrees repaired; 11 unused old-path links removed. 8 links REMAIN because tracked files hard-code the old paths: autolens_profiling, autolens_profiling_wt, autolens_profiling_corpus, autolens_inference, autofit_inference, autofit_inference_b5a_dryrun, autofit_profiling, euclid.
- Local untracked `hpc/sync.conf` HPC_BASE repointed for all 9 projects/repos and witnessed with `hpc/sync logs`.
- Human decisions 2026-10-15: keep profiling/ and inference/ split (mirrors Pulse/Insight); RAL links are temporary — removed as soon as their repo edits merge (no Gut month sweep); `admin_jammy` untouched; Heart RED development override granted for this task.

## Design

Do not swap one hard-coded path for another: `activate.sh` derives its own root from `BASH_SOURCE`; SLURM templates keep one overridable root variable at the top (`AP_ROOT=${AP_ROOT:-/mnt/ral/jnightin/profiling/autolens_profiling}`) because sbatch spools the script; historical per-experiment submit scripts get a mechanical old→new rewrite. results/, provenance JSON, Cortex archive/, rulings, complete/ records are never rewritten.

## Phase 1 — now (repos free)

1. autolens_inference: activate.sh, hpc/README.md, hpc/batch_{cpu,gpu}/template + submit scripts (14 files) → `/mnt/ral/jnightin/inference/autolens_inference`.
2. autofit_profiling: activate.sh, hpc/README.md, hpc/batch_cpu/template (3 files) → `/mnt/ral/jnightin/profiling/autofit_profiling`.
3. PyAutoMind `policy/hpc_ral.md` "Projects live under …" → category layout; PyAutoPulse live path mentions (4 files).
4. euclid (personal repo Jammy2211/euclid-dr1-modeling, laptop `Science/active/euclid`): 26 submit scripts `PROJECT_PATH=/mnt/ral/jnightin/euclid/…` → `/mnt/ral/jnightin/active/euclid/…`; commit ONLY those files (the repo has unrelated staged renames catalogue_swg/ → catalogue/); no GitHub push unless the human asks; `hpc/sync push --no-data`.
5. After merge: human runs `git pull` on RAL for each repo, then removes the autolens_inference, autofit_profiling and euclid links.

## Phase 2 — blocked (claims)

6. autolens_profiling (+_wt, _corpus; ~77 files incl. hpc/sync line 62 LOCAL_PULL_ROOT default → `Science/profiling/autolens_profiling`) — after autolens_profiling#418 (hst-mge-pilot-qualification) merges.
7. autofit_inference (+ b5a_dryrun; 15 files) and PyAutoCortex `ral_root` for every remaining row + register `subhalo` (active) + `euclid` → active at `active/euclid` + schema comment — after search-ext-b5b2-remainder releases them (its wave-2 jobs run on RAL now).
8. PyAutoMemory live path mention (1 file) — with phase 2.
9. Remove the remaining RAL links (human-run).
