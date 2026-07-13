## autoprompt-cleanup
- issue: https://github.com/PyAutoLabs/PyAutoPrompt/issues/15 (closed automatically via PR's "Closes #15")
- completed: 2026-04-28
- library-pr: https://github.com/PyAutoLabs/PyAutoPrompt/pull/16
- repos: PyAutoPrompt
- notes: Closes the autoprompt/ workflow-infrastructure sweep. Moved 05_sync_slash_command.md, 06_repo_health_audit.md, 08_test_summary.md → `issued/` (matches the 01/02/03 precedent of archiving shipped prompts). Deleted 07_worktree_only_edits.md (matches the 04 precedent — explicitly skipped during the sweep, no point keeping the spec). Rewrote `autoprompt/README.md` as a historical record with an Outcomes table (per-prompt status: Shipped / Shipped re-scoped / Skipped) plus What-shipped / What-deliberately-didn't sections, replacing the stale TODO-list framing that still referenced 04 and listed 07 as "the biggest fix". After this, `autoprompt/` contains only the README — closed chapter. Net: +68 / -166 lines, mostly the 07 deletion (121 lines) and the README rewrite.
