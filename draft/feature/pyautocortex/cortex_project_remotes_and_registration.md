# Cortex phase 3 — private remotes for the Science-folder projects, and the body-map rows

Type: feature
Target: pyautocortex
Repos:
- PyAutoCortex
- autolens_profiling
Themes:
- hpc-gpu
- mind-workflow
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: `projects.yaml` has rows for inference-programme, subhalo_validation, euclid, euclid_dr1_prelim (planned) and every other Science-folder tree as `dormant`; `git -C /mnt/c/Users/Jammy/Science/subhalo_validation ls-files results/` lists the pl_eff witness JSONs; `gh repo view PyAutoLabs/subhalo_validation --json visibility` says PRIVATE
Review-minutes: 15
Unattended: never
Lane: local-dev
Epic: cortex-birth
Phase: 3
Parent: draft/feature/pyautocortex/cortex_birth_epic.md
Filed: 2026-09-01

Phase 3 of 7 in the PyAutoCortex birth epic. **Gate: phase 1** (the
`projects.yaml` schema). May overlap phase 2. Gates phase 4. **Laptop lane
throughout** — the projects live under `/mnt/c/Users/Jammy/Science/` and the
remotes are created by the human.

## Context (ruled 2026-09-01)

Each Science-folder project gets a **private PyAutoLabs remote** holding code,
config, wiki and witness result files only. Outputs, checkpoints and laptop
mirrors stay local and gitignored. **No Euclid data files of any kind** —
consortium-controlled, private repo or not. The `inference_programme` mirror
stays remote-less ("holds data, not science"). PyAutoLabs rather than a
personal account so `repo_settings.yml`'s live org enumeration applies policy
to them; the personal-repo convention applies to papers, not projects.

State of the trees today (audit 2026-09-01): `subhalo_validation` is a local git
repo, no remote, not in any body map; its README says the witness JSONs are
tracked but the pl_eff pair is untracked. `Science/euclid` is the private DR1
source-of-truth tree with no remote. `euclid_dr1_prelim` does not exist yet
(euclid-dr1-prep phase 4 creates it). `inference_programme` is the profiling
mirror (`LOCAL_PULL_ROOT`), local git, no remote by design. Other trees:
`PJ011646`, `aris_PJ011646`, `concr`, `cowls_diana`, `euclid_group`,
`ic50_workspace`, `profiling` (2026-05 sweep harness — name collides with
`autolens_profiling`), `slope_hierarchy`, `subhalo`, `subhalo_simulations`,
`z_dataset`, `z_projects_complete/`, `z_vault`.

## Task

1. **`subhalo_validation`**: write a `.gitignore` that excludes `output/`,
   `hpc/batch_*/output/`, `hpc/batch_*/error/`, `*.zip`, `*.hdf5`, `*.dill`,
   `dataset/` FITS, and keeps `scripts/`, `simulators/`, `config/`, `hpc/`
   (scripts and `sync`, not `sync.conf`), `wiki/`, `results/**/*.json`,
   `results/figures/*.jpg`. Track the untracked pl_eff witness JSONs. Human
   creates `PyAutoLabs/subhalo_validation` private; push `main`. Fix the README
   line that claims the witnesses are tracked so it is true.
2. **`Science/euclid`**: same pattern, with a **data audit first**: list every
   file over 1 MB and every `.fits`/`.h5`/catalogue CSV, and confirm with the
   human which are consortium data before any remote exists. Push only after
   that list is ruled on. If the ruling is "too entangled", record the reason in
   `projects.yaml` (`remote: none — data-entangled, see ruling R-…`) and move on
   — the epic does not block on it.
3. **`autolens_profiling`**: already has a remote. Add a `CORTEX.md` pointer
   (one paragraph: "rulings of record live in PyAutoCortex; DECISIONS.md is
   commentary and cites ruling ids") — the DECISIONS backfill itself is phase 4.
4. **`projects.yaml` rows** in the Cortex, from the audit's where-to-look table:
   - `inference-programme`: repo `autolens_profiling`, RAL
     `/mnt/ral/jnightin/autolens_profiling` (git checkout), mirror
     `/mnt/c/Users/Jammy/Science/inference_programme` (no remote), sync
     `hpc/sync` (pull-only: `pull logs status submit jobs sacct cancel tail du
     check` — no push by design), ledger
     `results/notes/inference/PROGRAMME.md` + `DECISIONS.md`, witness result
     JSON (`results/searches/**/hpc_hpc_a100_fp64_*.json`: stamp + `target_id` +
     provenance triple), partition `gpu` (gpu-1 excluded) + `ral`.
   - `subhalo_validation`: local `/mnt/c/Users/Jammy/Science/subhalo_validation`,
     RAL `/mnt/ral/jnightin/subhalo_validation` (rsync), mirror = project
     itself (`PULL_DIRS=(output results)`), sync `hpc/sync` (push/pull/
     push-submit/wait-and-pull/…) + `hpc/run_chain.sh`, ledger
     `wiki/project/state.md` + journal + `results_summary.md`, witness
     `results/<pipeline>/<lens>_no_subhalo.json` → `evidence_increase` (< 5),
     `subhalo_stage`, `test_mode`, partition `ral`.
   - `euclid`: local `/mnt/c/Users/Jammy/Science/euclid`, pipeline repo
     `euclid_strong_lens_modeling_pipeline`, RAL
     `/mnt/ral/jnightin/euclid_strong_lens_modeling_pipeline`, sync `hpc/sync`
     (`push pull sync status`; submit from the cluster), ledger: none (the
     euclid-dr1-prep epic file until phase 4 migrates it), witness: undefined
     until the science phase pre-registers one.
   - `euclid_dr1_prelim`: `status: planned`, everything else `tbd` — created by
     euclid-dr1-prep phase 4.
   - Every other tree above: `status: dormant`, `local_path` only, one-line
     `note:` (e.g. `profiling`: "2026-05 checkpointed sweep harness, PyAutoNSS
     venv; name collides with autolens_profiling").
5. Add the three private remotes to `PyAutoMind/repos.yaml`? **No.** The Mind's
   body map is the workspace; science projects are the Cortex's body map. Record
   that boundary in `projects.yaml`'s header comment.

## Acceptance

- The witness above; `cortex.py check` passes with the seeded rows; each
  pushed remote's `main` contains no file over the size the human ruled and no
  `.fits`.
- Commits on the project repos' `main` (they are not PR-shaped repos; the
  Cortex PR carries `projects.yaml`).

## Out of scope

- Unifying the three `hpc/sync` CLIs (deferred; epic ledger).
- Moving any tree out of `/mnt/c/Users/Jammy/Science/`.
- Creating `euclid_dr1_prelim` (euclid-dr1-prep phase 4, which will by then be a
  Cortex phase).
