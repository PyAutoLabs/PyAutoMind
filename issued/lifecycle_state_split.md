# Split the PyAutoMind prompt-file lifecycle into draft / active / complete

Type: feature
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoBrain
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

## Problem

`issued/` is a flat, append-only pile of 444 prompt files — every prompt ever
`start_dev`'d, whether long-merged or still in flight — so it is unusable for
tracking state. The root cause is that the Mind runs **two parallel lifecycles
that have drifted apart**:

| | draft (not started) | in-flight | done |
|---|---|---|---|
| **Prompt files** | `<work-type>/<target>/<name>.md` | `issued/<name>.md` | *(never moves — stuck in `issued/`)* |
| **Ledger entries** | — | `active.md` | `complete.md` |

`create_issue` moves the file `<work-type>/ → issued/` and adds a row to
`active.md`. On merge, `ship_*` moves the ledger **entry** `active.md →
complete.md` but **leaves the file in `issued/` forever**. The file lifecycle
stops at "issued" and never advances to "done".

## Goal — make the file lifecycle track the three ledger states

Introduce a clean top-level state split, moving the prompt file in lockstep
with its ledger entry:

```
PyAutoMind/
  draft/            <- was the bare bug/ feature/ refactor/ ... dirs
    bug/ feature/ refactor/ research/ docs/ maintenance/ test/
      <target>/<name>.md
  active/           <- was issued/  (in-flight only; flat)
    <name>.md
  complete/         <- new; finished work, bucketed by completion date
    2026/
      07/
        <slug>.md   <- one rich record per finished task
    index.md        <- generated (Phase 2 grows this into a wiki)
```

- **`draft/` wrapper** (user decision 2026-07-13): move the work-type dirs under
  a single `draft/` so state is legible at the Mind root. Keep the
  `<work-type>/<target>/` taxonomy *inside* `draft/` — census/dashboard rely on
  it.
- **`active/`**: rename of `issued/`, flat, holds only in-flight prompts.
- **`complete/YYYY/MM/`**: zero-padded months so lexical order == numerical
  order. Bucket by the `completed:` date of the ledger entry.

## Key decision — complete.md is split into per-file records

(User decision 2026-07-13.) The real knowledge about a finished task lives in
the **rich `complete.md` entry** (summary, traps, PRs, worktree notes), not the
thin original prompt. So `complete/YYYY/MM/<slug>.md` holds that rich record
(and the original prompt appended under a `## Original prompt` heading). The
6000-line `complete.md` is **split into these per-file records and retired** (or
regenerated as a thin roll-up index). This is what makes the Phase-2 wiki worth
building — see the follow-up `complete_archive_wiki.md`.

## Blast radius — everything wired to `issued/` / `complete.md`

Update every reference (grep-verify none are missed):

**PyAutoBrain skills**
- `create_issue/SKILL.md` — the `mv <path> issued/` step → `active/`; the
  "timestamp-suffix if exists in issued/" guard → `active/`.
- `ship_library/{ship_library,reference}.md` — on merge, *also move the file*
  `active/<name>.md → complete/<year>/<month>/<slug>.md` and write the rich
  record, in the same beat it moves the ledger entry `active.md → complete.md`.
- `ship_workspace/{ship_workspace,reference}.md` — same completion move.
- `start_dev/reference.md` — the "exists at `issued/<basename>` → issued" lookup
  → `active/`; the `grep complete.md for ^## <candidate>$` shipped-check →
  scan `complete/**` (or the generated index).
- `intake/intake.md` — the `reconcile` cross-ref against `complete.md` and
  `issued/`, and "retire to `issued/` by hand" → new paths.
- `WORKFLOW.md`, `OWNERSHIP.md` — schema/pointer text mentioning
  `active.md`/`complete.md`/`issued/`.

**PyAutoMind scripts**
- `spawn.py` — glob `("issued/*", "DROP")` → `("active/*", "DROP")` +
  `("complete/**", ...)`; `("complete.md", "EMPTY")` handling as complete.md is
  split/retired.
- `status.sh` — `LIFECYCLE_DIRS` (`issued` → `active`, add `complete`);
  `complete_count` now counts `complete/**/*.md` not `complete.md` H2s.
- `prompt_sync.sh` — the `grep -v '^issued/'` exclusion → `active/`.

**One new helper — `scripts/lifecycle.py` (+ `--check`)**
Mirrors `repos_sync.py --check`. `--check` catches drift so this never rots
again: a file in `active/` whose ledger entry already reached `complete.md`; a
`complete/` file with no ledger entry; a draft with an open issue; mis-bucketed
dates. Wire `--check` into `/health` and/or CI.

## One-time migration of the 444 `issued/` files

Scripted pass with a reviewable manifest (filenames map only *fuzzily* to
`complete.md` slugs — e.g. `03_gamma_from_mode_wrong_formula.md` vs
`autofit-navigator-catalogue-staleness`), so do NOT trust names:
1. For each `issued/` file, decide its state by cross-referencing `active.md`
   (→ `active/`) and `complete.md` (→ `complete/YYYY/MM/`, dated by that
   entry's `completed:`).
2. Files matching neither ledger (orphaned/abandoned) → `complete/unknown/` for
   human triage, never silently dropped.
3. Emit the manifest, human-review, then execute the moves + complete.md split
   in one commit series. Use `git mv` to preserve history.

## Constraints / traps

- **Template parity:** `spawn.py` stamps the PyAutoMind-template; the new dir
  layout + retired `complete.md` must round-trip through `spawn --check`
  (`spawn_drift` CI) — regenerate + republish the template as part of the PR.
- **`active.md` `  - Repo` lines are claims** (`feedback_active_md_dash_repos`) —
  don't let the migration script misread them.
- **Do not bulk-issue** the Phase-2 wiki with this — file both, issue Phase 2
  only as this nears shipping (`feedback_no_bulk_issue_queues`).
- Ship library-side (skills/scripts) coherently; this is Mind-internal so there
  is no downstream workspace API impact, but there IS a `/start_dev` +
  `create_issue` behaviour change — smoke the create_issue → ship round-trip on
  a throwaway prompt before merge.

## Original request (verbatim)

> pyautomind/issued is huge and hard ot track, can we: (i) put all things not in
> issued in a folder called active, to make state split; (ii) make a complete
> folder which is for complete and separate from issued which are on going; (iii)
> put a folder for not yet active, e.g. drafts or thigns which are intaken but
> not start_dev; (iv) For complete, put them in folders by year and month in a
> way that appears numerically in order.
