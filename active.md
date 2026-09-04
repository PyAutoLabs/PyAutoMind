# Active Tasks

## heart-worktree-drift-hidden-dirs
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/198
- issued: 2026-09-04
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/heart-worktree-drift-hidden-dirs
- repos:
  - PyAutoHeart: feature/heart-worktree-drift-hidden-dirs
- summary: |
    worktree_drift.scan treats every directory under the wt root as a task
    worktree, so the user's JetBrains ~/Code/PyAutoLabs-wt/.idea is reported as
    a permanent orphan. Skip hidden dirs in the discovery sweep only (claimed
    paths keep going through note() unconditionally); extend
    tests/test_worktree_drift.py with a .idea-beside-a-real-orphan case.

## profiles-jit-powerlaw-exact-zero-atol
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/291
- issued: 2026-09-04
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/292
- corrective-red:
  reason: release validation FAILED (stage integrate)
  authorization: https://github.com/PyAutoLabs/autolens_workspace_test/issues/291
- worktree: ~/Code/PyAutoLabs-wt/profiles-jit-powerlaw-exact-zero-atol
- repos:
  - autolens_workspace_test: feature/profiles-jit-powerlaw-exact-zero-atol
- summary: |
    Release Integrate run 33847995194 fails scripts/misc/profiles_jit.py on
    mp.PowerLaw deflections: numpy returns exactly 0.0 on-axis (PyAutoGalaxy#598
    exact unit-vector transform), JAX returns 1.2e-16, and the check is
    rtol-only. Add atol=1e-12 on the mp.PowerLaw checks, mirroring
    mp.ExternalPotential.
