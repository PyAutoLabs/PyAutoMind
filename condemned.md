# Condemned material

The catalog of **condemned self-material** — stale branches, `git stash`
entries, dead code and retired tests that a hygiene / `repo_cleanup` sweep is
95%-but-not-100% sure is trash. Symmetric to `parked.md`: `parked.md` holds work
that is *paused and will resume*; this file holds material that is *spent and
awaiting elimination*, recoverable right up until it is voided.

This is the **index**; the payload is durable **git refs**, not markdown. Fragile
forms (local unmerged branches, stashes) are first materialised as real commits
and pushed under the archive namespace `refs/archive/condemned/<name>` (which
stays out of `git branch -a`) into **PyAutoGut** as the attic remote — *before*
the local copy is deleted. Recovery is a checkout. The organ (PyAutoGut) holds
and voids; the Brain hygiene conductor drives (decides what to condemn, triggers
a sweep), mirroring the Heart ↔ vitals template. See the decision:
`research/pyautobrain/pyautogut_organ_decision.md`.

## Lifecycle

1. **Condemn** — the hygiene `tidy` pass files an entry here (async, no
   synchronous per-item gate). Fragile forms are archived to a durable ref
   first; merged branches and committed deletions need only a SHA recorded.
2. **Transit** — the entry sits with a `sweep-after` date. Until then it is
   recoverable (reabsorption): restore the branch/stash from its archive ref.
3. **Void** — a batch `sweep` runs the existing `repo_cleanup` safety gates
   against entries past `sweep-after` and eliminates them; the entry moves out
   of this file (to a voided log or is deleted).

## Entry schema

One `##` block per item. Fields:

- `type` — `branch` | `stash` | `file` | `test`
- `locator` — the local name/path (e.g. `feature/old-thing`,
  `stash@{2}`, `src/legacy/foo.py`)
- `confidence` — how sure it is trash (e.g. `0.95`)
- `reason` — why it is condemned
- `merged` — `yes` | `no` (a merged branch is reachable from `main` forever →
  skips the pen; near-zero risk)
- `condemned` — date filed (YYYY-MM-DD)
- `sweep-after` — earliest date it may be voided (the transit clock)
- `breaks-if-wrong` — what is lost if this was a false positive (informs the
  gate)
- `archive-ref` — the durable ref + SHA to recover from
  (`refs/archive/condemned/<name>` @ `<sha>`), or `n/a` for a merged branch /
  committed deletion whose bytes live in remote history (record the pre-delete
  SHA instead)

### Recoverability is not uniform

- **Merged branches** — reachable from `main` forever; `archive-ref: n/a`, a note
  is enough. The conductor recommends these straight to deletion without staging.
- **Committed code / test deletions** — the old bytes live in remote history;
  record only the pre-delete SHA.
- **Local-only unmerged branches / stashes** — exist in one machine's reflog and
  are gc-pruned. These **must** be materialised as an archive ref before deletion;
  a manifest that merely *points* at a stash is worthless the moment it is dropped.

<!-- Example entry (schema illustration only — not a live condemnation):

## feature/abandoned-spike
- type: branch
- locator: feature/abandoned-spike
- confidence: 0.95
- reason: superseded by feature/real-approach; no unique commits worth keeping
- merged: no
- condemned: 2026-07-12
- sweep-after: 2026-08-12
- breaks-if-wrong: loses ~3 exploratory commits (delaunay prototype)
- archive-ref: refs/archive/condemned/abandoned-spike @ 0de4514
-->

<!-- No live condemned entries yet — the hygiene `tidy` drive seam
     (feature/pyautobrain/hygiene_pyautogut_drive_seam.md) populates this file
     once PyAutoGut exists as the attic remote. -->
