# Multi-dataset shared-state — Phase 4: docs

Phase 4 of 4 of `feature/autolens/multi_shared_state_examples.md`. **Blocked on
Phase 3.** Small, deliberately last.

## Scope

- Docs are **minimal not maximal** (`feedback_docs_minimal_not_maximal`): the
  multi feature docs page / README gets the flag + one-line note pointing at
  the Phase 3 example sections; no ported runnable blocks.
- API reference (`docs/api/*.rst`) entries for `PreloadsImaging` +
  `AnalysisImaging.shared_preloads` where the existing structure has homes for
  them (check against the interferometer siblings added by PR#344/#566).
- `autolens_workspace/scripts/multi/README.md` + `features/README.md` rows for
  the new sections.
- Sweep: notebook regeneration is PyAutoBuild's job at release; just keep
  scripts py-percent clean.
