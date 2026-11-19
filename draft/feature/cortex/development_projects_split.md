# Cortex: split development projects from paper-bound science projects on the register and board

Type: feature
Target: PyAutoCortex
Repos:
- PyAutoCortex
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: medium
Lane: any
Witness: `pyauto-brain cortex census --json` carries a `category` for every project, equal to the category folder in its `local_path`; the generated `dashboard.md` has a "Science" section and a "Development" section, each listing exactly the projects of that category, with per-section Running / Open / Projects counts beside the unchanged overall counts table; `python3 scripts/cortex.py check` is OK; the new tests in both repos pass.

## Why

The Cortex treats every project the same. A paper-bound science project (for example
`euclid_detailed`, `sdssj0946_subhalo`) and an exploratory development project (for example
`dm_sightlines`, `stars_dm_slope`, `ep_gnfw_slope`) have identical rows, identical ledgers and
sit in one undivided list on the board and in `Science/STATE.md`.

The human wants the two kinds told apart at a glance. Development projects exist to develop or
validate the software; their outcome is library issues and PRs filed in PyAutoMind, not a paper.
They are exploratory, they are not Mind epics, and most of their day-to-day state lives in the
project's own `wiki/project/`. Reading the board today, nothing says which projects are which.

## What exists today (checked 2026-11-19)

- `development/` is already an official Science category: schema decision 62 in
  `@PyAutoCortex/docs/schema_decisions.md` (2026-10-29). The laptop tree is
  `<Science root>/<category>/<project>` with categories `active`, `development`, `complete`,
  `archive`, and RAL mirrors it under `/mnt/ral/jnightin/<category>/`.
- In `@PyAutoCortex/projects.yaml` the category appears only inside `local_path` and `ral_root`.
  There is no category or kind field. `status` is `active | dormant | planned | retired` for
  every project.
- The `drift` verb of the Brain's cortex conductor
  (`@PyAutoBrain/agents/conductors/cortex/_cortex.py`) already parses the category out of the
  paths and checks it against the tree.
- The board (`dashboard.md`, `dashboard.html`, `state.json`), the `census` verb, the `checkin`
  summary and the `Science/STATE.md` mirror are rendered by that conductor and do not group or
  label by category. `REFERENCE.md` "The board" describes one counts table (Running, Open,
  Projects), one Summary table and one card per project.
- Development-category rows today: `analytic_gaussian`, `ep_toy_gaussian`, `ic50_workspace`,
  `slope_hierarchy_scale`, `dm_sightlines`, `stars_dm_slope`, `ep_gnfw_slope`.

## Ask

1. Derive each project's category from the category folder in its `local_path` string, in one
   place, and expose it wherever the conductor reports a project: `census` (text and `--json`),
   the `checkin` summary, the board and the `STATE.md` mirror.
2. Render the board and `STATE.md` in two sections, Science (categories `active`, and
   `complete` / `archive` for retired rows as now) and Development. Within each, keep the
   present layout. Add per-section Running / Open / Projects counts.
3. Let `pull` and `checkin` take an optional `--category` filter.
4. Record the change as a new dated entry in `docs/schema_decisions.md` and update
   `REFERENCE.md` (the `projects.yaml` fields table and "The board").
5. Tests in both repos for the derivation, the grouping and the filter.

## Constraints

- Derive, do not add a field, unless the ruling below says otherwise. A second copy of the
  category in `projects.yaml` would be one more thing to drift.
- The derivation must read the `local_path` string only, never the filesystem: `census()` has to
  stay machine-independent because the board is rendered in CI (decision 62).
- Keep the overall counts table and its three row names exactly as they are; the Brain board and
  the organ-cockpit feed (`board/_state.py`, `state.json` v1) read them.
- `projects.yaml` is code: any edit to it goes to the human as a PR. Ledgers change only through
  `scripts/cortex.py` verbs. The ledger grammar (Now / Runs / Log) does not change.
- Do not move any project, change any status or touch any Science folder.

## Ruling needed before building

Is the folder category enough to say "development", or does the human want an explicit intent
that is independent of the folder (for example `intent: paper | development | exploratory`), so
that an exploratory project could live in `active/` or a development project could be marked
paper-bound later? The default in this prompt is: folder category only, two sections.

## Out of scope

A separate ledger format, workflow or orchestrator for development projects; tracking
development tasks in the Cortex (it is not a task tracker); anything in PyAutoMind beyond this
prompt.
