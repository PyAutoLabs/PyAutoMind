- issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/24 (closed completed 2026-09-08)
- completed: 2026-09-08
- library-pr: PyAutoCortex https://github.com/PyAutoLabs/PyAutoCortex/pull/25 (`5f65fa0` birth/retire/gate,
  `3e3e520` remote → `PyAutoLabs/slope_hierarchy_scale`, `bff7124` board re-render; merge `866d8f0`).
  Plus **no PR at all** for the science tree itself: `acce42a` (birth, 135 files) + `9ebdf0e`
  (`visibility_stage: github_private`) pushed direct to `main` on the brand-new **PRIVATE** remote
  `PyAutoLabs/slope_hierarchy_scale` — the human created the repo by hand, as the no-org-repo-creation
  rule requires.
- classification: research (graphical_ep) — epic `graphical-ep`, campaign phase 3. Consequence `judge`,
  supervised, difficulty small. PyAutoCortex is an **organ** repo (`category: organ` in `repos.yaml`),
  so the Heart release-freeze gate does not apply to this merge and was not consulted.
- summary: the phase that gives the EP campaign a Cortex science project to run in. Three trees changed.
  **Science vault** — `Science/slope_hierarchy` (17 commits, its `Jammy2211/slope_hierarchy` remote left
  intact) moved whole to `Science/z_projects_complete/slope_hierarchy`; it is the vault the new project
  mines and cites, not a deleted tree.
  **`Science/slope_hierarchy_scale`** — born fresh per `autolens_assistant/skills/start-new-project.md`
  Phase 1 (thin refer-back scaffold: `README.md`, `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json` API
  gate, `project.yaml` with `assistant_ref`, `CITATION.cff`, `wiki/project/`, `results/`, `paper/`,
  `.gitignore`), borrowing `scripts/{ep,graphical,one_by_one,util}.py`, `simulators/sample.py`, `config/`,
  `activate.sh`, `environment.yml` and `hpc/` from the vault, with `hpc/sync.conf` written for
  `PROJECT_NAME=slope_hierarchy_scale`, `HPC_HOST=euclid_jump`, `HPC_BASE=/mnt/ral/jnightin`. No `output/`,
  no `dataset/` (N=25 is re-simulated), no old `results/`; `wiki/project/state.md` cites the vault's
  `results/ep_history_n5_maxsteps12/` as the N=5 baseline.
  **PyAutoCortex** — new active row `slope_hierarchy_scale` (`assistant: autolens_assistant`,
  `remote: PyAutoLabs/slope_hierarchy_scale`, `sync_cli: hpc/sync` with verbs verified,
  `ledger: wiki/project/state.md`, `witness_file: results/**/*.json`, `partition: both`, dated `note:`);
  row `slope_hierarchy` retired via `cortex.py retire … --why` with `local_path` repointed at the vault;
  task `tasks/slope_hierarchy/n25_scale_up.md` `git mv`-ed to `tasks/slope_hierarchy_scale/`, re-pointed
  at the new project, `Gates: PyAutoFit#1405, #1558, #1560, #1562` written from the shipped gate evidence,
  and moved `planned` → `gated`; board re-rendered.
- checks: PyAutoCortex **126 tests pass**, `cortex.py check` OK. CI on the merged head `bff7124`:
  `Cortex Check` (`check`) and `Dashboard Refresh` (`refresh`) both `success`, `mergeStateStatus: CLEAN`,
  `mergeable: MERGEABLE`. Merge proven from the canonical checkout
  (`git merge-base --is-ancestor bff7124 origin/main`, `rev-list --count origin/main..bff7124` = 0).
- the remote ruling — `remote: PyAutoLabs/slope_hierarchy_scale`, **private**. The prompt's scope said
  `remote: none` and "hand the human the `gh repo create` line"; the human created the private org repo
  during the run instead, so the row ships with a real remote and `visibility_stage: github_private`.
  That is the first EP-campaign science tree hosted under the org rather than a personal account.
