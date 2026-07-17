# CTI resurrection — Phase 3: CI + ecosystem plumbing

Type: feature
Target: PyAutoCTI
Repos:
- @PyAutoCTI
- @PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Phase 3 of the CTI resurrection epic (Phases 0-2 merged: #83/#85/#87). Wire
PyAutoCTI back into the ecosystem's operational plumbing.

## Scope

1. **GitHub Actions**: replace the 2-year-old `main.yml` (actions/checkout@v2,
   deprecated set-output, requirements.txt install) with the current
   PyAutoGalaxy workflow pattern (pyproject install, python 3.12/3.13 matrix,
   arcticpy build step with libgsl-dev + --no-build-isolation --no-deps).
2. **Workspace tooling (PyAutoBrain)**: add PyAutoCTI to `bin/worktree.sh`'s
   library list (activate.sh PYTHONPATH — the trap hit in every phase) and the
   CTI repos to `bin/ensure_workspace_labels.sh`; matching FIREWALL_ALLOWLIST
   tokens in `PyAutoMind/scripts/repos_sync.py`.
3. **readthedocs.yaml**: modernize to the current PyAutoGalaxy standard (RTD
   project activation itself is a human web step, noted on the issue).

## Deferred (deliberate)

PyAutoBuild release-path / nightly inclusion and Heart gating of CTI stay OFF
until Phase 5 (first modern release) — registering them before the workspace
(Phase 4) is updated would only produce RED noise and nightly failures.

## Context

- Phase records: `PyAutoMind/complete/2026/07/cti-resurrection-phase{0,1,2}.md`.
- PyAutoBrain may be claimed by ic50-assistant-seed — zero-overlap parallel-PR
  override per established pattern if so, surfaced at ship.
