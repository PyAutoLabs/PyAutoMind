# Rework Heart version_skew for floor semantics (stamps are frozen)

Type: feature
Target: PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: normal
Status: fix-implemented-on-branch (claude/wake-up-u53v8z, PyAutoHeart) — pending review/merge

<!-- 2026-07-19: implemented on branch claude/wake-up-u53v8z. version_skew.py now
compares each workspace's version.minimum_library_version floor against the
newest YYYY.M.D.B git tag of its library (local tags, no import/network);
UNSATISFIABLE (floor > newest release) is RED, OK when satisfiable, UNKNOWN
(STALE) when the newest release can't be resolved, BAD on unparseable input. The
general.yaml<->version.txt MISMATCH leg and AHEAD/BEHIND were dropped. readiness.py,
dashboard.py, capabilities.yaml and the test suites updated (289 pass). Build-chain
#155 Phase 4 task 2. NOT DONE here (deeper, separate): yank-awareness of the floor
(needs PyPI API), and removing the legacy workspace_version/version.txt from the 7
workspaces. -->


## Context

Follow-up to PyAutoConf#119 + PyAutoBuild#121 (merged 2026-07-08). Heart's
`heart/checks/version_skew.py` compares each workspace's recorded pin
(`workspace_version`/`version.txt`) against the library `__init__.py` stamp.
Both artifacts are now frozen — releases no longer write either — so the
check is functional but inert (permanently MATCH on stale values).

## Scope

- Re-point the check at live signals: the workspace's
  `version.minimum_library_version` floor (once adopted) vs the newest
  library release tag (`git tag`/GitHub API) — flag when a floor exceeds the
  newest released version (users cannot satisfy it: release-blocking) and
  optionally when floors lag far behind (informational).
- Drop the general.yaml↔version.txt MISMATCH leg once workspaces shed the
  legacy files (feature/workspaces/minimum_library_version_adoption.md).
- Keep the tick cheap (no library imports), per Heart's <30s budget.
- Update `tests/test_version_skew.py` accordingly.
