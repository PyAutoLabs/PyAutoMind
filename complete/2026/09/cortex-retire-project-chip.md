The Nothing-open table under Summary (from
`complete/2026/09/cortex-checkin-stamp-prominent.md`) listed the projects with
nothing open but offered no way to act on one. The human wanted a copy chip on
each dormant row whose payload goes into the laptop chat to retire that
project. There was no retire door: `projects.yaml` `status` was a closed
`active | dormant | planned` vocabulary with a parser and no writer, and the
Brain conductor knew three states. The chip needed a door behind it.

## What shipped

**PyAutoCortex #16** (merged 3e797e5) — `scripts/cortex.py`:

- `status: retired` joins `PROJECT_STATUSES`; `check` accepts it.
- `python3 scripts/cortex.py retire <project> --why "<one line>"`: refuses an
  unknown or already-retired key, refuses while any phase of the project is in
  a live state (`submitted running pulled awaiting-ruling ready gated` — i.e.
  anything outside `RULED_STATES ∪ {planned}`; planned phases are unasked
  questions and may stay), and refuses up front if `projects.yaml` already has
  drift. Otherwise it line-edits exactly the row's `status:` and `note:`
  (`"retired <today>: <why>"`, rewritten or appended), re-parses and requires no
  problems, restoring the original bytes on failure. Rulings and the row itself
  are never deleted: the row is the only record of where a project's data lives.
- `REFERENCE.md` vocabulary + "Retiring a project" paragraph, `AGENTS.md`,
  `projects.yaml` header comment. 122 tests (5 new), incl. a byte-identity check
  outside the two edited lines and a CLI round-trip.
- `dashboard.md` / `dashboard.html` regenerated.

**PyAutoBrain #359** (merged 1f425f0) — `agents/conductors/cortex/_cortex.py`:

- `STATUS_RANK["retired"] = 3`; ordering active → planned → dormant → retired.
- `_retire_payload(key)`: the `/cortex` paste — confirm nothing live, run the
  retire command with `--why`, `check`, `pyauto-brain cortex dashboard --apply`,
  push the ledger.
- Nothing-open table gains a Retire column: HTML `📋 retire` copy button
  (`class="copy text"` — the theme's worded-chip face; the document-level
  click handler already binds every `button.copy`) on `dormant` rows, empty
  cell otherwise; markdown `retire ↓` cell plus one 📋 task row per dormant
  project under the table (a `<details>` inside a table cell does not render on
  GitHub). Retired projects leave the table for one folded "N retired" line
  carrying each note. `census --by-project` prints a separate Retired line.
- `skills/cortex/cortex.md`: `retire` in the verb appendix and a rule bullet
  (retiring never deletes a row or a ruling).
- 85 conductor tests, 914 full suite, run with `PYAUTO_CORTEX=<worktree>`.

Live board after merge: seven retire chips (`concr cowls_diana ic50_workspace
pj011646 profiling slope_hierarchy subhalo_simulations`), none on the planned
`euclid_dr1_prelim`, no retired fold yet.

## Merge order

Brain first; the Cortex PR's `refresh` check renders against Brain `main` and
was red until #359 landed — re-run green, then merged.

## Deviations from the plan

Chip class `copy text` rather than bare `copy` (a bare `button.copy` is a
fixed square that a worded label spills out of). `retire` pre-checks for
existing drift so the post-edit `problems == []` assertion cannot blame the
edit for a file that was already broken. `parse_projects` is PyYAML now, not a
hand parser; the writer is still a pure line edit.

## Original prompt

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
