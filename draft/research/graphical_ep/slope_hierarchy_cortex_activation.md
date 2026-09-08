# Activate `slope_hierarchy` as the EP campaign's first Cortex science project (phase 3 gate)

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

## Scope

1. **PyAutoCortex `projects.yaml`, row `slope_hierarchy`** — `status: dormant` → `active`;
   `assistant: none` → `autofit_assistant`; `sync_verbs: [pull]` → the verbs the checkout's
   `hpc/sync` actually exposes and the Cortex needs (`push`, `pull`, `sync`, `status`, `submit`,
   `push-submit`, `jobs`, `tail`, `check` — verify against `hpc/sync help` and REFERENCE.md's
   bare-word rule); `note:` rewritten to keep the personal-remote fact and drop the stale
   "ral_root planned, sync_verbs unverified" (both verified 2026-09-08). `ral_root`, `local_path`,
   `ledger: README.md`, `witness_file`, `partition: both` stay.
2. **`tasks/slope_hierarchy/n25_scale_up.md`** — fill `Gates:` with the phase-2 evidence
   (`PyAutoFit#1405`, the phase-2 record's umbrella issue, deliberately left open for the cure
   decision; plus the cure PRs `PyAutoFit#1558`, `#1560`, `#1562`), rewrite the "Ready when" line to
   cite `PyAutoMind/complete/2026/09/ep-scale-collapse-basin-cure-or-caveat.md` and the 2026-09-07
   review bundle (`#1572/#1573/#1574/#1576`, `#1580`), then `python3 scripts/cortex.py move
   slope_hierarchy/n25_scale_up gated`. `ready` is the human's edge (`move … ready` after reading
   `gates`), not this task's.
3. **Cortex hygiene in the same PR** — `python3 scripts/cortex.py check`, PyYAML parity, tests, and
   `pyauto-brain cortex dashboard --apply` so the board shows `slope_hierarchy` as active with a
   gated next-task chip and its work brief.
4. **PyAutoMind ledger** — `ep_campaign.md` phase-3 row: gated, activation PR ref, "submission is a
   human `/cortex` ask"; phase-4 row: fix the companion path to `draft/feature/autofit/ep_lbfgs_jax.md`
   and note ic50 stays dormant until its checkout is cleaned and a `results/` witness path exists;
   `epics.md`: replace the three stale "PyAutoCortex epics.md#<slug>" pointers (Cortex#14 replaced
   `epics.md` with `checkin.yaml`; the epic is carried by `Epic:` on task files) with the task-file
   pointer.

Out of scope: submitting the N=25 run (the human asks via `/cortex`, ruled 2026-09-05),
activating `ic50_workspace`, the moment-matching cure decision, `methods_writeup` (stays planned).

## Acceptance

- `slope_hierarchy` renders on the Cortex board as an active project with `n25_scale_up` gated.
- `cortex.py check` OK; Cortex CI (`Cortex Check`, `Dashboard Refresh`) green on the PR.
- The next `/cortex` check-in lists `n25_scale_up` under `gates` with resolvable refs.
- `ep_campaign.md` and `epics.md` no longer point at a non-existent `PyAutoCortex/epics.md`.
