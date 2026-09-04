# Cortex board: a 📋 retire chip beside every dormant project

Type: feature
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoCortex
Themes:
- dashboard
- cortex
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Review-minutes: 20
Unattended: no
Filed: 2026-09-04

## Original request (verbatim, 2026-09-04)

> Next to dormant projects can you put a copy thing which I would put into
> claude to retire it

Follow-up to `complete/2026/09/cortex-checkin-stamp-prominent.md` (the
Nothing-open table under Summary) and `cortex-dashboard-projects-first`.

## Scope

There is no retire door today: `projects.yaml` `status` is a closed
`active | dormant | planned` vocabulary (`PyAutoCortex/scripts/cortex.py`
`PROJECT_STATUSES`, `REFERENCE.md`), the file is hand-written in a
restricted format with a parser but no writer, and the Brain conductor's
`STATUS_RANK` / `by_project_keys` know three states.

- **PyAutoCortex:** a fourth status `retired` and a `cortex.py retire
  <project> --why "<one line>"` command that refuses while any phase of the
  project is open, flips the row's `status:` line in place (line edit, format
  preserved) and stamps the reason into `note:`; `check` accepts the new
  value; REFERENCE.md / AGENTS.md vocabulary updated; tests.
- **PyAutoBrain conductor:** `STATUS_RANK` gains `retired`; retired rows leave
  the Nothing-open table for a folded one-line "N retired" `<details>` at its
  foot; the Nothing-open table gains a 📋 column whose chip, on every
  `dormant` row, carries the paste for the laptop chat — the retire door as
  one sentence naming the project and the command, like the check-in chip.
  `/cortex` skill appendix documents the verb. Tests; pages regenerated.
