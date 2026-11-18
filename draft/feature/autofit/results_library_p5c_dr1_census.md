# Results library 5c — read-only census of the DR1 v5 500-lens sample on RAL (the epic's witness)

Type: feature
Target: autofit
Repos:
- PyAutoCortex
Themes:
- results
- euclid
- hpc
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: on the 500-lens sample (`complete/euclid_dr1/inspect/dr1_catalogue_v5_sample500/sample500.csv`), `census/` lists every expected (object, search) with a state class and every gap with a reason; every one of the catalogue's 62 exclusions (`inspect/dr1_catalogue_v5/excluded_tiles.csv`) is reproduced with a reason and zero gaps are unexplained; `af.export.verify` passes on the 500-lens sample package; the Cortex `euclid_dr1` ledger carries one `library` line whose index hash equals `autofit.export.index_hash` of the pulled `index/`
Review-minutes: 30
Unattended: ready
Lane: ral
Epic: results-library
Phase: 5c
Filed: 2026-11-16
Progress: 2026-11-16 — prep done (path repointed, bundle rebuilt from 2026.11.12.1, import check ok); human submitted RAL job 415560. Remaining: shape steps 3–4 after the job ends.

Gate (human, not an issue ref): the census job is a cluster submit. The 2026-11-02
ledger line says it "awaits a human submit: `cd /mnt/ral/jnightin/scratch/results_library_census_20261102 && sbatch census.sbatch` (or a grant)".
An agent never runs raw `sbatch` (Brain `bin/scheduler_action_guard.py`), and a
`ral` task never submits on its own (REFERENCE.md `Lane:`).

## Context

Phases 0–4 (PyAutoFit), 5a (autolens_assistant) and 5b (PyAutoCortex `library`
verb, decision 65) are merged. Released stack 2026.11.12.1 carries phases 0–4.
Ledger: `draft/feature/autofit/results_library_epic.md` (Phase 5 witness, ruling
F8, CENSUS RULING 2026-11-02, the 5c staging line). 5d (pipeline shrink) is
NOT in scope: it waits on DR1 v1.0 and on
`draft/feature/euclid/upstream_dr1_final_catalogue_tooling.md`.

Staged on 2026-11-02, never submitted: `census.py` + `census.sbatch` (copy in
`Workspace/Science/scratch/results_library_p5c_census/`, live copy and
`census_bundle.tgz` in `/mnt/ral/jnightin/scratch/results_library_census_20261102/`).
Narrowed scope chosen by the human: vis_lp / vis_pix / SED-vis only (~1,700
results), `--partition=ral`, 2 CPU, node-local disk (NFS login-node runs indexed
~2 results/min). Read-only: no modelling compute, never the shared mirror's
`main` pulled (`HPCPullPyAuto` forbidden here), never `gpu`.

## Known drift since staging (fix before submit)

- `euclid_dr1` moved to `/mnt/ral/jnightin/complete/euclid_dr1` on 2026-11-13
  (`policy/hpc_ral.md`); `census.py` hardcodes `.../active/euclid_dr1`. Repoint.
- The bundle is a `git archive` of PyAutoFit `963ff296a` + PyAutoNerves
  `68cbac3` (pre-release mains). Human ruling 2026-11-16: rebuild it from the
  2026.11.12.1 tags and record that in the census README.

## Shape

1. Attended prep (laptop, RAL login node read-only): repoint the path, refresh
   or keep the bundle, `python3 -c` import check of `autofit.results` /
   `autofit.export` inside the bundle on the login node (no indexing there).
2. **Human submits** (or grants a one-off scheduler action through the euclid
   project's `hpc/sync submit`). Record the job id as a Cortex `## Runs` line.
3. After the job ends: pull `census/` + `index/` to
   `Workspace/Science/scratch/results_library_p5c_census/`, write a short
   README (counts per state class, gaps vs the 62 exclusions, verify result).
4. `cortex.py library euclid_dr1 <index_dir>` → `claude/**` ledger push
   (auto-lands via `ledger_merge.yml`); epic ledger line in Mind. If any repo
   code change proves necessary, stop at PR-open.

Done = witness above. Any unexplained gap is a finding for the human, not a fix
in this task.

## Answers from the human
- Q9 (2026-11-18, ruling unattended, shift ready-2026-11-18): (a) make it ready: slice or size it so a shift can start it
- Q10 (2026-11-18, ruling human-required, shift ready-2026-11-18): (a) lower it to supervised
