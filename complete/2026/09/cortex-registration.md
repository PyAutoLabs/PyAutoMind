- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/382 (closed completed 2026-09-01)
- completed: 2026-09-01
- library-pr: PyAutoCortex https://github.com/PyAutoLabs/PyAutoCortex/pull/3 (`1d36c6e`, merge `5fa9cf0`) →
  PyAutoBrain https://github.com/PyAutoLabs/PyAutoBrain/pull/331 (`4954083`, merge `af73219`) →
  autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/204 (`2aa29cf`, merge `e0c85ee`),
  merged in that order. Plus **no PR at all** for `subhalo_validation`: `9a1bbcc` + `8ba3875` pushed direct to
  `main` on its brand-new **PRIVATE** remote `PyAutoLabs/subhalo_validation` (a Science-folder tree, not a
  workspace repo — the human created the repo by hand, as the epic's no-org-repo-creation rule requires).
- classification: feature (pyautocortex) — epic `cortex-birth`, phase 3 of 7. Gate: phase 1 (SHIPPED #379);
  overlapped phase 2 (SHIPPED #380) as the epic allows. Gates phase 4.
- summary: the phase that gives the Cortex **something to register**. Four trees changed.
  **PyAutoCortex** — `projects.yaml` seeded with eleven rows: the two live projects
  (`inference_programme`, `subhalo_validation` — the latter now on its private remote), `euclid`
  (`remote: none`, by ruling), `euclid_dr1_prelim` (`status: planned`) and seven dormant rows for the remaining
  git-repo Science trees. Two grammar additions carry them: `status: planned` and an optional quoted `note:`;
  the unknown-field rule and PyYAML parity still hold on the live file. Decisions 50–52 written (40 amended-by-51),
  `dashboard.md` + `dashboard.html` re-rendered so the Projects table lists every row.
  **autolens_profiling** — `CORTEX.md` (new) states where the inference programme's rulings of record live
  (PyAutoCortex `projects.yaml` row `inference_programme`), that `results/notes/inference/DECISIONS.md` is
  scientific commentary citing ruling ids (backfill is phase 4), and that the laptop mirror holds data, not
  science; `README.md` gains the pointer; `hpc/sync pull` writes the pull manifest.
  **subhalo_validation** — `.gitignore` gaps closed, the witness JSONs tracked
  (`results/delaunay_adapt_split/pl_eff_0_no_subhalo.json`, `pl_eff_1_outer_no_subhalo.json`, and the
  pre-existing `pl_sersic_0_no_subhalo.json`), `hpc/sync.conf.example` added, `README.md` extended, and the
  same pull manifest written by its own sync CLI.
  **PyAutoBrain** — `cortex collect` now reads the manifest's v1 `checkpoints` table
  (`agents/conductors/cortex/_cortex.py`, `_manifest_run_dir_key`): lookup order `runs[ident]` → `runs[stem]` →
  `checkpoints[<run dir relative to the pull root>]`, `bytes: 0` is FAIL, and a manifest without `schema` still
  reads as the phase-2 shape. The checkpoint leg therefore stops being UNOBSERVABLE wherever a run is in flight —
  the deferral phase 2 wrote down as a first-class UNOBSERVABLE is now closed.
- the pull manifest, v1: `<LOCAL_PULL_ROOT>/.cortex/pull.json`, `schema: 1`, `pulled_at` + `checkpoints`
  **keyed by run directory**; always filled from one `ssh find` over the existing mux; `runs` only where a job
  links to a run dir; `.cortex/` gitignored; dry-run guarded so `status` never writes; a failed gather records
  `gather_error` and never breaks the pull. Written by both projects' own sync CLIs, in their own commits.
- witness (real pulls, not fixtures): `autolens_profiling`'s `hpc/sync pull` wrote **2 checkpoints** from live
  nautilus point-source searches under `output/searches/nautilus/point_source/…`; `hpc/sync status` left the
  manifest untouched. `subhalo_validation`'s wrote **0 checkpoints — correctly**, because no search is in flight
  there. Tests: PyAutoCortex **130 passed** (`cortex.py check` OK, PyYAML parity True, `dashboard --check`
  current under the canonical Brain), PyAutoBrain **744 passed** (tenant firewall OK). CI: `Cortex Check` +
  `Dashboard Refresh` green on PyAutoCortex#3 and again on `main`, `Pages Dashboard` green and
  https://pyautolabs.github.io/PyAutoCortex/ serving HTTP 200 with the seeded Projects table; `Brain Tests`
  green on 3.12 and 3.13 (`Docs` correctly did not fire — the diff touches no `docs/**`); `lint` green on
  autolens_profiling#204 (`profile.yml` is `workflow_dispatch`/`release` only, so `lint` is the whole check
  surface there). Post-merge from the canonical checkouts: `repos_sync.py --check` 15 legs OK,
  `cortex.py check` OK, `_cortex.py dashboard --check` current, `cortex census` lists the 11 projects.
- the `/files` key correction (found by the real pull, not by review): the checkpoint lives at
  `<run dir>/files/search_internal/checkpoint.hdf5` — `AbstractPaths.search_internal_path` is
  `_files_path / "search_internal"` — so the *parent* of `search_internal` is the run directory's `files/`,
  not the run directory. Keyed that way the manifest could never be matched to a run: neither the output path a
  fit logs nor the directory a Cortex member resolves ends in `/files`. The segment is dropped (`8ba3875`), and
  the Brain reader is written against the corrected key.
- the euclid ruling — `remote: none`. The euclid tree tracks a DR1 tile-keyed catalogue CSV
  (`catalogue/inspection/failure_mode_breakdown_consensus75.csv`), already pushes to a **personal** remote
  (`Jammy2211/euclid-dr1-modeling`), **nests the Overleaf paper repo**, and weighs **34 GB**. Any of those alone
  argues against a PyAutoLabs remote; together they settle it. Its code half already lives at
  `PyAutoLabs/euclid_strong_lens_modeling_pipeline`, so nothing is orphaned by the ruling — the Cortex row
  simply records that this project's tree is not org-hosted.
- heart: readiness YELLOW (score 80, 2026-09-01T21:02 snapshot) acknowledged by the human's standing `/prm`
  authorisation for this epic — `! PyAutoArray: open PR 10d old`; `? release validation incomplete: no rehearsal
  for current source`. Both pre-existing and structurally unrelated: no PyAuto library source is touched, and no
  release is involved.
- decisions of note (PyAutoCortex `docs/schema_decisions.md` 50–52):
  - **50** — the `projects.yaml` grammar extension: `status: planned` for a project that does not yet exist on
    disk, and an optional quoted `note:` for the one-line why. The unknown-field rule is unchanged, so the
    grammar grew rather than loosened.
  - **51** — the pull manifest v1 (amends 40): `.cortex/pull.json` keyed by **run directory**, always filled
    from one `ssh find`, `runs` only where a job links to a run dir, `.cortex/` gitignored, dry-run guarded,
    written by the projects' own sync CLIs — the Cortex reads, it never pulls.
  - **52** — the euclid ruling and the dormant-row rules: a Science tree earns a row whether or not it has a
    remote; `remote: none` is a recorded verdict, not a gap.
  - science repos are **not** added to `PyAutoMind/repos.yaml` — the body map is the organism's organs and
    libraries; the Cortex's `projects.yaml` is the science body map. Two maps, one boundary.
- follow-ups found, NOT filed (for the human):
  - `results/rectangular_adapt/*.json` in `subhalo_validation` are **untracked witnesses** (`?? results/rectangular_adapt/`
    is the tree's only dirt). Whether they join the tracked witness set is a scientific call, not a close-out's.
  - `subhalo_simulations` is a **21 GB git repo with zero commits** — neither registered nor initialised; it needs
    a decision before it can earn a row.
  - `subhalo_validation`'s `.gitignore` has a **broken inline comment on the `sources/` line** (git does not strip
    trailing comments, so the pattern is not what it reads as).
  - the **three sync CLIs still differ** (`autolens_profiling/hpc/sync`, `subhalo_validation/hpc/sync`, the euclid
    one) — deliberately deferred by the epic; the manifest is the first thing they now share.
  - `PAT_PYAUTOLABS` **still lacks admin on PyAutoCortex** (a phase-2 follow-up), and now on the new private
    `PyAutoLabs/subhalo_validation` as well, if the settings sweep reddens there.
- epic state: phases **0–3 SHIPPED**. Next is phase 4,
  `draft/feature/pyautocortex/cortex_migration_split_epics.md` — both its gates (2 and 3) are now shipped.

## Original prompt

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
Issued: 2026-09-01

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
