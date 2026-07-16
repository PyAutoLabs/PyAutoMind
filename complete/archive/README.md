# complete/archive/ — retired non-record material

This holds material that isn't a **dated task record** (those live in
`complete/<YYYY>/<MM>/` and are the completion ledger). `lifecycle.py`
`check` and `index` deliberately **skip** this directory.

- **`epics/`** — retired multi-task **epic trackers** (formerly `z_features/`).
  Each tracked a series of related tasks; the per-task completion records live
  in `complete/<YYYY>/<MM>/`. Kept for the epic-level narrative.
- **`shelved/`** — **deferred / shelved** prompts and dev notes (formerly
  `z_vault/`). Not shipped; parked here rather than lost. Pull one back into
  `draft/<work-type>/<target>/` if you decide to action it.

The `z_features/` and `z_vault/` top-level folders were retired here (2026-07-13)
once the `draft/ → active/ → complete/` lifecycle (issue #71) made them
redundant.
