# Version model: fix the exact-pin consumers + orphaned README pins (Phase 4 tasks 3-4)

Type: feature
Target: PyAutoBuild
Repos:
- autolens_assistant
- PyAutoBuild
- autofit_workspace
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Build-chain campaign (PyAutoBuild#155) Phase 4, tasks 3-4. Fork (b) decided
(mains authoritative). Task 1 (floors, 2026.7.9.1, done) and task 2
(version_skew rework, draft/feature/pyautoheart/version_skew_floor_rework.md)
precede these.

- **Task 3 — assistant `--check-version` source-checkout-aware.**
  `autolens_assistant/autoassistant/audit_skill_apis.py --check-version` does
  exact equality on `__version__`, which structurally-permanently
  false-positives when libs resolve to SOURCE checkouts (frozen `__version__`)
  vs the wheel-derived baseline. Fix: `git describe` for checkouts else
  `__version__`, OR drop version equality for the API-surface hash it already
  computes (reports ZERO API drift; the version compare is redundant + worse).
  Last exact-pin holdout in the stack.
- **Task 4 — README version pins.** Per the Phase 1 audit
  (`PyAutoBuild/docs/pre_build_failure_audit.md`) the `<pkg> vX` pins are
  ORPHANED: pre_build's sed (deleted #158) edited but nothing staged; runner
  bump removed under #120. Stale on origin. Decide: runner owns them (explicit
  sed+commit in `release.yml release_workspaces`) OR drop the pins for "install
  the latest release" + floors. Never name a yanked version.
- **Then remove the legacy `workspace_version` key + `version.txt`** from the 7
  workspaces (kept by task 1 only until version_skew stops reading them —
  task 2). Sequenced last.

<!-- filed 2026-07-17 wrapping the build-chain campaign; fork (b), tasks 1-2 precede -->
