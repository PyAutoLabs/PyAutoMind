# Mind's PR ledger: schematise `library-pr:`/`workspace-pr:`, render PRs and the pending-release chain

Type: feature
Target: pyautomind
Repos:
- PyAutoMind
- PyAutoBrain
Themes:
- mind-workflow
Difficulty: medium
Autonomy: safe
Priority: high
Status: draft
Consequence: judge
Witness: `REFERENCE.md` "Registry entries → active.md" lists `library-pr:`, `workspace-pr:` and `release-gate:`; `python3 scripts/lifecycle.py check` fails on a fixture row whose `status:` says `awaiting-merge` but carries no `*-pr:` key and passes on the live ledger; the regenerated `dashboard.md` In-flight table has a PR column linking every `*-pr:` and a new "Pending release" section listing merged-but-unreleased library PRs and the active tasks whose `release-gate:` names them; Brain intake tests cover both renders
Review-minutes: 20
Unattended: ready
Epic: mind-post-cortex
Phase: 3
Filed: 2026-09-03
Issued: 2026-09-03

Phase 3 of `mind-post-cortex` — assessment gaps 1 and 2. Two PRs: Mind
(schema + drift check) and Brain (dashboard renderer).

## Gap 1 — the PR ledger is unschematised (S)

`library-pr:` / `workspace-pr:` are written by `ship_library` (`skills/ship_library/ship_library.md` ~L113)
and read by `/prm` (`skills/prm/prm.md` ~L69) but absent from the `active.md`
schema (`REFERENCE.md` ~L525-553); they are documented only for completion
records (~L631). So nothing validates them and the dashboard renders only the
free-text `status:`.

- Add `library-pr:`, `workspace-pr:` (URL, repeatable — a task may have several
  per kind; keep the existing single-line form working) and `release-gate:`
  (see gap 2) to the `active.md` schema in `REFERENCE.md`, with the rule:
  a row whose `status:` contains `awaiting-merge`, `PR open` or `shipped`
  must carry at least one `*-pr:`.
- `scripts/lifecycle.py check`: enforce that rule (warn → error after one
  release cycle if you prefer; state which). Add a test.
- Brain `_intake.py` dashboard: In-flight rows get a **PR** column — one link
  per `*-pr:` labelled by repo (`PyAutoFit#1555`), plus the `pending-release`
  badge when the PR carries that GitHub label *as recorded in the ledger*
  (never a live `gh` call at render time). Extend the dashboard fixture test.
- Ship skills: confirm `ship_library`/`ship_workspace` write the keys in the
  schematised form; fix the wording in `skills/*/reference.md` if it differs.

## Gap 2 — no pending-release → release → unblocked-workspace chain (M)

Two libraries (PyAutoArray, PyAutoLens) have sat `pending-release` since
2026-09-02 (`epics.md` image-source-mappings status) and phase 3 was opened
ahead of the release by hand. The only machine view is the Brain board's live
`gh` search (`board/_board.py` ~L653-664).

Design (prefer the lean existing lever; do not build a fourth surface):

- **Source of truth stays GitHub** (the `pending-release` label on merged
  library PRs) and Hands (the release that clears it). Mind holds only the
  *link and gate*.
- `ship_library` writes `pending-release: <lib>@<pr-url>` into the task's
  `active.md` row when it opens a pending-release PR; `ship_workspace` writes
  `release-gate: <lib>` on a workspace task blocked behind an unreleased
  library. `/prm` close-out carries `pending-release:` into the completion
  record; the release path (`pre_build`/Hands post-publish or `/prm` on the
  release) clears it — specify exactly which step and edit that skill.
- Dashboard: a **Pending release** section under In flight, grouped by
  library: merged-but-unreleased PRs (from `active.md` rows and
  `complete/` records whose `pending-release:` is not yet cleared) and, under
  each, the active tasks whose `release-gate:` names it. Empty section is
  omitted.
- `lifecycle.py check`: a `complete/` record with an uncleared
  `pending-release:` older than N days is a warning, not an error.

Keep the Brain board's live query as the fresh view; the dashboard section is
the ledger view and must say so in one line.