- the activation route — `projects.yaml` is code (Cortex#22 ruling), so moving these rows could not be done
  by a `/cortex` check-in: a check-in sweeps only `status: active` rows (and projects owning a
  `submitted|running` task), and both EP rows were `status: dormant`, which is why the campaign ledger's
  "move to `gated` at the next check-in" instruction had sat unexecutable since 2026-09-02. It ships as a
  PR with a human merge instead.
- decisions / residue:
  - `tasks/slope_hierarchy/methods_writeup.md` stays **planned under the retired row** — deliberate
    (the prompt's scope says so); it is a write-up of the completed N=5 work, not of the scale-up.
  - `simulators/sample.py`'s `info.json` keeps `domain: slope_hierarchy` — deliberate, so the N=25 run
    stays directly comparable with the vault's N=3/N=5 baseline.
  - `config/general.yaml` `workspace_version` bumped to `2026.8.17.1`.
  - Out of scope and still the human's: **submitting** the N=25 run (a `/cortex` ask, ruled 2026-09-05 —
    the task is `gated`, and `ready` is the human's edge), activating `ic50_workspace` (phase 4; its
    checkout is dirty with 170 files of line-ending churn and has no `results/` witness path), and the
    moment-matching cure decision.
  - Mind ledger for this phase landed ahead of the merge in `2b348f41`:
    `draft/research/graphical_ep/ep_campaign.md` phase-3 and phase-4 rows, and `epics.md`'s three stale
    `PyAutoCortex epics.md#<slug>` pointers replaced (Cortex#14 replaced `epics.md` with `checkin.yaml`).

## Original prompt

# Birth `slope_hierarchy_scale` — the EP campaign's first Cortex science project (phase 3)

Type: research
Target: graphical_ep
Repos:
- PyAutoCortex
- PyAutoMind
Themes:
- graphical-ep
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 10
Unattended: fits
Epic: graphical-ep
Filed: 2026-09-08
Issued: 2026-09-08

## Original request (verbatim)

> Can we set up the first project as part of the EP epic which should be managed via a cortex
> science project, and what is it? Continue the 'Expectation propagation (EP) campaign' epic. Its
> canonical state lives in draft/research/graphical_ep/ep_campaign.md — read that ledger (and any
> DECISIONS/RESULTS files beside it) first. Cross-check this epic's entry in PyAutoMind/epics.md, any
> related rows in PyAutoMind/active.md, and the referenced repos' open issues and PRs, to work out the
> last completed phase and what is currently in flight. Then pick the next logical step and continue
> it through the normal workflow (/start_dev — filing the phase's prompt first if none exists),
> updating the ledger as the work advances. Note: umbrella phase map — each phase's real content
> lives in its own prompt under draft/research/graphical_ep/; the campaign file itself is never
> issued. Science half: PyAutoCortex epics.md#graphical-ep (campaign phases 3 and 4).

## Answer to the question

The first Cortex science project of the `graphical-ep` epic is **`slope_hierarchy`**, whose phase-1
task `tasks/slope_hierarchy/n25_scale_up.md` *is* campaign phase 3 (graphical non-EP JAX scaling,
"NUTS headline, EP cautionary"). It is chosen over phase 4 (`ic50_workspace/ep_scale_up.md`)
because the checkout is clean and in sync with its remote, the N=3/N=5 results the scale-up extends
are committed under `results/` (so the row's `witness_file` glob resolves), the project issue
`Jammy2211/slope_hierarchy#1` the witness comment needs already exists, the RAL root
`/mnt/ral/jnightin/slope_hierarchy` exists with `output/` and `results/` (verified 2026-09-08 over
`euclid_jump`), and it depends on neither the moment-matching cure nor the unissued
`draft/feature/autofit/ep_lbfgs_jax.md` companion. The ic50 checkout is dirty (170 files of
line-ending churn), has no `results/` at its declared witness path, and sits outside the workspace.

## Why the phase has not started

Survey 2026-09-08: phases 1 and 2 are SHIPPED (last movement 2026-09-08, PyAutoFit#1580); nothing
EP-shaped is in `active.md`, and no open PRs on PyAutoFit, autofit_workspace_test or PyAutoCortex.
Phases 3 and 4 migrated to the Cortex on 2026-09-01 and have sat at `State: planned` with an empty
`Gates:` ever since, although their "Ready when phase 2 is issued" condition has held since
2026-09-02. The ledger says "move to `gated` at the next `/cortex` check-in", but a check-in only
sweeps `status: active` rows (and projects owning a `submitted|running` task) — both EP rows are
`status: dormant`, so the instruction is unexecutable as written. `projects.yaml` is code (Cortex#22
ruling), so the activation is a PR to PyAutoLabs/PyAutoCortex with a human merge.

## Ruling (human, 2026-09-08)

The phase runs as a **fresh project `slope_hierarchy_scale`** in `/mnt/c/Users/Jammy/Science/`,
not in the old `slope_hierarchy` tree: the old tree (17 commits, `Jammy2211/slope_hierarchy`,
wrapped up 2026-07-22 after answering its four N=5 goals) moves to `Science/z_projects_complete/`
and is mined for code. Assistant of record is `autolens_assistant` (the old `project.yaml`'s
`assistant_ref`; the science is lens modelling).

## Scope

1. **Science tree** (the Cortex `local_path` exception to the workspace-paths rule) — with the old
   checkout clean and in sync, `mv Science/slope_hierarchy Science/z_projects_complete/slope_hierarchy`
   (whole git repo, remote untouched). Birth `Science/slope_hierarchy_scale` per
   `autolens_assistant/skills/start-new-project.md` Phase 1 (thin, refer-back scaffold:
   `README.md`, `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json` API gate, `project.yaml` with
   `assistant_ref` at the current assistant commit, `CITATION.cff`, `wiki/project/`, `results/`,
   `paper/`, `.gitignore`). Borrow from the vault: `scripts/{ep,graphical,one_by_one,util}.py`,
   `simulators/sample.py`, `config/`, `activate.sh`, `environment.yml`, `hpc/` (sync CLI, conf
   examples, batch dirs, template). Write `hpc/sync.conf` (`PROJECT_NAME=slope_hierarchy_scale`,
   `HPC_HOST=euclid_jump`, `HPC_BASE=/mnt/ral/jnightin`). Do **not** copy `output/`, `dataset/`
   (re-simulate at N=25), old `results/` or the old journal — `wiki/project/state.md` cites the
   vault's `results/ep_history_n5_maxsteps12/` as the N=5 baseline. `git init` + one birth commit.
   Remote stays `none` (org repo creation is human-only; hand the human the `gh repo create` line).
2. **PyAutoCortex `projects.yaml`** — new row `slope_hierarchy_scale` (`remote: none`,
   `local_path`/`ral_root` as above, `sync_cli: hpc/sync`, verified `sync_verbs`, `ledger:
   wiki/project/state.md`, `assistant: autolens_assistant`, `witness_file: results/**/*.json`,
   `partition: both`, `status: active`, dated `note:`). Old row: `cortex.py retire slope_hierarchy
   --why …` (both its tasks are `planned`) plus `local_path` hand-edited to the vault path.
3. **Task** — `git mv tasks/slope_hierarchy/n25_scale_up.md tasks/slope_hierarchy_scale/`,
   `Project: slope_hierarchy_scale`, `Gates: PyAutoFit#1405, PyAutoFit#1558, PyAutoFit#1560,
   PyAutoFit#1562`, "Ready when" line replaced by the gate evidence
   (`PyAutoMind/complete/2026/09/ep-scale-collapse-basin-cure-or-caveat.md`, bundle
   #1572/#1573/#1574/#1576, #1580) and a "Borrowed from" note; `cortex.py move … gated`.
   `ready` is the human's edge. `methods_writeup.md` stays planned under the retired row.
4. **Cortex hygiene in the same PR** — `cortex.py check`, tests, `pyauto-brain cortex dashboard
   --apply` from the canonical Brain; PR to PyAutoLabs/PyAutoCortex (projects.yaml is code →
   human merge).
5. **PyAutoMind ledger** — `ep_campaign.md` phase-3 row (gated, birth, PR ref, human submits via
   `/cortex`), phase-4 row (companion path `draft/feature/autofit/ep_lbfgs_jax.md`; ic50 stays
   dormant until its checkout is cleaned and a `results/` witness path exists); `epics.md`: replace
   the three stale "PyAutoCortex epics.md#<slug>" pointers (Cortex#14 replaced `epics.md` with
   `checkin.yaml`) with the task-file pointer.

Out of scope: submitting the N=25 run (human `/cortex` ask, ruled 2026-09-05), activating
`ic50_workspace`, the moment-matching cure decision, creating the GitHub remote.

## Acceptance

- `Science/slope_hierarchy_scale` exists with one birth commit; the old tree sits under `z_projects_complete/` intact.
- `slope_hierarchy_scale` renders on the Cortex board as an active project with `n25_scale_up` gated; `slope_hierarchy` reads retired.
- `cortex.py check` OK; Cortex CI (`Cortex Check`, `Dashboard Refresh`) green on the PR.
- The next `/cortex` check-in lists `n25_scale_up` under `gates` with resolvable refs.
- `ep_campaign.md` and `epics.md` no longer point at a non-existent `PyAutoCortex/epics.md`.
