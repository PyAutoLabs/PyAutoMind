# lifecycle record auto-index

Difficulty: trivial
Autonomy: safe
Priority: medium

## Request (verbatim)

Make PyAutoMind `scripts/lifecycle.py` `cmd_record` automatically regenerate and
`git add` `complete/index.md` when `--apply` is passed, so the index can never
drift stale after a ship.

## Root cause

`record --apply` writes the completion record and stages it, but leaves
`complete/index.md` stale. The separate `index --apply` step is documented in the
ship skills (`ship_library`/`ship_workspace`) but gets forgotten. The **Lifecycle
Drift** workflow (`.github/workflows/lifecycle_drift.yml`) runs `index --check` on
every direct push to `main` that touches `complete/**`; a forgotten regen fails
the run and emails the maintainer on every ship.

## Fix

In `cmd_record`, under the `--apply` branch (after the record is written and the
prompt folded), regenerate the index via the existing `_render_index` /
`_existing_curated` helpers, write `complete/index.md`, and `git add` it — the
same effect as `index --apply`, folded into `record` so the two steps can't drift
apart. Behaviour-preserving except `record --apply` now also freshens the index.

@PyAutoMind
