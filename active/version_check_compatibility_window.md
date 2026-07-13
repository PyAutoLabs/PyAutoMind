# Version check: compatibility floor + staleness warning instead of exact match (R2)

Type: feature
Target: autoconf
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

## Original request (verbatim)

> ok, I support all this input — R1–R4 endorsed on PyAutoBuild#118. [After
> morning-status-release-rehearsal shipped:] ok, those PRs are done so we can
> do this work now --auto

## Context

R2 of the version-pinning design review (PyAutoLabs/PyAutoBuild#118, report
comment of 2026-07-08). Today `autoconf.workspace.check_version()` raises
`WorkspaceVersionMismatchError` on **exact** inequality between the installed
library version and the workspace-recorded version. Exact equality is
maximally brittle under the (reinstated) daily release cadence, forces the
release pipeline to commit to every workspace daily, and currently advises
users to pin-install yanked versions.

## Scope

- Replace exact-match semantics in `PyAutoConf/autoconf/workspace.py` with a
  **compatibility floor**: workspace records
  `version.minimum_library_version`; raise only when
  `installed < minimum` (scripts genuinely need newer API).
- Legacy keys (`version.workspace_version`, `version.txt`) are reinterpreted
  as floors — old clones with a newer installed library pass instead of
  hard-failing.
- **Staleness warning** (never raise): when the installed library's date
  version is much newer (>30 days) than the recorded floor, warn to
  `git pull` the workspace.
- Advice text must never recommend `pip install pkg==<version>` exact pins
  (the recorded version may be yanked/unpublished); recommend plain upgrade
  + workspace pull, and the existing bypasses.
- Keep both bypasses (`workspace_version_check: False`,
  `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1`) and cwd-based workspace discovery.
- Update `test_autoconf` coverage for the new semantics.
- Workspace-side `general.yaml` key adoption + release-pipeline write changes
  are follow-ups (workspace task + R3), not this task.
