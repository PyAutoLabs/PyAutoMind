# Rework Heart version_skew for floor semantics (stamps are frozen)

Type: feature
Target: PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

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
