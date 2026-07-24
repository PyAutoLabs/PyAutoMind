## lifecycle-record-auto-index

issue: none (shipped directly as PR #97)
completed: 2026-07-24
pr: PyAutoMind#97

Recurring `[PyAutoLabs/PyAutoMind] Run failed: Lifecycle Drift - main` emails were
the `lifecycle_drift.yml` workflow failing its `index --check` on every direct
push to main touching `complete/**`. Root cause: `lifecycle.py record --apply`
wrote + staged the completion record but left `complete/index.md` stale; the
separate `index --apply` step (documented in ship_library/ship_workspace) was easy
to forget, so the index drifted on nearly every ship.

Fix: folded the index regeneration (`_render_index`/`_existing_curated` +
`git add complete/index.md`) into `cmd_record`'s `--apply` branch so record and
index can no longer drift apart. Behaviour-preserving except `record --apply` now
also freshens the index. This very record was written with the merged code —
the index below was regenerated automatically, dogfooding the fix.

Traps: a concurrent session was shipping into the same PyAutoMind checkout
during the work (main advanced underfoot; a `git add -A` swept the untracked
draft into the other session's local commit). Recovery: rebuilt on a fresh
branch off origin/main, committed only explicit paths, and did main-side index
work in detached throwaway worktrees.
