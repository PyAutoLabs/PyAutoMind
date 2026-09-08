## cortex-assistant-entry
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/362
- completed: 2026-09-07
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/367
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/23

Cortex projects now route through their domain assistant at execution time, in
one direction only: the project names the assistant, the assistant never learns
about the Cortex.

- **Cortex schema** (PyAutoCortex#23, merge `02318d7d`, head `133620ed`): every
  `projects.yaml` row carries a new **required** `assistant:` field — `none` or
  a bare workspace-relative repo name. `cortex.py check` validates it and stats
  nothing, so the CI render needs no assistant checkout. `subhalo_validation`
  and `euclid_dr1_prelim` declare `autolens_assistant`; every dormant and
  retired row (including the retired `inference_programme`) declares `none`.
  126 tests pass.
- **Brain briefs** (PyAutoBrain#367, merge `29dc4796`, head `33136c3`): every
  work-shaped `/cortex` payload (next task, rerun, planned) now carries a
  **work brief** — the entry protocol for the execution-tier subagent: read the
  assistant's `AGENTS.md`, then the project's `wiki/project/` state and journal,
  then the named skills; finish by writing the journal entry and rewriting
  `state.md`; return the outcome against the witness plus any assistant drift.
  New `_work_brief(r, projects)` / `_with_brief(payload, r, projects)`;
  `_planned_payload` gains the `projects` map. Check-in, ruling, gate and retire
  payloads are unchanged and name no assistant. A row without the field renders
  as `none`, so the Brain half merges cleanly against a pre-field Cortex `main`.
  91 conductor tests, 920 tests overall.
- **Contract docs**: `/cortex` gains step 4 "Work on a project" and the rule
  "the door names the assistant, never reads it"; `WORKFLOW.md` gains the
  "Cortex project work" subsection under the subagent prompt contract.
- **Backfill (local science commits, outside the workspace, unpushed here)**:
  `Science/subhalo_validation` `8df4bf0` (profile.md filled from what the
  workspace records about the human) and `Science/euclid_dr1_prelim` `f486cee`
  (assistant refer-back block in `AGENTS.md`; its origin is the Euclid pipeline
  repo, so it is committed locally and never pushed there).

Traps and notes:

- **Merge order is load-bearing.** The Cortex `refresh` check renders through
  Brain `main`, so it stays red until the Brain PR merges; merge Brain first,
  then re-run the Cortex check.
- **The conductor names the assistant and never reads it** — no stat, no
  resolve, still stdlib-only. That is what keeps `grep -ril cortex
  autolens_assistant` empty and lets users run an assistant without ever
  touching the Cortex.
- **Migration for any external `projects.yaml`**: add `assistant: none` (or the
  assistant's repo name) to every row, placed after `ledger:` — `check` reports
  it missing otherwise.

## Original prompt

# Cortex projects route through the domain assistant at execution time

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoCortex
Themes:
- mind-workflow
- assistants
Difficulty: medium
Autonomy: human-required
Priority: high
Status: formalised
Consequence: judge
Witness: `projects.yaml` rows carry an `assistant:` field (workspace-relative assistant repo path or `none`) that `cortex.py check` validates and that the retired `inference_programme` row leaves as `none`; every work-shaped `/cortex` payload (ruling-follow-up, rerun, next-task, planned, gate) prints a subagent brief that starts `cd <local_path> && source activate.sh`, then reads the assistant's `AGENTS.md`, the project's `wiki/project/state.md`, its newest dated journal entry and the named skills, and ends by writing a journal entry, rewriting `state.md` and returning assistant-drift findings; the check-in door and the ruling prompt are unchanged and name no assistant; `skills/cortex/cortex.md` and `skills/WORKFLOW.md` carry a "work on a project" subagent contract; `grep -ril cortex autolens_assistant` still returns nothing; `Science/euclid_dr1_prelim/AGENTS.md` carries the assistant refer-back block and `Science/subhalo_validation/wiki/project/profile.md` has no `_unrecorded_` field left; Brain + Cortex tests cover the field, the check rule and the brief text
Review-minutes: 25
Unattended: never
Filed: 2026-09-07
Issued: 2026-09-07

Human direction (2026-09-07, verbatim):

"""
PyAutoCortex has become my science project manager, but I have noted that it
means I do not necessary interface with or use autolens_assistant (or another
assistant). When I checked, it wasnt clear the existing project suse
autolens_assistant. However, I want to be sure that Cortex projects always
route through the asssistant, as this should help AI work and also ensure the
assistant is functioning as best and possible and is being used. Do an
assessment of how Cortex, and assistants, should interface. Currently, I find
myself using Cortex as a single chat to manage all projects, rather than
individual chats per project. I therefor think given this is the use I find
myself oging towards we should continue to build arond that work flow, but that
probably means the project-to-assistant interface needs to be a bit more
dynamic, maybe only using the assistant when sub agents spawn for work on a
particular project maybe? I guess its also worth assesing for sure that going
via assistants makes sense with Cortex.
"""

After the assessment:

"""
Sounds good, assistants should not "know" about Cortex ideally as users may use
them without ever using Cortex, other than tht I agree with the plan but note
that inference has been retired so dont worry bout setting this up for that.
"""

## Assessment of record (2026-09-07)

- The Cortex schema has no assistant field; the Brain cortex conductor and the
  `/cortex` skill contain no "assistant" hit; all five assistants contain no
  "cortex" hit. The only link is implicit: `ledger: wiki/project/state.md` is
  the file the assistant's `start-new-project` scaffolds.
- Only `subhalo_validation` is assistant-born (`project.yaml` `assistant_ref`,
  refer-back `AGENTS.md`); `euclid_dr1_prelim` is a clone of the Euclid pipeline
  repo with no refer-back. Even the assistant-born project shows non-use: its
  `profile.md` is the unfilled template, `state.md` was last rewritten
  2026-09-02 while runs launched 2026-09-07, its journals name the assistant
  only as drift, and the assistant benchmark harness has never recorded a run.
- The check-in door is mechanical (pull, score, move, render, push, print
  prompts) and reasons about no science. Its payloads are pastes for a fresh
  chat with no stated working directory.

Ruling: the assistant is the **entry protocol of the execution subagents** the
single Cortex chat spawns per project, never part of the check-in door or the
ruling. The pointer is one-way, project → assistant; assistants stay
Cortex-unaware so users who never use the Cortex are unaffected.

## Scope

1. **Cortex schema.** `assistant:` row field in `projects.yaml` (workspace-
   relative path such as `autolens_assistant`, or `none`), parsed like `note:`
   is today, validated by `check` (known key, `none` or an existing directory
   holding an `AGENTS.md`), documented in `REFERENCE.md` and the file's header
   comment. Rows: `subhalo_validation` and `euclid_dr1_prelim` →
   `autolens_assistant`; every dormant/retired row → `none`.
2. **Brain briefs.** Work-shaped payloads in `agents/conductors/cortex/_cortex.py`
   become subagent briefs carrying the entry protocol when the row's
   `assistant` is not `none`; the paste form survives for the board. Mechanical
   payloads (check-in, ruling, submit, retire) do not change.
3. **Contract.** A "Work on a project" section in `skills/cortex/cortex.md` and
   a sibling subsection under "Model delegation" in `skills/WORKFLOW.md`: the
   architect delegates project work one rung down with the brief; the subagent
   ends by writing the journal entry and rewriting `state.md`, and returns the
   outcome plus assistant-drift findings, which the architect files via
   `/intake` as assistant work.
4. **Backfill (outside the workspace, local commits).** Refer-back block in
   `Science/euclid_dr1_prelim/AGENTS.md` (its origin is the pipeline repo:
   commit locally, never push there); fill
   `Science/subhalo_validation/wiki/project/profile.md` from what this
   workspace already records about the human (push to the project's remote).

Out of scope: `inference_programme` (retired 2026-09-07); any edit to an
assistant repo; the check-in door; ruling prompts.
