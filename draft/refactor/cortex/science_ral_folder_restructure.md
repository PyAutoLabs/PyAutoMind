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

## Original request (verbatim, 2026-10-14)

> Ok I removed a load of old folders on RAL, so now do the folder updates but I want to sync this with updates in the "Science" Folder which have active, complete (instead of archive?), inference, profiling, scratch. I also want PyAutoCortex to be updated to use this structure and any other organs

> I want to get rid of these weird z_ folders, I guess complete does that for z_projects_Complete, maybe archieve is still warranted as a way to dump unifished projects and we probably need a generic dataset folder like we do now.

Human decisions (same session): euclid_dr1 is NOT moved now (sorted separately later); `euclid` → active; `subhalo` → active and registered in the Cortex; `collaborator/` stays a top-level Science folder; `admin_jammy` to be deleted (held in archive/ — it has uncommitted edits, human to confirm); old-path symlinks kept one month, then a Gut sweep.

## Layout (laptop `/mnt/c/Users/Jammy/Science` ⇄ RAL `/mnt/ral/jnightin`)

- `active/` — euclid, subhalo, subhalo_validation, slope_hierarchy_scale, ic50_workspace
- `complete/` — ex `z_projects_complete` (PJ011646_final, slope_hierarchy, concr_cosmology, …)
- `archive/` — ex `z_vault`, unfinished/abandoned (PJ011646, concr, cowls_diana, euclid_dr1_prelim, subhalo_simulations, inference_programme, profiling, …)
- `inference/` — analytic_gaussian, ep_toy_gaussian; RAL also autolens_inference, autofit_inference, autofit_inference_b5a_dryrun
- `profiling/` — RAL: autolens_profiling, autolens_profiling_{wt,corpus,delaunay}, autofit_profiling, tune_profiling; laptop: profiling pull roots
- `scratch/`, `dataset/` (ex `z_dataset`), `collaborator/` (laptop only)
- RAL `PyAuto/` and (for now) `euclid_dr1/` stay top-level.

Laptop moves DONE 2026-10-14 (old paths are symlinks). RAL moves: script `scratch/ral_reorg_20261014.sh`, human-run.

## Edits

1. PyAutoCortex: `projects.yaml` local_path / ral_root / mirror for every row; register `subhalo` (active); `euclid` status → active and ral_root → `/mnt/ral/jnightin/active/euclid`; schema comment `ral_root` example; current text of `projects/*.md`; re-render dashboard (`--cortex <wt>`).
2. PyAutoMind: `policy/hpc_ral.md` "Projects live under …" → category layout.
3. PyAutoPulse (4 files), PyAutoMemory (1 file): live path mentions only.
4. autolens_profiling, autolens_inference, autofit_profiling, autofit_inference: tracked `activate.sh` and live `hpc/` submit-script PROJECT_PATH defaults / hard-coded `/mnt/ral/jnightin/<repo>` → `/mnt/ral/jnightin/{profiling,inference}/<repo>`.
5. Local untracked `hpc/sync.conf` (all repos + active Science projects): `HPC_BASE` → `/mnt/ral/jnightin/<category>`; autolens_profiling `LOCAL_PULL_ROOT` (points at missing `Science/inference_programme`) → `Science/profiling/autolens_profiling`. Only after the RAL moves ran.
6. PyAutoGut: register the old-path symlinks for a sweep after 2026-11-14 (RAL: `git worktree repair` in `profiling/autolens_profiling` first).

Never rewrite history: results, provenance JSON, Cortex `archive/`, rulings, complete/ records.
