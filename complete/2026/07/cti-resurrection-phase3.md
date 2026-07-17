- issue: https://github.com/PyAutoLabs/PyAutoCTI/issues/88 (closed)
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/87 (merge first, a277103), https://github.com/PyAutoLabs/PyAutoBrain/pull/135 (4e6e4fa), https://github.com/PyAutoLabs/PyAutoCTI/pull/89 (90213f30) — all merged 2026-07-17
- summary: CTI resurrection Phase 3 — CI + ecosystem plumbing. PyAutoHeart lib-tests.yml gains the autocti case (deps PyAutoConf/PyAutoFit/PyAutoArray) plus a conditional arcticpy step (libgsl-dev, numpy-first, --no-build-isolation --no-deps; no-op for other libs); PyAutoCTI main.yml is the standard thin caller of that reusable workflow (replacing the checkout@v2/set-output-era CI) and readthedocs.yaml → modern .readthedocs.yaml (ubuntu-22.04, py3.12, pip .[docs], GSL apt + arcticpy post_install). PyAutoBrain worktree.sh PYAUTO_LIBS gains PyAutoCTI (kills the missing-PYTHONPATH trap) and ensure_workspace_labels.sh sweeps the 3 CTI repos; FIREWALL_ALLOWLIST tokens committed to Mind main ahead of the merges.
- deferred: PyAutoBuild release/nightly inclusion + PyAutoHeart config/repos.yaml gating stay OFF until Phase 5 by design (wiring before the Phase 4 workspace update would produce RED noise). RTD project re-activation on readthedocs.org is a human web step.
- traps: mind_commit_guard fires workspace-wide on `git add -A && git commit` — commit with explicit pathspecs everywhere, not just in Mind. Workflow-file pushes went through on the existing token scope (no workflow-scope rejection).
- heart: shipped + merged through the same pre-existing CTI-unrelated RED reasons on human ack 2026-07-17 ("Ship + merge + Phase 4").
- epic-next: Phase 4 autocti_workspace update (118 scripts / 79 notebooks) — the epic's biggest phase — starts per the same authorization.

## Original prompt

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
