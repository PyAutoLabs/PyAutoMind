## dashboard-dirty-listing
- issue: https://github.com/PyAutoLabs/PyAutoPrompt/issues/4
- completed: 2026-04-27
- library-pr: https://github.com/PyAutoLabs/PyAutoPrompt/pull/5
- repos: PyAutoPrompt
- notes: Follow-up to pyauto-status-shell. Split the dashboard's single `DIRTY` column into `MOD` (tracked-modified) + `UNTR` (untracked) so accumulating noise is distinguishable from real edits-in-progress, and append a `Dirty files:` listing after the main table showing the actual `git status --porcelain` lines per repo (only repos with content; `??` and ` M` prefixes preserved). Cached porcelain output via a bash associative array so the listing reuses the same data the counts came from — no new git invocations. Day-1 use already surfaced real signal: pyc pollution committed in `euclid_strong_lens_modeling_pipeline`, untracked `scripts/imaging/images/` in `autogalaxy_workspace_test` (worth feeding into prompt 02's gitignore patterns), and 14 dirty entries in `autolens_assistant` worth a closer look. Sweep time unchanged at ~3s.
