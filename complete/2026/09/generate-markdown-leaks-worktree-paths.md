Shipped as PyAutoHands#281 (issue PyAutoHands#280), merged 2026-09-14.

`generate_markdown.py` scrubbed the local machine layout out of executed pages by
mapping `workspace_path.parent` to `...`, encoding "sibling checkouts live next
to the workspace". True in a canonical checkout, false in a task worktree — where
the workspace sits under `<root>-wt/<task>/` while imported libraries still
resolve into the canonical tree. Those paths matched no redaction but the home
one, so pages published one contributor's directory layout, and the same warning
rendered differently depending on where the build ran. Since development routes
through task worktrees, **the leaking path was the default and the clean one was
the exception.**

`_sibling_checkout_roots()` now derives the roots from where the checkouts
actually are — `workspace_path.parent`, the canonical root via git's
`--git-common-dir` (self-describing: it assumes no worktree layout), and
`PYAUTO_MAIN` when set — and redacts all of them. Roots at or above `$HOME` are
dropped; pairs are sorted longest-first so prefix ordering is enforced rather
than incidental.

`check_no_local_paths()` refuses to publish a page still containing an absolute
home path, before the page is staged. It also covers a gap redaction never
touched: only stream outputs were ever scrubbed, not error tracebacks or
`execute_result` payloads.

12 new tests build a real canonical checkout and a real `git worktree` and assert
identical published output from both; reverting the old function fails 4 of them.

**CI caught a real convention violation on the first push**: the tenant firewall
(organ code) check flagged real repo names in the new docstring and test
fixtures. Fixed by making both instance-neutral rather than by widening
`FIREWALL_ALLOWLIST` — an allowlist entry would have recorded them as legitimate
instance facts and re-permitted exactly the drift the check exists to catch.

Left out as cross-repo docs/content calls: the `PYTHONPATH=…` form documented in
~5 workspace `AGENTS.md` files replaces rather than appends (and is redundant),
and PyAutoNerves handshake warnings appear inconsistently across published pages.

Found while rendering pages under `howto-stale-self-location`; see
`complete/2026/09/howto-stale-self-location.md`.
